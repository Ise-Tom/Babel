"""Regression tests for source packaging and fail-closed CI scope."""

import gzip
import hashlib
import importlib.util
import io
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope = load("check_ci_scope")
package = load("package_source")


class ComponentScope(unittest.TestCase):
    def test_repository_tooling_is_supported(self):
        self.assertEqual(
            scope.check(
                ROOT,
                [
                    "scripts/tool.py",
                    "tests/test_tool.py",
                    "docs/a.md",
                    "docs/github-main-ruleset.json",
                    ".github/workflows/ci.yml",
                    "requirements-ci.txt",
                    "lab/windows-reference.toml",
                    "lab/phase0-contract.json",
                    "experiments/postgres_store/schema.sql",
                    "experiments/postgres_store/experiment.py",
                ],
            ),
            [],
        )

    def test_reviewed_native_component_and_fuzz_scope_are_registered(self):
        self.assertEqual(
            scope.check(
                ROOT,
                [
                    "Cargo.toml",
                    "Cargo.lock",
                    "rust-toolchain.toml",
                    "deny.toml",
                    "native/babel-ldap/Cargo.toml",
                    "native/babel-ldap/src/lib.rs",
                    "native/babel-ldap/tests/transport.rs",
                    "native/babel-ldap/tests/smoke_ldap.py",
                    "fuzz/Cargo.lock",
                    "fuzz/fuzz_targets/ldap_frame.rs",
                    "fuzz/corpus/ldap_frame/rootdse",
                ],
            ),
            [],
        )

    def test_dashboard_scope_is_registered_with_its_own_gates(self):
        self.assertEqual(
            scope.check(
                ROOT,
                [
                    "dashboard/package.json",
                    "dashboard/package-lock.json",
                    "dashboard/build.d.mts",
                    "dashboard/src/main.ts",
                    "dashboard/src/style.css",
                    "dashboard/tests/build.test.mjs",
                    "dashboard/progress.json",
                ],
            ),
            [],
        )

    def test_new_languages_and_build_manifests_need_gates(self):
        names = [
            "dashboard/unregistered.go",
            "dashboard/src/unreviewed.py",
            "src/server.go",
            "native/unregistered/src/main.rs",
            "native/babel-ldap/other.js",
            "fuzz/unreviewed.rs",
            "src/server.py",
            "unregistered/Cargo.toml",
            "package.json",
            "Dockerfile",
            "docs/package.json",
            "lab/unreviewed.toml",
            "experiments/postgres_store/unreviewed.sql",
            "experiments/unreviewed/experiment.py",
            "scripts/run.sh",
        ]
        self.assertEqual(len(scope.check(ROOT, names)), len(names))

    def test_symlink_cannot_hide_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").symlink_to(ROOT / "README.md")
            self.assertEqual(len(scope.check(root, ["README.md"])), 1)

    def test_only_the_named_ruleset_is_supported_and_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            path = root / "docs/github-main-ruleset.json"
            for contents in ("invalid", "[]"):
                path.write_text(contents)
                self.assertTrue(scope.check(root, ["docs/github-main-ruleset.json"]))
            path.write_text("{}")
            self.assertEqual(scope.check(root, ["docs/github-main-ruleset.json"]), [])
            self.assertTrue(scope.check(root, ["docs/other-ruleset.json"]))


class SourcePackaging(unittest.TestCase):
    def test_deterministic_commit_archive_and_checksum_exclude_local_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
            (root / "README.md").write_text("committed content\n")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "-c",
                    "commit.gpgsign=false",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                cwd=root,
                check=True,
            )
            (root / "README.md").write_text("uncommitted modification\n")
            (root / "private.txt").write_text("untracked fixture\n")
            first = package.build(root, "v0.1.0-alpha.1", root / "one")
            second = package.build(root, "v0.1.0-alpha.1", root / "two")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(
                (first.parent / "SHA256SUMS").read_text(),
                f"{hashlib.sha256(first.read_bytes()).hexdigest()}  {first.name}\n",
            )
            with tarfile.open(fileobj=io.BytesIO(gzip.decompress(first.read_bytes()))) as archive:
                self.assertEqual(
                    archive.getnames(), ["Babel-v0.1.0-alpha.1", "Babel-v0.1.0-alpha.1/README.md"]
                )
                self.assertEqual(
                    archive.extractfile("Babel-v0.1.0-alpha.1/README.md").read(),
                    b"committed content\n",
                )

    def test_invalid_tag_cannot_become_archive_path(self):
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            package.build(Path(directory), "../../escape", Path(directory) / "output")

    def test_git_failure_cannot_create_success_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(subprocess.CalledProcessError):
                package.build(root, "v0.1.0-rc.1", root / "output")
            self.assertFalse((root / "output").exists())
