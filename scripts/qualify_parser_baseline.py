"""Bind observed Linux/compiler/ELF facts to P00-04's bounded parser baseline."""

import argparse
import datetime as dt
import hashlib
import json
import platform
import re
import tomllib
from pathlib import Path
from typing import Any

from collect_native_notices import runtime_closure

ROOT = Path(__file__).resolve().parents[1]
TARGET = "x86_64-unknown-linux-gnu"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def collect(
    root: Path,
    metadata: dict[str, Any],
    compiler: str,
    elf: str,
    inspector: str,
    binary: Path,
    os_info: dict[str, str],
    revision: str,
    runner_image: str,
) -> dict[str, Any]:
    require(bool(re.fullmatch(r"[a-f0-9]{40}", revision)), "Full source revision required")
    require(
        (os_info.get("ID"), os_info.get("VERSION_ID")) in {("ubuntu", "24.04"), ("debian", "13")},
        "Host outside the declared Ubuntu 24.04 / Debian 13 baseline",
    )
    toolchain = tomllib.loads((root / "rust-toolchain.toml").read_text())["toolchain"]
    require(toolchain["channel"] == "1.100.0", "Compiler pin needs requalification")
    require(
        set(toolchain["components"]) == {"rustfmt", "clippy", "llvm-tools-preview", "rust-docs"},
        "Toolchain components need review",
    )
    fields = dict(line.split(": ", 1) for line in compiler.splitlines() if ": " in line)
    require(fields.get("release") == toolchain["channel"], "Observed compiler differs from pin")
    require(fields.get("host") == TARGET, "Unqualified compiler host/architecture")
    require(
        bool(re.fullmatch(r"[a-f0-9]{40}", fields.get("commit-hash", ""))),
        "Compiler commit required",
    )
    require(bool(fields.get("LLVM version")), "LLVM version required")
    workspace = tomllib.loads((root / "Cargo.toml").read_text())
    require(
        workspace.get("profile", {}).get("release", {}).get("overflow-checks") is True,
        "Optimized builds must keep overflow checks",
    )
    package = next((p for p in metadata["packages"] if p["name"] == "babel-ldap"), None)
    if not isinstance(package, dict):
        raise ValueError("Parser package metadata required")
    require(
        package.get("source") is None and package.get("license") == "Apache-2.0",
        "Local licensed parser required",
    )
    require(package.get("links") is None, "Parser FFI linkage needs review")
    require(
        all(dep["kind"] == "dev" for dep in package["dependencies"]),
        "Parser normal/build dependency expansion needs requalification",
    )
    require(
        all("custom-build" not in t["kind"] for t in package["targets"]),
        "Parser build script needs requalification",
    )
    require(
        runtime_closure(metadata, ("babel-ldap",)) == {package["id"]},
        "Parser runtime closure changed",
    )
    for source in ("lib.rs", "main.rs"):
        text = (root / "native/babel-ldap/src" / source).read_text()
        require(
            bool(re.search(r"^#!\[forbid\(unsafe_code\)\]$", text, re.M)),
            "Both parser crate roots must forbid unsafe code",
        )
    require(not binary.is_symlink() and binary.is_file(), "Regular qualification binary required")
    require(20 <= binary.stat().st_size <= 64 * 1024 * 1024, "Binary size outside budget")
    raw = binary.read_bytes()
    require(
        raw[:6] == b"\x7fELF\x02\x01" and raw[16:18] == b"\x03\x00" and raw[18:20] == b"\x3e\x00",
        "Expected Linux x86_64 ELF64",
    )
    require(bool(re.search(r"Type:\s+DYN\b", elf)), "PIE executable required")
    require(bool(re.search(r"\(FLAGS_1\).*\bPIE\b", elf)), "ELF PIE flag required")
    require(bool(re.search(r"^\s*GNU_RELRO\s", elf, re.M)), "GNU RELRO required")
    require(
        bool(re.search(r"\(FLAGS\).*\bBIND_NOW\b|\(FLAGS_1\).*\bNOW\b", elf)),
        "Immediate binding required",
    )
    stacks = re.findall(r"^\s*GNU_STACK\s+(.+)$", elf, re.M)
    require(
        len(stacks) == 1
        and bool(re.search(r"\sRW\s", stacks[0]))
        and not re.search(r"\s[RWE]*E[RWE]*\s", stacks[0]),
        "Explicit non-executable stack required",
    )
    require(inspector.startswith("GNU readelf "), "Observed ELF inspector version required")
    inputs = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in (
            "rust-toolchain.toml",
            "Cargo.toml",
            "Cargo.lock",
            "fuzz/Cargo.toml",
            "fuzz/Cargo.lock",
            "deny.toml",
            "native/babel-ldap/Cargo.toml",
        )
    }
    return {
        "requirement": "P00-04",
        "scope": (
            "Linux/Rust bounded parser baseline; passing CI binds tests/fuzz/audits separately"
        ),
        "source_revision": revision,
        "profile": "linux-x86_64-gnu-bounded-parser-v1",
        "host": {
            key: os_info.get(key, "")
            for key in ("ID", "VERSION_ID", "PRETTY_NAME", "DEBIAN_VERSION_FULL")
        },
        "runner_image": runner_image,
        "compiler": fields,
        "target": TARGET,
        "elf_inspector": inspector.splitlines()[0],
        "input_sha256": inputs,
        "binary_sha256": hashlib.sha256(raw).hexdigest(),
        "elf_report_sha256": hashlib.sha256(elf.encode()).hexdigest(),
        "protections": ["PIE", "full_RELRO", "non_executable_stack", "release_overflow_checks"],
        "parser_runtime_crates": [],
        "system_shared_libraries": sorted(
            set(re.findall(r"\(NEEDED\).*Shared library: \[([^\]]+)\]", elf))
        ),
        "unsafe_boundary": (
            "Parser roots forbid unsafe; Rust/std/libc internals are upstream trust"
        ),
        "product_ad_conformance": "unrun",
        "owner_acceptance": "not_inferred",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--compiler", type=Path, required=True)
    parser.add_argument("--elf", type=Path, required=True)
    parser.add_argument("--inspector", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--runner-image", default="local")
    args = parser.parse_args()
    try:
        result = collect(
            args.root,
            json.loads(args.metadata.read_text()),
            args.compiler.read_text(),
            args.elf.read_text(),
            args.inspector.read_text(),
            args.binary,
            platform.freedesktop_os_release(),
            args.revision,
            args.runner_image,
        )
        require(
            platform.system() == "Linux" and platform.machine() == "x86_64",
            "Native Linux x86_64 observation host required",
        )
        result["host_runtime"] = {"kernel": platform.release(), "machine": platform.machine()}
        result["observed_at"] = dt.datetime.now(dt.UTC).isoformat()
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        raise SystemExit(f"Parser baseline rejected: {error}") from error
