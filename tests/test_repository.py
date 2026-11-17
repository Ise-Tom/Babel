import hashlib
import importlib.util
import io
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


links = load("check_docs")
release = load("check_release")
installer = load("install_ci_tools")


class DocumentationLinks(unittest.TestCase):
    def test_existing_relative_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.md").write_text("# Target\n")
            (root / "README.md").write_text("[Target](target.md#heading)\n")
            self.assertEqual(links.check(root), [])

    def test_missing_file_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[Broken](missing.md)\n")
            self.assertEqual(len(links.check(root)), 1)

    def test_escape_is_rejected_even_if_file_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "repo"
            root.mkdir()
            (parent / "private.md").write_text("private")
            (root / "README.md").write_text("[Escape](../private.md)\n")
            self.assertEqual(len(links.check(root)), 1)

    def test_external_links_and_fenced_examples_are_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "[Web](https://example.com/)\n[Section](#section)\n"
                "```md\n[Example](absent.md)\n```\n"
            )
            self.assertEqual(links.check(root), [])

    def test_encoded_local_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a b.md").write_text("example")
            (root / "README.md").write_text("[Space](a%20b.md)")
            self.assertEqual(links.check(root), [])


class GeneratedDocumentation(unittest.TestCase):
    def test_generated_dependency_docs_are_not_validated_as_project_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("Project documentation")
            for name in ("node_modules", "target", "test-results", "dist"):
                output = root / name
                output.mkdir()
                (output / "README.md").write_text("[Generated](missing.md)")
            self.assertEqual(links.check(root), [])


class ReleasePolicy(unittest.TestCase):
    def test_source_prereleases(self):
        for tag in ("v0.1.0-alpha.1", "v0.12.4-beta.2", "v0.2.0-rc.0"):
            with self.subTest(tag=tag):
                release.validate(tag)

    def test_stable_and_malformed_releases_are_rejected(self):
        for tag in (
            "v1.0.0",
            "v0.1.0",
            "v1.0.0-alpha.1",
            "v0.01.0-rc.1",
            "v0.1.0-preview.1",
            "v0.1.0-alpha.01",
            "v0.1.0-rc.1\n",
            "../main",
            "v0.1.0-rc.1;echo unsafe",
        ):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                release.validate(tag)


class VerifiedInstaller(unittest.TestCase):
    @staticmethod
    def archive(name="tool", symlink=False):
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode="w:gz") as bundle:
            member = tarfile.TarInfo(name)
            if symlink:
                member.type = tarfile.SYMTYPE
                member.linkname = "/tmp/untrusted"
                bundle.addfile(member)
            else:
                payload = b"test executable"
                member.size = len(payload)
                bundle.addfile(member, io.BytesIO(payload))
        return output.getvalue()

    def test_checksum_mismatch_preserves_existing_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "tool"
            target.write_bytes(b"existing")
            with (
                patch.object(installer, "TOOLS", {"tool": ("https://example.com", "0" * 64)}),
                patch.object(installer.urllib.request, "urlopen", return_value=io.BytesIO(b"bad")),
                self.assertRaises(SystemExit),
            ):
                installer.install(Path(directory))
            self.assertEqual(target.read_bytes(), b"existing")

    def test_verified_binary_installs_with_executable_mode(self):
        archive = self.archive()
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(
                    installer,
                    "TOOLS",
                    {"tool": ("https://example.com", hashlib.sha256(archive).hexdigest())},
                ),
                patch.object(installer.urllib.request, "urlopen", return_value=io.BytesIO(archive)),
            ):
                installer.install(Path(directory))
            target = Path(directory) / "tool"
            self.assertEqual(target.read_bytes(), b"test executable")
            self.assertTrue(target.stat().st_mode & 0o111)

    def test_symlink_entry_rejected(self):
        archive = self.archive(symlink=True)
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(
                    installer,
                    "TOOLS",
                    {"tool": ("https://example.com", hashlib.sha256(archive).hexdigest())},
                ),
                patch.object(installer.urllib.request, "urlopen", return_value=io.BytesIO(archive)),
                self.assertRaises(SystemExit),
            ):
                installer.install(Path(directory))
            self.assertFalse((Path(directory) / "tool").exists())


class InstallerAbuseCases(unittest.TestCase):
    def test_unknown_tool_selection_is_rejected_before_network(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(installer.urllib.request, "urlopen") as request,
            self.assertRaises(SystemExit),
        ):
            installer.install(Path(directory), ["unknown-fixture"])
        request.assert_not_called()

    def test_tool_selection_does_not_fetch_unrequested_artifacts(self):
        archive = VerifiedInstaller.archive()
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(
                    installer,
                    "TOOLS",
                    {
                        "tool": ("https://example.com", hashlib.sha256(archive).hexdigest()),
                        "other": ("http://invalid.example", "0" * 64),
                    },
                ),
                patch.object(
                    installer.urllib.request, "urlopen", return_value=io.BytesIO(archive)
                ) as request,
            ):
                installer.install(Path(directory), ["tool"])
                self.assertEqual(request.call_count, 1)
                self.assertFalse((Path(directory) / "other").exists())

    def test_insecure_url_is_rejected_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(installer, "TOOLS", {"tool": ("http://example.com", "0" * 64)}),
                patch.object(installer.urllib.request, "urlopen") as request,
                self.assertRaises(SystemExit),
            ):
                installer.install(Path(directory))
            request.assert_not_called()

    def test_network_failure_is_not_suppressed(self):
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(
                    installer.urllib.request, "urlopen", side_effect=OSError("network unavailable")
                ),
                self.assertRaises(OSError),
            ):
                installer.install(Path(directory))
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_unsupported_platform_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(installer.platform, "system", return_value="Unsupported"),
                self.assertRaises(SystemExit),
            ):
                installer.install(Path(directory))

    def test_missing_or_traversal_member_cannot_extract_outside_destination(self):
        for name in ("../escape", "unrelated"):
            archive = VerifiedInstaller.archive(name=name)
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                with (
                    patch.object(
                        installer,
                        "TOOLS",
                        {"tool": ("https://example.com", hashlib.sha256(archive).hexdigest())},
                    ),
                    patch.object(
                        installer.urllib.request, "urlopen", return_value=io.BytesIO(archive)
                    ),
                    self.assertRaises(KeyError),
                ):
                    installer.install(Path(directory))
                self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
