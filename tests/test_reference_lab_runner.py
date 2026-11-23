"""Synthetic lifecycle checks; no Hyper-V command or licensed image is used."""

import copy
import hashlib
import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_reference_lab as runner  # noqa: E402

PROFILE = tomllib.loads(runner.PROFILE.read_text(encoding="utf-8"))
RUN = "a" * 32


class FakeHyperV:
    def __init__(self):
        self.live = {}
        self.items = {}
        self.fail_at = None
        self.creates = 0
        self.deleted = []

    def call(self, action, item):
        name = item["name"]
        if action == "inspect":
            return self.live.get(name, {"exists": False, "owned": False})
        if action == "create":
            self.creates += 1
            self.live[name] = {"exists": True, "owned": True}
            self.items[name] = item
            if self.fail_at == self.creates:
                raise RuntimeError("synthetic failure after creation")
            return {"created": True}
        if action == "delete":
            if item["kind"] in {"disk", "switch"}:
                field = "disk" if item["kind"] == "disk" else "switch"
                if any(
                    x["kind"] == "vm" and x[field] == name and vm_name in self.live
                    for vm_name, x in self.items.items()
                ):
                    raise RuntimeError("synthetic resource still attached")
            self.deleted.append(name)
            self.live.pop(name)
            self.items.pop(name)
            return {"deleted": True}
        raise AssertionError(action)


class ReferenceLabRunnerTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.storage = self.root / "storage"
        self.storage.mkdir()
        self.state = self.root / "state"
        self.backend = FakeHyperV()
        synthetic = b"synthetic not bootable media"
        (self.root / "synthetic.iso").write_bytes(synthetic)
        self.media = {
            g["id"]: {"path": "synthetic.iso", "sha256": hashlib.sha256(synthetic).hexdigest()}
            for g in PROFILE["machines"]
        }
        self.ready = {
            "status": "ready_for_provisioner_review",
            "media": {g["id"]: "digest_verified" for g in PROFILE["machines"]},
            "blockers": [],
        }

    def provision(self):
        with patch.object(runner, "preflight", return_value=self.ready):
            return runner.provision(
                PROFILE, self.media, self.root, self.storage, self.state, self.backend, RUN
            )

    def test_plan_names_all_resources_and_probes(self):
        p = runner.plan(PROFILE, RUN, self.storage)
        self.assertEqual(len(p["networks"]), 2)
        self.assertEqual(len(p["guests"]), 6)
        self.assertEqual(len(runner.resources(p)), 14)
        self.assertEqual({x["type"] for x in p["networks"]}, {"Private"})
        self.assertTrue(
            all(x["default_gateway"] is None and x["external_dns"] is None for x in p["networks"])
        )
        self.assertTrue(all("denied_egress" in x["probes"] for x in p["guests"]))
        self.assertNotIn("synthetic.iso", json.dumps(p))
        with self.assertRaisesRegex(ValueError, "Run ID"):
            runner.plan(PROFILE, "unsafe", self.storage)
        unsafe = copy.deepcopy(PROFILE)
        unsafe["safety"]["production_bridge"] = True
        with self.assertRaisesRegex(ValueError, "production_bridge"):
            runner.plan(unsafe, RUN, self.storage)

    def test_preflight_blocks_before_any_resource_or_journal(self):
        blocked = dict(self.ready, status="blocked", blockers=["guest_memory_capacity_shortfall"])
        with patch.object(runner, "preflight", return_value=blocked):
            with self.assertRaisesRegex(ValueError, "Preflight blocked"):
                runner.provision(
                    PROFILE, self.media, self.root, self.storage, self.state, self.backend, RUN
                )
        self.assertFalse(self.state.exists())
        self.assertEqual(self.backend.creates, 0)

    def test_changed_or_outside_media_is_rejected_before_create(self):
        (self.root / "synthetic.iso").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "digest changed"):
            self.provision()
        self.assertEqual(self.backend.creates, 0)
        self.media["reference-dc"]["path"] = "../outside.iso"
        with self.assertRaisesRegex(ValueError, "under manifest directory"):
            self.provision()
        self.assertFalse(self.state.exists())

    def test_success_discovery_and_manifest_scoped_teardown(self):
        journal, record = self.provision()
        self.assertEqual(record["phase"], "provisioned")
        self.assertEqual(len(self.backend.live), 14)
        foreign = "unrelated-hyper-v-resource"
        self.backend.live[foreign] = {"exists": True, "owned": False}
        discovered = runner.discover(journal, self.backend)
        self.assertEqual(discovered["guest_probes"], "unrun")
        self.assertFalse(discovered["p00_05_cycle_complete"])
        result = runner.teardown(journal, self.backend)
        self.assertEqual(result["phase"], "torn_down")
        self.assertFalse(Path(record["plan"]["storage_dir"]).exists())
        self.assertEqual(self.backend.live, {foreign: {"exists": True, "owned": False}})
        self.assertEqual(runner.teardown(journal, self.backend)["phase"], "torn_down")

    def test_failure_after_create_is_cleaned_from_pending_journal(self):
        self.backend.fail_at = 5
        with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
            self.provision()
        self.assertEqual(self.backend.live, {})
        journal = self.state / f"babel-lab-{RUN}.json"
        self.assertEqual(json.loads(journal.read_text())["phase"], "torn_down")

    def test_interrupted_run_and_ownership_mismatch(self):
        journal, _ = self.provision()
        vm = next(x for x in self.backend.live if x.endswith("reference-dc"))
        self.backend.live[vm]["owned"] = False
        result = runner.teardown(journal, self.backend)
        self.assertEqual(result["phase"], "teardown_incomplete")
        self.assertEqual({x["kind"] for x in result["failures"]}, {"vm", "disk", "switch"})
        self.assertIn(vm, self.backend.live)
        self.backend.live[vm]["owned"] = True
        self.assertEqual(runner.teardown(journal, self.backend)["phase"], "torn_down")
        self.assertEqual(self.backend.live, {})

    def test_tampered_journal_cannot_expand_cleanup_scope(self):
        journal, _ = self.provision()
        record = json.loads(journal.read_text())
        record["resources"].append({"item": {"kind": "vm", "name": "foreign"}, "state": "created"})
        runner.save(journal, record)
        with self.assertRaisesRegex(ValueError, "does not match"):
            runner.teardown(journal, self.backend)
        self.assertEqual(len(self.backend.live), 14)

    def test_foreign_file_in_run_directory_is_preserved(self):
        journal, record = self.provision()
        foreign = Path(record["plan"]["storage_dir"]) / "operator-note.txt"
        foreign.write_text("do not remove", encoding="utf-8")
        result = runner.teardown(journal, self.backend)
        self.assertEqual(result["phase"], "teardown_incomplete")
        self.assertEqual(result["failures"][0]["kind"], "directory")
        self.assertEqual(foreign.read_text(encoding="utf-8"), "do not remove")


if __name__ == "__main__":
    unittest.main()
