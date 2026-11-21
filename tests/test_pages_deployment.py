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
        self.artifacts = [
            {
                "id": 456,
                "name": "dashboard-standalone",
                "expired": False,
                "size_in_bytes": 200,
                "digest": "sha256:" + "b" * 64,
            }
        ]
        self.candidates = [{"event": "pull_request"}, self.run]
        self.artifacts_by_run = {}
        self.current = REVISION
        self.calls = []

    def request(self, method, path, payload=None):
        self.assertEqual(method, "GET")
        self.assertIsNone(payload)
        self.calls.append(path)
        if path == "branches/main":
            return {"commit": {"sha": self.current}}
        if path.endswith("/artifacts"):
            run_id = int(path.split("/")[-2])
            return {"artifacts": self.artifacts_by_run.get(run_id, self.artifacts)}
        if path.startswith("actions/workflows/"):
            return {"workflow_runs": self.candidates}
        return self.run

    def test_exact_successful_main_run_and_manual_retry_are_supported(self):
        expected = (123, self.artifacts[0])
        self.assertEqual(pages.source_artifact(REVISION, "123", request=self.request), expected)
        self.assertEqual(pages.source_artifact(REVISION, request=self.request), expected)
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
        self.assertIsNone(pages.source_artifact(REVISION, "123", request=self.request))
        self.assertEqual(self.calls, ["branches/main"])

    def test_unverified_or_expired_artifacts_are_rejected(self):
        for artifacts in (
            [],
            [dict(self.artifacts[0], expired=True)],
            [dict(self.artifacts[0], size_in_bytes=0)],
            [dict(self.artifacts[0], size_in_bytes=True)],
            [self.artifacts[0], self.artifacts[0]],
            [dict(self.artifacts[0], name="unrelated")],
            [dict(self.artifacts[0], size_in_bytes=2 * 1024 * 1024 + 1)],
            [dict(self.artifacts[0], id=True)],
            [dict(self.artifacts[0], id=0)],
            [dict(self.artifacts[0], digest="missing")],
        ):
            self.artifacts = artifacts
            with (
                self.subTest(artifacts=artifacts),
                self.assertRaisesRegex(ValueError, "missing or expired|metadata is invalid"),
            ):
                pages.source_artifact(REVISION, "123", request=self.request)

    def test_manual_retry_uses_the_latest_eligible_retained_artifact(self):
        self.candidates = [dict(self.run, id=126), dict(self.run, id=125), self.run]
        self.artifacts_by_run = {126: [], 125: [dict(self.artifacts[0], expired=True)]}
        self.assertEqual(
            pages.source_artifact(REVISION, request=self.request), (123, self.artifacts[0])
        )
        self.assertEqual(
            [path for path in self.calls if path.endswith("/artifacts")],
            [
                "actions/runs/126/artifacts",
                "actions/runs/125/artifacts",
                "actions/runs/123/artifacts",
            ],
        )

    def test_event_pins_its_run_and_manual_retry_rejects_invalid_metadata(self):
        self.run = dict(self.run, id=124)
        self.candidates.insert(0, self.run)
        self.artifacts_by_run[124] = []
        with self.assertRaisesRegex(ValueError, "missing or expired"):
            pages.source_artifact(REVISION, "124", request=self.request)
        self.artifacts_by_run[124] = [dict(self.artifacts[0], digest="invalid")]
        self.calls.clear()
        with self.assertRaisesRegex(ValueError, "metadata is invalid"):
            pages.source_artifact(REVISION, request=self.request)
        self.assertNotIn("actions/runs/123/artifacts", self.calls)

    def test_no_matching_successful_ci_refuses_publication(self):
        self.run["conclusion"] = "failure"
        with self.assertRaisesRegex(ValueError, "run CI first"):
            pages.source_artifact(REVISION, request=self.request)

    def test_invalid_ids_do_not_reach_unintended_api_routes(self):
        with self.assertRaisesRegex(ValueError, "source revision"):
            pages.source_artifact("bad", request=self.request)
        self.assertEqual(self.calls, [])
        with self.assertRaisesRegex(ValueError, "CI run ID"):
            pages.source_artifact(REVISION, "../other", request=self.request)
        self.assertEqual(self.calls, ["branches/main"])
