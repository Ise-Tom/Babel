"""Actual upstream notices must survive packaging without silent omission or replacement."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import collect_native_notices as notices  # noqa: E402


class NativeNotices(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        for name in ("LICENSE", "NOTICE", "DCO"):
            (self.project / name).write_text("Synthetic project fixture notice\n")
        self.package = self.root / "test-crate-1.0.0"
        self.package.mkdir()
        (self.package / "LICENSE").write_text("Synthetic copyright and permission terms\n")
        (self.package / "third-party").mkdir()
        (self.package / "third-party/NOTICE").write_text("Nested upstream notice\n")
        self.docs = self.root / "rust-docs"
        self.docs.mkdir()
        (self.docs / "licenses").mkdir()
        (self.docs / "COPYRIGHT-library.html").write_text("Synthetic Rust library notice fixture\n")
        (self.docs / "licenses/MIT.txt").write_text("Synthetic license text\n")
        self.meta = {
            "packages": [
                {"name": "local", "id": "local-id", "source": None},
                {
                    "name": "test-crate",
                    "id": "crate-id",
                    "version": "1.0.0",
                    "source": "registry+https://github.com/rust-lang/crates.io-index",
                    "license": "MIT",
                    "manifest_path": str(self.package / "Cargo.toml"),
                },
            ]
        }
        self.meta["resolve"] = {
            "nodes": [
                {"id": "local-id", "deps": [{"pkg": "crate-id", "dep_kinds": [{"kind": None}]}]},
                {"id": "crate-id", "deps": []},
            ]
        }
        self.system = self.root / "system"
        for name in notices.SYSTEM_TERMS.values():
            target = self.system / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("Synthetic system runtime license/copyright fixture\n")
        self.output = self.root / "out"

    def assemble(self):
        return notices.assemble(
            self.meta,
            self.project,
            self.docs,
            self.output,
            selected=("local",),
            system_root=self.system,
        )

    def test_actual_nested_terms_project_and_rust_notices_are_retained(self):
        manifest = self.assemble()
        notices.verify(self.output)
        self.assertEqual(len(manifest["packages"]), 1)
        self.assertEqual(len(manifest["files"]), 13)
        self.assertEqual(
            (self.output / "third-party/test-crate-1.0.0/third-party/NOTICE").read_bytes(),
            (self.package / "third-party/NOTICE").read_bytes(),
        )
        with self.assertRaises(FileExistsError):
            self.assemble()

    def test_explicit_license_file_is_included(self):
        (self.package / "terms.txt").write_text("Explicit retained terms\n")
        self.meta["packages"][1]["license_file"] = "terms.txt"
        self.assertEqual(len(self.assemble()["packages"][0]["notices"]), 3)

    def test_missing_unknown_or_unsafe_inputs_fail(self):
        self.meta["packages"][1]["source"] = "git+https://unreviewed.example"
        with self.assertRaises(ValueError):
            self.assemble()
        self.output = self.root / "bad-2"
        self.meta["packages"][1]["source"] = "registry+https://github.com/rust-lang/crates.io-index"
        self.meta["packages"][1]["name"] = "../escape"
        with self.assertRaises(ValueError):
            self.assemble()

    def test_missing_terms_and_symlinked_terms_cannot_qualify(self):
        (self.package / "LICENSE").unlink()
        (self.package / "third-party/NOTICE").unlink()
        with self.assertRaises(ValueError):
            self.assemble()
        (self.package / "LICENSE").symlink_to(self.project / "LICENSE")
        with self.assertRaises(ValueError):
            notices.assemble(
                self.meta,
                self.project,
                self.docs,
                self.root / "other",
                selected=("local",),
                system_root=self.system,
            )

    def test_empty_or_oversized_terms_fail(self):
        (self.package / "LICENSE").write_text("")
        with self.assertRaises(ValueError):
            self.assemble()

    def test_tampered_missing_or_traversal_notices_fail_verification(self):
        self.assemble()
        target = self.output / "project/LICENSE"
        target.write_text("Tampered same tool data\n")
        with self.assertRaises(ValueError):
            notices.verify(self.output)
        manifest = json.loads((self.output / "manifest.json").read_text())
        manifest["files"][0]["path"] = "../private"
        (self.output / "manifest.json").write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            notices.verify(self.output)

    def test_runtime_closure_excludes_dev_only_code_without_skipping_license_audit(self):
        self.meta["resolve"]["nodes"][0]["deps"].append(
            {"pkg": "dev-id", "dep_kinds": [{"kind": "dev"}]}
        )
        self.assertEqual(notices.runtime_closure(self.meta, ("local",)), {"local-id", "crate-id"})
        self.meta["resolve"]["nodes"][0]["deps"].append(
            {"pkg": "local-id", "dep_kinds": [{"kind": None}]}
        )
        self.assertEqual(notices.runtime_closure(self.meta, ("local",)), {"local-id", "crate-id"})
        with self.assertRaises(ValueError):
            notices.runtime_closure(self.meta, ("missing",))
        with self.assertRaises(ValueError):
            notices.runtime_closure({"packages": None}, ("local",))

    def test_same_length_notice_tampering_is_detected_by_digest(self):
        self.assemble()
        path = self.output / "project/LICENSE"
        data = path.read_bytes()
        path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaisesRegex(ValueError, "digest"):
            notices.verify(self.output)

    def test_omitted_unlisted_required_or_unaccounted_notices_cannot_pass(self):
        self.assemble()
        path = self.output / "manifest.json"
        original = json.loads(path.read_text())
        for edit in (
            "omit",
            "missing_project",
            "missing_rust",
            "missing_system",
            "drop_package",
            "duplicate_package",
            "wrong_package",
            "empty_terms",
            "missing_license",
            "missing_roots",
            "missing_inventory",
        ):
            manifest = json.loads(json.dumps(original))
            if edit == "omit":
                manifest["files"].pop()
            elif edit == "missing_project":
                manifest["files"] = [r for r in manifest["files"] if r["path"] != "project/LICENSE"]
            elif edit == "missing_rust":
                manifest["files"] = [
                    r for r in manifest["files"] if not r["path"].startswith("rust/licenses/")
                ]
            elif edit == "missing_system":
                manifest["files"] = [r for r in manifest["files"] if r["path"] != "system/LGPL-2.1"]
            elif edit == "drop_package":
                manifest["packages"] = []
            elif edit == "duplicate_package":
                manifest["packages"].append(manifest["packages"][0])
            elif edit == "wrong_package":
                manifest["packages"][0]["name"] = "wrong"
            elif edit == "empty_terms":
                manifest["packages"][0]["notices"] = []
            elif edit == "missing_license":
                manifest["packages"][0]["license"] = ""
            elif edit == "missing_roots":
                manifest["root_packages"] = []
            else:
                manifest["packages"] = None
            path.write_text(json.dumps(manifest))
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                notices.verify(self.output)

    def test_expected_manifest_digest_survives_extraction_and_detects_rewritten_terms(self):
        import hashlib

        self.assemble()
        path = self.output / "manifest.json"
        expected = hashlib.sha256(path.read_bytes()).hexdigest()
        notices.verify(self.output, expected)
        with self.assertRaisesRegex(ValueError, "manifest digest"):
            notices.verify(self.output, "invalid")
        manifest = json.loads(path.read_text())
        manifest["scope"] = "Tampered claim"
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "manifest digest"):
            notices.verify(self.output, expected)

    def test_additional_symlinks_and_unlisted_files_fail_even_when_manifest_is_unchanged(self):
        self.assemble()
        extra = self.output / "extra"
        extra.write_text("Unlisted terms")
        with self.assertRaisesRegex(ValueError, "tree and manifest"):
            notices.verify(self.output)
        extra.unlink()
        extra.symlink_to(self.project, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            notices.verify(self.output)

    def test_missing_symlinked_manifest_and_symlinked_root_are_rejected(self):
        self.assemble()
        path = self.output / "manifest.json"
        raw = path.read_bytes()
        path.unlink()
        with self.assertRaisesRegex(ValueError, "manifest"):
            notices.verify(self.output)
        other = self.root / "manifest-copy"
        other.write_bytes(raw)
        path.symlink_to(other)
        with self.assertRaisesRegex(ValueError, "manifest"):
            notices.verify(self.output)
        link = self.root / "linked-root"
        link.symlink_to(self.output, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "directory"):
            notices.verify(link)

    def test_system_runtime_terms_are_required_and_cannot_escape_the_trusted_tree(self):
        path = self.system / "common-licenses/LGPL-2.1"
        path.unlink()
        with self.assertRaises(ValueError):
            self.assemble()
        path.symlink_to(self.project / "LICENSE")
        with self.assertRaises(ValueError):
            notices.assemble(
                self.meta,
                self.project,
                self.docs,
                self.root / "escaped-system",
                selected=("local",),
                system_root=self.system,
            )
