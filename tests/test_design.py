"""Regression tests for incomplete or contradictory phase requirement structure."""

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_design", ROOT / "scripts/check_design.py")
design = importlib.util.module_from_spec(spec)
spec.loader.exec_module(design)


class DesignIntegrity(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "docs", self.root / "docs")
        self.phase = self.root / "docs/phases/phase-00.md"

    def rewrite(self, old, new):
        self.phase.write_text(self.phase.read_text().replace(old, new))

    def test_current_baseline_covers_every_phase_and_catalog(self):
        self.assertEqual(design.check(self.root), [])

    def test_missing_phase_is_rejected(self):
        self.phase.unlink()
        self.assertTrue(any("Missing phase" in error for error in design.check(self.root)))

    def test_duplicate_or_wrong_phase_ids_are_rejected(self):
        self.rewrite("| P00-02 |", "| P00-01 |")
        self.assertTrue(any("unique IDs" in error for error in design.check(self.root)))

    def test_wrong_phase_requirement_is_rejected(self):
        self.rewrite("| P00-02 |", "| P01-02 |")
        self.assertTrue(any("belonging to this phase" in e for e in design.check(self.root)))

    def test_phase_counts_can_differ_and_ids_need_not_be_contiguous(self):
        # Synthetic scope changes exercise the validator, not removal of real requirements.
        lines = self.phase.read_text().splitlines()
        self.phase.write_text(
            "\n".join(line for line in lines if not line.startswith("| P00-02 |"))
        )
        other = self.root / "docs/phases/phase-01.md"
        other.write_text(other.read_text() + "\n| P01-42 | Additional fixture | Test evidence |\n")
        self.assertEqual(design.check(self.root), [])

    def test_empty_requirement_list_is_rejected(self):
        self.phase.write_text(
            "\n".join(
                line
                for line in self.phase.read_text().splitlines()
                if not line.startswith("| P00-")
            )
        )
        self.assertTrue(any("unique IDs" in error for error in design.check(self.root)))

    def test_unknown_requirement_is_rejected(self):
        self.rewrite("Traceability: PLAT-01,", "Traceability: UNKNOWN-99,")
        self.assertTrue(any("unknown requirement" in error for error in design.check(self.root)))

    def test_empty_acceptance_is_rejected(self):
        text = self.phase.read_text()
        line = next(line for line in text.splitlines() if line.startswith("| P00-01 |"))
        parts = line.split("|")
        parts[-2] = " "
        self.rewrite(line, "|".join(parts))
        self.assertTrue(any("empty requirement" in error for error in design.check(self.root)))

    def test_missing_sections_and_status_are_rejected(self):
        self.rewrite("## Design and interfaces", "## Other")
        self.rewrite("Status: specified; product acceptance not demonstrated.", "Status: complete")
        failures = design.check(self.root)
        self.assertTrue(any("non-acceptance status" in error for error in failures))
        self.assertTrue(any("missing or empty" in error for error in failures))

    def test_new_unassigned_global_requirement_is_rejected(self):
        catalog = self.root / "docs/requirements.md"
        catalog.write_text(catalog.read_text() + "\n| AD-99 | New requirement | Evidence |\n")
        self.assertTrue(any("Unassigned global" in error for error in design.check(self.root)))

    def test_duplicate_global_definition_is_rejected(self):
        catalog = self.root / "docs/requirements.md"
        catalog.write_text(catalog.read_text() + "\n| AD-01 | Duplicate | Evidence |\n")
        self.assertTrue(any("Duplicate global" in error for error in design.check(self.root)))

    def test_missing_catalog_and_extra_phase_are_rejected(self):
        (self.root / "docs/security-roadmap.md").unlink()
        (self.root / "docs/phases/phase-18.md").write_text("unregistered")
        failures = design.check(self.root)
        self.assertTrue(any("Missing requirement catalog" in error for error in failures))
        self.assertTrue(any("Unregistered phase" in error for error in failures))

    def test_lost_baseline_and_traceability_line_are_rejected(self):
        catalog = self.root / "docs/requirements.md"
        catalog.write_text(catalog.read_text().replace("| PLAT-01 |", "| LOST-01 |"))
        self.rewrite("Traceability:", "References:")
        failures = design.check(self.root)
        self.assertTrue(any("Missing baseline requirement" in error for error in failures))
        self.assertTrue(any("explicit traceability" in error for error in failures))

    def test_wrong_phase_heading_is_rejected(self):
        self.rewrite("# Phase 00 — ", "# Phase 42 — ")
        self.assertTrue(any("wrong phase heading" in error for error in design.check(self.root)))
