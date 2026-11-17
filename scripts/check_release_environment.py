"""Validate source-only prerelease environments for solo or team operation."""

import argparse
from typing import Any, Literal

from publish_dashboard import Api, api


def validate(
    environment: dict[str, Any], policies: dict[str, Any], *, mode: Literal["solo", "team"] = "solo"
) -> None:
    if mode not in {"solo", "team"}:
        raise ValueError("Unknown source-release maintainer mode")
    reviewers = [
        rule
        for rule in environment.get("protection_rules", [])
        if rule.get("type") == "required_reviewers"
    ]
    branch_policy = environment.get("deployment_branch_policy", {})
    if (
        environment.get("name") != "source-release"
        or environment.get("can_admins_bypass") is not False
        or branch_policy.get("protected_branches") is not False
        or branch_policy.get("custom_branch_policies") is not True
        or policies.get("total_count") != 1
        or [
            {"name": row.get("name"), "type": row.get("type")}
            for row in policies.get("branch_policies", [])
        ]
        != [{"name": "v*", "type": "tag"}]
    ):
        raise ValueError("source-release requires no admin bypass and only v* tags")
    if mode == "solo":
        if reviewers:
            raise ValueError("Solo source prereleases must not require another reviewer")
        return
    if (
        len(reviewers) != 1
        or reviewers[0].get("prevent_self_review") is not True
        or not reviewers[0].get("reviewers")
    ):
        raise ValueError("Team source prereleases require independent review")
    for entry in reviewers[0]["reviewers"]:
        reviewer = entry.get("reviewer", {})
        if entry.get("type") not in {"User", "Team"} or (
            type(reviewer.get("id")) is not int or reviewer["id"] <= 0
        ):
            raise ValueError("source-release requires explicit eligible reviewers")


def check(*, request: Api = api, mode: Literal["solo", "team"] = "solo") -> None:
    environment = request("GET", "environments/source-release", None)
    policies = request("GET", "environments/source-release/deployment-branch-policies", None)
    validate(environment, policies, mode=mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("solo", "team"), default="solo")
    args = parser.parse_args()
    try:
        check(mode=args.mode)
    except (RuntimeError, ValueError, TypeError, AttributeError, KeyError) as error:
        raise SystemExit(
            "Source prerelease blocked: configure and verify the existing source-release "
            "environment for the selected maintainer mode in Settings > Environments."
        ) from error
    print(f"Source-release environment/tag protections verified ({args.mode} maintainer mode)")
