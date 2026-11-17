"""Select an immutable dashboard artifact from successful CI on current main."""

import argparse
import re
from pathlib import Path
from typing import Any

from publish_dashboard import Api, api


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


def source_run(revision: str, run_id: str = "", *, request: Api = api) -> int | None:
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Invalid source revision")
    if request("GET", "branches/main", None)["commit"]["sha"] != revision:
        return None
    if run_id:
        if not re.fullmatch(r"[1-9][0-9]*", run_id):
            raise ValueError("Invalid CI run ID")
        selected = validate_run(request("GET", f"actions/runs/{run_id}", None), revision)
    else:
        candidates = request(
            "GET",
            f"actions/workflows/ci.yml/runs?head_sha={revision}&status=success&per_page=10",
            None,
        )["workflow_runs"]
        selected = None
        for candidate in candidates:
            try:
                selected = validate_run(candidate, revision)
                break
            except ValueError:
                continue
        if selected is None:
            raise ValueError("No successful main CI exists for this revision; run CI first")
    artifacts = request("GET", f"actions/runs/{selected}/artifacts", None)["artifacts"]
    matches = [item for item in artifacts if item.get("name") == "dashboard-standalone"]
    if (
        len(matches) != 1
        or matches[0].get("expired") is not False
        or type(matches[0].get("size_in_bytes")) is not int
        or matches[0]["size_in_bytes"] <= 0
    ):
        raise ValueError("The verified standalone dashboard artifact is missing or expired")
    return selected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    selected = source_run(args.revision, args.run_id)
    args.output.write_text(
        f"ready={'true' if selected is not None else 'false'}\nrun_id={selected or ''}\n",
        encoding="utf-8",
    )
    print(f"Verified CI run {selected}" if selected else "Skipped an outdated main revision")
