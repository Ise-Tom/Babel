"""Planning decisions must stay separate from observed product recovery/conformance."""

import copy
import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_phase0_contract as contract  # noqa: E402

KNOWN = contract.requirement_ids(ROOT)
NOW = dt.datetime(2026, 11, 18, 12, tzinfo=dt.UTC)


class PhaseZeroContract(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads(contract.CONTRACT.read_text())
        self.matrix = json.loads((ROOT / "lab/compatibility.json").read_text())

    def validate(self):
        contract.validate(self.policy, self.matrix, NOW, KNOWN)

    @staticmethod
    def exception():
        return {
            "id": "EX-SYNTHETIC-01",
            "owner": "Synthetic reviewer",
            "operation": "optional module test scheduling",
            "client": "synthetic client",
            "site": "synthetic site",
            "scope": "test fixture only",
            "reason": "synthetic scheduling example",
            "control": "module stays unavailable",
            "production_impact": "No production qualification inferred",
            "waived_requirements": ["EDR-01"],
            "activation": "2026-11-18T00:00:00Z",
            "expiry": "2026-11-19T00:00:00Z",
            "review": {
                "disposition": "owner_reviewed",
                "evidence": "Synthetic fixture, not approval",
            },
            "changes_observed_outcomes": False,
        }

    def test_committed_contract_preserves_unqualified_product_state(self):
        self.validate()
        self.assertEqual(self.policy["functional_profile"]["advertised_levels"], [])
        self.assertEqual(self.policy["active_exceptions"], [])
        self.assertTrue(all(c["runtime_outcome"] == "unrun" for c in self.policy["worked_changes"]))

    def test_creation_profile_is_design_only_and_all_transitions_fail_closed(self):
        self.assertEqual(contract.level_plan("create", "2016", "2016"), "design_only")
        for domain, forest in (
            ("2012_R2", "2012_R2"),
            ("2025", "2025"),
            ("2016", "2025"),
            ("2025", "2016"),
            ("2019", "2022"),
        ):
            with self.subTest(domain=domain, forest=forest):
                self.assertEqual(contract.level_plan("create", domain, forest), "unsupported")
        for op in ("raise_domain", "raise_forest", "lower_domain", "lower_forest", "coexist"):
            self.assertEqual(contract.level_plan(op, "2016", "2016"), "unsupported")
        with self.assertRaisesRegex(ValueError, "Unknown functional"):
            contract.level_plan("unknown", "2016", "2016")

    def test_malformed_schema_and_false_qualification_are_rejected(self):
        for key, value in (
            ("schema_version", True),
            ("schema_version", 2),
            ("status", "qualified"),
            ("functional_profile", None),
            ("references", {}),
            ("worked_changes", [None]),
            ("active_exceptions", None),
        ):
            self.setUp()
            self.policy[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.validate()

    def test_level_host_feature_reference_and_client_drift_are_rejected(self):
        original = copy.deepcopy(self.policy)
        edits = [
            ("domain", "2025"),
            ("forest", "2012_R2"),
            ("advertised_levels", ["2016"]),
            ("host_os", "windows"),
            ("client_profiles", ["win11-pro"]),
            ("client_profiles", ["win11-pro", "win11-pro"]),
            ("transitions", {"create": "implemented"}),
            ("reference_dc_os", ["2016"]),
            ("incompatibilities", {}),
            ("incompatibilities", None),
        ]
        for key, value in edits:
            self.policy = copy.deepcopy(original)
            self.policy["functional_profile"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate()
        self.policy = original
        for field in ("domain", "forest"):
            old = self.matrix["functional_level"][field]
            self.matrix["functional_level"][field] = "2025"
            with self.assertRaisesRegex(ValueError, "drift"):
                self.validate()
            self.matrix["functional_level"][field] = old

    def test_reference_pins_and_conflict_review_are_mandatory(self):
        for field, value in (
            ("url", "https://github.com/MicrosoftDocs/windowsserverdocs/blob/main/page.md"),
            ("review", ""),
        ):
            policy = copy.deepcopy(self.policy)
            policy["references"][0][field] = value
            with self.assertRaises(ValueError):
                contract.validate(policy, self.matrix, NOW, KNOWN)
        duplicate = copy.deepcopy(self.policy)
        duplicate["references"][1] = duplicate["references"][0]
        with self.assertRaisesRegex(ValueError, "Distinct"):
            contract.validate(duplicate, self.matrix, NOW, KNOWN)
        self.policy["references"].pop()
        with self.assertRaises(ValueError):
            self.validate()

    def test_all_six_change_families_and_distinct_ids_are_required(self):
        original = copy.deepcopy(self.policy)
        for edit in ("missing", "duplicate_kind", "duplicate_id"):
            self.policy = copy.deepcopy(original)
            if edit == "missing":
                self.policy["worked_changes"].pop()
            elif edit == "duplicate_kind":
                self.policy["worked_changes"][1]["kind"] = "schema"
            else:
                self.policy["worked_changes"][1]["id"] = self.policy["worked_changes"][0]["id"]
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                self.validate()

    def test_each_change_requires_real_review_material_and_no_runtime_pass(self):
        for change in self.policy["worked_changes"]:
            contract.validate_change(change, KNOWN)
            for field in (
                "id",
                "owner",
                "scope",
                "forward",
                "interrupted",
                "recovery",
                "production_impact",
            ):
                bad = copy.deepcopy(change)
                bad[field] = " "
                with self.subTest(kind=change["kind"], field=field), self.assertRaises(ValueError):
                    contract.validate_change(bad, KNOWN)
            for field, value in (
                ("kind", "unknown"),
                ("requirements", []),
                ("requirements", ["unknown"]),
                ("requirements", ["P99-99"]),
                ("impacts", None),
                ("impacts", {}),
                ("recovery_controls", []),
                ("binary_revert_is_recovery", True),
                ("runtime_outcome", "passed"),
                ("evidence_invalidation", None),
                ("review", None),
            ):
                bad = copy.deepcopy(change)
                bad[field] = value
                with self.subTest(kind=change["kind"], field=field), self.assertRaises(ValueError):
                    contract.validate_change(bad, KNOWN)

    def test_impacts_evidence_invalidation_and_review_cannot_be_omitted(self):
        change = self.policy["worked_changes"][0]
        for parent, field, value in (
            ("impacts", "security", ""),
            ("evidence_invalidation", "on_change", ["source"]),
            ("evidence_invalidation", "rerun", ""),
            ("review", "disposition", "approved"),
            ("review", "accountable_owner", ""),
        ):
            bad = copy.deepcopy(change)
            bad[parent][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                contract.validate_change(bad, KNOWN)

    def test_exception_expiry_is_exclusive_and_clock_is_explicit_utc(self):
        ex = self.exception()
        contract.validate_exception(ex, NOW, KNOWN)
        for value in ("2026-11-18T12:00:00Z", "2026-11-18T11:59:59Z"):
            ex["expiry"] = value
            with self.assertRaisesRegex(ValueError, "expired"):
                contract.validate_exception(ex, NOW, KNOWN)
        ex = self.exception()
        ex["activation"] = "2026-11-18T12:00:01Z"
        with self.assertRaisesRegex(ValueError, "inactive"):
            contract.validate_exception(ex, NOW, KNOWN)
        for value in (None, "2026-11-19T00:00:00", "2026-11-19T01:00:00+01:00", "invalidZ"):
            ex = self.exception()
            ex["expiry"] = value
            with self.assertRaises(ValueError):
                contract.validate_exception(ex, NOW, KNOWN)
        with self.assertRaisesRegex(ValueError, "clock"):
            contract.validate_exception(self.exception(), NOW.replace(tzinfo=None), KNOWN)

    def test_no_baseline_waiver_or_outcome_rewrite_can_pass(self):
        for identifier in contract.BASELINE_IDS:
            ex = self.exception()
            ex["waived_requirements"] = [identifier]
            with (
                self.subTest(identifier=identifier),
                self.assertRaisesRegex(ValueError, "baseline"),
            ):
                contract.validate_exception(ex, NOW, KNOWN)
        for field, value in (
            ("scope", ""),
            ("waived_requirements", []),
            ("waived_requirements", ["invalid"]),
            ("waived_requirements", ["SEC-99"]),
            ("waived_requirements", ["P00-15"]),
            ("changes_observed_outcomes", True),
            ("review", None),
            ("review", {}),
        ):
            ex = self.exception()
            ex[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                contract.validate_exception(ex, NOW, KNOWN)

    def test_exception_register_is_checked_and_duplicate_ids_are_rejected(self):
        self.policy["active_exceptions"] = [self.exception()]
        self.validate()
        self.policy["active_exceptions"].append(self.exception())
        with self.assertRaisesRegex(ValueError, "Duplicate exception"):
            self.validate()

    def test_report_binds_actual_inputs_and_never_infers_acceptance(self):
        report = contract.check(ROOT, "a" * 40, NOW)
        self.assertEqual(report["source_revision"], "a" * 40)
        self.assertEqual(report["runtime_recovery"], "unrun")
        self.assertEqual(report["owner_acceptance"], "not_inferred")
        self.assertEqual(len(report["worked_transition_kinds"]), 6)
        with self.assertRaisesRegex(ValueError, "source revision"):
            contract.check(ROOT, "main", NOW)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "docs", root / "docs")
            (root / "lab").mkdir()
            (root / "lab/phase0-contract.json").write_text(json.dumps(self.policy, indent=4))
            (root / "lab/compatibility.json").write_text(json.dumps(self.matrix, indent=4))
            other = contract.check(root, "a" * 40, NOW)
            self.assertNotEqual(report["contract_sha256"], other["contract_sha256"])
            self.assertNotEqual(report["matrix_sha256"], other["matrix_sha256"])
