"""Retain actual dependency/Rust-library notices in experimental native archives."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

MAX_FILE = 4 * 1024 * 1024
MAX_TOTAL = 32 * 1024 * 1024


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def runtime_closure(metadata: dict[str, Any], selected: tuple[str, ...]) -> set[str]:
    packages = metadata.get("packages")
    if not isinstance(packages, list):
        raise ValueError("Cargo metadata packages required")
    roots = {p["name"]: p["id"] for p in packages if p.get("source") is None}
    require(bool(selected) and set(selected) <= roots.keys(), "Unknown native archive packages")
    nodes = {node["id"]: node for node in metadata["resolve"]["nodes"]}
    pending = [roots[name] for name in selected]
    result = set()
    while pending:
        identifier = pending.pop()
        if identifier in result:
            continue
        require(identifier in nodes, "Missing dependency graph node")
        result.add(identifier)
        pending.extend(
            dep["pkg"]
            for dep in nodes[identifier]["deps"]
            if any(k["kind"] is None for k in dep["dep_kinds"])
        )
    return result


def assemble(
    metadata: dict[str, Any],
    project: Path,
    rust_docs: Path,
    output: Path,
    selected: tuple[str, ...] = ("babel-ldap", "babel-tls-lab"),
) -> dict[str, Any]:
    packages = metadata.get("packages")
    if not isinstance(packages, list):
        raise ValueError("Cargo metadata packages required")
    included = runtime_closure(metadata, selected)
    output.mkdir(mode=0o700)
    records = []
    inventory = []
    total = 0

    def retain(source: Path, base: Path, relative: Path) -> None:
        nonlocal total
        require(
            not source.is_symlink()
            and source.is_file()
            and source.resolve().is_relative_to(base.resolve()),
            "Notice must be a regular in-tree file",
        )
        require(not relative.is_absolute() and ".." not in relative.parts, "Unsafe notice target")
        require(0 < source.stat().st_size <= MAX_FILE, "Missing or oversized notice content")
        data = source.read_bytes()
        total += len(data)
        require(len(data) <= MAX_FILE and total <= MAX_TOTAL, "Notice size budget exceeded")
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        records.append(
            {
                "path": relative.as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    for name in ("LICENSE", "NOTICE", "DCO"):
        retain(project / name, project, Path("project") / name)
    for package in packages:
        if package["id"] not in included or package.get("source") is None:
            continue
        require(
            package["source"] == "registry+https://github.com/rust-lang/crates.io-index",
            "Unreviewed registry/git source",
        )
        name, version = package["name"], package["version"]
        require(
            bool(re.fullmatch(r"[A-Za-z0-9_-]{1,80}", name))
            and bool(re.fullmatch(r"[0-9][0-9A-Za-z.+-]{0,80}", version)),
            "Invalid package identity",
        )
        require(
            isinstance(package.get("license"), str) and bool(package["license"].strip()),
            "Package license expression missing",
        )
        base = Path(package["manifest_path"]).parent
        paths = {
            p
            for p in base.rglob("*")
            if p.name.upper().startswith(("LICENSE", "COPYING", "COPYRIGHT", "NOTICE"))
            and p.is_file()
        }
        if package.get("license_file"):
            paths.add(base / package["license_file"])
        require(0 < len(paths) <= 128, "Dependency notice files missing or excessive")
        retained = []
        for source in sorted(paths):
            relative = Path("third-party") / f"{name}-{version}" / source.relative_to(base)
            retain(source, base, relative)
            retained.append(relative.as_posix())
        inventory.append(
            {"name": name, "version": version, "license": package["license"], "notices": retained}
        )
    retain(rust_docs / "COPYRIGHT-library.html", rust_docs, Path("rust") / "COPYRIGHT-library.html")
    licenses = sorted((rust_docs / "licenses").glob("*.txt"))
    require(bool(licenses), "Rust library license texts missing")
    for path in licenses:
        retain(path, rust_docs, Path("rust/licenses") / path.name)
    result = {
        "schema_version": 1,
        "scope": (
            "Notices for selected normal/runtime dependency closure and Rust library bundle; "
            "not legal clearance or an assertion that every listed component is linked."
        ),
        "root_packages": list(selected),
        "packages": inventory,
        "files": records,
    }
    with (output / "manifest.json").open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    return result


def verify(output: Path, expected_sha256: str | None = None) -> None:
    require(output.is_dir() and not output.is_symlink(), "Regular notice directory required")
    manifest_path = output / "manifest.json"
    require(
        manifest_path.is_file()
        and not manifest_path.is_symlink()
        and 0 < manifest_path.stat().st_size <= MAX_FILE,
        "Regular bounded notice manifest required",
    )
    raw = manifest_path.read_bytes()
    if expected_sha256 is not None:
        require(
            bool(re.fullmatch(r"[a-f0-9]{64}", expected_sha256))
            and hashlib.sha256(raw).hexdigest() == expected_sha256,
            "Expected notice manifest digest mismatch",
        )
    manifest = json.loads(raw)
    require(
        manifest.get("schema_version") == 1 and bool(manifest.get("files")),
        "Unknown/empty notice manifest",
    )
    seen = set()
    total = 0
    for row in manifest["files"]:
        path = Path(row["path"])
        require(
            not path.is_absolute() and ".." not in path.parts and row["path"] not in seen,
            "Unsafe or duplicate notice path",
        )
        seen.add(row["path"])
        source = output / path
        require(
            not source.is_symlink()
            and source.resolve().is_relative_to(output.resolve())
            and source.is_file(),
            "Missing or linked notice file",
        )
        require(0 < source.stat().st_size == row["bytes"] <= MAX_FILE, "Notice size mismatch")
        total += source.stat().st_size
        require(total <= MAX_TOTAL, "Notice size budget exceeded")
        require(
            hashlib.sha256(source.read_bytes()).hexdigest() == row["sha256"],
            "Notice digest mismatch",
        )

    required = {"project/LICENSE", "project/NOTICE", "project/DCO", "rust/COPYRIGHT-library.html"}
    require(
        required <= seen and any(p.startswith("rust/licenses/") for p in seen),
        "Required project/Rust notices missing from manifest",
    )
    tree = set()
    for path in output.rglob("*"):
        require(not path.is_symlink(), "Symlink in notice tree")
        if path.is_file():
            tree.add(path.relative_to(output).as_posix())
    require(tree == seen | {"manifest.json"}, "Notice tree and manifest differ")
    roots = manifest.get("root_packages")
    require(
        isinstance(roots, list) and bool(roots) and len(roots) == len(set(roots)),
        "Selected notice roots required",
    )
    inventory = manifest.get("packages")
    require(isinstance(inventory, list), "Package notice inventory required")
    packages = set()
    declared = set()
    for package in inventory:
        identity = f"{package['name']}-{package['version']}"
        require(
            identity not in packages and bool(package.get("license")),
            "Duplicate package or missing license",
        )
        packages.add(identity)
        terms = package.get("notices")
        require(
            isinstance(terms, list) and bool(terms) and len(terms) == len(set(terms)),
            "Package notices required",
        )
        require(
            all(p in seen and p.startswith(f"third-party/{identity}/") for p in terms),
            "Package notice binding mismatch",
        )
        declared.update(terms)
    require(
        declared == {p for p in seen if p.startswith("third-party/")},
        "Unaccounted dependency notice files",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--rust-docs", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packages", nargs="+", default=["babel-ldap", "babel-tls-lab"])
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--expected-sha256")
    args = parser.parse_args()
    try:
        if args.verify:
            verify(args.output, args.expected_sha256)
        else:
            if args.metadata is None or args.rust_docs is None:
                parser.error("--metadata and --rust-docs are required for assembly")
            assemble(
                json.loads(args.metadata.read_text()),
                args.project,
                args.rust_docs,
                args.output,
                tuple(args.packages),
            )
            verify(args.output, args.expected_sha256)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        raise SystemExit(f"Native notices rejected: {error}") from error
    print(
        "Native experimental notice bundle verified; "
        "broader distribution rights remain separately reviewed."
    )
