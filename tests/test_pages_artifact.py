"""Reject tampered archives, zip extraction hazards and weakened browser policy."""

import hashlib
import io
import stat
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verify_pages_artifact as verifier  # noqa: E402

HASH = "'sha256-" + "A" * 43 + "='"
POLICY = (
    "default-src 'none'; script-src "
    + HASH
    + " "
    + HASH
    + "; style-src "
    + HASH
    + "; img-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
)
HTML = (
    '<!doctype html><meta http-equiv="Content-Security-Policy" content="' + POLICY + '">'
    '<meta name="referrer" content="no-referrer"><p>Fixture only</p>'
)


def archive(content=HTML, name="index.html", extra=False, mode=stat.S_IFREG | 0o644):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        info = zipfile.ZipInfo(name)
        info.external_attr = mode << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        bundle.writestr(info, content)
        if extra:
            bundle.writestr("credentials.txt", "Synthetic extra file")
    raw = buffer.getvalue()
    return raw, "sha256:" + hashlib.sha256(raw).hexdigest()


class PagesArtifact(unittest.TestCase):
    def test_valid_archive_returns_only_the_html_bytes(self):
        self.assertEqual(verifier.verified_page(*archive()), HTML.encode())

    def test_digest_tampering_and_invalid_size_are_rejected_before_extraction(self):
        raw, digest = archive()
        for data, expected in (
            (raw + b"changed", digest),
            (raw, "not-a-digest"),
            (b"", digest),
            (b"x" * (verifier.LIMIT + 1), digest),
        ):
            with self.subTest(expected=expected), self.assertRaises(ValueError):
                verifier.verified_page(data, expected)

    def test_extra_files_traversal_and_symlinks_cannot_be_extracted(self):
        for fixture in (
            archive(extra=True),
            archive(name="../index.html"),
            archive(name="/index.html"),
            archive(mode=stat.S_IFLNK | 0o777),
            archive(mode=stat.S_IFDIR | 0o755),
            archive(content="x" * (verifier.LIMIT + 1)),
        ):
            with self.subTest(digest=fixture[1]), self.assertRaises(ValueError):
                verifier.verified_page(*fixture)

    def test_weak_or_duplicate_csp_and_referrer_policies_are_rejected(self):
        for content in (
            HTML.replace("default-src 'none'", "default-src *"),
            HTML.replace(HASH, "'unsafe-inline'"),
            HTML.replace("connect-src 'none'", "connect-src https:"),
            HTML.replace("img-src 'none'", "img-src data:"),
            HTML.replace("form-action 'none'", "form-action 'none'; form-action *"),
            HTML.replace("form-action 'none'", "form-action 'none'; script-src-elem *"),
            HTML + '<meta http-equiv="Content-Security-Policy" content="default-src *">',
            HTML.replace('name="referrer"', 'name="different"'),
            HTML.replace('content="no-referrer"', 'content="unsafe-url"'),
        ):
            with self.subTest(content=content), self.assertRaises(ValueError):
                verifier.verified_page(*archive(content=content))

    def test_external_code_active_elements_and_event_handlers_are_rejected(self):
        for extra in (
            '<script src="https://example.invalid/code.js"></script>',
            '<iframe src="https://example.invalid"></iframe>',
            '<form action="https://example.invalid"></form>',
            '<body onload="alert(1)">',
            '<meta name="referrer" name="other" content="no-referrer">',
            '<meta http-equiv="refresh" content="0;url=https://example.invalid">',
        ):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                verifier.verified_page(*archive(content=HTML + extra))

    def test_policy_must_precede_code_and_styles(self):
        for prefix in ("<script>alert(1)</script>", "<style>body{color:red}</style>"):
            with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                verifier.verified_page(*archive(content=prefix + HTML))
