"""Public hosting may consume only a successful immutable main CI artifact."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_pages_source as pages  # noqa: E402

REVISION = "a" * 40


def successful_run():
    return {
        "id": 123,
        "repository": {"full_name": "Ise-Tom/Babel"},
        "head_repository": {"full_name": "Ise-Tom/Babel"},
        "head_branch": "main",
        "head_sha": REVISION,
        "path": ".github/workflows/ci.yml",
        "event": "push",
        "status": "completed",
        "conclusion": "success",
    }


class PagesSource(unittest.TestCase):
    def setUp(self):
        self.run = successful_run()
        self.artifacts = [{"name": "dashboard-standalone", "expired": False, "size_in_bytes": 200}]
        self.current = REVISION
        self.calls = []

    def request(self, method, path, payload=None):
        self.assertEqual(method, "GET")
        self.assertIsNone(payload)
        self.calls.append(path)
        if path == "branches/main":
            return {"commit": {"sha": self.current}}
        if path.endswith("/artifacts"):
            return {"artifacts": self.artifacts}
        if path.startswith("actions/workflows/"):
            return {"workflow_runs": [{"event": "pull_request"}, self.run]}
        return self.run

    def test_exact_successful_main_run_and_manual_retry_are_supported(self):
        self.assertEqual(pages.source_run(REVISION, "123", request=self.request), 123)
        self.assertEqual(pages.source_run(REVISION, request=self.request), 123)
        self.run["event"] = "workflow_dispatch"
        self.assertEqual(pages.validate_run(self.run, REVISION), 123)

    def test_fork_pr_schedule_failure_wrong_workflow_and_revision_cannot_publish(self):
        for change in (
            {"repository": {"full_name": "other/repo"}},
            {"head_repository": {"full_name": "other/repo"}},
            {"head_branch": "feature"},
            {"head_sha": "b" * 40},
            {"path": ".github/workflows/unrelated.yml"},
            {"event": "pull_request"},
            {"event": "schedule"},
            {"status": "in_progress"},
            {"conclusion": "failure"},
            {"id": True},
        ):
            run = copy.deepcopy(self.run)
            run.update(change)
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "successful CI"):
                pages.validate_run(run, REVISION)

    def test_outdated_main_skips_before_artifact_access(self):
        self.current = "b" * 40
        self.assertIsNone(pages.source_run(REVISION, "123", request=self.request))
        self.assertEqual(self.calls, ["branches/main"])

    def test_unverified_or_expired_artifacts_are_rejected(self):
        for artifacts in (
            [],
            [dict(self.artifacts[0], expired=True)],
            [dict(self.artifacts[0], size_in_bytes=0)],
            [dict(self.artifacts[0], size_in_bytes=True)],
            [self.artifacts[0], self.artifacts[0]],
            [dict(self.artifacts[0], name="unrelated")],
        ):
            self.artifacts = artifacts
            with (
                self.subTest(artifacts=artifacts),
                self.assertRaisesRegex(ValueError, "missing or expired"),
            ):
                pages.source_run(REVISION, "123", request=self.request)

    def test_no_matching_successful_ci_refuses_publication(self):
        self.run["conclusion"] = "failure"
        with self.assertRaisesRegex(ValueError, "run CI first"):
            pages.source_run(REVISION, request=self.request)

    def test_invalid_ids_do_not_reach_unintended_api_routes(self):
        with self.assertRaisesRegex(ValueError, "source revision"):
            pages.source_run("bad", request=self.request)
        self.assertEqual(self.calls, [])
        with self.assertRaisesRegex(ValueError, "CI run ID"):
            pages.source_run(REVISION, "../other", request=self.request)
        self.assertEqual(self.calls, ["branches/main"])
