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
        self.output = self.root / "out"

    def assemble(self):
        return notices.assemble(
            self.meta, self.project, self.docs, self.output, selected=("local",)
        )

    def test_actual_nested_terms_project_and_rust_notices_are_retained(self):
        manifest = self.assemble()
        notices.verify(self.output)
        self.assertEqual(len(manifest["packages"]), 1)
        self.assertEqual(len(manifest["files"]), 7)
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
                self.meta, self.project, self.docs, self.root / "other", selected=("local",)
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
