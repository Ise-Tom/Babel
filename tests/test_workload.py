"""Fixture integrity, independent relational invariants and bounded deterministic generation."""

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_workload as audit  # noqa: E402
import generate_workload as generator  # noqa: E402


class SyntheticWorkload(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "dataset"
        self.manifest = generator.generate(
            self.output,
            seed="fixture-1",
            source_revision="a" * 40,
            profile=generator.PROFILES["smoke"],
        )

    def save(self):
        (self.output / "manifest.json").write_bytes(generator.encoded(self.manifest))

    def change_rows(self, name, change):
        path = self.output / name
        rows = [json.loads(row) for row in path.read_bytes().splitlines()]
        change(rows)
        raw = b"".join(generator.encoded(row) for row in rows)
        path.write_bytes(raw)
        self.manifest["files"][name] = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "records": len(rows),
        }
        self.save()

    def test_smoke_profile_has_exact_counts_and_no_claimed_benchmark(self):
        result = audit.verify(self.output)
        self.assertEqual(result["objects"], 165)
        self.assertEqual(result["principal_membership_edges"], 508)
        self.assertEqual(result["nested_group_edges"], 12)
        self.assertEqual(result["max_effective_group_count"], 100)
        self.assertTrue(all(v is None for v in result["unmeasured"].values()))
        self.assertFalse(self.manifest["import_supported"])

    def test_same_inputs_are_byte_identical_and_different_seed_changes_identity(self):
        second = self.root / "second"
        same = generator.generate(
            second, seed="fixture-1", source_revision="a" * 40, profile=generator.PROFILES["smoke"]
        )
        self.assertEqual(same, self.manifest)
        for path in self.output.iterdir():
            self.assertEqual(path.read_bytes(), (second / path.name).read_bytes())
        different = generator.generate(
            self.root / "third",
            seed="fixture-2",
            source_revision="a" * 40,
            profile=generator.PROFILES["smoke"],
        )
        self.assertNotEqual(different["domain_sid"], same["domain_sid"])
        self.assertNotEqual(different["files"], same["files"])
        audit.verify(self.root / "third")

    def test_profile_and_inputs_are_bounded_before_creating_output(self):
        for changes in (
            {"users": 0},
            {"computers": True},
            {"groups": 80},
            {"ous": 21},
            {"users": 10020},
            {"gpos": 0},
            {"gpos": True},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                generator.generate(
                    self.root / "bad",
                    seed="valid",
                    source_revision="a" * 40,
                    profile=replace(generator.PROFILES["smoke"], **changes),
                )
            self.assertFalse((self.root / "bad").exists())
        for seed, revision in (("../escape", "a" * 40), ("valid", "main")):
            with self.assertRaises(ValueError):
                generator.generate(self.root / "bad", seed=seed, source_revision=revision)
        with self.assertRaises(ValueError):
            generator.buckets("s", "p", 1, (1, 2), (20, 80))

    def test_existing_and_symlink_outputs_are_not_overwritten(self):
        marker = self.output / "keep"
        marker.write_text("preserve")
        with self.assertRaises(FileExistsError):
            generator.generate(self.output, seed="s", source_revision="a" * 40)
        self.assertEqual(marker.read_text(), "preserve")
        link = self.root / "link"
        link.symlink_to(self.output, target_is_directory=True)
        with self.assertRaises(ValueError):
            generator.generate(link / "child", seed="s", source_revision="a" * 40)
        with self.assertRaises(ValueError):
            audit.verify(link)

    def test_partial_write_is_not_a_verified_completed_dataset(self):
        with patch.object(generator.Writer, "append", side_effect=OSError("synthetic disk fault")):
            with self.assertRaises(OSError):
                generator.generate(
                    self.root / "partial",
                    seed="s",
                    source_revision="a" * 40,
                    profile=generator.PROFILES["smoke"],
                )
        self.assertFalse((self.root / "partial/manifest.json").exists())
        with self.assertRaisesRegex(ValueError, "incomplete"):
            audit.verify(self.root / "partial")

    def test_sampler_is_unique_and_has_a_work_bound(self):
        values = generator.choose_groups("fixture", 0, 100, 100)
        self.assertEqual(sorted(values), list(range(100)))
        with self.assertRaises(ValueError):
            generator.choose_groups("fixture", 0, 101, 100)
        with patch.object(generator, "score", return_value=b"\xff" * 32):
            with self.assertRaisesRegex(ValueError, "exhausted"):
                generator.choose_groups("fixture", 0, 1, 100)
        with patch.object(generator, "score", return_value=b"\x00" * 32):
            with self.assertRaisesRegex(ValueError, "exhausted"):
                generator.choose_groups("fixture", 0, 2, 100)

    def test_file_digest_is_checked_even_when_rows_are_valid(self):
        self.manifest["files"]["objects.ndjson"]["sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(ValueError, "digest"):
            audit.verify(self.output)

    def test_unknown_fields_cannot_hide_credentials_in_object_records(self):
        def change(rows):
            rows[20]["password"] = "synthetic-forbidden-field"

        self.change_rows("objects.ndjson", change)
        with self.assertRaisesRegex(ValueError, "principal fields"):
            audit.verify(self.output)

    def test_duplicate_guid_sid_and_wrong_ou_are_rejected_even_after_rehash(self):
        original = (self.output / "objects.ndjson").read_bytes()
        manifest = copy.deepcopy(self.manifest)
        for field, value in (("guid", "guid"), ("sid", "sid"), ("ou_guid", "guid")):
            (self.output / "objects.ndjson").write_bytes(original)
            self.manifest = copy.deepcopy(manifest)

            def change(rows, field=field, value=value):
                rows[21][field] = rows[20][value]

            self.change_rows("objects.ndjson", change)
            with self.subTest(field=field), self.assertRaises(ValueError):
                audit.verify(self.output)

    def test_count_site_dn_and_payload_semantics_are_independent_of_file_hash(self):
        original = (self.output / "objects.ndjson").read_bytes()
        manifest = copy.deepcopy(self.manifest)
        for change in (
            lambda rows: rows.pop(),
            lambda rows: rows[20].update(site="unknown"),
            lambda rows: rows[20].update(dn_label="CN=other,DC=production"),
            lambda rows: rows[20].update(payload="x" * 512),
            lambda rows: rows[20].update(enabled=False),
            lambda rows: rows[20].update(name="invalid"),
            lambda rows: rows[0].update(name="wrong"),
        ):
            (self.output / "objects.ndjson").write_bytes(original)
            self.manifest = copy.deepcopy(manifest)
            self.change_rows("objects.ndjson", change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                audit.verify(self.output)

    def test_duplicate_unknown_and_cyclic_membership_is_rejected(self):
        original = (self.output / "memberships.ndjson").read_bytes()
        manifest = copy.deepcopy(self.manifest)
        for change in (
            lambda rows: rows.append(rows[0]),
            lambda rows: rows[0].update(member_guid="unknown"),
            lambda rows: rows[0].update(group_guid="unknown"),
            lambda rows: rows.append(
                {
                    **rows[-1],
                    "group_guid": rows[-1]["member_guid"],
                    "member_guid": rows[-1]["group_guid"],
                }
            ),
        ):
            (self.output / "memberships.ndjson").write_bytes(original)
            self.manifest = copy.deepcopy(manifest)
            self.change_rows("memberships.ndjson", change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                audit.verify(self.output)

    def test_wrong_distribution_and_runtime_claims_are_rejected(self):
        original = copy.deepcopy(self.manifest)
        for change in (
            lambda m: m.update(schema_version=True),
            lambda m: m.update(generator_version=2),
            lambda m: m.update(generator_version=True),
            lambda m: m.update(sid_history_values=1),
            lambda m: m.update(extra_benchmark_claim=100),
            lambda m: m.update(import_supported=True),
            lambda m: m["unmeasured"].update(throughput=100),
            lambda m: m["input_sha256"].update({"lab/compatibility.json": "0" * 64}),
            lambda m: m.update(direct_memberships={"1": 40}),
            lambda m: m.update(payload_bytes={"512": 140}),
            lambda m: m.update(nesting_depths=[1, 3, 9]),
            lambda m: m.update(topology=[]),
            lambda m: m.update(domain_sid="S-1-5-21-9999999999-1-1"),
        ):
            self.manifest = copy.deepcopy(original)
            change(self.manifest)
            self.save()
            with self.subTest(change=change), self.assertRaises(ValueError):
                audit.verify(self.output)

    def test_negative_cases_are_inputs_and_have_real_cycle_and_depth_shapes(self):
        path = self.output / "negative-fixtures.json"
        data = json.loads(path.read_bytes())
        self.assertIn("not executed", data["scope"])
        data["cases"][0]["edges"].pop()
        raw = generator.encoded(data)
        path.write_bytes(raw)
        self.manifest["files"][path.name].update(
            sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)
        )
        self.save()
        with self.assertRaisesRegex(ValueError, "acyclic"):
            audit.verify(self.output)

    def test_bounded_reader_and_directory_inventory_reject_extra_or_oversized_data(self):
        (self.output / "extra").write_text("unexpected")
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            audit.verify(self.output)
        (self.output / "extra").unlink()
        (self.output / "objects.ndjson").write_bytes(b"x" * (audit.MAX_LINE + 1))
        with self.assertRaisesRegex(ValueError, "Oversized"):
            audit.verify(self.output)
        with patch.object(audit, "MAX_FILE", 1):
            with self.assertRaisesRegex(ValueError, "oversized"):
                audit.verify(self.output)

    def test_acyclic_graph_with_wrong_chain_profiles_is_not_accepted(self):
        objects = [
            json.loads(line) for line in (self.output / "objects.ndjson").read_bytes().splitlines()
        ]
        groups = [row["guid"] for row in objects if row["kind"] == "group"]

        def change(rows):
            del rows[-12:]
            for start, depth in ((0, 4), (5, 8)):
                rows.extend(
                    {
                        "kind": "nested",
                        "group_guid": groups[start + i],
                        "member_guid": groups[start + i + 1],
                    }
                    for i in range(depth)
                )

        self.change_rows("memberships.ndjson", change)
        with self.assertRaisesRegex(ValueError, "chain profiles"):
            audit.verify(self.output)

    def test_missing_membership_cannot_retain_the_declared_distribution(self):
        self.change_rows("memberships.ndjson", lambda rows: rows.pop(0))
        with self.assertRaisesRegex(ValueError, "membership distribution"):
            audit.verify(self.output)

    def test_declared_negative_depth_must_actually_exceed_its_budget(self):
        path = self.output / "negative-fixtures.json"
        data = json.loads(path.read_bytes())
        data["cases"][1]["edges"].pop()
        raw = generator.encoded(data)
        path.write_bytes(raw)
        self.manifest["files"][path.name].update(
            sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)
        )
        self.save()
        with self.assertRaisesRegex(ValueError, "within budget"):
            audit.verify(self.output)
