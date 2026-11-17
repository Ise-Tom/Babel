"""PR reporting consumes bounded data without executing proposals or accepting requirements."""

import base64
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_dashboard as dashboard  # noqa: E402
import collect_pr_progress as tracking  # noqa: E402
import render_dashboard as view  # noqa: E402

MAIN = "a" * 40
HEAD = "b" * 40


class PullRequestProgress(unittest.TestCase):
    def setUp(self):
        self.model = dashboard.build(ROOT, MAIN)
        self.baseline = json.loads((ROOT / "dashboard/progress.json").read_text())
        self.proposed = copy.deepcopy(self.baseline)
        work = copy.deepcopy(self.proposed["work_items"][0])
        work.update(
            id="TEST-ONLY",
            title="Bounded PR change",
            how="New filter implementation",
            requirements=["P01-04"],
            sources=[{"path": "native/babel-ldap/src/filter.rs", "label": "filter.rs"}],
        )
        self.proposed["work_items"].append(work)
        self.pr = {
            "number": 17,
            "title": "Filter change",
            "body": "<script>unsafe()</script>\n![x](https://evil.invalid)",
            "draft": True,
            "head": {"sha": HEAD, "repo": {"full_name": "Ise-Tom/Babel"}},
        }
        self.files = [{"filename": "native/babel-ldap/src/filter.rs", "status": "added"}]
        self.tracked = {
            s["path"]
            for item in self.baseline["work_items"] + self.baseline["problems"]
            for s in item["sources"]
        }
        self.private = True
        self.current = MAIN
        self.main_success = True
        self.fail_progress = False
        self.calls = []
        self.prs = [self.pr]

    def request(self, method, path, payload=None):
        self.assertEqual(method, "GET")
        self.assertIsNone(payload)
        self.calls.append(path)
        if path == "":
            return {"private": self.private}
        if path == "branches/main":
            return {"commit": {"sha": self.current}}
        if path.startswith("actions/workflows/"):
            if MAIN in path:
                return {
                    "workflow_runs": [
                        {
                            "id": 42,
                            "repository": {"full_name": "Ise-Tom/Babel"},
                            "head_repository": {"full_name": "Ise-Tom/Babel"},
                            "head_branch": "main",
                            "head_sha": MAIN,
                            "path": ".github/workflows/ci.yml",
                            "event": "push",
                            "status": "completed",
                            "conclusion": "success" if self.main_success else "failure",
                        }
                    ]
                }
            return {"workflow_runs": [{"status": "in_progress", "conclusion": None}]}
        if path.startswith("pulls?"):
            return self.prs
        if path.startswith("pulls/"):
            return self.files
        if self.fail_progress:
            raise RuntimeError("No progress file")
        raw = json.dumps(self.proposed).encode()
        return {"size": len(raw), "content": base64.b64encode(raw).decode()}

    def collect(self):
        tracking.collect(self.model, ROOT, request=self.request, tracked=self.tracked)
        return self.model["pullRequests"]

    def test_pr_delta_has_real_head_evidence_without_changing_main_acceptance(self):
        previous = copy.deepcopy(self.model)
        self.proposed["work_items"][0]["source_revision"] = HEAD
        prs = self.collect()
        self.assertEqual(self.model["workItems"], previous["workItems"])
        self.assertEqual(self.model["phases"], previous["phases"])
        self.assertEqual(len(prs), 1)
        self.assertEqual(prs[0]["ci"], "in_progress")
        self.assertEqual([w["id"] for w in prs[0]["workItems"]], ["TEST-ONLY"])
        self.assertIn(HEAD, prs[0]["workItems"][0]["sources"][0]["url"])
        report = view.render(self.model)
        self.assertIn("Pending merge", report)
        self.assertIn("Main-branch totals above exclude", report)
        self.assertIn("**Pending PR proposals:**", report)
        self.assertIn("    <script>unsafe()</script>", report)
        self.assertIn("New filter implementation", report)
        self.assertIn("0 phases accepted", report)

    def test_changes_to_existing_records_and_proposed_problem_resolutions_are_included(self):
        self.proposed["work_items"][0]["how"] = "Revised explanation"
        self.proposed["problems"][0]["resolution"] = "Revised resolution"
        pr = self.collect()[0]
        self.assertEqual(len(pr["workItems"]), 2)
        self.assertEqual(pr["problems"][0]["resolution"], "Revised resolution")
        self.assertIn("Proposed problem update", view.render(self.model))

    def test_public_repository_or_stale_main_never_import_pr_data(self):
        self.private = False
        with self.assertRaisesRegex(ValueError, "private report"):
            self.collect()
        self.assertEqual(self.calls, [""])
        self.private = True
        self.current = HEAD
        with self.assertRaisesRegex(ValueError, "Outdated main"):
            self.collect()
        self.current = MAIN
        self.main_success = False
        self.collect()
        self.assertEqual(self.model["mainCi"]["state"], "failure")
        self.assertIn("Current main CI: failure", view.render(self.model))
        self.assertEqual(sum(p["status"] == "accepted" for p in self.model["phases"]), 0)

    def test_missing_invalid_or_fork_facts_preserve_the_pr_metadata(self):
        self.fail_progress = True
        pr = self.collect()[0]
        self.assertEqual(pr["workItems"], [])
        self.assertEqual(pr["files"], [self.files[0]["filename"]])
        self.assertIn("unavailable", pr["note"])
        self.fail_progress = False
        self.proposed["work_items"][-1]["sources"][0]["path"] = "../../private"
        self.assertIn("invalid", self.collect()[0]["note"])
        self.pr["head"]["repo"]["full_name"] = "fork/repo"
        self.assertEqual(self.collect()[0]["workItems"], [])

    def test_oversized_duplicate_unknown_or_incomplete_progress_is_rejected(self):
        original = copy.deepcopy(self.proposed)
        changes = [
            lambda p: p.update(schema_version=99),
            lambda p: p.update(extra="x" * (tracking.MAX_PROGRESS_BYTES + 1)),
            lambda p: p["work_items"].append(p["work_items"][-1]),
            lambda p: p["work_items"][-1].update(requirements=["P99-01"]),
            lambda p: p["work_items"][-1].update(how=""),
            lambda p: p["work_items"][-1].update(kind="unknown"),
            lambda p: p["work_items"][-1].update(status="accepted"),
            lambda p: p["work_items"][-1].update(title="x" * 513),
            lambda p: p.update(work_items=None),
        ]
        for change in changes:
            self.proposed = copy.deepcopy(original)
            change(self.proposed)
            with self.subTest(change=change):
                self.assertIn("invalid", self.collect()[0]["note"])

    def test_no_prs_and_bounded_file_listing_are_explicit(self):
        self.prs = []
        self.assertEqual(self.collect(), [])
        self.assertIn("No open pull requests", view.render(self.model))
        self.prs = [self.pr]
        self.files = self.files * 100
        self.assertIn("first 100", self.collect()[0]["note"])
        self.pr["head"]["sha"] = "invalid"
        with self.assertRaisesRegex(ValueError, "PR SHA"):
            self.collect()

    def test_default_tracked_manifest_is_read_with_fixed_git_arguments(self):
        raw = "\0".join(self.tracked) + "\0"
        with patch.object(tracking.subprocess, "check_output", return_value=raw) as read:
            tracking.collect(self.model, ROOT, request=self.request)
            self.assertEqual(read.call_args.args[0], ["git", "ls-files", "-z"])

    def test_per_record_revisions_override_the_historical_snapshot(self):
        original = copy.deepcopy(self.baseline)
        original["work_items"][0]["source_revision"] = HEAD
        with patch.object(
            dashboard,
            "read_json",
            side_effect=lambda path: (
                original if path.name == "progress.json" else json.loads(path.read_text())
            ),
        ):
            model = dashboard.build(ROOT, MAIN)
            self.assertIn(HEAD, model["workItems"][0]["sources"][0]["url"])
            original["work_items"][0]["source_revision"] = "unsafe"
            with self.assertRaisesRegex(ValueError, "source revision"):
                dashboard.build(ROOT, MAIN)
