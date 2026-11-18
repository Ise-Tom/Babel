"""Validate reporting facts, acceptance distinctions and safe source references."""

import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_dashboard as dashboard  # noqa: E402


class DashboardModel(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "docs", self.root / "docs")
        (self.root / "dashboard").mkdir()
        for name in ("progress.json", "associations.json", "capabilities.json"):
            shutil.copy2(ROOT / "dashboard" / name, self.root / "dashboard" / name)
        self.progress = json.loads((self.root / "dashboard/progress.json").read_text())
        for item in self.progress["work_items"] + self.progress["problems"]:
            for source in item["sources"]:
                path = self.root / source["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    path.write_text("Synthetic source-reference fixture; not executed")

    def model(self):
        (self.root / "dashboard/progress.json").write_text(json.dumps(self.progress))
        return dashboard.build(self.root, "a" * 40)

    def test_complete_model_has_no_invented_acceptance(self):
        data = self.model()
        self.assertEqual(len(data["phases"]), 18)
        canonical_count = sum(
            len(re.findall(r"^\| P\d{2}-\d{2} \|", path.read_text(), re.M))
            for path in (self.root / "docs/phases").glob("phase-*.md")
        )
        self.assertEqual(sum(len(p["steps"]) for p in data["phases"]), canonical_count)
        self.assertGreater(len({len(p["steps"]) for p in data["phases"]}), 1)
        self.assertEqual(len(data["features"]), 130)
        self.assertEqual(sum(p["status"] == "accepted" for p in data["phases"]), 0)
        self.assertEqual(data["phases"][1]["status"], "in_progress")
        self.assertTrue(all(p["status"] == "planned" for p in data["phases"][2:]))

    def test_unknown_or_undocumented_status_is_rejected(self):
        self.progress["requirements"]["P01-01"]["status"] = "done"
        with self.assertRaisesRegex(ValueError, "unknown status"):
            self.model()

    def test_additional_noncontiguous_requirement_keeps_other_phase_counts(self):
        baseline = self.model()
        phase = self.root / "docs/phases/phase-01.md"
        phase.write_text(phase.read_text() + "\n| P01-42 | Fixture task | Fixture proof |\n")
        path = self.root / "dashboard/associations.json"
        associations = json.loads(path.read_text())
        associations["P01-42"] = associations["P01-01"]
        path.write_text(json.dumps(associations))
        data = self.model()
        self.assertEqual(len(data["phases"][0]["steps"]), len(baseline["phases"][0]["steps"]))
        self.assertEqual(len(data["phases"][1]["steps"]), len(baseline["phases"][1]["steps"]) + 1)
        self.assertEqual(data["phases"][1]["steps"][-1]["id"], "P01-42")
        self.assertEqual(data["phases"][1]["steps"][-1]["status"], "planned")

    def test_acceptance_requires_review_and_implemented_explanation(self):
        # Keep the missing-explanation fixture independent of new design/work records.
        self.progress["work_items"] = [
            item for item in self.progress["work_items"] if "P01-02" not in item["requirements"]
        ]
        self.progress["requirements"]["P01-02"] = {"status": "accepted"}
        with self.assertRaisesRegex(ValueError, "object required"):
            self.model()
        self.progress["requirements"]["P01-02"]["acceptance"] = {
            "reviewer": "Fixture",
            "date": "2026-11-17",
            "evidence": "Fixture only",
        }
        with self.assertRaisesRegex(ValueError, "explanation record"):
            self.model()

    def test_phase_acceptance_requires_every_requirement(self):
        self.progress["phase_acceptance"]["1"] = {
            "reviewer": "Fixture",
            "date": "2026-11-17",
            "evidence": "Fixture only",
        }
        with self.assertRaisesRegex(ValueError, "without all requirements"):
            self.model()

    def test_reviewed_requirements_need_separate_phase_approval(self):
        proof = {
            "reviewer": "Fixture reviewer",
            "date": "2026-11-17",
            "evidence": "Synthetic validation fixture",
        }
        all_ids = re.findall(
            r"^\| (P00-\d{2}) \|", (self.root / "docs/phases/phase-00.md").read_text(), re.M
        )
        for identifier in all_ids:
            self.progress["requirements"][identifier] = {"status": "accepted", "acceptance": proof}
        record = dict(self.progress["work_items"][0])
        record.update(id="TEST-ONLY", requirements=all_ids)
        self.progress["work_items"].append(record)
        self.assertEqual(self.model()["phases"][0]["status"], "in_progress")
        self.progress["phase_acceptance"]["0"] = proof
        self.assertEqual(self.model()["phases"][0]["status"], "accepted")

    def test_implemented_work_requires_how_sources_validation_and_limits(self):
        for field in ("how", "verification", "limitations"):
            original = self.progress["work_items"][0][field]
            self.progress["work_items"][0][field] = ""
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.model()
            self.progress["work_items"][0][field] = original
        self.progress["work_items"][0]["sources"] = []
        with self.assertRaisesRegex(ValueError, "source evidence"):
            self.model()

    def test_path_escape_and_missing_source_are_rejected(self):
        for path in ("../private.txt", "/etc/passwd", "missing.txt"):
            self.progress["work_items"][0]["sources"][0]["path"] = path
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "Unsafe or missing"):
                self.model()

    def test_arbitrary_ci_link_and_invalid_commit_are_rejected(self):
        self.progress["snapshot"]["ci_url"] = "javascript:alert(1)"
        with self.assertRaisesRegex(ValueError, "Unsafe CI"):
            self.model()
        self.progress["snapshot"]["ci_url"] = "https://github.com/Ise-Tom/Babel/actions/runs/1"
        self.progress["snapshot"]["commit"] = "invalid"
        with self.assertRaisesRegex(ValueError, "evidence revision"):
            self.model()

    def test_unknown_feature_or_missing_association_is_rejected(self):
        path = self.root / "dashboard/associations.json"
        associations = json.loads(path.read_text())
        associations["P01-01"] = ["UNKNOWN-99"]
        path.write_text(json.dumps(associations))
        with self.assertRaisesRegex(ValueError, "unknown/empty features"):
            self.model()

    def test_unknown_requirement_and_problem_reference_are_rejected(self):
        self.progress["requirements"]["P99-01"] = {"status": "planned"}
        with self.assertRaisesRegex(ValueError, "association/status"):
            self.model()
        self.progress["requirements"].pop("P99-01")
        self.progress["work_items"][0]["problems"] = ["UNKNOWN"]
        with self.assertRaisesRegex(ValueError, "Unknown work problem"):
            self.model()

    def test_resolved_problem_requires_resolution(self):
        self.progress["problems"][0]["resolution"] = ""
        with self.assertRaisesRegex(ValueError, "resolution"):
            self.model()

    def test_duplicate_records_are_rejected(self):
        self.progress["problems"].append(self.progress["problems"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate problem"):
            self.model()
        self.progress["problems"].pop()
        self.progress["work_items"].append(self.progress["work_items"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate work"):
            self.model()

    def test_invalid_schema_focus_and_build_revision_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "build revision"):
            dashboard.build(self.root, "bad")
        self.progress["schema_version"] = 99
        with self.assertRaisesRegex(ValueError, "schema"):
            self.model()
        self.progress["schema_version"] = 1
        self.progress["focus_phase"] = 99
        with self.assertRaisesRegex(ValueError, "focus phase"):
            self.model()

    def test_broken_canonical_design_prevents_build(self):
        (self.root / "docs/phases/phase-17.md").unlink()
        with self.assertRaisesRegex(ValueError, "design validation"):
            self.model()

    def test_shared_preparation_does_not_start_future_phase_execution(self):
        for kind in ("design", "implementation"):
            work = dict(self.progress["work_items"][0])
            work.update(id=f"PREPARATION-{kind}", kind=kind, requirements=["P05-01", "P10-01"])
            self.progress["work_items"].append(work)
        data = self.model()
        self.assertEqual(data["phases"][5]["status"], "planned")
        self.assertEqual(data["phases"][10]["status"], "planned")
        self.assertEqual(data["phases"][5]["steps"][0]["status"], "planned")
        self.progress["requirements"]["P05-01"] = {
            "status": "in_progress",
            "note": "Synthetic explicit execution fixture",
        }
        self.assertEqual(self.model()["phases"][5]["status"], "in_progress")

    def test_validation_ready_requires_pinned_packet_and_does_not_invent_acceptance(self):
        self.progress["requirements"]["P00-15"] = {
            "status": "ready_for_validation",
            "note": "Complete fixture exit; review pending",
        }
        with self.assertRaisesRegex(ValueError, "validation packet required"):
            self.model()
        self.progress["requirements"]["P00-15"]["validation"] = {
            "scope": "Entire Phase 0 driver review; no product acceptance",
            "source_revision": "b" * 40,
            "packet": {"path": "docs/validation/p00-15.md", "label": "Exit criteria"},
        }
        data = self.model()
        step = next(s for s in data["phases"][0]["steps"] if s["id"] == "P00-15")
        self.assertEqual(step["status"], "ready_for_validation")
        self.assertIsNone(step["acceptance"])
        self.assertIn("/" + "b" * 40 + "/", step["validation"]["packet"]["url"])
        self.assertEqual(sum(s["status"] == "accepted" for s in data["phases"][0]["steps"]), 2)
        self.assertEqual(data["phases"][0]["status"], "in_progress")
