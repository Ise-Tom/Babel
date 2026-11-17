"""Missing review controls must block release before an environment job can auto-create one."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_release_environment as policy  # noqa: E402


class ReleaseEnvironment(unittest.TestCase):
    def setUp(self):
        self.environment = {
            "name": "source-release",
            "can_admins_bypass": False,
            "deployment_branch_policy": {
                "protected_branches": False,
                "custom_branch_policies": True,
            },
            "protection_rules": [
                {
                    "type": "required_reviewers",
                    "prevent_self_review": True,
                    "reviewers": [{"type": "User", "reviewer": {"id": 123}}],
                }
            ],
        }
        self.policies = {"total_count": 1, "branch_policies": [{"type": "tag", "name": "v*"}]}

    def test_explicit_independent_review_and_scoped_tags_are_required(self):
        policy.validate(self.environment, self.policies)

    def test_bypass_self_review_missing_reviewers_or_wrong_scope_are_rejected(self):
        changes = [
            lambda e: e.update(name="other"),
            lambda e: e.update(can_admins_bypass=True),
            lambda e: e.update(protection_rules=[]),
            lambda e: e["protection_rules"].append(e["protection_rules"][0]),
            lambda e: e["protection_rules"][0].update(prevent_self_review=False),
            lambda e: e["protection_rules"][0].update(reviewers=[]),
            lambda e: e["protection_rules"][0]["reviewers"][0].update(type="Unknown"),
            lambda e: e["protection_rules"][0]["reviewers"][0]["reviewer"].update(id=True),
            lambda e: e["deployment_branch_policy"].update(custom_branch_policies=False),
            lambda e: e["deployment_branch_policy"].update(protected_branches=True),
        ]
        for change in changes:
            environment = copy.deepcopy(self.environment)
            change(environment)
            with self.subTest(change=change), self.assertRaises(ValueError):
                policy.validate(environment, self.policies)

    def test_unrestricted_extra_or_branch_policies_are_rejected(self):
        for policies in (
            {},
            {"total_count": 0, "branch_policies": []},
            {"total_count": 2, "branch_policies": self.policies["branch_policies"] * 2},
            {"total_count": 1, "branch_policies": [{"name": "*", "type": "tag"}]},
            {"total_count": 1, "branch_policies": [{"name": "v*", "type": "branch"}]},
        ):
            with self.subTest(policies=policies), self.assertRaises(ValueError):
                policy.validate(self.environment, policies)

    def test_checker_uses_read_only_fixed_endpoints_and_missing_access_fails(self):
        calls = []

        def request(method, path, payload):
            calls.append((method, path, payload))
            return self.environment if path.endswith("source-release") else self.policies

        policy.check(request=request)
        self.assertEqual(
            calls,
            [
                ("GET", "environments/source-release", None),
                ("GET", "environments/source-release/deployment-branch-policies", None),
            ],
        )

        def unavailable(method, path, payload):
            raise RuntimeError("Unavailable")

        with self.assertRaises(RuntimeError):
            policy.check(request=unavailable)
