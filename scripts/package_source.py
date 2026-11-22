"""Build deterministic source archives from the selected repository HEAD."""

import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess  # nosec B404
import tarfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

from check_ci_scope import allowed_path
from check_conformance import digest, indexed, require
from check_release import validate
from check_state_security import (
    ASSET_LIMIT,
    asset_for_use,
    pending_external_asset,
    verify_asset_bytes,
)

REGISTRY = "lab/specification-pins.json"
LAB_METADATA = {
    "lab/compatibility.json",
    "lab/conformance-evidence.json",
    "lab/windows-reference.toml",
    REGISTRY,
    "lab/kerberos/ap_req_probe.c",
    "lab/kerberos/run.sh",
}
SQL_FIXTURES = {
    "experiments/postgres_store/schema.sql",
    "native/babel-store-driver-lab/tests/fixture.sql",
}


def fixture_path(name: str) -> bool:
    return (
        name.startswith("fuzz/corpus/")
        or name in SQL_FIXTURES
        or (name.startswith("lab/") and name not in LAB_METADATA)
    )


def member_bytes(bundle: tarfile.TarFile, member: tarfile.TarInfo) -> bytes:
    require(member.size <= ASSET_LIMIT, f"Source archive member exceeds limit: {member.name}")
    stream = bundle.extractfile(member)
    if stream is None:
        raise ValueError(f"Missing source archive member: {member.name}")
    with stream:
        return stream.read()


def source_text(name: str, raw: bytes) -> None:
    require(
        not raw.lstrip().startswith((b"%PDF-", b"-----BEGIN "))
        and not re.search(rb"^Request for Comments:\s+\d+", raw[:4096], re.M),
        f"Publisher document or opaque payload in source archive: {name}",
    )
    try:
        content = raw.decode("utf-8")
    except UnicodeError as error:
        raise ValueError(f"Unexpected binary content in source archive: {name}") from error
    require(
        not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", content),
        f"Unexpected binary content in source archive: {name}",
    )


def audit_source(source: bytes, prefix: str) -> dict[str, Any]:
    """Inspect exactly what is sent to gzip; the working tree is not a policy input."""
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:") as bundle:
        revision = bundle.pax_headers.get("comment")
        require(digest(revision, 40), "Source archive needs a Git commit identifier")
        directories: set[str] = set()
        files: dict[str, tarfile.TarInfo] = {}
        for member in bundle:
            # Reject surprising members without extracting an archive to the filesystem.
            path = member.name.removeprefix(prefix + "/")
            require(
                member.name == prefix
                or (
                    member.name.startswith(prefix + "/")
                    and path == PurePosixPath(path).as_posix()
                    and ".." not in PurePosixPath(path).parts
                    and not any(c in path for c in ("\\", "\r", "\n"))
                ),
                "Unexpected source archive path",
            )
            require(
                path not in files and path not in directories, "Duplicate source archive member"
            )
            if member.isdir():
                directories.add(path)
            else:
                require(
                    member.isfile() and allowed_path(path),
                    f"Unapproved source archive member: {path}",
                )
                files[path] = member

        require(
            prefix in directories and REGISTRY in files, "Source archive needs the asset registry"
        )
        raw_registry = member_bytes(bundle, files[REGISTRY])
        registry = json.loads(raw_registry)
        registered: dict[str, dict[str, Any]] = {}
        for asset in indexed(registry.get("assets"), "assets").values():
            name = asset.get("path")
            if asset.get("kind") == "project_synthetic" or name is not None:
                asset_for_use(asset, "source_distribution")
                if not isinstance(name, str) or name in registered or name not in files:
                    raise ValueError("Registered asset must bind one archived source path")
                registered[name] = asset
            else:
                pending_external_asset(asset)
        document_hashes = {
            row["sha256"] for row in indexed(registry.get("documents"), "documents").values()
        }
        for name, member in files.items():
            raw = member_bytes(bundle, member)
            require(
                hashlib.sha256(raw).hexdigest() not in document_hashes,
                f"Pinned publisher document in source archive: {name}",
            )
            if name in registered:
                verify_asset_bytes(registered[name], raw)
            else:
                require(not fixture_path(name), f"Unregistered fixture in source archive: {name}")
            if not name.startswith("fuzz/corpus/"):
                source_text(name, raw)

    return {
        "requirement": "P00-16",
        "source_revision": revision,
        "registry_sha256": hashlib.sha256(raw_registry).hexdigest(),
        "regular_files": len(files),
        "files_by_directory": dict(
            sorted(
                Counter(name.partition("/")[0] if "/" in name else "root" for name in files).items()
            )
        ),
        "approved_project_assets": [
            {"id": asset["id"], "path": name, "sha256": asset["sha256"]}
            for name, asset in sorted(registered.items())
        ],
        "publisher_document_pins_checked": len(document_hashes),
        "disposition": "source_archive_passed",
    }


def build(root: Path, tag: str, output: Path, *, audit_report: Path | None = None) -> Path:
    validate(tag)
    prefix = f"Babel-{tag}"
    # The archive must describe the tested commit, not ignored/local workspace files.
    source = subprocess.check_output(  # nosec B603, B607
        ["git", "archive", "--format=tar", f"--prefix={prefix}/", "HEAD"], cwd=root
    )
    audited = audit_source(source, prefix)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"{prefix}.tar.gz"
    compressed = gzip.compress(source, mtime=0)
    archive.write_bytes(compressed)
    archive_digest = hashlib.sha256(compressed).hexdigest()
    (output / "SHA256SUMS").write_text(f"{archive_digest}  {archive.name}\n", encoding="utf-8")
    if audit_report is not None:
        audited.update(archive=archive.name, archive_sha256=archive_digest)
        audit_report.parent.mkdir(parents=True, exist_ok=True)
        audit_report.write_text(json.dumps(audited, indent=2) + "\n", encoding="utf-8")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-report", type=Path)
    options = parser.parse_args()
    try:
        print(build(Path.cwd(), options.tag, options.output, audit_report=options.audit_report))
    except (ValueError, KeyError, TypeError, AttributeError, OSError, tarfile.TarError) as error:
        raise SystemExit(f"Source archive rejected: {error}") from error
