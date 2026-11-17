"""Install pinned upstream Linux x86-64 binaries without bypassing TLS or hashes."""

import argparse
import hashlib
import io
import os
import platform
import tarfile
import tempfile
import urllib.request
from pathlib import Path

TOOLS = {
    "syft": (
        "https://github.com/anchore/syft/releases/download/v1.57.2/syft_1.57.2_linux_amd64.tar.gz",
        "ad92bd3ec1b94a3df01d4d0aec199afa9c42b72e86da436ff5f837914d32706b",
    ),
    "actionlint": (
        "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz",
        "8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8",
    ),
    "gitleaks": (
        "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz",
        "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb",
    ),
}


def install(directory: Path, names: list[str] | None = None) -> None:
    if platform.system() != "Linux" or platform.machine() not in ("x86_64", "AMD64"):
        raise SystemExit("CI tools require Linux x86-64")
    if names is not None and any(name not in TOOLS for name in names):
        raise SystemExit("Unknown CI tool selection")
    selected = TOOLS if names is None else {name: TOOLS[name] for name in names}
    directory.mkdir(parents=True, exist_ok=True)
    for name, (url, expected) in selected.items():
        if not url.startswith("https://"):
            raise SystemExit(f"Only HTTPS tool sources are permitted: {name}")
        # Fixed upstream HTTPS URLs; default TLS verification remains enabled.
        with urllib.request.urlopen(url, timeout=60) as response:  # nosec B310
            archive = response.read()
        if hashlib.sha256(archive).hexdigest() != expected:
            raise SystemExit(f"Checksum mismatch for {name}; refusing installation")
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
            member = bundle.getmember(name)
            if not member.isfile():
                raise SystemExit(f"Invalid executable entry for {name}")
            source = bundle.extractfile(member)
            if source is None:
                raise SystemExit(f"Missing executable data for {name}")
            # Never extract arbitrary archive paths or symlinks.
            with tempfile.NamedTemporaryFile(
                dir=directory, prefix=f".{name}.", delete=False
            ) as target:
                temporary = Path(target.name)
                target.write(source.read())
            temporary.chmod(0o755)
            os.replace(temporary, directory / name)
        print(f"Installed verified {name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--tools", nargs="+", choices=sorted(TOOLS))
    options = parser.parse_args()
    install(options.directory, options.tools)
