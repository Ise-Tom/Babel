"""Restrict this foundation's release workflow to explicit v0 prereleases."""

import re
import sys


def validate(tag: str) -> None:
    number = r"(?:0|[1-9][0-9]*)"
    if not re.fullmatch(rf"v0\.{number}\.{number}-(?:alpha|beta|rc)\.{number}", tag):
        raise ValueError(
            "Only v0.MINOR.PATCH-alpha.N, -beta.N, or -rc.N source prereleases are allowed"
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/check_release.py TAG")
    try:
        validate(sys.argv[1])
    except ValueError as error:
        sys.exit(str(error))
