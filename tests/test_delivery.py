"""Regression tests for source packaging and fail-closed CI scope."""

import gzip
import hashlib
import importlib.util
import io
import json
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
                    "lab/state-security-contract.json",
                    "lab/specification-pins.json",
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
    def commit_fixture(self, root):
        subprocess.run(["git", "add", "--all"], cwd=root, check=True)
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

    def fixture(self, root):
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=root, check=True)
        (root / "README.md").write_bytes(b"committed content\n")
        fixtures = root / "fuzz/corpus/ldap_frame"
        fixtures.mkdir(parents=True)
        seed = fixtures / "rootdse"
        seed.write_bytes(b"\x30\x00")
        registry_path = root / package.REGISTRY
        registry_path.parent.mkdir()
        registry = {
            "documents": [
                {
                    "id": "fixture-doc",
                    "sha256": hashlib.sha256(b"synthetic publisher placeholder").hexdigest(),
                }
            ],
            "assets": [
                {
                    "id": "project-fixture",
                    "path": seed.relative_to(root).as_posix(),
                    "sha256": hashlib.sha256(seed.read_bytes()).hexdigest(),
                    "kind": "project_synthetic",
                    "rights": "owner_selected_project_license",
                    "allowed_uses": ["unit_testing", "source_distribution"],
                    "review_evidence": "Project-owned synthetic parser fixture",
                },
                {
                    "id": "vendor-image-placeholder",
                    "kind": "windows_image",
                    "path": None,
                    "sha256": None,
                    "review_evidence": None,
                    "selected_version": None,
                    "candidate": "No real image used",
                    "publisher_terms": ["https://example.invalid/terms"],
                    "missing_evidence": "Synthetic negative control",
                    "rights": "unprovided",
                    "allowed_uses": [],
                },
            ],
        }
        return seed, registry_path, registry

    def test_deterministic_commit_archive_and_checksum_exclude_local_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed, registry_path, registry = self.fixture(root)
            committed_seed = seed.read_bytes()
            registry_path.write_text(json.dumps(registry))
            self.commit_fixture(root)
            (root / "README.md").write_text("uncommitted modification")
            (root / "private.txt").write_text("untracked fixture")
            seed.write_bytes(b"Working-tree fixture differs from Git")
            report_path = root / "audit.json"
            first = package.build(root, "v0.1.0-alpha.1", root / "one", audit_report=report_path)
            second = package.build(root, "v0.1.0-alpha.1", root / "two")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            archive_digest = hashlib.sha256(first.read_bytes()).hexdigest()
            self.assertEqual(
                (first.parent / "SHA256SUMS").read_text(), f"{archive_digest}  {first.name}\n"
            )
            report = json.loads(report_path.read_bytes())
            self.assertEqual(report["archive_sha256"], archive_digest)
            self.assertEqual(report["regular_files"], 3)
            self.assertEqual(report["approved_project_assets"][0]["id"], "project-fixture")
            self.assertRegex(report["source_revision"], r"^[a-f0-9]{40}$")
            with tarfile.open(fileobj=io.BytesIO(gzip.decompress(first.read_bytes()))) as archive:
                prefix = "Babel-v0.1.0-alpha.1/"
                self.assertEqual(
                    sorted(m.name.removeprefix(prefix) for m in archive if m.isfile()),
                    ["README.md", "fuzz/corpus/ldap_frame/rootdse", package.REGISTRY],
                )
                self.assertEqual(
                    archive.extractfile(prefix + "README.md").read(), b"committed content\n"
                )
                self.assertEqual(
                    archive.extractfile(prefix + seed.relative_to(root).as_posix()).read(),
                    committed_seed,
                )

    def test_source_archive_rejects_unapproved_assets_and_uses_before_writing(self):
        cases = {
            "unexpected-image": "Unapproved source archive member",
            "renamed-document": "Publisher document or opaque payload",
            "pinned-document": "Pinned publisher document",
            "unregistered-seed": "Unregistered fixture",
            "unknown-purpose": "Asset purpose not approved",
            "changed-seed": "Asset source digest changed",
            "unauthorized-external": "Unprovided external-image/capture rights",
        }
        for case, message in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                seed, registry_path, registry = self.fixture(root)
                if case == "unexpected-image":
                    (root / "lab/placeholder.iso").write_bytes(b"Project-authored mock image")
                elif case == "renamed-document":
                    (root / "README.md").write_bytes(b"%PDF-1.7\nProject-authored mock PDF")
                elif case == "pinned-document":
                    (root / "README.md").write_bytes(b"synthetic publisher placeholder")
                elif case == "unregistered-seed":
                    registry["assets"].pop(0)
                elif case == "unknown-purpose":
                    registry["assets"][0]["allowed_uses"] = ["unit_testing"]
                elif case == "changed-seed":
                    seed.write_bytes(b"Project-authored but changed fixture")
                else:
                    registry["assets"] = [
                        {
                            **registry["assets"][1],
                            "path": seed.relative_to(root).as_posix(),
                            "allowed_uses": ["source_distribution"],
                        }
                    ]
                registry_path.write_text(json.dumps(registry))
                self.commit_fixture(root)
                output = root / "rejected"
                with self.assertRaisesRegex(ValueError, message):
                    package.build(root, "v0.1.0-rc.1", output, audit_report=root / "rejected.json")
                self.assertFalse(output.exists())
                self.assertFalse((root / "rejected.json").exists())

    def test_invalid_tag_cannot_become_archive_path(self):
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            package.build(Path(directory), "../../escape", Path(directory) / "output")

    def test_git_failure_cannot_create_success_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(subprocess.CalledProcessError):
                package.build(root, "v0.1.0-rc.1", root / "output")
            self.assertFalse((root / "output").exists())
