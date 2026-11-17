"""Real PostgreSQL transaction/process-crash evidence plus controller safety regressions."""

import json
import subprocess
import tempfile
import time
import unittest
import uuid
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from experiments.postgres_store.experiment import (
    MUTATE,
    Mutation,
    PostgresLab,
    SqlRejected,
    locked_image,
)


def mutation(label="alpha", rid=1000):
    return Mutation(str(uuid.uuid4()), str(uuid.uuid4()), label, sid=f"S-1-5-21-100-200-300-{rid}")


class PostgreSQLTransactions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = PostgresLab().__enter__()

    @classmethod
    def tearDownClass(cls):
        container = cls.lab.owned()
        cls.lab.close()
        if cls.lab.docker(["inspect", container]).returncode == 0:
            raise AssertionError("Owned experiment container was not removed")

    def setUp(self):
        self.lab.query(
            "TRUNCATE babel_lab.receipts, babel_lab.audit_intent, babel_lab.journal, "
            "babel_lab.objects; UPDATE babel_lab.state SET last_usn=0; "
            "UPDATE babel_lab.actors SET active=true;"
        )

    def snapshot(self):
        return json.loads(
            self.lab.query(
                "SELECT json_build_array((SELECT last_usn FROM babel_lab.state), "
                "(SELECT count(*) FROM babel_lab.objects), "
                "(SELECT count(*) FROM babel_lab.journal), "
                "(SELECT count(*) FROM babel_lab.audit_intent), "
                "(SELECT count(*) FROM babel_lab.receipts));"
            )
        )

    def rejected(self, operation, code):
        before = self.snapshot()
        with self.assertRaises(SqlRejected) as result:
            self.lab.mutate(operation)
        self.assertEqual(result.exception.state, code)
        self.assertEqual(self.snapshot(), before)

    def test_create_rename_preserves_identity_and_couples_all_records(self):
        original = mutation()
        self.assertEqual(self.lab.mutate(original), 1)
        renamed = replace(
            original, request=str(uuid.uuid4()), operation="rename", expected=1, label="beta"
        )
        self.assertEqual(self.lab.mutate(renamed), 2)
        row = json.loads(
            self.lab.query(
                "SELECT json_build_array(object_id, synthetic_sid, "
                "synthetic_label, object_version) FROM babel_lab.objects;"
            )
        )
        self.assertEqual(row, [original.object_id, original.sid, "beta", 2])
        self.assertEqual(self.snapshot(), [2, 1, 2, 2, 2])

    def test_idempotency_returns_same_result_and_rejects_different_payload(self):
        original = mutation()
        self.assertEqual(self.lab.mutate(original), 1)
        self.assertEqual(self.lab.mutate(original), 1)
        self.assertEqual(self.snapshot(), [1, 1, 1, 1, 1])
        self.rejected(replace(original, label="different"), "22023")

    def test_collision_invalid_input_and_sql_injection_leave_no_partial_state(self):
        original = mutation()
        self.lab.mutate(original)
        for operation, code in [
            (mutation("alpha", 1001), "23505"),
            (mutation("beta", 1000), "23505"),
            (
                replace(
                    original,
                    request=str(uuid.uuid4()),
                    label="beta",
                    sid="S-1-5-21-100-200-300-1001",
                ),
                "23505",
            ),
            (mutation("x'); DROP SCHEMA babel_lab CASCADE; --", 1001), "22023"),
            (replace(mutation("beta", 1001), sid="not-a-sid"), "22023"),
            (replace(mutation("beta", 1001), operation="delete"), "22023"),
            (replace(mutation("beta", 1001), expected=-1), "22023"),
            (replace(mutation("beta", 1001), expected=1), "40001"),
            (replace(original, request=str(uuid.uuid4()), operation="rename", expected=9), "40001"),
            (replace(mutation("beta", 1001), operation="rename", expected=1), "40001"),
        ]:
            with self.subTest(code=code):
                self.rejected(operation, code)

    def test_revoked_or_unknown_test_actor_cannot_mutate_or_retrieve_receipt(self):
        original = mutation()
        self.lab.mutate(original)
        self.rejected(replace(mutation("beta", 1001), actor=str(uuid.uuid4())), "42501")
        self.lab.query("UPDATE babel_lab.actors SET active=false;")
        self.rejected(original, "42501")

    def test_unsafe_commit_settings_and_exhausted_journal_fail_atomically(self):
        original = mutation()
        with self.assertRaises(SqlRejected) as result:
            self.lab.query(
                "BEGIN; SET LOCAL synchronous_commit=off; " + MUTATE, original.variables()
            )
        self.assertEqual(result.exception.state, "55000")
        self.assertEqual(self.snapshot(), [0, 0, 0, 0, 0])
        self.lab.query("UPDATE babel_lab.state SET last_usn=9223372036854775807;")
        self.rejected(original, "54000")

    def test_identity_trigger_and_public_privileges_are_enforced(self):
        self.lab.mutate(mutation())
        for statement in (
            "UPDATE babel_lab.objects SET object_id=:'value'::uuid;",
            "UPDATE babel_lab.objects SET synthetic_sid=:'value';",
        ):
            value = str(uuid.uuid4()) if "object_id" in statement else "S-1-5-21-100-200-300-1001"
            with self.assertRaises(SqlRejected) as result:
                self.lab.query(statement, {"value": value})
            self.assertEqual(result.exception.state, "23000")
        self.lab.query(
            "CREATE ROLE babel_lab_guest NOLOGIN; "
            "GRANT USAGE ON SCHEMA babel_lab TO babel_lab_guest;"
        )
        try:
            for statement in ("SELECT * FROM babel_lab.objects;", MUTATE):
                with self.assertRaises(SqlRejected) as result:
                    self.lab.query("SET ROLE babel_lab_guest; " + statement, mutation().variables())
                self.assertEqual(result.exception.state, "42501")
        finally:
            self.lab.query("DROP OWNED BY babel_lab_guest; DROP ROLE babel_lab_guest;")

    def test_rollback_discards_state_journal_receipt_and_audit(self):
        pending = self.lab.spawn(mutation())
        self.lab.await_state(pending)
        self.assertEqual(self.snapshot(), [0, 0, 0, 0, 0])
        self.lab.finish(pending, commit=False)
        self.assertEqual(self.snapshot(), [0, 0, 0, 0, 0])

    def test_concurrent_writer_waits_for_earlier_commit(self):
        first = self.lab.spawn(mutation("alpha", 1000))
        self.lab.await_state(first)
        second = self.lab.spawn(mutation("beta", 1001), commit=True)
        self.lab.await_state(second, blocked=True)
        self.assertEqual(self.snapshot(), [0, 0, 0, 0, 0])
        self.lab.finish(first)
        second.process.communicate(timeout=10)
        self.lab.sessions.remove(second)
        self.assertEqual(second.process.returncode, 0)
        self.assertEqual(
            self.lab.query(
                "SELECT string_agg(local_usn::text, ',' ORDER BY local_usn) FROM babel_lab.journal;"
            ),
            "1,2",
        )
        self.assertEqual(self.snapshot(), [2, 2, 2, 2, 2])

    def test_concurrent_writer_after_rollback_has_no_committed_gap(self):
        first = self.lab.spawn(mutation("alpha", 1000))
        self.lab.await_state(first)
        second = self.lab.spawn(mutation("beta", 1001), commit=True)
        self.lab.await_state(second, blocked=True)
        self.lab.finish(first, commit=False)
        second.process.communicate(timeout=10)
        self.lab.sessions.remove(second)
        self.assertEqual(second.process.returncode, 0)
        self.assertEqual(self.snapshot(), [1, 1, 1, 1, 1])

    def test_kill_before_commit_recovers_old_complete_state(self):
        pending = self.lab.spawn(mutation())
        self.lab.await_state(pending)
        self.lab.crash_restart()
        pending.process.communicate(timeout=10)
        self.lab.sessions.remove(pending)
        self.assertEqual(self.snapshot(), [0, 0, 0, 0, 0])

    def test_committed_result_survives_kill_and_retry_after_discarded_reply(self):
        original = mutation()
        pending = self.lab.spawn(original, commit=True)
        deadline = time.monotonic() + 10
        while self.snapshot() != [1, 1, 1, 1, 1]:
            if time.monotonic() >= deadline:
                self.fail("Commit was not visible before the crash")
            time.sleep(0.05)
        # Do not consume the command's result; emulate a client that cannot determine its outcome.
        self.lab.crash_restart()
        pending.process.communicate(timeout=10)
        self.lab.sessions.remove(pending)
        self.assertEqual(self.lab.mutate(original), 1)
        self.assertEqual(self.snapshot(), [1, 1, 1, 1, 1])

    def test_container_is_isolated_and_has_no_published_ports_or_host_mounts(self):
        result = self.lab.docker(["inspect", "--format", "{{json .HostConfig}}", self.lab.owned()])
        config = json.loads(result.stdout)
        self.assertEqual(config["NetworkMode"], "none")
        self.assertFalse(config["Privileged"])
        self.assertTrue(config["ReadonlyRootfs"])
        self.assertFalse(config["Binds"])
        self.assertFalse(config["PortBindings"])
        self.assertEqual(config["Memory"], 512 * 1024 * 1024)
        self.assertEqual(self.lab.query("SHOW listen_addresses;"), "")


class ControllerSafety(unittest.TestCase):
    def setUp(self):
        self.lab = PostgresLab()

    def test_mutable_or_executable_image_manifests_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "Dockerfile"
            for content in (
                "FROM postgres:18-bookworm",
                "FROM other/image@sha256:" + "a" * 64,
                "FROM postgres:18-bookworm@sha256:" + "a" * 64 + "\nRUN malicious",
            ):
                manifest.write_text(content)
                with self.subTest(content=content), self.assertRaises(ValueError):
                    locked_image(manifest)

    def test_only_owned_full_container_ids_can_be_targeted(self):
        for value in ("", "postgres", "--all", "abc\n"):
            self.lab.container = value
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                self.lab.owned()

    def test_variables_are_bounded_and_arguments_never_use_a_shell(self):
        self.lab.container = "a" * 64
        for variables in ({"invalid-key": "x"}, {"name": "x" * 513}):
            with self.assertRaises(ValueError):
                self.lab.command(variables, "babel-test")
        result = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with patch(
            "experiments.postgres_store.experiment.subprocess.run", return_value=result
        ) as run:
            self.lab.docker(["inspect", self.lab.container])
            self.assertEqual(run.call_args.args[0][:2], ["docker", "inspect"])
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_failures_export_only_safe_sqlstate_or_static_diagnostics(self):
        self.lab.container = "a" * 64
        for stderr, kind in (
            ("unexpected private details", RuntimeError),
            ("ERROR: 22023 private details", SqlRejected),
        ):
            result = subprocess.CompletedProcess([], 1, stdout="private details", stderr=stderr)
            with (
                patch.object(self.lab, "docker", return_value=result),
                self.assertRaises(kind) as error,
            ):
                self.lab.query("SELECT 1;")
            self.assertNotIn("private details", str(error.exception))

    def test_missing_pinned_image_stops_before_container_creation(self):
        result = subprocess.CompletedProcess([], 1, stdout="", stderr="")
        with patch.object(self.lab, "docker", return_value=result) as docker:
            with self.assertRaisesRegex(RuntimeError, "image unavailable"):
                self.lab.__enter__()
            self.assertEqual(docker.call_count, 2)
        self.assertEqual(self.lab.container, "")

    def test_failed_creation_does_not_target_a_preexisting_container(self):
        success = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        failure = subprocess.CompletedProcess(
            [], 1, stdout="private details", stderr="private details"
        )
        with patch.object(self.lab, "docker", side_effect=[success, failure]):
            with self.assertRaisesRegex(RuntimeError, "Unable to create"):
                self.lab.__enter__()
        self.assertEqual(self.lab.container, "")

    def test_unsupported_server_version_cleans_up_the_owned_container(self):
        success = subprocess.CompletedProcess([], 0, stdout="a" * 64, stderr="")
        with (
            patch.object(self.lab, "docker", return_value=success) as docker,
            patch.object(self.lab, "wait_ready"),
            patch.object(self.lab, "query", return_value="170000"),
        ):
            with self.assertRaisesRegex(RuntimeError, "PostgreSQL 18"):
                self.lab.__enter__()
            self.assertEqual(docker.call_args.args[0], ["rm", "--force", "--volumes", "a" * 64])

    def test_readiness_and_transaction_barriers_have_deadlines(self):
        self.lab.container = "a" * 64
        with patch("experiments.postgres_store.experiment.time.monotonic", side_effect=[0, 30]):
            with self.assertRaisesRegex(RuntimeError, "did not become ready"):
                self.lab.wait_ready()

    def test_failed_crash_or_cleanup_is_not_reported_as_success(self):
        self.lab.container = "a" * 64
        failure = subprocess.CompletedProcess([], 1, stdout="", stderr="")
        with patch.object(self.lab, "docker", return_value=failure):
            with self.assertRaisesRegex(RuntimeError, "crash/restart failed"):
                self.lab.crash_restart()
            with self.assertRaisesRegex(RuntimeError, "cleanup failed"):
                self.lab.close()
