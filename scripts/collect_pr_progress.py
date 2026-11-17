"""Read PR metadata/progress as untrusted data; never check out or execute PR code."""

import base64
import datetime
import json
import re
import subprocess  # nosec B404
from pathlib import Path
from typing import Any
from urllib.parse import quote
from zoneinfo import ZoneInfo

from build_dashboard import REPO, require, strings, text
from publish_dashboard import Api, api, check_repository

MAX_PROGRESS_BYTES = 512 * 1024


def bounded(value: Any, label: str, limit: int = 8192) -> str:
    result = text(value, label)
    require(len(result) <= limit, f"{label}: text exceeds reporting limit")
    return result


def pr_sources(
    value: Any, available: set[str], revision: str, *, required: bool = True
) -> list[dict[str, str]]:
    require(
        isinstance(value, list) and len(value) <= 20 and (bool(value) or not required),
        "PR source evidence required",
    )
    result = []
    for source in value:
        name = bounded(source.get("path"), "source path", 512)
        path = Path(name)
        require(
            not path.is_absolute() and ".." not in path.parts and name in available,
            "PR source path is not a file in the reviewed tree",
        )
        result.append(
            {
                "path": name,
                "label": bounded(source.get("label"), "source label", 512),
                "url": f"{REPO}/blob/{revision}/{quote(name)}",
            }
        )
    return result


def proposals(
    progress: dict[str, Any],
    baseline: dict[str, Any],
    model: dict[str, Any],
    available: set[str],
    revision: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require(progress.get("schema_version") == 1, "Unknown PR progress schema")
    known = {step["id"] for phase in model["phases"] for step in phase["steps"]}
    output: dict[str, list[dict[str, Any]]] = {"work_items": [], "problems": []}
    for collection in output:
        records = progress.get(collection)
        if not isinstance(records, list) or len(records) > 200:
            raise ValueError("Invalid PR records")
        originals = {item["id"]: item for item in baseline[collection]}
        seen = set()
        for item in records:
            identifier = bounded(item.get("id"), "record ID", 80)
            require(identifier not in seen, "Duplicate PR record ID")
            seen.add(identifier)
            original = originals.get(identifier, {})
            if {k: v for k, v in item.items() if k != "source_revision"} == {
                k: v for k, v in original.items() if k != "source_revision"
            }:
                continue
            requirements = strings(item.get("requirements"), "PR requirements")
            require(
                set(requirements) <= known and (bool(requirements) or collection == "problems"),
                "Unknown PR requirement",
            )
            record: dict[str, Any] = {
                "id": identifier,
                "title": bounded(item.get("title"), "record title", 512),
                "requirements": requirements,
                "sources": pr_sources(
                    item.get("sources"), available, revision, required=collection == "work_items"
                ),
            }
            fields = (
                ("how", "verification", "limitations")
                if collection == "work_items"
                else (
                    "detail",
                    "next_action",
                    "provenance",
                )
            )
            for field in fields:
                record[field] = bounded(item.get(field), field)
            if collection == "work_items":
                require(item.get("status") == "implemented", "Invalid proposed work status")
                require(item.get("kind") in {"implementation", "design"}, "Invalid work kind")
                record.update(status="implemented", kind=item["kind"])
            else:
                require(item.get("status") in {"open", "resolved"}, "Invalid proposed problem")
                resolution = item.get("resolution", "")
                require(isinstance(resolution, str), "Invalid proposed resolution")
                if item["status"] == "resolved":
                    bounded(resolution, "resolution")
                record.update(status=item["status"], resolution=resolution[:8192])
            output[collection].append(record)
    return output["work_items"], output["problems"]


def collect(
    model: dict[str, Any],
    root: Path,
    *,
    request: Api = api,
    tracked: set[str] | None = None,
) -> None:
    repository = request("GET", "", None)
    check_repository(repository)
    revision = model["buildRevision"]
    require(bool(re.fullmatch(r"[a-f0-9]{40}", revision)), "Invalid report revision")
    require(request("GET", "branches/main", None)["commit"]["sha"] == revision, "Outdated main")
    main_runs = request(
        "GET", f"actions/workflows/ci.yml/runs?head_sha={revision}&per_page=1", None
    )["workflow_runs"]
    state = "unknown"
    if main_runs:
        state = str(main_runs[0].get("conclusion") or main_runs[0].get("status") or "unknown")[:40]
    model["mainCi"] = {"state": state, "revision": revision}
    baseline = json.loads((root / "dashboard/progress.json").read_text(encoding="utf-8"))
    if tracked is None:
        tracked = set(
            subprocess.check_output(  # nosec B603, B607
                ["git", "ls-files", "-z"], cwd=root, text=True
            ).split("\0")
        )
    pull_requests = request("GET", "pulls?state=open&base=main&per_page=50", None)
    require(isinstance(pull_requests, list), "Invalid PR listing")
    result = []
    for pr in pull_requests[:50]:
        number = pr.get("number")
        require(type(number) is int and number > 0, "Invalid PR number")
        head = pr["head"]["sha"]
        require(
            isinstance(head, str) and bool(re.fullmatch(r"[a-f0-9]{40}", head)), "Invalid PR SHA"
        )
        entry: dict[str, Any] = {
            "number": number,
            "title": bounded(pr.get("title"), "PR title", 512),
            "url": f"{REPO}/pull/{number}",
            "head": head,
            "draft": bool(pr.get("draft")),
            "body": str(pr.get("body") or "")[:12000],
            "ci": "unknown",
            "files": [],
            "workItems": [],
            "problems": [],
            "note": "",
        }
        try:
            files = request("GET", f"pulls/{number}/files?per_page=100", None)
            entry["files"] = [bounded(item.get("filename"), "PR filename", 512) for item in files]
            available = tracked | {
                item["filename"] for item in files if item["status"] != "removed"
            }
            available -= {item["filename"] for item in files if item["status"] == "removed"}
            if len(files) == 100:
                entry["note"] = "File list limited to the first 100 changed files. "
            runs = request(
                "GET", f"actions/workflows/ci.yml/runs?head_sha={head}&per_page=1", None
            )["workflow_runs"]
            if runs:
                run = runs[0]
                entry["ci"] = str(run.get("conclusion") or run.get("status") or "unknown")[:40]
            require(pr["head"]["repo"]["full_name"] == "Ise-Tom/Babel", "Fork facts not imported")
            file = request("GET", f"contents/dashboard/progress.json?ref={head}", None)
            require(
                type(file.get("size")) is int and file["size"] <= MAX_PROGRESS_BYTES,
                "PR facts too large",
            )
            encoded = file["content"]
            require(
                isinstance(encoded, str) and len(encoded) <= MAX_PROGRESS_BYTES * 2,
                "PR facts too large",
            )
            raw = base64.b64decode("".join(encoded.split()), validate=True)
            require(len(raw) <= MAX_PROGRESS_BYTES, "PR facts too large")
            progress = json.loads(raw)
            entry["workItems"], entry["problems"] = proposals(
                progress, baseline, model, available, head
            )
        except (ValueError, RuntimeError, KeyError, TypeError, AttributeError, RecursionError):
            entry["note"] += (
                "Structured progress unavailable or invalid; inspect the PR description/files."
            )
        result.append(entry)
    model["pullRequests"] = result
    model["prObservation"] = {
        "checked_at": datetime.datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="seconds"),
        "limited": len(pull_requests) >= 50,
    }
