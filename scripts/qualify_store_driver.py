"""Qualify a Rust driver only against an owned synthetic PostgreSQL container."""

import argparse
import json
import os
import re
import secrets
import subprocess  # nosec B404
import time
from pathlib import Path
from typing import Any

from experiments.postgres_store.experiment import IMAGE, PostgresLab

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "invalid_configuration_and_unavailable_socket_are_redacted",
    "scram_authentication_and_least_privilege_are_real",
    "parameter_binding_handles_literals_null_and_binary_without_sql_execution",
    "commit_and_explicit_or_drop_rollback_preserve_coupled_state",
    "caught_statement_failure_never_becomes_successful_commit",
    "deferred_commit_failure_never_acknowledges_success",
    "lock_timeout_is_bounded_and_session_can_be_reused",
    "serialization_failure_is_retryable_without_partial_commit",
    "server_statement_timeout_cancels_and_preserves_connection",
    "explicit_cancel_reaches_the_active_query",
    "client_deadline_discards_session_when_server_timeout_is_absent",
    "unresponsive_unix_peer_has_a_connection_deadline",
    "unsafe_session_durability_is_rejected",
    "lost_connection_during_transaction_has_unknown_commit_outcome",
    "transaction_deadline_prevents_commit_and_session_reuse",
    "raw_driver_aborted_commit_requires_application_failure_tracking",
}


def isolation(lab: PostgresLab) -> None:
    result = lab.docker(["inspect", lab.owned()])
    if result.returncode:
        raise RuntimeError("Owned fixture isolation unavailable")
    info = json.loads(result.stdout)[0]
    host = info["HostConfig"]
    mounts = [m for m in info["Mounts"] if m["Type"] == "bind"]
    socket = lab.socket_directory
    if (
        socket is None
        or len(mounts) != 1
        or mounts[0]["Source"] != str(socket)
        or mounts[0]["Destination"] != "/babel-driver-socket"
        or socket.parent.stat().st_mode & 0o777 != 0o700
        or host["NetworkMode"] != "none"
        or host.get("PortBindings")
        or host["Privileged"]
        or not host["ReadonlyRootfs"]
        or host["Memory"] != 512 * 1024 * 1024
        or host["NanoCpus"] != 1_000_000_000
        or host["PidsLimit"] != 128
        or "no-new-privileges" not in host["SecurityOpt"]
        or lab.query("SHOW listen_addresses;")
    ):
        raise RuntimeError("Owned fixture isolation mismatch")


def configure(lab: PostgresLab, password: str) -> None:
    lab.query("CREATE ROLE babel_driver_lab LOGIN PASSWORD :'password';", {"password": password})
    lab.query((ROOT / "native/babel-store-driver-lab/tests/fixture.sql").read_text())
    hba = lab.query("SHOW hba_file;")
    if not hba.startswith("/var/lib/postgresql/") or ".." in Path(hba).parts:
        raise RuntimeError("Unexpected owned lab configuration path")
    original = lab.docker(["exec", "--user", "postgres", lab.owned(), "cat", hba])
    if original.returncode:
        raise RuntimeError("Owned lab authentication configuration unavailable")
    rule = "local all babel_driver_lab scram-sha-256\n"
    result = lab.docker(
        ["exec", "--interactive", "--user", "postgres", lab.owned(), "tee", hba],
        data=rule + original.stdout,
    )
    if result.returncode or lab.query("SELECT pg_reload_conf();") != "t":
        raise RuntimeError("Owned SCRAM configuration failed")
    # Reload is asynchronous. Prove passwordless access has stopped before testing.
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        probe = lab.docker(
            [
                "exec",
                "--user",
                "postgres",
                lab.owned(),
                "psql",
                "--no-psqlrc",
                "--no-password",
                "-h",
                "/babel-driver-socket",
                "-U",
                "babel_driver_lab",
                "-d",
                "babel_store_lab",
                "-qAt",
                "-c",
                "SELECT 1;",
            ]
        )
        if probe.returncode and "no password supplied" in probe.stderr:
            return
        time.sleep(0.02)
    raise RuntimeError("Owned SCRAM authentication did not activate")


def case_results(output: str) -> list[str]:
    passed = re.findall(r"^test ([a-z_]+) \.\.\. ok$", output, flags=re.MULTILINE)
    if len(passed) != len(set(passed)) or set(passed) != CASES:
        raise RuntimeError("Driver case inventory incomplete or duplicated")
    return sorted(passed)


def qualify(*, coverage: bool = False) -> dict[str, Any]:
    password = secrets.token_hex(32)
    with PostgresLab(share_socket=True) as lab:
        isolation(lab)
        configure(lab, password)
        container = lab.owned()
        socket = lab.socket_directory
        if socket is None:
            raise RuntimeError("Owned private socket missing")
        version = lab.query("SHOW server_version;")
        environment = dict(
            os.environ, BABEL_DRIVER_SOCKET=str(socket), BABEL_DRIVER_PASSWORD=password
        )
        command = ["cargo", "llvm-cov" if coverage else "test"]
        command += [
            "--locked",
            "--package",
            "babel-store-driver-lab",
            "--features",
            "qualification",
            "--test",
            "database",
        ]
        if coverage:
            command += [
                "--ignore-filename-regex",
                "/tests/",
                "--fail-under-lines",
                "90",
                "--lcov",
                "--output-path",
                "reports/store-driver-coverage.lcov",
            ]
        command += ["--", "--test-threads=1"]
        try:
            # Fixed Cargo qualification argv; synthetic credentials are in its environment.
            result = subprocess.run(  # nosec B603
                command,
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                timeout=420,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise RuntimeError("Rust driver qualification unavailable or timed out") from None
        output = (result.stdout + result.stderr).replace(password, "[redacted]")
        print(output[:262144])
        if result.returncode:
            raise RuntimeError("Rust driver qualification failed")
        passed = case_results(output)
    if socket.exists() or lab.docker(["inspect", container]).returncode == 0:
        raise RuntimeError("Owned driver fixture cleanup incomplete")
    return {
        "scope": "Synthetic PostgreSQL driver candidate; no native directory/AD conformance",
        "source_revision": os.environ.get("GITHUB_SHA"),
        "image": IMAGE,
        "postgresql": version,
        "cases": passed,
        "passed": len(passed),
        "failed": 0,
        "unrun": 0,
        "transport": "private Unix socket; SCRAM role; no network/ports",
        "cleanup_verified": True,
        "fixture_isolation_verified": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage", action="store_true")
    args = parser.parse_args()
    try:
        report = qualify(coverage=args.coverage)
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(f"Driver qualification rejected: {error}") from None
    directory = ROOT / "reports"
    directory.mkdir(exist_ok=True)
    (directory / "store-driver-qualification.json").write_text(json.dumps(report, indent=2) + "\n")
    print("All owned driver qualification cases and cleanup verified")
