"""Synthetic bundle and collector checks; no host or guest is configured."""

import contextlib
import copy
import hashlib
import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import reference_guest_evidence as evidence  # noqa: E402
import reference_guest_linux as linux  # noqa: E402
import run_reference_lab as runner  # noqa: E402

RUN = "b" * 32


class GuestEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory()))
        storage = self.root / "storage"
        storage.mkdir()
        profile = tomllib.loads(runner.PROFILE.read_text(encoding="utf-8"))
        plan = runner.plan(profile, RUN, storage)
        self.journal = self.root / "journal.json"
        runner.save(
            self.journal,
            {
                "schema_version": 1,
                "phase": "provisioned",
                "plan": plan,
                "resources": [{"item": x, "state": "created"} for x in runner.resources(plan)],
                "media_pins": {
                    g["id"]: {
                        "id": "synthetic",
                        "build": "old",
                        "edition": "synthetic",
                        "sha256": "0" * 64,
                        "packages": {"pkg": "1"},
                    }
                    for g in plan["guests"]
                },
            },
        )
        self.bundle = self.root / "bundle"
        payload = b"synthetic staged package, never installable"
        (self.root / "win.msu").write_bytes(payload)
        (self.root / "linux.deb").write_bytes(payload)
        self.staging = self.root / "staging.json"
        self.staging.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "guests": {
                        g["id"]: {
                            "interface": "Ethernet"
                            if g["role"] in {"windows_reference_dc", "windows_client"}
                            else "eth0",
                            "expected_build": "10.0.1.2"
                            if g["role"] in {"windows_reference_dc", "windows_client"}
                            else "6.8.0-test",
                            "expected_packages": {"pkg": "1"},
                            "updates": [
                                {
                                    "path": "win.msu"
                                    if g["role"] in {"windows_reference_dc", "windows_client"}
                                    else "linux.deb",
                                    "sha256": hashlib.sha256(payload).hexdigest(),
                                    "approved_use": "private_isolated_install_and_run",
                                    "rights_record": "synthetic-rights",
                                    "publisher_terms": "https://example.test/terms",
                                }
                            ],
                        }
                        for g in plan["guests"]
                    },
                }
            ),
            encoding="utf-8",
        )

    def prepared(self):
        evidence.prepare(self.journal, self.staging, self.bundle)
        record = evidence.load_journal(self.journal)
        for guest in record["plan"]["guests"]:
            config = json.loads((self.bundle / guest["id"] / "config.json").read_text())
            report = {
                "schema_version": 1,
                "run_id": RUN,
                "plan_sha256": config["plan_sha256"],
                "guest_id": guest["id"],
                "vm": guest["vm"],
                "script_sha256": config["script_sha256"],
                "status": "complete",
                "steps": {step: "passed" for step in evidence.STEPS},
                "observed": {
                    "build": config["expected_build"],
                    "packages": config["expected_packages"],
                    "applied_update_sha256": [x["sha256"] for x in config["updates"]],
                    "address": guest["address"],
                    "dns_servers": [guest["dns_server"]],
                    "dns_suffix": guest["dns_suffix"],
                    "default_routes": [],
                    "denied_egress": True,
                    "time_offset_ms": 1.25,
                    "probes": {
                        "dc_a": {
                            "expected": guest["dns_server"],
                            "observed": guest["dns_server"],
                            "status": "passed",
                        },
                        "ldap_srv": {
                            "expected": f"dc.{guest['dns_suffix']}",
                            "observed": f"dc.{guest['dns_suffix']}",
                            "status": "passed",
                        },
                        "ldap_tcp": {"expected": True, "observed": True, "status": "passed"},
                    },
                },
            }
            runner.save(self.bundle / guest["id"] / "report.json", report)
        return record

    def closed(self):
        record = evidence.load_journal(self.journal)
        record["phase"] = "torn_down"
        record["host_discovery"] = {"status": "passed", "resources": {}}
        for item in record["resources"]:
            item["state"] = "deleted"
        runner.save(self.journal, record)

    def test_complete_synthetic_record_is_only_review_candidate(self):
        result = evidence.prepare(self.journal, self.staging, self.bundle)
        self.assertEqual(len(result["bundles"]), 6)
        self.assertNotIn("synthetic-rights", json.dumps(result))
        self.assertEqual(len(list(self.bundle.glob("*/update-*"))), 6)
        for guest in evidence.load_journal(self.journal)["plan"]["guests"]:
            config = json.loads((self.bundle / guest["id"] / "config.json").read_text())
            report = {
                "schema_version": 1,
                "run_id": RUN,
                "plan_sha256": config["plan_sha256"],
                "guest_id": guest["id"],
                "vm": guest["vm"],
                "script_sha256": config["script_sha256"],
                "status": "complete",
                "steps": {step: "passed" for step in evidence.STEPS},
                "observed": {
                    "build": config["expected_build"],
                    "packages": config["expected_packages"],
                    "applied_update_sha256": [x["sha256"] for x in config["updates"]],
                    "address": guest["address"],
                    "dns_servers": [guest["dns_server"]],
                    "dns_suffix": guest["dns_suffix"],
                    "default_routes": [],
                    "denied_egress": True,
                    "time_offset_ms": 1,
                    "probes": {
                        key: {"expected": expected, "observed": expected, "status": "passed"}
                        for key, expected in (
                            ("dc_a", guest["dns_server"]),
                            ("ldap_srv", f"dc.{guest['dns_suffix']}"),
                            ("ldap_tcp", True),
                        )
                    },
                },
            }
            runner.save(self.bundle / guest["id"] / "report.json", report)
        self.closed()
        assessed = evidence.assess(self.journal, self.bundle)
        self.assertTrue(assessed["cycle_record_complete"])
        self.assertFalse(assessed["p00_05_accepted"])
        self.assertEqual(len(assessed["guest_results"]), 6)

    def test_missing_failed_interrupted_and_unclosed_cannot_complete(self):
        self.prepared()
        self.closed()
        first = self.bundle / "reference-dc" / "report.json"
        baseline = json.loads(first.read_text())
        first.unlink()
        self.assertFalse(evidence.assess(self.journal, self.bundle)["cycle_record_complete"])
        runner.save(first, dict(baseline, status="incomplete"))
        self.assertFalse(evidence.assess(self.journal, self.bundle)["cycle_record_complete"])
        failed = copy.deepcopy(baseline)
        failed["steps"]["dns_probe"] = "failed"
        runner.save(first, failed)
        self.assertFalse(evidence.assess(self.journal, self.bundle)["cycle_record_complete"])
        runner.save(first, baseline)
        record = evidence.load_journal(self.journal)
        record["phase"] = "teardown_incomplete"
        runner.save(self.journal, record)
        self.assertIn("teardown_incomplete", evidence.assess(self.journal, self.bundle)["blockers"])

    def test_wrong_run_build_dns_time_and_probe_fail(self):
        self.prepared()
        self.closed()
        path = self.bundle / "babel-probe" / "report.json"
        bad = json.loads(path.read_text())
        bad["plan_sha256"] = "0" * 64
        bad["script_sha256"] = "0" * 64
        bad["observed"]["build"] = "wrong"
        bad["observed"]["applied_update_sha256"] = []
        bad["observed"]["dns_servers"] = ["8.8.8.8"]
        bad["observed"]["time_offset_ms"] = 6000
        bad["observed"]["denied_egress"] = False
        bad["observed"]["probes"]["ldap_tcp"]["observed"] = False
        runner.save(path, bad)
        result = evidence.assess(self.journal, self.bundle)
        self.assertFalse(result["cycle_record_complete"])
        self.assertEqual(
            {r.split(":", 1)[1] for r in result["blockers"] if r.startswith("babel-probe:")},
            {
                "plan_sha256_mismatch",
                "script_sha256_mismatch",
                "build_mismatch",
                "staged_updates_mismatch",
                "dns_servers_mismatch",
                "time_offset_invalid",
                "denied_egress_mismatch",
                "discovery_probe_mismatch",
            },
        )

    def test_unapproved_or_changed_update_refuses_bundle(self):
        manifest = json.loads(self.staging.read_text())
        manifest["guests"]["reference-dc"]["updates"][0]["approved_use"] = "unresolved"
        self.staging.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "rights not approved"):
            evidence.prepare(self.journal, self.staging, self.bundle)
        self.assertFalse(self.bundle.exists())
        manifest["guests"]["reference-dc"]["updates"][0]["approved_use"] = (
            "private_isolated_install_and_run"
        )
        manifest["guests"]["reference-dc"]["updates"][0]["sha256"] = "0" * 64
        self.staging.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            evidence.prepare(self.journal, self.staging, self.bundle)
        self.assertFalse(self.bundle.exists())

    def test_linux_guest_failed_update_and_interrupt_leave_checkpoint_incomplete(self):
        evidence.prepare(self.journal, self.staging, self.bundle)
        directory = self.bundle / "babel-probe"
        config = directory / "config.json"
        report = directory / "report.json"
        copied = directory / "update-1.deb"
        original = copied.read_bytes()
        copied.write_bytes(b"changed synthetic update")
        with patch.object(linux, "os", SimpleNamespace(name="posix", geteuid=lambda: 0)):
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                linux.execute(config, report)
        failed = json.loads(report.read_text())
        self.assertEqual(failed["status"], "incomplete")
        self.assertEqual(failed["steps"]["updates_verified"], "failed")
        copied.write_bytes(original)
        with (
            patch.object(linux, "os", SimpleNamespace(name="posix", geteuid=lambda: 0)),
            patch.object(linux, "run", side_effect=KeyboardInterrupt),
        ):
            with self.assertRaises(KeyboardInterrupt):
                linux.execute(config, report)
        interrupted = json.loads(report.read_text())
        self.assertEqual(interrupted["status"], "incomplete")
        self.assertEqual(interrupted["steps"]["updates_installed"], "failed")

    def test_linux_guest_executes_isolated_steps_with_synthetic_commands(self):
        evidence.prepare(self.journal, self.staging, self.bundle)
        bundle = self.bundle / "babel-probe"
        system = self.root / "synthetic-system"
        (system / "etc/chrony").mkdir(parents=True)
        (system / "etc/chrony/chrony.conf").write_text("pool outside.example\n")
        (system / "etc/os-release").write_text('VERSION_ID="24.04"\n')
        state = {"address_added": False}

        def command(*args):
            if args == ("ip", "-o", "link", "show"):
                return "1: lo: <LOOPBACK>\n2: eth0: <UP>"
            if args == ("ip", "-4", "route", "show", "default"):
                return ""
            if args[:6] == ("ip", "-4", "-o", "addr", "show", "dev"):
                return "2: eth0 inet 198.51.100.30/24" if state["address_added"] else ""
            if args[:3] == ("ip", "addr", "add"):
                state["address_added"] = True
                return ""
            if args[:2] == ("uname", "-r"):
                return "6.8.0-test"
            if args[0] == "dpkg-query":
                return "1"
            if args[:3] == ("dig", "+short", "A"):
                return "198.51.100.10"
            if args[:3] == ("dig", "+short", "SRV"):
                return "0 100 389 dc.babel.example.test."
            if args == ("chronyc", "tracking"):
                return "Last offset : +0.001 seconds"
            if args == ("resolvectl", "dns", "eth0"):
                return "Link 2 (eth0): 198.51.100.10"
            if args == ("resolvectl", "domain", "eth0"):
                return "Link 2 (eth0): babel.example.test"
            if args[0] in {"dpkg", "systemctl", "ip"}:
                return ""
            raise AssertionError(args)

        def connect(address, timeout):
            if address == ("198.51.100.10", 389):
                return contextlib.nullcontext(object())
            raise OSError("synthetic egress denied")

        with (
            patch.object(linux, "os", SimpleNamespace(name="posix", geteuid=lambda: 0)),
            patch.object(linux.socket, "create_connection", side_effect=connect),
        ):
            report = linux.execute(
                bundle / "config.json", bundle / "report.json", system_root=system, command=command
            )
        self.assertEqual(report["status"], "complete")
        self.assertEqual(set(report["steps"].values()), {"passed"})
        self.assertEqual(report["observed"]["dns_servers"], ["198.51.100.10"])
        self.assertEqual(report["observed"]["time_offset_ms"], 1.0)
        self.assertTrue(report["observed"]["denied_egress"])
        self.assertNotIn("pool outside.example", (system / "etc/chrony/chrony.conf").read_text())


if __name__ == "__main__":
    unittest.main()
