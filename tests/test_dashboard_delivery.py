"""Persistent reporting must preserve privacy, source history, and literal authored text."""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_dashboard as model  # noqa: E402
import publish_dashboard as delivery  # noqa: E402
import render_dashboard as view  # noqa: E402

REVISION = "a" * 40


class PersistentReport(unittest.TestCase):
    def setUp(self):
        self.data = model.build(ROOT, REVISION)

    def test_report_has_every_phase_substep_feature_and_explanation(self):
        report = view.render(self.data)
        for phase in self.data["phases"]:
            self.assertIn(f"## Phase {phase['id']:02}\n", report)
            for step in phase["steps"]:
                self.assertIn(f"### {step['id']}\n", report)
        for feature in self.data["features"]:
            self.assertIn(view.escaped(feature["title"]), report)
            self.assertIn(view.escaped(feature["verification"]), report)
        for item in self.data["workItems"]:
            for field in ("how", "verification", "limitations"):
                self.assertIn(view.escaped(item[field]), report)
        for problem in self.data["problems"]:
            self.assertIn(view.escaped(problem["detail"]), report)
        self.assertIn("0 phases accepted", report)
        self.assertIn("Recorded implementation evidence", report)
        self.assertIn("separate revisions", report)
        self.assertEqual(report.count("<details>"), 18)
        self.assertEqual(report.count("</details>"), 18)
        self.assertEqual(report, view.render(self.data))

    def test_preview_cannot_claim_main_publication(self):
        report = view.render(self.data, preview=True)
        self.assertIn("Development preview", report)
        self.assertIn("after the dashboard PR is merged", report)
        self.assertNotIn("Updated automatically after the full CI gate", report)

    def test_authored_markup_is_literal_and_unsafe_links_are_rejected(self):
        payload = "<script>alert(1)</script> ![image](https://evil.example) | **done**"
        self.data["phases"][0]["steps"][0]["note"] = payload
        report = view.render(self.data)
        self.assertNotIn("<script>", report)
        self.assertNotIn("![image]", report)
        self.assertIn("&lt;script&gt;", report)
        self.assertIn(r"\| \*\*done\*\*", report)
        for url in (
            "javascript:alert(1)",
            "https://github.com.evil/Ise-Tom/Babel/x",
            "https://evil.example",
            "https://github.com/other/repository/x",
        ):
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "within the HTTPS"):
                view.link("text", url)

    def test_validated_acceptance_is_displayed(self):
        self.data["phases"][0]["steps"][0]["acceptance"] = {
            "reviewer": "Test reviewer",
            "date": "2026-11-17",
            "evidence": "Fixture only",
        }
        self.assertIn("Test reviewer", view.render(self.data))
        self.data["buildRevision"] = "not-a-commit"
        with self.assertRaisesRegex(ValueError, "source revision"):
            view.render(self.data)


class FakeGitHub:
    def __init__(self, *, existing=False, same_tree=False):
        self.existing = existing
        self.same_tree = same_tree
        self.calls = []
        self.repository = {"private": True, "full_name": "Ise-Tom/Babel"}
        self.main_revision = REVISION
        self.entries = [{"path": "README.md", "type": "blob"}]
        self.fail_update = False

    def __call__(self, method, path, payload=None):
        self.calls.append((method, path, copy.deepcopy(payload)))
        if path == "":
            return self.repository
        if path == "branches/main":
            return {"commit": {"sha": self.main_revision}}
        if path.startswith("git/matching-refs"):
            refs = [{"ref": "refs/heads/dashboard-live-extra", "object": {"sha": "other"}}]
            return refs + (
                [{"ref": "refs/heads/dashboard-live", "object": {"sha": "old"}}]
                if self.existing
                else []
            )
        if path == "git/commits/old":
            return {"tree": {"sha": "same" if self.same_tree else "previous"}}
        if method == "GET" and path.startswith("git/trees/"):
            return {"tree": self.entries, "truncated": False}
        if path == "git/blobs":
            return {"sha": "blob"}
        if path == "git/trees":
            return {"sha": "same" if self.same_tree else "tree"}
        if path == "git/commits":
            return {"sha": "new"}
        if self.fail_update:
            raise RuntimeError("Concurrent update rejected")
        return {}


class PrivatePublisher(unittest.TestCase):
    def test_first_publication_has_a_readme_only_root_commit_on_report_branch(self):
        request = FakeGitHub()
        self.assertIn(view.LIVE_URL, delivery.publish("report", REVISION, request=request))
        commits = [body for method, path, body in request.calls if path == "git/commits"]
        self.assertEqual(commits[0]["parents"], [])
        self.assertEqual(
            request.calls[-1],
            ("POST", "git/refs", {"ref": "refs/heads/dashboard-live", "sha": "new"}),
        )
        trees = [body for method, path, body in request.calls if path == "git/trees"]
        self.assertEqual(trees[0]["tree"][0]["path"], "README.md")
        self.assertNotIn("base_tree", trees[0])

    def test_updates_are_fast_forward_only_and_unchanged_reports_do_not_commit(self):
        request = FakeGitHub(existing=True)
        delivery.publish("report", REVISION, request=request)
        self.assertEqual(
            request.calls[-1],
            ("PATCH", "git/refs/heads/dashboard-live", {"sha": "new", "force": False}),
        )
        request = FakeGitHub(existing=True, same_tree=True)
        self.assertIn("already current", delivery.publish("report", REVISION, request=request))
        self.assertFalse(any(path == "git/commits" for method, path, body in request.calls))

    def test_public_or_other_repositories_are_never_published(self):
        for repository in (
            {"private": False, "full_name": "Ise-Tom/Babel"},
            {"private": True, "full_name": "other/repository"},
        ):
            request = FakeGitHub()
            request.repository = repository
            with self.assertRaisesRegex(ValueError, "Private project"):
                delivery.publish("report", REVISION, request=request)
            self.assertTrue(all(method == "GET" for method, path, body in request.calls))

    def test_older_main_run_preserves_the_report_and_preview_is_labeled(self):
        request = FakeGitHub()
        request.main_revision = "b" * 40
        self.assertIn("Skipped", delivery.publish("report", REVISION, request=request))
        self.assertTrue(all(method == "GET" for method, path, body in request.calls))
        delivery.publish("preview", REVISION, preview=True, request=request)
        commits = [body for method, path, body in request.calls if path == "git/commits"]
        self.assertIn("preview", commits[0]["message"])

    def test_other_branch_files_and_concurrent_edits_are_preserved(self):
        request = FakeGitHub(existing=True)
        request.entries.append({"path": "user-file.txt", "type": "blob"})
        with self.assertRaisesRegex(ValueError, "unexpected files"):
            delivery.publish("report", REVISION, request=request)
        self.assertTrue(all(method == "GET" for method, path, body in request.calls))
        request = FakeGitHub(existing=True)
        request.fail_update = True
        with self.assertRaisesRegex(RuntimeError, "Concurrent update"):
            delivery.publish("report", REVISION, request=request)
        self.assertEqual(request.calls[-1][2]["force"], False)
        with self.assertRaisesRegex(ValueError, "source revision"):
            delivery.publish("report", "bad", request=request)

    def test_api_uses_structured_stdin_fixed_destination_and_no_secret_diagnostics(self):
        result = subprocess.CompletedProcess([], 0, stdout='{"sha":"ok"}', stderr="")
        with patch.object(delivery.subprocess, "run", return_value=result) as run:
            self.assertEqual(
                delivery.api("POST", "git/refs", {"text": "`$(literal)`\n"}), {"sha": "ok"}
            )
            call = run.call_args
            self.assertEqual(
                call.args[0][:7],
                [
                    "gh",
                    "api",
                    "--hostname",
                    "github.com",
                    "--method",
                    "POST",
                    "repos/Ise-Tom/Babel/git/refs",
                ],
            )
            self.assertEqual(json.loads(call.kwargs["input"]), {"text": "`$(literal)`\n"})
            self.assertNotIn("shell", call.kwargs)
        result = subprocess.CompletedProcess([], 1, stdout="private content", stderr="secret-value")
        with patch.object(delivery.subprocess, "run", return_value=result):
            with self.assertRaisesRegex(RuntimeError, "Existing report retained") as error:
                delivery.api("GET", "git/refs")
            self.assertNotIn("secret-value", str(error.exception))
