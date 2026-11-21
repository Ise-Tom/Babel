"""Select an immutable dashboard artifact from successful CI on current main."""

import argparse
import re
from pathlib import Path
from typing import Any

from publish_dashboard import Api, api


class ArtifactUnavailable(ValueError):
    """The run has no retained standalone dashboard."""


def validate_run(run: dict[str, Any], revision: str) -> int:
    conditions = (
        run.get("repository", {}).get("full_name") == "Ise-Tom/Babel",
        run.get("head_repository", {}).get("full_name") == "Ise-Tom/Babel",
        run.get("head_branch") == "main",
        run.get("head_sha") == revision,
        run.get("path") == ".github/workflows/ci.yml",
        run.get("event") in {"push", "workflow_dispatch"},
        run.get("status") == "completed",
        run.get("conclusion") == "success",
        type(run.get("id")) is int and run["id"] > 0,
    )
    if not all(conditions):
        raise ValueError("Pages requires successful CI from this repository's exact main revision")
    return int(run["id"])


def dashboard_artifact(selected: int, *, request: Api = api) -> dict[str, Any]:
    artifacts = request("GET", f"actions/runs/{selected}/artifacts", None)["artifacts"]
    matches = [item for item in artifacts if item.get("name") == "dashboard-standalone"]
    if not matches or (len(matches) == 1 and matches[0].get("expired") is True):
        raise ArtifactUnavailable("The standalone dashboard artifact is missing or expired")
    if (
        len(matches) != 1
        or matches[0].get("expired") is not False
        or type(matches[0].get("size_in_bytes")) is not int
        or not 0 < matches[0]["size_in_bytes"] <= 2 * 1024 * 1024
        or type(matches[0].get("id")) is not int
        or matches[0]["id"] <= 0
        or not re.fullmatch(r"sha256:[a-f0-9]{64}", str(matches[0].get("digest")))
    ):
        raise ValueError("The standalone dashboard artifact metadata is invalid")
    return dict(matches[0])


def source_artifact(
    revision: str, run_id: str = "", *, request: Api = api
) -> tuple[int, dict[str, Any]] | None:
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Invalid source revision")
    if request("GET", "branches/main", None)["commit"]["sha"] != revision:
        return None
    if run_id:
        if not re.fullmatch(r"[1-9][0-9]*", run_id):
            raise ValueError("Invalid CI run ID")
        selected = validate_run(request("GET", f"actions/runs/{run_id}", None), revision)
        return selected, dashboard_artifact(selected, request=request)

    candidates = request(
        "GET",
        f"actions/workflows/ci.yml/runs?branch=main&head_sha={revision}&status=success&per_page=10",
        None,
    )["workflow_runs"]
    for candidate in candidates:
        try:
            selected = validate_run(candidate, revision)
        except ValueError:
            continue
        try:
            return selected, dashboard_artifact(selected, request=request)
        except ArtifactUnavailable:
            continue
    raise ValueError("No retained dashboard from successful CI for this revision; run CI first")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = source_artifact(args.revision, args.run_id)
    selected, artifact = source if source is not None else (None, {})
    args.output.write_text(
        f"ready={'true' if selected is not None else 'false'}\nrun_id={selected or ''}\n"
        f"revision={args.revision}\nartifact_id={artifact.get('id', '')}\n"
        f"digest={artifact.get('digest', '')}\n",
        encoding="utf-8",
    )
    print(f"Verified CI run {selected}" if selected else "Skipped an outdated main revision")
