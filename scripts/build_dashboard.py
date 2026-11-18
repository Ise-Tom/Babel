"""Build a validated, offline dashboard model from canonical phase documents."""

import argparse
import datetime
import json
import re
import subprocess  # nosec B404
from pathlib import Path
from typing import Any
from urllib.parse import quote

from check_design import GLOBAL_ID, GLOBAL_SOURCES, SECTIONS, check

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Ise-Tom/Babel"
STATES = {"planned", "in_progress", "blocked", "ready_for_validation", "accepted"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any, label: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty text required")
    return str(value)


def strings(value: Any, label: str) -> list[str]:
    require(isinstance(value, list), f"{label}: list required")
    return [text(item, label) for item in value]


def record(value: Any, label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label}: object required")
    return dict(value)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def plain(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.replace("**", "").replace("`", "").strip()


def acceptance(value: Any, label: str) -> None:
    proof = record(value, label)
    for field in ("reviewer", "date", "evidence"):
        text(proof.get(field), f"{label}.{field}")
    datetime.date.fromisoformat(proof["date"])


def sources(root: Path, value: Any, revision: str) -> list[dict[str, str]]:
    require(isinstance(value, list), "sources: list required")
    result = []
    for raw in value:
        source = record(raw, "source")
        name = text(source.get("path"), "source.path")
        path = root / name
        require(
            not Path(name).is_absolute()
            and ".." not in Path(name).parts
            and path.resolve().is_relative_to(root.resolve())
            and path.is_file()
            and not path.is_symlink(),
            f"Unsafe or missing source: {name}",
        )
        result.append(
            {
                "path": name,
                "label": text(source.get("label"), "source.label"),
                "url": f"{REPO}/blob/{revision}/{quote(name)}",
            }
        )
    return result


def build(root: Path, revision: str) -> dict[str, Any]:
    require(bool(re.fullmatch(r"[a-f0-9]{40}", revision)), "Invalid build revision")
    require(not check(root), "Canonical design validation failed")
    progress = record(read_json(root / "dashboard/progress.json"), "progress")
    require(
        type(progress.get("schema_version")) is int and progress.get("schema_version") == 1,
        "Unsupported progress schema",
    )
    require(
        type(progress.get("focus_phase")) is int and 0 <= progress["focus_phase"] < 18,
        "Invalid focus phase",
    )
    text(progress.get("focus_summary"), "focus summary")
    snapshot = record(progress.get("snapshot"), "snapshot")
    datetime.date.fromisoformat(text(snapshot.get("date"), "snapshot.date"))
    evidence_revision = text(snapshot.get("commit"), "snapshot.commit")
    require(bool(re.fullmatch(r"[a-f0-9]{40}", evidence_revision)), "Invalid evidence revision")
    require(
        bool(
            re.fullmatch(
                re.escape(REPO) + r"/actions/runs/\d+", text(snapshot.get("ci_url"), "CI URL")
            )
        ),
        "Unsafe CI URL",
    )
    require(snapshot.get("ci_result") in {"passed", "failed", "unknown"}, "Invalid CI result")
    require(
        type(snapshot.get("checks_passed")) is int and snapshot["checks_passed"] >= 0,
        "Invalid check count",
    )
    text(snapshot.get("note"), "snapshot.note")
    require(isinstance(snapshot.get("pull_requests"), list), "PR snapshot required")
    for pr in snapshot["pull_requests"]:
        require(type(pr.get("number")) is int and pr["number"] > 0, "Invalid PR number")
        require(
            pr.get("state") in {"open", "closed", "merged"} and type(pr.get("draft")) is bool,
            "Invalid PR state",
        )
    features: dict[str, dict[str, Any]] = {}
    for filename in GLOBAL_SOURCES:
        content = (root / "docs" / filename).read_text()
        for identifier, title, verification in re.findall(
            rf"^\| ({GLOBAL_ID}) \| ([^|]+) \| ([^|]+) \|$", content, re.M
        ):
            features[identifier] = {
                "id": identifier,
                "title": plain(title),
                "verification": plain(verification),
                "url": f"{REPO}/blob/{revision}/docs/{filename}",
            }
    associations = record(read_json(root / "dashboard/associations.json"), "associations")
    overrides = record(progress.get("requirements"), "requirements")
    phase_acceptance = record(progress.get("phase_acceptance"), "phase_acceptance")
    phases: list[dict[str, Any]] = []
    ids: set[str] = set()
    for number in range(18):
        path = root / f"docs/phases/phase-{number:02}.md"
        content = path.read_text()
        heading = content.splitlines()[0].split(" — ", 1)[1]
        sections = {}
        for section in SECTIONS:
            match = re.search(
                rf"^## {re.escape(section)}\n\n(.+?)(?=\n## |\Z)", content, re.M | re.S
            )
            require(match is not None, f"Missing section {section}")
            if match:
                sections[section] = plain(match.group(1))
        owner = next(
            line.removeprefix("Owner roles: ")
            for line in content.splitlines()
            if line.startswith("Owner roles:")
        )
        rows = re.findall(r"^\| (P\d{2}-\d{2}) \|([^|]*)\|([^|]*)\|$", content, re.M)
        steps = []
        for identifier, title, verification in rows:
            ids.add(identifier)
            associated = strings(associations.get(identifier), f"{identifier} features")
            require(
                bool(associated) and all(item in features for item in associated),
                f"{identifier}: unknown/empty features",
            )
            override = record(overrides.get(identifier, {}), identifier)
            status = override.get("status", "planned")
            require(status in STATES, f"{identifier}: unknown status")
            if status == "accepted":
                acceptance(override.get("acceptance"), identifier)
            validation = override.get("validation")
            if status == "ready_for_validation":
                require(isinstance(validation, dict), f"{identifier}: validation packet required")
            if validation is not None:
                validation = record(validation, identifier + " validation")
                text(validation.get("scope"), identifier + " validation scope")
                packet_revision = text(validation.get("source_revision"), "validation revision")
                require(
                    bool(re.fullmatch(r"[a-f0-9]{40}", packet_revision)),
                    "Invalid validation revision",
                )
                validation = {
                    "scope": validation["scope"],
                    "packet": sources(root, [validation.get("packet")], packet_revision)[0],
                }
            steps.append(
                {
                    "id": identifier,
                    "title": plain(title),
                    "verification": plain(verification),
                    "status": status,
                    "note": text(
                        override.get("note", "No implementation or acceptance evidence recorded."),
                        identifier + " note",
                    ),
                    "acceptance": override.get("acceptance"),
                    "validation": validation,
                    "features": associated,
                }
            )
        phase_features = re.search(r"^Traceability: (.+)$", content, re.M)
        require(phase_features is not None, "Missing phase traceability")
        associated_phase = set(phase_features.group(1).split(", ")) if phase_features else set()
        associated_phase.update(feature for step in steps for feature in step["features"])
        accepted = sum(step["status"] == "accepted" for step in steps)
        phase_proof = phase_acceptance.get(str(number))
        if phase_proof is not None:
            require(
                accepted == len(steps),
                f"Phase {number}: acceptance without all requirements accepted",
            )
            acceptance(phase_proof, f"phase {number}")
        status = (
            "accepted"
            if phase_proof is not None
            else "in_progress"
            if any(
                step["status"] in {"in_progress", "ready_for_validation", "accepted"}
                for step in steps
            )
            else "planned"
        )
        phases.append(
            {
                "id": number,
                "title": heading,
                "owner": owner,
                "sections": sections,
                "steps": steps,
                "features": sorted(associated_phase),
                "status": status,
                "url": f"{REPO}/blob/{revision}/docs/phases/phase-{number:02}.md",
            }
        )
    require(
        set(associations) == ids and set(overrides) <= ids,
        "Unknown or missing requirement association/status",
    )
    require(set(phase_acceptance) <= {str(i) for i in range(18)}, "Unknown accepted phase")
    work = progress.get("work_items")
    problems = progress.get("problems")
    if not isinstance(work, list) or not isinstance(problems, list):
        raise ValueError("Work and problems lists required")
    problem_ids: set[str] = set()
    for index, raw in enumerate(problems):
        problem = record(raw, "problem")
        problems[index] = problem
        text(problem.get("id"), "problem ID")
        require(problem["id"] not in problem_ids, "Duplicate problem ID")
        problem_ids.add(text(problem.get("id"), "problem ID"))
        require(problem.get("status") in {"open", "resolved"}, "Invalid problem status")
        for field in ("title", "kind", "detail", "next_action", "provenance"):
            text(problem.get(field), f"problem.{field}")
        if problem["status"] == "resolved":
            text(problem.get("resolution"), "resolved problem resolution")
        require(
            bool(problem.get("phases"))
            and all(type(p) is int and 0 <= p < 18 for p in problem["phases"]),
            "Invalid problem phases",
        )
        require(
            set(strings(problem.get("requirements"), "problem requirements")) <= ids,
            "Unknown problem requirement",
        )
        source_revision = problem.get("source_revision", evidence_revision)
        require(
            isinstance(source_revision, str)
            and bool(re.fullmatch(r"[a-f0-9]{40}", source_revision)),
            "Invalid problem source revision",
        )
        problem["sources"] = sources(root, problem.get("sources"), source_revision)
    work_ids: set[str] = set()
    for index, raw in enumerate(work):
        item = record(raw, "work")
        work[index] = item
        identifier = text(item.get("id"), "work ID")
        require(identifier not in work_ids, "Duplicate work ID")
        work_ids.add(identifier)
        require(item.get("status") == "implemented", "Unknown work status")
        require(item.get("kind") in {"implementation", "design"}, "Invalid work kind")
        for field in ("title", "how", "verification", "limitations"):
            text(item.get(field), f"work.{field}")
        links = strings(item.get("requirements"), "work requirements")
        require(bool(links) and set(links) <= ids, "Unknown/empty work requirement")
        require(
            set(strings(item.get("problems"), "work problems")) <= problem_ids,
            "Unknown work problem",
        )
        source_revision = item.get("source_revision", evidence_revision)
        require(
            isinstance(source_revision, str)
            and bool(re.fullmatch(r"[a-f0-9]{40}", source_revision)),
            "Invalid work source revision",
        )
        item["sources"] = sources(root, item.get("sources"), source_revision)
        require(bool(item["sources"]), "Implemented work requires source evidence")
    for phase in phases:
        for step in phase["steps"]:
            if step["status"] in {"accepted", "ready_for_validation"}:
                require(
                    any(step["id"] in item["requirements"] for item in work),
                    "Accepted/validation-ready requirement needs implementation/explanation record",
                )
    from capability_tracker import enrich

    enrich(root, features, phases, work, problems, acceptance)
    return {
        "schemaVersion": 1,
        "buildRevision": revision,
        "focusPhase": progress["focus_phase"],
        "focusSummary": progress["focus_summary"],
        "snapshot": snapshot,
        "phases": phases,
        "features": list(features.values()),
        "workItems": work,
        "problems": problems,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "dashboard/generated/data.json")
    parser.add_argument("--revision")
    parser.add_argument("--check", action="store_true")
    options = parser.parse_args()
    revision = (
        options.revision
        or subprocess.check_output(  # nosec B603, B607
            ["git", "rev-parse", "HEAD"], cwd=options.root, text=True
        ).strip()
    )
    model = build(options.root, revision)
    if not options.check:
        options.output.parent.mkdir(parents=True, exist_ok=True)
        options.output.write_text(json.dumps(model, ensure_ascii=False), encoding="utf-8")
    phase_count = len(model["phases"])
    requirement_count = sum(len(phase["steps"]) for phase in model["phases"])
    print(f"Dashboard validated: {phase_count} phases, {requirement_count} requirements")
