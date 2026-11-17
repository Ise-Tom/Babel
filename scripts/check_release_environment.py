"""Refuse source prerelease jobs unless the existing review environment is protected."""

from typing import Any

from publish_dashboard import Api, api


def validate(environment: dict[str, Any], policies: dict[str, Any]) -> None:
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
        or len(reviewers) != 1
        or reviewers[0].get("prevent_self_review") is not True
        or not reviewers[0].get("reviewers")
        or policies.get("total_count") != 1
        or [
            {"name": row.get("name"), "type": row.get("type")}
            for row in policies.get("branch_policies", [])
        ]
        != [{"name": "v*", "type": "tag"}]
    ):
        raise ValueError("source-release requires independent review, no bypass and only v* tags")
    for entry in reviewers[0]["reviewers"]:
        reviewer = entry.get("reviewer", {})
        if entry.get("type") not in {"User", "Team"} or (
            type(reviewer.get("id")) is not int or reviewer["id"] <= 0
        ):
            raise ValueError("source-release requires explicit eligible reviewers")


def check(*, request: Api = api) -> None:
    environment = request("GET", "environments/source-release", None)
    policies = request("GET", "environments/source-release/deployment-branch-policies", None)
    validate(environment, policies)


if __name__ == "__main__":
    try:
        check()
    except (RuntimeError, ValueError, TypeError, AttributeError, KeyError) as error:
        raise SystemExit(
            "Source prerelease blocked: configure and verify the existing source-release "
            "review environment in repository Settings > Environments."
        ) from error
    print("Source-release environment review/tag protections verified")
