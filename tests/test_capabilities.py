"""Explicit implementation scope and evidence must not be inferred from broad associations."""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_dashboard import acceptance  # noqa: E402
from capability_tracker import enrich  # noqa: E402


class CapabilityTracker(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "dashboard").mkdir()
        self.data = {"schema_version": 1, "claims": {}}
        self.features = {
            "AD-04": {"verification": "Synthetic contract, not actual LDAP acceptance"}
        }
        self.phases = [
            {
                "status": "in_progress",
                "steps": [{"id": "P01-04", "features": ["AD-04"], "status": "accepted"}],
            }
        ]
        self.work = [
            {"id": "CODE", "kind": "implementation", "requirements": ["P01-04"]},
            {"id": "DESIGN", "kind": "design", "requirements": ["P01-04"]},
        ]
        self.problems = [{"id": "GAP"}]
        self.claim = {
            "status": "prototype",
            "category": "runtime_lab",
            "scope": "Synthetic bounded lab scope",
            "implemented": ["Fixture behavior"],
            "missing": ["Actual product behavior"],
            "work_items": ["CODE"],
            "blockers": ["GAP"],
            "acceptance": None,
        }

    def build(self):
        (self.root / "dashboard/capabilities.json").write_text(json.dumps(self.data))
        model = copy.deepcopy(self.features)
        enrich(self.root, model, self.phases, self.work, self.problems, acceptance)
        return model["AD-04"]

    def test_accepted_requirements_and_related_work_do_not_imply_capability_delivery(self):
        model = self.build()
        self.assertEqual(model["implementation"]["status"], "planned")
        self.assertEqual(model["implementation"]["implemented"], [])
        self.assertIsNone(model["implementation"]["acceptance"])
        self.assertEqual(model["supportingWork"], ["CODE", "DESIGN"])
        self.assertEqual(model["requirements"], ["P01-04"])

    def test_explicit_prototype_retains_scope_gaps_evidence_and_blockers(self):
        self.data["claims"]["AD-04"] = self.claim
        model = self.build()
        self.assertEqual(model["implementation"], self.claim)
        self.assertIsNone(model["implementation"]["acceptance"])

    def test_invalid_schema_unknown_capability_and_incomplete_fields_are_rejected(self):
        self.data["schema_version"] = True
        with self.assertRaisesRegex(ValueError, "schema"):
            self.build()
        self.data = {"schema_version": 1, "claims": {"AD-99": self.claim}}
        with self.assertRaisesRegex(ValueError, "Unknown capability claims"):
            self.build()
        self.data["claims"] = {"AD-04": {"status": "prototype"}}
        with self.assertRaisesRegex(ValueError, "fields"):
            self.build()

    def test_code_claims_require_real_record_references_and_visible_missing_scope(self):
        for change in (
            {"work_items": ["DESIGN"]},
            {"work_items": ["UNKNOWN"]},
            {"work_items": []},
            {"missing": []},
            {"implemented": []},
            {"blockers": ["UNKNOWN"]},
            {"scope": ""},
            {"status": "complete"},
            {"category": "production-ready"},
        ):
            self.data["claims"] = {"AD-04": {**self.claim, **change}}
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.build()

    def test_list_types_duplicate_refs_and_planned_code_claims_fail(self):
        for change in (
            {"work_items": ["CODE", "CODE"]},
            {"work_items": None},
            {"implemented": [""]},
            {"implemented": [{}]},
            {"status": "planned"},
        ):
            self.data["claims"] = {"AD-04": {**self.claim, **change}}
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.build()

    def test_tooling_or_partial_acceptance_cannot_accept_full_product_capability(self):
        proof = {"reviewer": "Fixture", "date": "2026-11-18", "evidence": "Synthetic test only"}
        for change in (
            {},
            {"status": "implemented", "category": "engineering", "missing": []},
            {"status": "implemented", "category": "product"},
        ):
            self.data["claims"] = {"AD-04": {**self.claim, **change, "acceptance": proof}}
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.build()
        self.data["claims"] = {
            "AD-04": {
                **self.claim,
                "status": "implemented",
                "category": "product",
                "missing": [],
                "acceptance": proof,
            }
        }
        self.assertEqual(self.build()["implementation"]["acceptance"], proof)
        self.data["claims"]["AD-04"]["acceptance"] = {"reviewer": "Fixture"}
        with self.assertRaises(ValueError):
            self.build()
