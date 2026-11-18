"""Build explicit capability implementation claims without inferring delivery from associations."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

STATUSES = {"planned", "prototype", "partial", "implemented"}
CATEGORIES = {"product", "runtime_lab", "experiment", "engineering"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def strings(value: Any, *, empty: bool = True) -> list[str]:
    require(isinstance(value, list), "Capability list required")
    require(
        all(isinstance(v, str) and v.strip() and len(v) <= 8192 for v in value),
        "Invalid capability text/reference",
    )
    require(len(value) == len(set(value)), "Duplicate capability reference")
    require(empty or bool(value), "Capability evidence/scope cannot be empty")
    return list(value)


def enrich(
    root: Path,
    features: dict[str, dict[str, Any]],
    phases: list[dict[str, Any]],
    work: list[dict[str, Any]],
    problems: list[dict[str, Any]],
    validate_acceptance: Callable[[Any, str], None],
) -> None:
    data = json.loads((root / "dashboard/capabilities.json").read_text())
    require(
        type(data.get("schema_version")) is int and data["schema_version"] == 1,
        "Unknown capability tracker schema",
    )
    claims = data.get("claims")
    require(
        isinstance(claims, dict) and set(claims) <= features.keys(), "Unknown capability claims"
    )
    works = {w["id"]: w for w in work}
    issues = {p["id"] for p in problems}
    steps = [s for p in phases for s in p["steps"]]
    for identifier, feature in features.items():
        related = [s["id"] for s in steps if identifier in s["features"]]
        feature["requirements"] = related
        feature["supportingWork"] = [w["id"] for w in work if set(w["requirements"]) & set(related)]
        claim = claims.get(
            identifier,
            {
                "status": "planned",
                "category": "product",
                "scope": (
                    "No functional implementation is claimed. "
                    "Related design/tooling does not qualify this capability."
                ),
                "implemented": [],
                "missing": [feature["verification"]],
                "work_items": [],
                "blockers": [],
                "acceptance": None,
            },
        )
        require(
            isinstance(claim, dict)
            and set(claim)
            == {
                "status",
                "category",
                "scope",
                "implemented",
                "missing",
                "work_items",
                "blockers",
                "acceptance",
            },
            "Incomplete or unknown capability fields",
        )
        require(
            claim["status"] in STATUSES and claim["category"] in CATEGORIES,
            "Unknown capability implementation state",
        )
        require(
            isinstance(claim["scope"], str)
            and bool(claim["scope"].strip())
            and len(claim["scope"]) <= 8192,
            "Capability scope required",
        )
        implemented = strings(claim["implemented"])
        missing = strings(claim["missing"])
        refs = strings(claim["work_items"])
        blockers = strings(claim["blockers"])
        require(
            set(refs) <= works.keys() and set(blockers) <= issues,
            "Unknown capability evidence or blocker",
        )
        if claim["status"] == "planned":
            require(not implemented, "Planned capability cannot claim implemented behavior")
        else:
            require(
                bool(implemented) and any(works[w]["kind"] == "implementation" for w in refs),
                "Functional capability claim requires explicit implementation evidence",
            )
        if claim["status"] in {"planned", "prototype", "partial"}:
            require(bool(missing), "Unqualified capability gaps must remain visible")
        else:
            require(not missing, "Implemented capability cannot retain declared gaps")
        proof = claim["acceptance"]
        if proof is not None:
            require(
                claim["status"] == "implemented" and claim["category"] == "product" and not missing,
                "Partial/tooling scope cannot accept the full capability",
            )
            validate_acceptance(proof, f"capability {identifier}")
        feature["implementation"] = {
            **claim,
            "implemented": implemented,
            "missing": missing,
            "work_items": refs,
            "blockers": blockers,
        }
