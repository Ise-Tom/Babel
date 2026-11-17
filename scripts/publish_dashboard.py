"""Update only the automation-owned dashboard-live branch of the private repository."""

import argparse
import json
import re
import subprocess  # nosec B404
from collections.abc import Callable
from typing import Any

from build_dashboard import ROOT, build
from render_dashboard import LIVE_URL, render

API_REPO = "repos/Ise-Tom/Babel"
BRANCH = "dashboard-live"
Api = Callable[[str, str, dict[str, Any] | None], Any]


def api(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    # Fixed hostname/repository, structured JSON on stdin, no shell or credential output.
    endpoint = f"{API_REPO}/{path}" if path else API_REPO
    command = ["gh", "api", "--hostname", "github.com", "--method", method, endpoint]
    if payload is not None:
        command.extend(["--input", "-"])
    result = subprocess.run(  # nosec B603, B607
        command,
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    if result.returncode:
        # Do not print API bodies/headers or credential-provider stderr.
        raise RuntimeError(f"GitHub request failed: {method} {path}. Existing report retained.")
    return json.loads(result.stdout)


def publish(report: str, revision: str, *, preview: bool = False, request: Api = api) -> str:
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Invalid source revision")
    repository = request("GET", "", None)
    if repository.get("private") is not True or repository.get("full_name") != "Ise-Tom/Babel":
        raise ValueError("Private project repository required; visibility is never changed")
    if not preview and request("GET", "branches/main", None)["commit"]["sha"] != revision:
        return "Skipped an older main revision; the previous report remains available."
    refs = request("GET", f"git/matching-refs/heads/{BRANCH}", None)
    matches = [ref for ref in refs if ref["ref"] == f"refs/heads/{BRANCH}"]
    if len(matches) > 1:
        raise ValueError("Unexpected duplicate dashboard refs")
    previous = matches[0]["object"]["sha"] if matches else None
    previous_tree = None
    if previous:
        previous_tree = request("GET", f"git/commits/{previous}", None)["tree"]["sha"]
        tree = request("GET", f"git/trees/{previous_tree}", None)
        if tree.get("truncated") or [(p["path"], p["type"]) for p in tree["tree"]] != [
            ("README.md", "blob")
        ]:
            raise ValueError("Dashboard branch has unexpected files; refusing to overwrite")
    blob = request("POST", "git/blobs", {"content": report, "encoding": "utf-8"})["sha"]
    tree_sha = request(
        "POST",
        "git/trees",
        {"tree": [{"path": "README.md", "mode": "100644", "type": "blob", "sha": blob}]},
    )["sha"]
    if tree_sha == previous_tree:
        return f"Dashboard is already current: {LIVE_URL}"
    commit = request(
        "POST",
        "git/commits",
        {
            "message": f"Update {'preview' if preview else 'main'} dashboard for {revision[:7]}",
            "tree": tree_sha,
            "parents": [previous] if previous else [],
        },
    )["sha"]
    if previous:
        # Fast-forward only. A concurrent edit fails without replacing another commit.
        request("PATCH", f"git/refs/heads/{BRANCH}", {"sha": commit, "force": False})
    else:
        request("POST", "git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": commit})
    return f"Published {'preview' if preview else 'main'} dashboard: {LIVE_URL}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--preview", action="store_true")
    options = parser.parse_args()
    model = build(ROOT, options.revision)
    report = render(model, preview=options.preview)
    print(publish(report, options.revision, preview=options.preview))
