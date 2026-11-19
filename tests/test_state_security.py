"""Protect design/source/rights boundaries without pretending to execute AD semantics."""

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_state_security as contract  # noqa: E402


class StateSecurityContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in (
            "lab/state-security-contract.json",
            "lab/specification-pins.json",
            "lab/compatibility.json",
            "docs/threat-model.md",
            "docs/requirements.md",
            "docs/security-roadmap.md",
            "docs/patch-management-roadmap.md",
            "docs/endpoint-operations-roadmap.md",
            "docs/adr/0005-directory-and-replication-invariants.md",
        ):
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        shutil.copytree(ROOT / "docs/phases", self.root / "docs/phases")
        self.state = json.loads((self.root / "lab/state-security-contract.json").read_text())
        self.registry = json.loads((self.root / "lab/specification-pins.json").read_text())

    def write(self):
        source = self.root / "lab/state-security-contract.json"
        source.write_text(json.dumps(self.state))
        self.registry["assets"][0]["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        (self.root / "lab/specification-pins.json").write_text(json.dumps(self.registry))

    def validate(self):
        self.write()
        return contract.validate(self.root)

    def test_committed_contract_and_report_never_infer_implementation_or_acceptance(self):
        state, registry = contract.validate(ROOT)
        self.assertEqual(len(state["cases"]), 20)
        self.assertEqual(len(state["boundaries"]), 11)
        self.assertEqual(len(registry["documents"]), 13)
        report = contract.check(ROOT, "a" * 40)
        self.assertEqual(report["native_runtime_outcomes"], "unrun")
        self.assertEqual(report["independent_assessment"], "not_performed")
        self.assertEqual(report["owner_acceptance"], "not_inferred")
        for name, expected in report["input_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected)
        with self.assertRaisesRegex(ValueError, "Full source revision"):
            contract.check(ROOT, "a" * 7)

    def test_schema_and_runtime_or_rights_claims_are_rejected(self):
        original_state, original_registry = copy.deepcopy(self.state), copy.deepcopy(self.registry)
        for target, key, value in (
            ("state", "schema_version", True),
            ("registry", "schema_version", 2),
            ("state", "status", "implemented"),
            ("state", "format_status", "frozen"),
            ("state", "production_assessment", "passed"),
            ("state", "source_documents", "other.json"),
            ("registry", "status", "cleared"),
            ("registry", "default_asset_disposition", "allow"),
        ):
            self.state, self.registry = (
                copy.deepcopy(original_state),
                copy.deepcopy(original_registry),
            )
            getattr(self, target)[key] = value
            with self.subTest(target=target, key=key), self.assertRaises(ValueError):
                self.validate()

    def test_missing_original_cases_and_boundaries_are_rejected(self):
        original = copy.deepcopy(self.state)
        for field in ("cases", "boundaries"):
            for index in range(len(original[field])):
                self.state = copy.deepcopy(original)
                del self.state[field][index]
                with self.subTest(field=field, index=index), self.assertRaises(ValueError):
                    self.validate()

    def test_state_case_requires_reviewable_denial_and_pinned_sections(self):
        original = copy.deepcopy(self.state)
        for key, value in (
            ("requirement", "P00-07"),
            ("owner", ""),
            ("initial_state", " "),
            ("operation", ""),
            ("expected", ""),
            ("denied_or_interrupted", None),
            ("runtime_outcome", "passed"),
            ("review", "accepted"),
            ("references", []),
            ("references", None),
        ):
            self.state = copy.deepcopy(original)
            self.state["cases"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate()
        for key, value in (
            ("document", "unknown"),
            ("section", "../../1"),
            ("title", ""),
            ("heading", "changed interpretation"),
            ("heading_sha256", "a" * 64),
        ):
            self.state = copy.deepcopy(original)
            self.state["cases"][0]["references"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate()

    def test_boundary_accountability_threats_and_independence_cannot_disappear(self):
        original = copy.deepcopy(self.state)
        for key, value in (
            ("accountable_owner", ""),
            ("assets", []),
            ("misuse_cases", [""]),
            ("required_denial_or_fault", ""),
            ("residual_risk", None),
            ("threats", ["T-99"]),
            ("implementation_gates", ["P99-99"]),
            ("review_model", "independent"),
            ("runtime_outcome", "passed"),
            ("independent_assessment", "performed"),
        ):
            self.state = copy.deepcopy(original)
            self.state["boundaries"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate()
        self.state = original
        for boundary in self.state["boundaries"]:
            boundary["threats"] = ["T-01"]
        with self.assertRaisesRegex(ValueError, "Every threat"):
            self.validate()
        (self.root / "docs/threat-model.md").write_text("# No canonical threats")
        with self.assertRaisesRegex(ValueError, "Canonical threat"):
            self.validate()

    def test_reference_versions_sources_sizes_notices_and_rights_are_bound(self):
        original = copy.deepcopy(self.registry)
        for key, value in (
            ("title", ""),
            ("reviewer", ""),
            ("reviewed_on", "not a date"),
            ("sha256", "a"),
            ("notice_sha256", ""),
            ("bytes", True),
            ("bytes", 0),
            ("bytes", 33 * 1024 * 1024),
            ("revision", "latest"),
            ("landing", "https://invalid.example"),
            ("url", "https://invalid.example/document.pdf"),
            ("copyright_notice", "patent_grant"),
            ("document_use", "redistribution"),
            ("patent_coverage", "approved"),
            ("image_fixture_rights", "granted"),
            ("redistribution_approval", "approved"),
        ):
            self.registry = copy.deepcopy(original)
            self.registry["documents"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate()
        self.registry = copy.deepcopy(original)
        self.registry["documents"].pop()
        with self.assertRaisesRegex(ValueError, "must be pinned"):
            self.validate()
        self.registry = original
        rfc = next(doc for doc in self.registry["documents"] if doc["id"] == "RFC4511")
        rfc["copyright_notice"] = "modern_bsd"
        with self.assertRaisesRegex(ValueError, "actual dated rights"):
            self.validate()

    def test_external_assets_are_denied_even_if_a_caller_lists_a_purpose(self):
        for identifier in ("unknown", "windows-reference-image", "macos-reference-image"):
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                contract.authorize_asset(
                    self.root, self.registry, identifier, "source_distribution"
                )
        contract.authorize_asset(self.root, self.registry, "state-design-examples", "unit_testing")
        with self.assertRaisesRegex(ValueError, "purpose"):
            contract.authorize_asset(
                self.root, self.registry, "state-design-examples", "production"
            )
        self.registry["assets"][1]["allowed_uses"] = ["testing"]
        with self.assertRaisesRegex(ValueError, "Unacquired"):
            self.validate()

    def test_asset_review_and_exact_source_cannot_be_silently_rebound(self):
        source = self.root / "lab/state-security-contract.json"
        source.write_text(source.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "digest changed"):
            contract.authorize_asset(
                self.root, self.registry, "state-design-examples", "unit_testing"
            )
        self.registry["assets"][0]["review_evidence"] = ""
        with self.assertRaisesRegex(ValueError, "rights block"):
            self.validate()
        self.registry["assets"] = self.registry["assets"][1:]
        (self.root / "lab/specification-pins.json").write_text(json.dumps(self.registry))
        with self.assertRaisesRegex(ValueError, "dispositions"):
            contract.validate(self.root)

    def test_asset_path_traversal_and_symlinks_are_rejected(self):
        for name in (None, "", "../escape", "/tmp/escape", "missing", "lab"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                contract.source_file(self.root, name)
        (self.root / "link").symlink_to(self.root / "lab", target_is_directory=True)
        (self.root / "direct").symlink_to(self.root / "lab/state-security-contract.json")
        for name in ("link/state-security-contract.json", "direct"):
            with self.assertRaisesRegex(ValueError, "symlink"):
                contract.source_file(self.root, name)

    def cache_fixture(self):
        cache = self.root / "cache"
        cache.mkdir()
        raw = b"synthetic fixed extractor input, not an upstream document"
        (cache / "MS-ADTS.pdf").write_bytes(raw)
        rfc = "Synthetic RFC text\n1 RFC heading\n"
        (cache / "RFC4511.txt").write_text(rfc)
        docs = [
            {
                "id": "MS-ADTS",
                "revision": "v20260824",
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            },
            {
                "id": "RFC4511",
                "bytes": len(rfc.encode()),
                "sha256": hashlib.sha256(rfc.encode()).hexdigest(),
            },
        ]
        state = {
            "cases": [
                {
                    "references": [
                        {"document": "MS-ADTS", "section": "1.2", "heading": "A heading"},
                        {"document": "RFC4511", "section": "1", "heading": "RFC heading"},
                    ]
                }
            ]
        }
        return cache, state, {"documents": docs}

    @patch.object(contract.subprocess, "run")
    def test_cache_checks_exact_bytes_edition_and_actual_section_headings(self, run):
        cache, state, registry = self.cache_fixture()
        run.return_value.stdout = "[MS-ADTS]: test v20260824\n\f1.2  A   heading\n"
        self.assertEqual(contract.verify_cache(cache, state, registry), 2)
        self.assertEqual(
            run.call_args.args[0],
            ["pdftotext", "-layout", str((cache / "MS-ADTS.pdf").resolve()), "-"],
        )
        self.assertEqual(run.call_args.kwargs["timeout"], 30)
        for output in ("protected wrapper", "[MS-ADTS]: v20260824\n1.2 Wrong heading"):
            run.return_value.stdout = output
            with self.subTest(output=output), self.assertRaises(ValueError):
                contract.verify_cache(cache, state, registry)
        run.side_effect = subprocess.TimeoutExpired("pdftotext", 30)
        with self.assertRaises(subprocess.SubprocessError):
            contract.verify_cache(cache, state, registry)

    def test_missing_changed_duplicate_and_symlinked_cached_documents_are_rejected(self):
        cache, state, registry = self.cache_fixture()
        pdf = cache / "MS-ADTS.pdf"
        original = pdf.read_bytes()
        pdf.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "bytes unavailable"):
            contract.verify_cache(cache, state, registry)
        pdf.write_bytes(original)
        alternate = cache / "MS-ADTS-current.pdf"
        alternate.write_bytes(original)
        with self.assertRaisesRegex(ValueError, "bytes unavailable"):
            contract.verify_cache(cache, state, registry)
        pdf.unlink()
        pdf.symlink_to(alternate)
        alternate.rename(cache / "other.pdf")
        with self.assertRaisesRegex(ValueError, "bytes unavailable"):
            contract.verify_cache(cache, state, registry)


if __name__ == "__main__":
    unittest.main()
