"""Reject misleading conformance claims, scope gaps and unsafe evidence artifacts."""

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_conformance as policy  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


class ConformanceEvidence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "docs", self.root / "docs")
        shutil.copytree(ROOT / "lab", self.root / "lab")
        self.contract = json.loads((self.root / "lab/compatibility.json").read_bytes())
        self.evidence = json.loads((self.root / "lab/conformance-evidence.json").read_bytes())

    def save(self):
        raw = (json.dumps(self.contract) + "\n").encode()
        (self.root / "lab/compatibility.json").write_bytes(raw)
        self.evidence["contract_sha256"] = hashlib.sha256(raw).hexdigest()
        (self.root / "lab/conformance-evidence.json").write_text(json.dumps(self.evidence))

    def check(self, ready=False):
        self.save()
        return policy.validate(self.root, require_ready=ready)

    def passing_fixture(self):
        # Synthetic validator fixture; never checked in as product evidence.
        proof = {
            "reviewer": "fixture",
            "date": "2026-11-18",
            "disposition": "accepted",
            "scope": "synthetic validation",
        }
        self.contract.update(status="approved", approval=proof)
        for profile in self.contract["profiles"]:
            profile.update(build="fixture-build", image_sha256="b" * 64, qualification="qualified")
        for operation in self.contract["operations"]:
            operation["implementation"] = "implemented"
            operation["exchanges"] = [
                x for x in operation["exchanges"] if x["kind"] != "unresolved"
            ]
        for spec in self.contract["specifications"]:
            spec["rights_review"] = "approved"
        artifact = self.root / "lab/evidence-artifacts/synthetic.txt"
        artifact.parent.mkdir()
        artifact.write_text("Synthetic fixture only; no client test was run.\n")
        receipt = {
            "path": "lab/evidence-artifacts/synthetic.txt",
            "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        }
        ops = {row["id"]: row for row in self.contract["operations"]}
        for row in self.evidence["records"]:
            op = ops[row["operation"]]
            row.update(outcome="passed", review=proof)
            row["executions"] = [
                {
                    "profile": profile,
                    "target": target,
                    "source_revision": "a" * 40,
                    "client_build": "fixture-build",
                    "run_id": "fixture-1",
                    "operator": "fixture",
                    "environment": "synthetic validation environment",
                    "dataset": "synthetic-fixture",
                    "expected": op["scenarios"][row["scenario"]],
                    "actual": "fixture-only result",
                    "duration_ms": 1,
                    "started_at": "2026-11-18T00:00:00+01:00",
                    "tools": {"fixture": "1"},
                    "artifacts": [copy.deepcopy(receipt)],
                    "result": "passed",
                }
                for profile in op["profiles"]
                for target in op["targets"]
            ]

    def test_current_inventory_is_explicitly_unrun_and_not_ready(self):
        counts = policy.validate(self.root)
        self.assertEqual(counts, {"unrun": 60})
        with self.assertRaisesRegex(ValueError, "Planned/lab-only"):
            policy.validate(self.root, require_ready=True)

    def test_scope_includes_linux_and_macos_without_claiming_windows_gpo(self):
        ops = {op["id"]: op for op in self.contract["operations"]}
        clients = {"linux-client", "debian-client", "macos-arm", "macos-intel"}
        self.assertEqual(set(ops["non-windows-clients"]["profiles"]), clients)
        self.assertTrue(clients <= set(ops["password"]["profiles"]))
        self.assertFalse(clients & set(ops["gpo"]["profiles"]))
        self.assertTrue(any("Mobile" in text for text in self.contract["limitations"]))

    def test_stale_contract_and_unknown_schema_cannot_reuse_evidence(self):
        path = self.root / "lab/compatibility.json"
        path.write_text(path.read_text() + " ")
        with self.assertRaisesRegex(ValueError, "Stale"):
            policy.validate(self.root)
        self.contract["schema_version"] = True
        with self.assertRaisesRegex(ValueError, "schema"):
            self.check()

    def test_positive_and_negative_and_all_baseline_requirements_are_mandatory(self):
        self.contract["operations"][0]["scenarios"].pop("negative")
        with self.assertRaisesRegex(ValueError, "Positive and negative"):
            self.check()
        self.contract["operations"][0]["scenarios"]["negative"] = "denied fixture"
        for operation in self.contract["operations"]:
            if operation["requirements"] == ["AD-01"]:
                operation["requirements"] = ["AD-02"]
        with self.assertRaisesRegex(ValueError, "Missing first-production"):
            self.check()

    def test_duplicate_unknown_and_missing_records_are_rejected(self):
        original = copy.deepcopy(self.evidence["records"])
        for rows in (
            [],
            original[:-1],
            original + [original[0]],
            [{**original[0], "operation": "unknown"}],
        ):
            self.evidence["records"] = rows
            with self.subTest(size=len(rows)), self.assertRaises(ValueError):
                self.check()

    def test_unknown_references_empty_owner_and_duplicate_ids_are_rejected(self):
        original = copy.deepcopy(self.contract)
        for change in (
            lambda c: c["operations"].append(c["operations"][0]),
            lambda c: c["operations"][0].update(owner=""),
            lambda c: c["operations"][0].update(profiles=["unknown"]),
            lambda c: c["operations"][0].update(requirements=["AD-99"]),
            lambda c: c["operations"][0].update(specifications=[]),
            lambda c: c["profiles"][0].update(qualification="supported"),
            lambda c: c["specifications"][0].update(rights_review="assumed"),
        ):
            self.contract = copy.deepcopy(original)
            change(self.contract)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check()

    def test_operation_report_covers_all_families_and_retains_unknowns(self):
        report = policy.check(self.root)
        self.assertEqual(report["families"], 30)
        self.assertGreater(report["exchange_counts"]["wire"], 30)
        self.assertGreater(report["exchange_counts"]["workflow"], 0)
        self.assertIn("join-login/join-variants", report["unresolved_mappings"])
        self.assertEqual(
            report["exchange_counts"]["unresolved"], len(report["unresolved_mappings"])
        )
        self.assertEqual(report["conformance_outcomes"], {"unrun": 60})
        self.assertEqual(
            report["input_sha256"]["lab/compatibility.json"],
            hashlib.sha256((self.root / "lab/compatibility.json").read_bytes()).hexdigest(),
        )

    def test_readiness_report_enumerates_blockers_before_strict_check(self):
        status = policy.check(self.root)["readiness"]
        self.assertFalse(status["ready"])
        self.assertEqual(len(status["unimplemented_families"]), 30)
        self.assertTrue(status["contract_approval_pending"])
        self.assertIn("win11-pro", status["unqualified_profiles"])
        self.assertIn("MS-ADTS", status["unreviewed_specifications"])
        self.assertEqual(status["scenario_blockers"]["ldap-directory/positive"], "unrun")
        self.assertEqual(len(status["scenario_blockers"]), 60)
        self.assertIn("join-login/join-variants", status["unresolved_mappings"])

        self.passing_fixture()
        proof = self.evidence["records"][0].pop("review")
        self.save()
        self.assertEqual(
            policy.check(self.root)["readiness"]["scenario_blockers"],
            {"objects/positive": "review_pending"},
        )
        self.evidence["records"][0]["review"] = proof
        self.save()
        self.assertTrue(policy.check(self.root, require_ready=True)["readiness"]["ready"])

    def test_exchange_mappings_require_assertions_and_resolvable_sections(self):
        operation = self.contract["operations"][0]
        exchanges = copy.deepcopy(operation["exchanges"])
        changes = (
            ("expected_success", "", "success, refusal"),
            ("expected_refusal", None, "success, refusal"),
            ("required_evidence", "", "required evidence"),
            ("references", ["MS-ADTS#99.99"], "pinned section"),
            ("references", ["MS-NRPC#3.5.4.4.1"], "pinned section"),
            ("references", ["BABEL-ARCH"], "Wire exchange"),
            ("kind", "assumed", "Unknown exchange type"),
            ("kind", "unresolved", "requires a blocker"),
            ("blocker", "unmarked mapping", "requires unresolved status"),
        )
        for field, value, message in changes:
            operation["exchanges"] = copy.deepcopy(exchanges)
            operation["exchanges"][0][field] = value
            with (
                self.subTest(field=field, value=value),
                self.assertRaisesRegex(ValueError, message),
            ):
                self.check()
        operation["exchanges"] = []
        with self.assertRaisesRegex(ValueError, "exchanges"):
            self.check()

    def test_unknown_policy_and_project_references_cannot_disappear(self):
        unknown = self.contract["unmapped_exchange_policy"]
        unknown["owner"] = ""
        with self.assertRaisesRegex(ValueError, "Unmapped exchange policy"):
            self.check()
        unknown["owner"] = "fixture-owner"
        self.contract["project_references"][0]["heading"] = "Unlisted project heading"
        with self.assertRaisesRegex(ValueError, "Project reference heading"):
            self.check()

    def test_unresolved_exchange_prevents_otherwise_ready_fixture(self):
        self.passing_fixture()
        self.contract["operations"][0]["exchanges"][0].update(
            kind="unresolved", blocker="Unmapped fixture variant"
        )
        with self.assertRaisesRegex(ValueError, "Unresolved exchange mappings"):
            self.check(ready=True)

    def test_skip_unsupported_and_unrun_require_a_reason_and_never_pass_readiness(self):
        self.passing_fixture()
        row = self.evidence["records"][0]
        for outcome in ("skipped", "unsupported", "unrun"):
            row.update(outcome=outcome, executions=[], reason="missing lab")
            self.assertEqual(self.check()[outcome], 1)
            with self.assertRaisesRegex(ValueError, "non-passing"):
                self.check(ready=True)
        row["reason"] = ""
        with self.assertRaisesRegex(ValueError, "reason"):
            self.check()

    def test_fabricated_pass_missing_build_or_partial_comparison_fails(self):
        self.evidence["records"][0]["outcome"] = "passed"
        with self.assertRaisesRegex(ValueError, "actual executions"):
            self.check()
        self.passing_fixture()
        self.contract["profiles"][1]["build"] = None
        with self.assertRaisesRegex(ValueError, "build"):
            self.check()
        self.contract["profiles"][1]["build"] = "fixture-build"
        self.evidence["records"][0]["executions"].pop()
        with self.assertRaisesRegex(ValueError, "every declared profile"):
            self.check()

    def test_pass_requires_all_results_but_failed_observations_can_be_retained(self):
        self.passing_fixture()
        row = self.evidence["records"][0]
        row["executions"][0]["result"] = "failed"
        with self.assertRaisesRegex(ValueError, "failed execution"):
            self.check()
        row["outcome"] = "failed"
        self.assertEqual(self.check()["failed"], 1)
        with self.assertRaisesRegex(ValueError, "non-passing"):
            self.check(ready=True)

    def test_synthetic_complete_fixture_exercises_readiness_not_product_conformance(self):
        self.passing_fixture()
        self.assertEqual(self.check(ready=True), {"passed": 60})
        self.evidence["records"][0]["review"] = None
        with self.assertRaisesRegex(ValueError, "Unaccepted"):
            self.check(ready=True)

    def test_missing_spec_revision_and_unqualified_profile_block_ready_gate(self):
        self.passing_fixture()
        pinned_revision = self.contract["specifications"][0]["revision"]
        self.contract["specifications"][0]["revision"] = None
        with self.assertRaisesRegex(ValueError, "Specification revision"):
            self.check(ready=True)
        self.contract["specifications"][0]["revision"] = pinned_revision
        self.contract["profiles"][0]["qualification"] = "unqualified"
        with self.assertRaisesRegex(ValueError, "Unqualified"):
            self.check(ready=True)

    def test_execution_identity_time_duration_and_artifacts_are_checked(self):
        self.passing_fixture()
        run = self.evidence["records"][0]["executions"][0]
        original = copy.deepcopy(run)
        for field, value in (
            ("source_revision", "main"),
            ("profile", None),
            ("target", "other"),
            ("client_build", "other"),
            ("run_id", ""),
            ("duration_ms", True),
            ("started_at", "2026-11-18T00:00:00"),
            ("tools", {}),
            ("artifacts", []),
        ):
            run.clear()
            run.update(copy.deepcopy(original))
            run[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.check()

    def test_artifact_digest_traversal_and_parent_symlinks_are_rejected(self):
        self.passing_fixture()
        receipt = self.evidence["records"][0]["executions"][0]["artifacts"][0]
        receipt["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "digest"):
            self.check()
        receipt["path"] = "lab/evidence-artifacts/../../../private"
        with self.assertRaisesRegex(ValueError, "stay in"):
            self.check()
        receipt["path"] = "lab/evidence-artifacts/link/synthetic.txt"
        (self.root / "lab/evidence-artifacts/link").symlink_to(
            self.root / "lab/evidence-artifacts", target_is_directory=True
        )
        with self.assertRaisesRegex(ValueError, "symlinks"):
            self.check()

    def test_bad_review_metadata_is_not_acceptance(self):
        self.assertFalse(policy.review(None))
        for change in (
            {"date": "tomorrow"},
            {"date": 42},
            {"disposition": "pending"},
            {"scope": ""},
        ):
            proof = {
                "reviewer": "fixture",
                "date": "2026-11-18",
                "disposition": "accepted",
                "scope": "fixture",
            }
            proof.update(change)
            self.assertFalse(policy.review(proof))

    def test_contract_approval_and_implementation_cannot_be_bypassed(self):
        self.passing_fixture()
        self.contract["approval"] = None
        with self.assertRaisesRegex(ValueError, "not reviewed"):
            self.check(ready=True)
        self.contract["status"] = "unknown"
        with self.assertRaisesRegex(ValueError, "Unknown contract"):
            self.check()

    def test_unknown_outcome_and_duplicate_runs_cannot_inflate_coverage(self):
        self.evidence["records"][0]["outcome"] = "simulated_pass"
        with self.assertRaisesRegex(ValueError, "Unknown evidence outcome"):
            self.check()
        self.passing_fixture()
        row = self.evidence["records"][0]
        row["executions"].append(row["executions"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate profile/target"):
            self.check()

    def test_changed_assertion_does_not_reuse_a_passing_observation(self):
        self.passing_fixture()
        self.evidence["records"][0]["executions"][0]["expected"] = "different assertion"
        with self.assertRaisesRegex(ValueError, "expectation differs"):
            self.check()

    def test_owner_selected_functional_and_cross_platform_scope_is_preserved(self):
        self.contract["functional_level"]["domain"] = "2025"
        with self.assertRaisesRegex(ValueError, "functional-level scope"):
            self.check()
        self.contract["functional_level"]["domain"] = "2016"
        self.contract["profiles"] = [p for p in self.contract["profiles"] if p["id"] != "macos-arm"]
        with self.assertRaisesRegex(ValueError, "Windows/Linux/macOS"):
            self.check()
