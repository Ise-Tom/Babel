"""Own an isolated synthetic PostgreSQL experiment; never connect to an external database."""

import os
import re
import secrets
import subprocess  # nosec B404
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Self


def locked_image(manifest: Path) -> str:
    lines = [
        line for line in manifest.read_text().splitlines() if line and not line.startswith("#")
    ]
    if len(lines) != 1 or not re.fullmatch(
        r"FROM postgres:18-bookworm@sha256:[a-f0-9]{64}", lines[0]
    ):
        raise ValueError("Only a digest-pinned official PostgreSQL 18 dependency is allowed")
    return lines[0].removeprefix("FROM ")


IMAGE = locked_image(Path(__file__).with_name("Dockerfile"))
ACTOR = "00000000-0000-4000-8000-000000000001"
SCHEMA = Path(__file__).with_name("schema.sql")
MUTATE = (
    "SELECT babel_lab.mutate(:'actor'::uuid, :'request'::uuid, :'operation', "
    ":'object_id'::uuid, :'sid', :'label', :'expected'::bigint);"
)


class SqlRejected(RuntimeError):
    def __init__(self, state: str) -> None:
        self.state = state
        super().__init__(f"Synthetic operation rejected ({state})")


@dataclass(frozen=True)
class Mutation:
    request: str
    object_id: str
    label: str
    sid: str = "S-1-5-21-100-200-300-1000"
    operation: str = "create"
    expected: int = 0
    actor: str = ACTOR

    def variables(self) -> dict[str, str]:
        return {
            "request": self.request,
            "object_id": self.object_id,
            "label": self.label,
            "sid": self.sid,
            "operation": self.operation,
            "expected": str(self.expected),
            "actor": self.actor,
        }


@dataclass
class Session:
    name: str
    process: subprocess.Popen[str]


class PostgresLab:
    def __init__(self) -> None:
        self.container = ""
        self.sessions: list[Session] = []

    @staticmethod
    def docker(
        args: list[str],
        *,
        data: str | None = None,
        environment: dict[str, str] | None = None,
        timeout: int = 30,
    ) -> subprocess.CompletedProcess[str]:
        try:
            # Fixed Docker command, argv only, never a shell.
            return subprocess.run(  # nosec B603, B607
                ["docker", *args],
                input=data,
                capture_output=True,
                text=True,
                env=environment,
                timeout=timeout,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise RuntimeError("Isolated container command unavailable or timed out") from None

    def owned(self) -> str:
        if not re.fullmatch(r"[a-f0-9]{64}", self.container):
            raise RuntimeError("No owned experiment container")
        return self.container

    def __enter__(self) -> Self:
        if self.docker(["image", "inspect", IMAGE]).returncode:
            if self.docker(["pull", IMAGE], timeout=180).returncode:
                raise RuntimeError("Pinned PostgreSQL image unavailable")
        environment = dict(os.environ, POSTGRES_PASSWORD=secrets.token_hex(32))
        result = self.docker(
            [
                "run",
                "--detach",
                "--network",
                "none",
                "--memory",
                "512m",
                "--cpus",
                "1",
                "--pids-limit",
                "128",
                "--security-opt",
                "no-new-privileges",
                "--read-only",
                "--tmpfs",
                "/var/run/postgresql:rw,nosuid,noexec,size=8m",
                "--log-opt",
                "max-size=1m",
                "--log-opt",
                "max-file=1",
                "-e",
                "POSTGRES_PASSWORD",
                "-e",
                "POSTGRES_DB=babel_store_lab",
                "-e",
                "TMPDIR=/var/run/postgresql",
                IMAGE,
                "postgres",
                "-c",
                "listen_addresses=",
                "-c",
                "max_connections=12",
                "-c",
                "shared_buffers=32MB",
                "-c",
                "fsync=on",
                "-c",
                "full_page_writes=on",
                "-c",
                "synchronous_commit=on",
            ],
            environment=environment,
        )
        if result.returncode:
            raise RuntimeError("Unable to create isolated experiment container")
        self.container = result.stdout.strip()
        try:
            self.wait_ready()
            if int(self.query("SHOW server_version_num;")) // 10000 != 18:
                raise RuntimeError("PostgreSQL 18 required")
            self.query(SCHEMA.read_text())
            return self
        except BaseException:
            self.close()
            raise

    def wait_ready(self) -> None:
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            # The image's temporary initialization server is not the final ready server.
            main = self.docker(["exec", self.owned(), "cat", "/proc/1/comm"])
            if main.returncode or main.stdout.strip() != "postgres":
                time.sleep(0.1)
                continue
            result = self.docker(
                [
                    "exec",
                    "--user",
                    "postgres",
                    self.owned(),
                    "pg_isready",
                    "-q",
                    "-h",
                    "/var/run/postgresql",
                    "-d",
                    "babel_store_lab",
                    "-t",
                    "1",
                ]
            )
            if result.returncode == 0:
                return
            time.sleep(0.1)
        raise RuntimeError("Experiment database did not become ready")

    def command(self, variables: dict[str, str], application: str) -> list[str]:
        args = [
            "exec",
            "--interactive",
            "--user",
            "postgres",
            "-e",
            f"PGAPPNAME={application}",
            self.owned(),
            "psql",
            "--no-psqlrc",
            "--no-password",
            "-qAt",
            "-h",
            "/var/run/postgresql",
            "-U",
            "postgres",
            "-d",
            "babel_store_lab",
            "-v",
            "ON_ERROR_STOP=1",
            "-v",
            "VERBOSITY=sqlstate",
            "-v",
            "SHOW_CONTEXT=never",
        ]
        for key, value in variables.items():
            if not re.fullmatch(r"[a-z_]+", key) or len(value) > 512:
                raise ValueError("Invalid experiment SQL variable")
            args.extend(["-v", f"{key}={value}"])
        return args

    def query(self, sql: str, variables: dict[str, str] | None = None) -> str:
        result = self.docker(self.command(variables or {}, "babel-lab-query"), data=sql)
        if result.returncode:
            match = re.search(r"ERROR:\s+([0-9A-Z]{5})\b", result.stderr)
            if match:
                raise SqlRejected(match[1])
            raise RuntimeError("Experiment query failed; no SQL or diagnostics exported")
        return result.stdout.strip()

    def mutate(self, mutation: Mutation) -> int:
        return int(self.query(MUTATE, mutation.variables()))

    def spawn(self, mutation: Mutation, *, commit: bool = False) -> Session:
        name = "babel-lab-" + uuid.uuid4().hex
        # Fixed Docker/psql command with quoted SQL variables, never a shell.
        process = subprocess.Popen(  # nosec B603, B607
            ["docker", *self.command(mutation.variables(), name)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        session = Session(name, process)
        self.sessions.append(session)
        if process.stdin is None:
            raise RuntimeError("Experiment session has no input pipe")
        process.stdin.write("BEGIN;\n" + MUTATE + ("\nCOMMIT;\n" if commit else "\n"))
        process.stdin.flush()
        return session

    def await_state(self, session: Session, *, blocked: bool = False) -> None:
        statement = (
            "SELECT count(*) FROM pg_stat_activity WHERE application_name=:'app' "
            "AND wait_event_type='Lock';"
            if blocked
            else "SELECT count(*) FROM pg_stat_activity WHERE application_name=:'app' "
            "AND state='idle in transaction';"
        )
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if session.process.poll() is not None:
                raise RuntimeError("Experiment session exited before its transaction barrier")
            if self.query(statement, {"app": session.name}) == "1":
                return
            time.sleep(0.05)
        raise RuntimeError("Experiment transaction barrier timed out")

    def finish(self, session: Session, *, commit: bool = True) -> None:
        self.drain(session, "COMMIT;\n" if commit else "ROLLBACK;\n")
        self.sessions.remove(session)
        if session.process.returncode:
            raise RuntimeError("Experiment transaction did not complete")

    @staticmethod
    def drain(session: Session, data: str | None = None) -> None:
        try:
            session.process.communicate(data, timeout=10)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Experiment session timed out; diagnostics not exported") from None

    def crash_restart(self) -> None:
        for args in (["kill", "--signal", "KILL", self.owned()], ["start", self.owned()]):
            if self.docker(args).returncode:
                raise RuntimeError("Experiment crash/restart failed")
        self.wait_ready()

    def close(self) -> None:
        if self.container:
            if self.docker(["rm", "--force", "--volumes", self.owned()]).returncode:
                raise RuntimeError("Experiment cleanup failed")
            self.container = ""
        for session in self.sessions:
            self.drain(session)
        self.sessions.clear()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
