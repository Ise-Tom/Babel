"""Check a synthetic offline P00-17 record without promoting it to live evidence."""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED = (
    "draft_prepared",
    "submitted",
    "reporter_visible",
    "notification_observed",
    "owner_opened",
    "owner_acknowledged",
    "backup_role_accepted",
    "backup_opened",
    "escalation_acknowledged",
    "closed",
)
ACTORS = {
    "draft_prepared": "simulated-reporter",
    "submitted": "simulated-reporter",
    "reporter_visible": "simulated-reporter",
    "notification_observed": "simulated-owner",
    "owner_opened": "simulated-owner",
    "owner_acknowledged": "simulated-owner",
    "backup_role_accepted": "simulated-backup",
    "backup_opened": "simulated-backup",
    "escalation_acknowledged": "simulated-backup",
    "closed": "simulated-owner",
}
SCENARIOS = {
    "all_mock_fields",
    "notification_without_owner_receipt",
    "owner_receipt_without_backup",
    "owner_opened_without_acknowledgment",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check(record: dict[str, Any]) -> dict[str, Any]:
    require(record.get("schema_version") == 1, "Unexpected schema")
    require(
        record.get("kind") == "offline_simulation_only", "Live evidence cannot use this fixture"
    )
    require(record.get("repository") == "Ise-Tom/Babel", "Wrong repository")
    require(record.get("live_report_id") is None, "Offline record cannot contain a report ID")
    require(record.get("real_backup_contact") is None, "Offline record cannot claim a backup")
    require(
        isinstance(record.get("base_revision"), str) and len(record["base_revision"]) == 40,
        "Base revision required",
    )
    scenarios = record.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) != len(SCENARIOS):
        raise ValueError("All rehearsal cases required")
    outcomes = {}
    for scenario in scenarios:
        require(isinstance(scenario, dict), "Case must be an object")
        name = scenario.get("id")
        require(name in SCENARIOS and name not in outcomes, "Unknown or duplicate case")
        events = scenario.get("events")
        require(isinstance(events, list) and bool(events), f"{name}: events required")
        seen = set()
        prior = None
        for event in events:
            require(isinstance(event, dict), f"{name}: event must be an object")
            kind = event.get("type")
            require(kind in ACTORS and kind not in seen, f"{name}: unknown or duplicate event")
            require(event.get("actor") == ACTORS[kind], f"{name}: wrong simulated actor")
            stamp = event.get("at_utc")
            require(
                isinstance(stamp, str) and stamp.endswith("Z"), f"{name}: UTC timestamp required"
            )
            try:
                current = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"{name}: invalid timestamp") from exc
            require(prior is None or current > prior, f"{name}: nonmonotonic event time")
            prior = current
            seen.add(kind)
        require(
            "notification_observed" not in seen or "submitted" in seen,
            f"{name}: notification before submission",
        )
        missing = [kind for kind in REQUIRED if kind not in seen]
        outcome = (
            "incomplete:" + ",".join(missing) if missing else "offline_complete_not_gate_evidence"
        )
        require(scenario.get("expected") == outcome, f"{name}: expected outcome mismatch")
        outcomes[name] = outcome
    require(set(outcomes) == SCENARIOS, "Missing rehearsal case")
    require(
        outcomes["all_mock_fields"] == "offline_complete_not_gate_evidence",
        "Nominal simulation must not pass gate",
    )
    return {
        "schema_version": 1,
        "kind": "offline_recordkeeping_check",
        "outcomes": outcomes,
        "p00_17_ready": False,
        "unmet": [
            "authorized live private drill with independently verified receipt and escalation",
            "real available backup responder",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--record", type=Path, default=Path("lab/security-intake/offline-rehearsal.json")
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check(json.loads(args.record.read_text(encoding="utf-8")))
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
