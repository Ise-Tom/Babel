"""Reject source/build trees for which this foundation has no executable CI gates."""

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
    ".gitignore",
    "pyproject.toml",
    "requirements-ci.in",
    "requirements-ci.txt",
}


def check(root: Path, paths: Iterable[str]) -> list[str]:
    errors = []
    for name in paths:
        path = Path(name)
        allowed = (
            name in ROOT_FILES
            or (path.parts[0] == "docs" and path.suffix == ".md")
            or (path.parts[0] in {"scripts", "tests"} and path.suffix == ".py")
            or (path.parts[0] == ".github" and path.suffix in {".yml", ".yaml", ".md"})
            or name == ".github/CODEOWNERS"
        )
        if not allowed or (root / path).is_symlink():
            errors.append(
                f"{name}: unsupported CI scope or symlink. Add the component's locked build, "
                "lint/type, functional, security and packaging gates before extending this policy."
            )
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
