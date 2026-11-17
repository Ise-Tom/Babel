"""Verify the CI archive digest and bound the exact static HTML published to Pages."""

import argparse
import hashlib
import io
import re
import stat
import zipfile
from html.parser import HTMLParser
from pathlib import Path

LIMIT = 2 * 1024 * 1024


class PagePolicy(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.policies: list[str] = []
        self.referrers: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if len(values) != len(attrs) or any(name.startswith("on") for name in values):
            raise ValueError("Duplicate attributes or inline event handlers")
        if tag in {"base", "iframe", "object", "embed", "form", "link"}:
            raise ValueError("Unexpected active or external content")
        if tag == "script" and "src" in values:
            raise ValueError("External script is not part of the standalone dashboard")
        if tag in {"script", "style"} and len(self.policies) != 1:
            raise ValueError("CSP must precede all executable content")
        if tag == "meta":
            if str(values.get("http-equiv", "")).lower() == "refresh":
                raise ValueError("Automatic navigation is not part of the dashboard")
            if str(values.get("http-equiv", "")).lower() == "content-security-policy":
                self.policies.append(values.get("content") or "")
            if str(values.get("name", "")).lower() == "referrer":
                self.referrers.append(values.get("content") or "")

    def validate(self) -> None:
        if len(self.policies) != 1 or self.referrers != ["no-referrer"]:
            raise ValueError("One CSP and the no-referrer policy are required")
        directives: dict[str, list[str]] = {}
        for raw in self.policies[0].split(";"):
            if not raw.strip():
                continue
            name, *values = raw.split()
            if name in directives:
                raise ValueError("Duplicate CSP directive")
            directives[name] = values
        if set(directives) != {
            "default-src",
            "script-src",
            "style-src",
            "img-src",
            "connect-src",
            "object-src",
            "base-uri",
            "form-action",
        }:
            raise ValueError("Unexpected CSP directive set")
        for name in (
            "default-src",
            "img-src",
            "connect-src",
            "object-src",
            "base-uri",
            "form-action",
        ):
            if directives.get(name) != ["'none'"]:
                raise ValueError(f"Restrictive {name} policy required")
        for name, count in (("script-src", 2), ("style-src", 1)):
            hashes = directives.get(name, [])
            if len(hashes) != count or any(
                not re.fullmatch(r"'sha256-[A-Za-z0-9+/]{43}='", item) for item in hashes
            ):
                raise ValueError("Only exact script/style hashes may authorize inline code")


def verified_page(archive: bytes, digest: str) -> bytes:
    if not re.fullmatch(r"sha256:[a-f0-9]{64}", digest):
        raise ValueError("Invalid expected archive digest")
    if not 0 < len(archive) <= LIMIT:
        raise ValueError("Unexpected archive size")
    if "sha256:" + hashlib.sha256(archive).hexdigest() != digest:
        raise ValueError("CI artifact digest mismatch")
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        entries = bundle.infolist()
        if len(entries) != 1 or entries[0].filename != "index.html":
            raise ValueError("Only one index.html may be published")
        page = entries[0]
        if (
            stat.S_IFMT(page.external_attr >> 16) not in {0, stat.S_IFREG}
            or page.flag_bits & 1
            or page.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
            or not 0 < page.file_size <= LIMIT
        ):
            raise ValueError("Expected bounded regular HTML")
        content = bundle.read(page)
    policy = PagePolicy()
    policy.feed(content.decode("utf-8"))
    policy.close()
    policy.validate()
    return content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--digest", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    with args.archive.open("rb") as source:
        html = verified_page(source.read(LIMIT + 1), args.digest)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "index.html").write_bytes(html)
    (args.output / ".nojekyll").touch()
    print("Verified archive digest, file boundary and standalone page policy")
