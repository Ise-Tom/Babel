"""Reject source/build trees for which this foundation has no executable CI gates."""

import json
import subprocess  # nosec B404
import sys
from collections.abc import Iterable
from pathlib import Path

ROOT_FILES = {
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    "NOTICE",
    "DCO",
    ".gitignore",
    "pyproject.toml",
    "requirements-ci.in",
    "requirements-ci.txt",
    "Cargo.toml",
    "Cargo.lock",
    "rust-toolchain.toml",
    "deny.toml",
}


def check(root: Path, paths: Iterable[str]) -> list[str]:
    errors = []
    for name in paths:
        path = Path(name)
        allowed = (
            name in ROOT_FILES
            or name
            in {
                "experiments/postgres_store/Dockerfile",
                "experiments/postgres_store/experiment.py",
                "experiments/postgres_store/schema.sql",
                "experiments/postgres_store/test_store.py",
            }
            or (
                path.parts[0] == "dashboard"
                and (
                    name
                    in {
                        "dashboard/package.json",
                        "dashboard/package-lock.json",
                        "dashboard/tsconfig.json",
                        "dashboard/eslint.config.mjs",
                        "dashboard/playwright.config.ts",
                        "dashboard/build.mjs",
                        "dashboard/lint.mjs",
                        "dashboard/build.d.mts",
                        "dashboard/progress.json",
                        "dashboard/associations.json",
                    }
                    or (
                        len(path.parts) > 2
                        and path.parts[1] in {"src", "tests"}
                        and path.suffix in {".ts", ".mjs", ".css", ".html"}
                    )
                )
            )
            or (
                path.parts[:2] == ("native", "babel-ldap")
                and (
                    name == "native/babel-ldap/Cargo.toml"
                    or (
                        len(path.parts) >= 4
                        and path.parts[2] in {"src", "tests"}
                        and path.suffix == ".rs"
                    )
                    or name == "native/babel-ldap/tests/smoke_ldap.py"
                )
            )
            or name in {"fuzz/Cargo.toml", "fuzz/Cargo.lock", "fuzz/fuzz_targets/ldap_frame.rs"}
            or name
            in {
                "fuzz/corpus/ldap_frame/anonymous-bind",
                "fuzz/corpus/ldap_frame/unbind",
                "fuzz/corpus/ldap_frame/oversized",
                "fuzz/corpus/ldap_frame/rootdse",
                "fuzz/corpus/ldap_frame/rootdse-filter",
            }
            or (path.parts[0] == "docs" and path.suffix == ".md")
            or name == "docs/github-main-ruleset.json"
            or name == "lab/windows-reference.toml"
            or (path.parts[0] in {"scripts", "tests"} and path.suffix == ".py")
            or (path.parts[0] == ".github" and path.suffix in {".yml", ".yaml", ".md"})
            or name == ".github/CODEOWNERS"
        )
        if not allowed or (root / path).is_symlink():
            errors.append(
                f"{name}: unsupported CI scope or symlink. Add the component's locked build, "
                "lint/type, functional, security and packaging gates before extending this policy."
            )
        elif name == "docs/github-main-ruleset.json":
            try:
                if not isinstance(json.loads((root / path).read_text()), dict):
                    raise ValueError("Expected an object")
            except (ValueError, OSError):
                errors.append(f"{name}: ruleset must be a readable JSON object")
    return errors


if __name__ == "__main__":
    # Includes untracked files for local checks; CI checks the complete checkout.
    files = (
        subprocess.check_output(  # nosec B603, B607
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=Path.cwd()
        )
        .decode()
        .split("\0")
    )
    failures = check(Path.cwd(), filter(None, files))
    for failure in failures:
        print(failure, file=sys.stderr)
    sys.exit(1 if failures else 0)
