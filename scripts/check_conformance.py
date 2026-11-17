"""Validate versioned compatibility/evidence records; never run or invent client tests."""

import argparse
import datetime
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from check_design import GLOBAL_ID, GLOBAL_SOURCES

ROOT = Path(__file__).resolve().parents[1]
OUTCOMES = {"passed", "failed", "skipped", "unsupported", "unrun"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 4096


def digest(value: Any, length: int = 64) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(rf"[a-f0-9]{{{length}}}", value))


def indexed(value: Any, label: str) -> dict[str, dict[str, Any]]:
    require(isinstance(value, list) and bool(value), f"{label}: nonempty list required")
    result = {}
    for row in value:
        require(isinstance(row, dict), f"{label}: object required")
        identifier = row.get("id")
        require(
            isinstance(identifier, str)
            and bool(re.fullmatch(r"[A-Za-z0-9-]{1,80}", identifier))
            and identifier not in result,
            f"{label}: unique bounded ID required",
        )
        result[identifier] = row
    return result


def references(value: Any, allowed: set[str], label: str) -> None:
    require(
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) for item in value)
        and len(set(value)) == len(value)
        and set(value) <= allowed,
        f"{label}: nonempty unique known references required",
    )


def review(value: Any) -> bool:
    if not isinstance(value, dict) or not text(value.get("reviewer")):
        return False
    try:
        datetime.date.fromisoformat(value.get("date", ""))
    except (ValueError, TypeError):
        return False
    return value.get("disposition") == "accepted" and text(value.get("scope"))


def artifact(root: Path, value: Any) -> None:
    require(isinstance(value, dict), "Artifact object required")
    name = value.get("path")
    require(isinstance(name, str), "Artifact path required")
    path = Path(name)
    require(
        path.parts[:2] == ("lab", "evidence-artifacts")
        and ".." not in path.parts
        and not path.is_absolute(),
        "Artifact must stay in lab/evidence-artifacts",
    )
    target = root / path
    require(
        target.resolve().is_relative_to(root.resolve())
        and not any(
            (root / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)
        )
        and target.is_file(),
        "Artifact must be an existing regular file without symlinks",
    )
    require(
        digest(value.get("sha256"))
        and target.stat().st_size <= 8 * 1024 * 1024
        and hashlib.sha256(target.read_bytes()).hexdigest() == value["sha256"],
        "Artifact size/digest mismatch",
    )


def execution(
    root: Path,
    run: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
    operation: dict[str, Any],
    scenario: str,
) -> tuple[str, str]:
    profile, target = run.get("profile"), run.get("target")
    if not isinstance(profile, str) or not isinstance(target, str):
        raise ValueError("Run profile/target must be strings")
    require(profile in operation["profiles"] and target in operation["targets"], "Wrong run scope")
    require(
        digest(run.get("source_revision"), 40)
        and profiles[profile].get("qualification") == "qualified"
        and text(profiles[profile].get("build"))
        and run.get("client_build") == profiles[profile]["build"]
        and digest(profiles[profile].get("image_sha256")),
        "Run requires exact qualified client build/image and source revision",
    )
    require(
        run.get("expected") == operation["scenarios"][scenario],
        "Run expectation differs from declared scenario",
    )
    for field in ("run_id", "operator", "environment", "dataset", "expected", "actual"):
        require(text(run.get(field)), f"Run requires {field}")
    require(
        type(run.get("duration_ms")) is int and run["duration_ms"] > 0,
        "Run duration must be a positive integer",
    )
    stamp = datetime.datetime.fromisoformat(run.get("started_at", ""))
    require(stamp.tzinfo is not None, "Run timestamp needs a timezone")
    versions = run.get("tools")
    require(
        isinstance(versions, dict)
        and bool(versions)
        and all(text(k) and text(v) for k, v in versions.items()),
        "Exact tool versions required",
    )
    artifacts = run.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("Executed runs need retained artifacts")
    for value in artifacts:
        artifact(root, value)
    return profile, target


def validate(root: Path, *, require_ready: bool = False) -> Counter[str]:
    raw = (root / "lab/compatibility.json").read_bytes()
    contract = json.loads(raw)
    evidence = json.loads((root / "lab/conformance-evidence.json").read_bytes())
    require(
        type(contract.get("schema_version")) is int
        and contract["schema_version"] == 1
        and type(evidence.get("schema_version")) is int
        and evidence["schema_version"] == 1,
        "Unknown compatibility/evidence schema",
    )
    require(contract.get("status") in {"proposed", "approved"}, "Unknown contract status")
    require(text(contract.get("id")), "Contract ID required")
    require(
        evidence.get("contract_sha256") == hashlib.sha256(raw).hexdigest(), "Stale contract digest"
    )
    profiles = indexed(contract.get("profiles"), "profiles")
    level = contract.get("functional_level", {})
    require(
        level.get("domain") == "2016" and level.get("forest") == "2016",
        "Initial functional-level scope must remain 2016",
    )
    require(
        {
            "linux-host",
            "win11-pro",
            "win11-enterprise",
            "server-2022",
            "server-2025",
            "linux-client",
            "debian-client",
            "macos-arm",
            "macos-intel",
        }
        <= profiles.keys(),
        "Initial Windows/Linux/macOS client scope is incomplete",
    )
    specs = indexed(contract.get("specifications"), "specifications")
    operations = indexed(contract.get("operations"), "operations")
    known = set()
    for name in GLOBAL_SOURCES:
        known.update(re.findall(rf"^\| ({GLOBAL_ID}) \|", (root / "docs" / name).read_text(), re.M))
    covered = set()
    for operation in operations.values():
        references(operation.get("requirements"), known, "requirements")
        references(operation.get("profiles"), set(profiles), "profiles")
        references(operation.get("specifications"), set(specs), "specifications")
        references(operation.get("targets"), {"babel", "reference"}, "targets")
        covered.update(operation["requirements"])
        require(
            operation.get("implementation") in {"planned", "lab_only", "implemented"}
            and text(operation.get("owner"))
            and text(operation.get("title")),
            "Operation needs owner, title and implementation status",
        )
        scenarios = operation.get("scenarios", {})
        require(
            set(scenarios) == {"positive", "negative"} and all(text(s) for s in scenarios.values()),
            "Positive and negative expectations required",
        )
    required = {f"AD-{i:02}" for i in range(1, 11)} | {f"PLAT-{i:02}" for i in range(1, 4)}
    require(required | {"IAM-01", "OPS-01", "UX-01"} <= covered, "Missing first-production scope")
    for profile in profiles.values():
        require(
            profile.get("qualification") in {"unqualified", "qualified"}, "Unknown profile state"
        )
        require(
            all(text(profile.get(k)) for k in ("product", "role", "architecture")),
            "Profile identity required",
        )
        if profile["qualification"] == "qualified":
            require(
                text(profile.get("build")) and digest(profile.get("image_sha256")),
                "Exact image/build required",
            )
    for spec in specs.values():
        require(spec.get("rights_review") in {"pending", "approved"}, "Unknown rights review state")
        require(
            text(spec.get("url")) and spec["url"].startswith("https://"),
            "HTTPS spec reference required",
        )
    if require_ready:
        require(
            all(op["implementation"] == "implemented" for op in operations.values()),
            "Planned/lab-only operations cannot qualify production conformance",
        )
        require(
            contract["status"] == "approved" and review(contract.get("approval")),
            "Contract is not reviewed/approved",
        )
        require(
            all(p["qualification"] == "qualified" for p in profiles.values()),
            "Unqualified client profiles remain",
        )
        require(
            all(
                text(s.get("revision")) and s["rights_review"] == "approved" for s in specs.values()
            ),
            "Specification revision/rights review incomplete",
        )
    records = evidence.get("records")
    require(isinstance(records, list) and bool(records), "Zero-case evidence is not qualification")
    expected = {
        (identifier, scenario) for identifier in operations for scenario in ("positive", "negative")
    }
    seen = set()
    counts: Counter[str] = Counter()
    for row in records:
        key = (row.get("operation"), row.get("scenario"))
        require(key in expected and key not in seen, "Unknown or duplicate evidence scenario")
        seen.add(key)
        outcome = row.get("outcome")
        require(outcome in OUTCOMES, "Unknown evidence outcome")
        counts[outcome] += 1
        runs = row.get("executions")
        require(isinstance(runs, list), "Execution list required")
        if outcome in {"unrun", "skipped", "unsupported"}:
            require(
                text(row.get("reason")) and not runs,
                "Non-executed cases need reason and no executions",
            )
        else:
            require(bool(runs), "Passed/failed requires actual executions")
            operation = operations[key[0]]
            require(
                all(text(specs[name].get("revision")) for name in operation["specifications"]),
                "Executed observation requires exact specification revisions",
            )
            pairs = [execution(root, run, profiles, operation, row["scenario"]) for run in runs]
            require(len(set(pairs)) == len(pairs), "Duplicate profile/target execution")
            if outcome == "passed":
                require(
                    set(pairs)
                    == {(p, t) for p in operation["profiles"] for t in operation["targets"]},
                    "Passing scenario must cover every declared profile and comparison target",
                )
                require(
                    all(run.get("result") == "passed" for run in runs),
                    "Passing case contains failed execution",
                )
            else:
                require(
                    all(r.get("result") in {"passed", "failed"} for r in runs)
                    and any(r.get("result") == "failed" for r in runs),
                    "Failed case needs a failed execution",
                )
        if require_ready:
            require(
                outcome == "passed" and review(row.get("review")),
                "Unaccepted or non-passing scenario blocks qualification",
            )
    require(seen == expected, "Missing positive/negative evidence scenarios")
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Fail on any unqualified or unaccepted conformance evidence",
    )
    args = parser.parse_args()
    try:
        counts = validate(args.root, require_ready=args.require_ready)
    except (ValueError, OSError, TypeError, AttributeError, KeyError) as error:
        raise SystemExit(f"Compatibility/evidence rejected: {error}") from error
    print(
        f"Compatibility/evidence structure valid: {dict(sorted(counts.items()))}. "
        "Structural validation is not conformance or phase acceptance."
    )
