"""Preflight tests use project-owned synthetic bytes and mocked Hyper-V inventory."""

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import preflight_reference_lab as preflight  # noqa: E402

TODAY = date(2026, 11, 23)
PLAN = tomllib.loads(preflight.PROFILE.read_text(encoding="utf-8"))
HOST = {
    "inventory": "observed",
    "architecture": "x86_64",
    "hypervisor_present": True,
    "vmms_running": True,
    "vm_count": 0,
    "switch_count": 0,
    "logical_cpus": 24,
    "available_memory_mib": 32768,
    "available_storage_gib": 400,
}


class ReferenceLabPreflight(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.root = Path(directory)
        image = b"project-owned synthetic bytes, never a bootable image"
        path = self.root / "private-media"
        path.write_bytes(image)
        self.media = {
            guest["id"]: {
                "path": path.name,
                "id": "test-image",
                "edition": "synthetic",
                "architecture": "x86_64",
                "build": "synthetic-build",
                "sha256": hashlib.sha256(image).hexdigest(),
                "packages": {"synthetic-package": "1.0"},
                "publisher_terms": "https://example.test/licence",
                "rights_record": "private-license-record",
                "approved_use": "private_isolated_install_and_run",
                "expires_on": date(2026, 12, 1),
            }
            for guest in PLAN["machines"]
        }

    def test_eligible_inputs_are_redacted_and_keep_cycles_unrun(self):
        report = preflight.check(PLAN, HOST, self.media, self.root, TODAY)
        self.assertEqual(report["status"], "ready_for_provisioner_review")
        self.assertEqual(
            report["required"],
            {"guest_vcpus": 16, "guest_memory_mib": 30720, "guest_storage_gib": 344},
        )
        self.assertEqual(set(report["media"].values()), {"digest_verified"})
        self.assertEqual(report["provisioning_cycles"], ["unrun", "unrun"])
        self.assertEqual(report["macos"], "separate_track")
        for private in (
            "private-media",
            "private-license-record",
            "example.test",
            "synthetic-build",
        ):
            self.assertNotIn(private, json.dumps(report))

    def test_blocked_hypervisor_and_capacity(self):
        host = dict(
            HOST,
            architecture="aarch64",
            logical_cpus=10,
            hypervisor_present=False,
            switch_count=None,
            available_memory_mib=15000,
        )
        del host["available_storage_gib"]
        report = preflight.check(PLAN, host, {}, self.root, TODAY)
        self.assertEqual(report["status"], "blocked")
        self.assertEqual(
            report["blockers"][:6],
            [
                "x86_64_hyper_v_host_required",
                "hyper_v_not_running",
                "hyper_v_inventory_unavailable",
                "logical_cpu_capacity_shortfall",
                "guest_memory_capacity_shortfall",
                "guest_storage_capacity_unmeasured",
            ],
        )
        self.assertEqual(set(report["media"].values()), {"missing"})

    def test_unavailable_host_unknown_guest_and_unsafe_topology(self):
        with patch.object(preflight.sys, "platform", "linux"):
            host = preflight.host_inventory(self.root)
        report = preflight.check(PLAN, host, {}, self.root, TODAY)
        self.assertIn("windows_host_required", report["blockers"])
        with self.assertRaisesRegex(ValueError, "Unknown guest"):
            preflight.check(PLAN, host, {"duplicate": {}}, self.root, TODAY)
        plan = copy.deepcopy(PLAN)
        plan["safety"]["production_bridge"] = True
        with self.assertRaisesRegex(ValueError, "production_bridge"):
            preflight.check(plan, host, {}, self.root, TODAY)

    def test_media_refusals(self):
        for overrides, expected in (
            (False, "invalid_metadata"),
            ({"build": ""}, "invalid_metadata"),
            ({"packages": {}}, "invalid_metadata"),
            ({"packages": {"pkg": ""}}, "invalid_metadata"),
            ({"architecture": "aarch64"}, "invalid_metadata"),
            ({"sha256": "0" * 64}, "digest_mismatch"),
            ({"path": "missing"}, "file_unavailable"),
            ({"path": "bad\0"}, "file_unavailable"),
            ({"path": r"\\server\share\image"}, "nonlocal_path"),
            ({"approved_use": "redistribute"}, "rights_unresolved"),
            ({"publisher_terms": "https://[broken"}, "rights_unresolved"),
            ({"publisher_terms": None}, "rights_unresolved"),
            ({"rights_record": ""}, "rights_unresolved"),
            ({"expires_on": TODAY}, "rights_expired"),
            ({"expires_on": "2026-11-23"}, "invalid_metadata"),
        ):
            with self.subTest(overrides=overrides):
                record = overrides
                if overrides is not False:
                    record = dict(self.media["reference-dc"], **overrides)
                self.assertEqual(preflight.media_status(record, self.root, TODAY), expected)

    def test_rights_are_required_before_opening_media(self):
        record = dict(self.media["reference-dc"], approved_use="unresolved")
        with patch.object(preflight.Path, "open") as image_open:
            self.assertEqual(preflight.media_status(record, self.root, TODAY), "rights_unresolved")
        image_open.assert_not_called()

    def test_windows_inventory_uses_read_only_commands_and_storage(self):
        with (
            patch.object(preflight.sys, "platform", "win32"),
            patch.object(
                preflight.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(
                    [], 0, stdout='{"vm_count": null, "switch_count": 1}'
                ),
            ) as run,
            patch.object(preflight.shutil, "disk_usage") as disk,
        ):
            disk.return_value.free = 350 * preflight.GIB
            self.assertEqual(
                preflight.host_inventory(self.root),
                {
                    "vm_count": None,
                    "switch_count": 1,
                    "inventory": "observed",
                    "available_storage_gib": 350,
                },
            )
            self.assertEqual(
                preflight.host_inventory(self.root / "missing")["inventory"], "observed"
            )
            self.assertIn("Get-VMSwitch", run.call_args.args[0][-1])
            disk.side_effect = OSError
            self.assertNotIn("available_storage_gib", preflight.host_inventory(self.root))
            run.side_effect = subprocess.TimeoutExpired("powershell", 30)
            self.assertEqual(
                preflight.host_inventory(self.root), {"inventory": "windows_query_failed"}
            )
