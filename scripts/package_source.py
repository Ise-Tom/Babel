"""Build deterministic source archives from the selected repository HEAD."""

import argparse
import gzip
import hashlib
import subprocess  # nosec B404
from pathlib import Path

from check_release import validate


def build(root: Path, tag: str, output: Path) -> Path:
    validate(tag)
    # The archive must describe the tested commit, not ignored/local workspace files.
    source = subprocess.check_output(  # nosec B603, B607
        ["git", "archive", "--format=tar", f"--prefix=Babel-{tag}/", "HEAD"], cwd=root
    )
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"Babel-{tag}.tar.gz"
    archive.write_bytes(gzip.compress(source, mtime=0))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    print(build(Path.cwd(), options.tag, options.output))
