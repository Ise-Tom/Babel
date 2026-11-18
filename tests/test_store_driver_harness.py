"""Harness regressions supplement, rather than replace, the real Rust/database job."""

import copy
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from scripts import qualify_store_driver as harness


def result(code=0, stdout="", stderr=""):
    return subprocess.CompletedProcess([], code, stdout=stdout, stderr=stderr)


class DriverHarness(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.socket = Path(self.temp.name) / "socket"
        self.socket.mkdir()
        self.lab = Mock()
        self.lab.socket_directory = self.socket
        self.lab.owned.return_value = "a" * 64
        self.info = {
            "HostConfig": {
                "NetworkMode": "none",
                "PortBindings": {},
                "Privileged": False,
                "ReadonlyRootfs": True,
                "Memory": 512 * 1024 * 1024,
                "NanoCpus": 1_000_000_000,
                "PidsLimit": 128,
                "SecurityOpt": ["no-new-privileges"],
            },
            "Mounts": [
                {"Type": "bind", "Source": str(self.socket), "Destination": "/babel-driver-socket"}
            ],
        }

    def test_case_accounting_rejects_empty_missing_duplicates_and_false_success(self):
        output = "\n".join(f"test {name} ... ok" for name in harness.CASES)
        self.assertEqual(harness.case_results(output), sorted(harness.CASES))
        for invalid in (
            "",
            output.splitlines()[0],
            output + "\n" + output.splitlines()[0],
            output.replace("... ok", "... ignored", 1),
        ):
            with (
                self.subTest(output=invalid[:40]),
                self.assertRaisesRegex(RuntimeError, "inventory"),
            ):
                harness.case_results(invalid)

    def test_observed_isolation_rejects_extra_mounts_network_or_privilege(self):
        def check(info):
            self.lab.docker.return_value = result(stdout=json.dumps([info]))
            self.lab.query.return_value = ""
            harness.isolation(self.lab)

        check(self.info)
        for key, value in [
            ("NetworkMode", "host"),
            ("PortBindings", {"5432/tcp": []}),
            ("Privileged", True),
            ("ReadonlyRootfs", False),
            ("Memory", 0),
            ("NanoCpus", 0),
            ("PidsLimit", 0),
            ("SecurityOpt", []),
        ]:
            changed = copy.deepcopy(self.info)
            changed["HostConfig"][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, "isolation mismatch"):
                check(changed)
        for change in ({"Source": "/"}, {"Destination": "/var/lib/postgresql"}):
            changed = copy.deepcopy(self.info)
            changed["Mounts"][0].update(change)
            with self.assertRaisesRegex(RuntimeError, "isolation mismatch"):
                check(changed)
        changed = copy.deepcopy(self.info)
        changed["Mounts"].append(changed["Mounts"][0])
        with self.assertRaisesRegex(RuntimeError, "isolation mismatch"):
            check(changed)
        self.lab.docker.return_value = result(1)
        with self.assertRaisesRegex(RuntimeError, "unavailable"):
            harness.isolation(self.lab)
        self.lab.docker.return_value = result(stdout=json.dumps([self.info]))
        self.lab.query.return_value = "localhost"
        with self.assertRaisesRegex(RuntimeError, "isolation mismatch"):
            harness.isolation(self.lab)
        self.lab.query.return_value = ""
        Path(self.temp.name).chmod(0o755)
        with self.assertRaisesRegex(RuntimeError, "isolation mismatch"):
            harness.isolation(self.lab)

    def prepare_auth(self):
        self.lab.query.side_effect = lambda sql, *_: (
            "/var/lib/postgresql/18/docker/pg_hba.conf" if sql == "SHOW hba_file;" else "t"
        )
        self.lab.docker.side_effect = [
            result(stdout="local all all trust\n"),
            result(),
            result(2, stderr="no password supplied"),
        ]

    def test_auth_setup_uses_quoted_parameters_and_observes_activation(self):
        self.prepare_auth()
        harness.configure(self.lab, "synthetic")
        self.assertEqual(
            self.lab.query.call_args_list[0].args,
            ("CREATE ROLE babel_driver_lab LOGIN PASSWORD :'password';", {"password": "synthetic"}),
        )
        self.assertTrue(
            self.lab.docker.call_args_list[1]
            .kwargs["data"]
            .startswith("local all babel_driver_lab scram-sha-256\n")
        )

    def test_failed_auth_configuration_never_reports_ready(self):
        for outputs in ([result(1)], [result(), result(1)], [result(), result(), result()]):
            self.prepare_auth()
            self.lab.docker.side_effect = outputs
            with (
                patch.object(harness.time, "monotonic", side_effect=[0, 6]),
                self.assertRaises(RuntimeError),
            ):
                harness.configure(self.lab, "synthetic")
        self.prepare_auth()
        self.lab.query.side_effect = lambda sql, *_: (
            "/etc/private" if sql == "SHOW hba_file;" else "t"
        )
        with self.assertRaisesRegex(RuntimeError, "configuration path"):
            harness.configure(self.lab, "synthetic")
        self.prepare_auth()
        self.lab.query.side_effect = lambda sql, *_: (
            "/var/lib/postgresql/x" if sql == "SHOW hba_file;" else "f"
        )
        with self.assertRaisesRegex(RuntimeError, "configuration failed"):
            harness.configure(self.lab, "synthetic")

    def qualify(self, *, coverage=False, cargo=None, cleanup=True):
        shutil.rmtree(Path(self.temp.name) / "driver-control", ignore_errors=True)
        self.lab.__enter__ = Mock(return_value=self.lab)
        self.lab.__exit__ = Mock(
            side_effect=lambda *_: self.socket.rmdir() if cleanup and self.socket.exists() else None
        )
        self.lab.query.return_value = "18.7"
        self.lab.docker.return_value = result(1)
        output = "\n".join(f"test {name} ... ok" for name in harness.CASES) + "\nsynthetic-secret"
        with (
            patch.object(harness, "PostgresLab", return_value=self.lab),
            patch.object(harness, "configure"),
            patch.object(harness, "isolation"),
            patch.object(harness.secrets, "token_hex", return_value="synthetic-secret"),
            patch.object(
                harness,
                "run_owned",
                side_effect=cargo if isinstance(cargo, BaseException) else None,
                return_value=cargo or result(stdout=output),
            ) as run,
            redirect_stdout(io.StringIO()) as captured,
        ):
            report = harness.qualify(coverage=coverage)
            self.assertNotIn("synthetic-secret", captured.getvalue())
            self.assertNotIn("synthetic-secret", run.call_args.args[0])
            self.assertEqual(
                run.call_args.kwargs["env"]["BABEL_DRIVER_PASSWORD"], "synthetic-secret"
            )
            return report, run.call_args.args[0]

    def test_command_uses_owned_environment_and_reports_only_all_passed_cases(self):
        for coverage in (False, True):
            self.socket.mkdir(exist_ok=True)
            report, command = self.qualify(coverage=coverage)
            self.assertTrue(report["cleanup_verified"])
            self.assertTrue(report["fixture_isolation_verified"])
            self.assertEqual(report["passed"], len(harness.CASES))
            self.assertEqual(command[:2], ["cargo", "llvm-cov" if coverage else "test"])
            self.assertEqual(command[-1], "--test-threads=1")

    def test_process_failure_timeout_and_remaining_socket_fail_closed(self):
        for cargo in (OSError("private"), subprocess.TimeoutExpired(["private"], 1), result(1)):
            self.socket.mkdir(exist_ok=True)
            with self.assertRaises(RuntimeError) as error:
                self.qualify(cargo=cargo)
            self.assertNotIn("private", str(error.exception))
        self.socket.mkdir(exist_ok=True)
        with self.assertRaisesRegex(RuntimeError, "cleanup incomplete"):
            self.qualify(cleanup=False)

    def test_owned_process_coordinates_actual_checkpoint_calls_before_reporting_success(self):
        control = Path(self.temp.name) / "coordinator"
        control.mkdir()
        process = Mock(pid=76543, returncode=0)
        process.poll.return_value = 0
        calls = 0

        def communicate(*_, **__):
            nonlocal calls
            calls += 1
            if calls == 1:
                for checkpoint in harness.RECOVERY_CHECKPOINTS:
                    (control / f"{checkpoint}.ready").write_text("ready")
                raise subprocess.TimeoutExpired(["cargo"], 0.2)
            return "complete", ""

        process.communicate.side_effect = communicate
        with patch.object(harness.subprocess, "Popen", return_value=process) as start:
            finished = harness.run_owned(
                ["cargo", "test"], cwd=Path(self.temp.name), env={}, lab=self.lab, control=control
            )
        self.assertEqual(finished.returncode, 0)
        self.assertEqual(self.lab.crash_restart.call_count, 2)
        self.assertTrue(start.call_args.kwargs["start_new_session"])
        for checkpoint in harness.RECOVERY_CHECKPOINTS:
            self.assertEqual((control / f"{checkpoint}.done").read_text(), "restarted")

    def test_owned_process_rejects_missing_recovery_and_kills_only_its_group_on_timeout(self):
        control = Path(self.temp.name) / "coordinator"
        control.mkdir()
        process = Mock(pid=76543, returncode=0)
        process.communicate.return_value = ("", "")
        process.poll.return_value = 0
        with patch.object(harness.subprocess, "Popen", return_value=process):
            with self.assertRaisesRegex(RuntimeError, "checkpoints incomplete"):
                harness.run_owned(["cargo"], cwd=control, env={}, lab=self.lab, control=control)
        process.poll.return_value = None
        with (
            patch.object(harness.subprocess, "Popen", return_value=process),
            patch.object(harness.time, "monotonic", side_effect=[0, 421]),
            patch.object(harness.os, "killpg") as kill,
        ):
            with self.assertRaisesRegex(RuntimeError, "deadline"):
                harness.run_owned(["cargo"], cwd=control, env={}, lab=self.lab, control=control)
        kill.assert_called_once_with(76543, harness.signal.SIGKILL)
        process.communicate.assert_called_with(timeout=10)
