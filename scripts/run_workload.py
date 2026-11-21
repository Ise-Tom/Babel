"""Run the bounded Phase 0 RootDSE workload against an owned Babel lab process."""

import argparse
import asyncio
import hashlib
import os
import platform
import re
import tempfile
import time
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from check_workload import verify
from generate_workload import PROFILES, encoded, generate, score

Operation = Literal["rootdse_base", "rootdse_scope_denial"]
Outcome = Literal["succeeded", "denied", "timed_out", "rejected", "unexpected_error"]
OPERATIONS: tuple[Operation, ...] = ("rootdse_base", "rootdse_scope_denial")
OUTCOMES: tuple[Outcome, ...] = ("succeeded", "denied", "timed_out", "rejected", "unexpected_error")
UNRUN = {
    "operation_classes": {
        "kerberos_as_tgs_and_denials": "Native KDC and real clients required",
        "ldap_indexed_reads_and_denials": "Dataset import, indexed reads, paging and ACLs required",
        "directory_writes_and_denials": "Native directory mutations and authorization required",
    },
    "scenarios": {
        "cold_cache": "Storage and query caches absent; cache state uncontrolled",
        "warm_steady_state": "Mixed traffic, separate generators and six DCs required",
        "auth_burst": "Native KDC and concurrent directory traffic required",
        "24h_soak": "Mixed traffic, separate generators and six DCs required",
        "hot_key_and_site_skew": "Native directory and multi-site topology required",
        "concurrent_rename_and_revocation": "Native directory and real clients required",
        "lan_baseline_and_wan_degradation": "Owned network with measured shaping required",
        "one_dc_down": "Six independent DCs required",
        "site_loss": "Six independent DCs required",
        "24h_partition_and_rejoin": "Six independent DCs required",
        "asymmetric_links": "Owned network with measured shaping required",
        "dns_and_dc_locator_failure": "Isolated DNS and real clients required",
        "clock_skew": "Isolated time sources and real clients required",
        "expired_trust": "Integrated trust and real clients required",
        "key_provider_outage": "Integrated directory key provider required",
        "process_and_host_kill": "State-bearing service and isolated fault hosts required",
        "disk_full": "Native storage and an isolated fault volume required",
        "audit_collector_loss": "Integrated audit collector required",
    },
}


@dataclass(frozen=True)
class Profile:
    name: str = "ldap-rootdse-loopback-smoke-v1"
    duration_s: int = 3
    rate_per_s: int = 60
    inflight_limit: int = 4
    outstanding_limit: int = 12
    deadline_ms: int = 500


@dataclass(frozen=True)
class Offer:
    offset_us: int
    operation: Operation


@dataclass(frozen=True)
class Sample:
    operation: Operation
    outcome: Outcome
    queue_us: int | None
    end_to_end_us: int


SMOKE = Profile()


def schedule(profile: Profile, seed: str) -> list[Offer]:
    """Place one denial per five offers, at a seeded position within each block."""
    offers = []
    for index in range(profile.rate_per_s * profile.duration_s):
        block, slot = divmod(index, 5)
        denied_slot = int.from_bytes(score(seed, "rootdse-denial-slot", block), "big") % 5
        operation: Operation = "rootdse_scope_denial" if slot == denied_slot else "rootdse_base"
        offers.append(Offer(index * 1_000_000 // profile.rate_per_s, operation))
    return offers


async def drive(
    profile: Profile, offers: Sequence[Offer], exchange: Callable[[Operation], Awaitable[Outcome]]
) -> tuple[list[Sample], int, int]:
    clock = asyncio.get_running_loop().time
    slots = asyncio.Semaphore(profile.inflight_limit)
    samples: list[Sample] = []
    outstanding = peak = 0
    active = peak_active = 0

    async def attempt(offer: Offer, due: float, deadline: float) -> None:
        nonlocal active, peak_active, outstanding
        started = None
        outcome: Outcome = "timed_out"
        try:
            async with asyncio.timeout_at(deadline), slots:
                started_at = clock()
                if started_at < deadline:
                    started = started_at
                    active += 1
                    peak_active = max(peak_active, active)
                    try:
                        outcome = await exchange(offer.operation)
                    finally:
                        active -= 1
        except TimeoutError:
            outcome = "timed_out"
        except (OSError, EOFError, ValueError):
            outcome = "unexpected_error"
        ended = clock()
        if ended >= deadline:
            outcome = "timed_out"
        samples.append(
            Sample(
                offer.operation,
                outcome,
                None if started is None else micros(started - due),
                micros(ended - due),
            )
        )
        outstanding -= 1

    origin = clock()
    async with asyncio.TaskGroup() as tasks:
        for offer in offers:
            due = origin + offer.offset_us / 1_000_000
            deadline = due + profile.deadline_ms / 1000
            # Wake at the planned instant even when every worker is occupied.
            while (delay := due - clock()) > 0:
                await asyncio.sleep(delay)
            now = clock()
            if now >= deadline:
                samples.append(Sample(offer.operation, "timed_out", None, micros(now - due)))
            elif outstanding >= profile.outstanding_limit:
                samples.append(Sample(offer.operation, "rejected", None, micros(now - due)))
            else:
                outstanding += 1
                peak = max(peak, outstanding)
                tasks.create_task(attempt(offer, due, deadline))
    return samples, peak, peak_active


def micros(seconds: float) -> int:
    return max(0, round(seconds * 1_000_000))


# Fixed, short-form LDAP messages for this lab's public RootDSE interface only.
def tlv(tag: int, body: bytes) -> bytes:
    return bytes((tag, len(body))) + body


def message(message_id: int, tag: int, body: bytes) -> bytes:
    return tlv(0x30, b"\x02\x01" + bytes((message_id,)) + tlv(tag, body))


BIND = message(1, 0x60, b"\x02\x01\x03\x04\x00\x80\x00")
VENDOR_ENTRY = message(
    2, 0x64, b"\x04\x00" + tlv(0x30, tlv(0x30, b"\x04\x0avendorName\x31\x07\x04\x05Babel"))
)[2:]


async def read_message(reader: asyncio.StreamReader) -> bytes:
    tag, length = await reader.readexactly(2)
    if tag != 0x30 or length >= 128:
        raise ValueError("Unexpected lab LDAP frame")
    return await reader.readexactly(length)


def result(frame: bytes, message_id: int, tag: int, code: int) -> bool:
    # Match message ID, result code and empty matched DN. Ignore diagnostic text.
    return (
        len(frame) >= 12
        and frame[:4] == bytes((2, 1, message_id, tag))
        and frame[4] == len(frame) - 5
        and frame[5:12] == bytes((10, 1, code, 4, 0, 4, len(frame) - 12))
    )


async def rootdse(port: int, operation: Operation) -> Outcome:
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    try:
        writer.write(BIND)
        await writer.drain()
        if not result(await read_message(reader), 1, 0x61, 0):
            return "unexpected_error"
        # Empty base DN, base/subtree scope, no dereference or limits, (objectClass=*).
        scope = 0 if operation == "rootdse_base" else 2
        search = (
            b"\x04\x00\x0a\x01"
            + bytes((scope,))
            + b"\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00"
            + b"\x87\x0bobjectClass\x30\x0c\x04\x0avendorName"
        )
        writer.write(message(2, 0x63, search))
        await writer.drain()
        reply = await read_message(reader)
        if operation == "rootdse_scope_denial":
            return "denied" if result(reply, 2, 0x65, 53) else "unexpected_error"
        if reply == VENDOR_ENTRY and result(await read_message(reader), 2, 0x65, 0):
            return "succeeded"
        return "unexpected_error"
    finally:
        writer.close()


async def run_binary(binary: Path, offers: list[Offer]) -> tuple[list[Sample], int, int]:
    process = await asyncio.create_subprocess_exec(
        str(binary.resolve()),
        "--listen",
        "127.0.0.1:0",
        "--max-connections",
        str(len(offers)),
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    try:
        if process.stdout is None:
            raise RuntimeError("Missing lab startup stream")
        line = await asyncio.wait_for(process.stdout.readline(), timeout=5)
        address = re.fullmatch(rb"LISTENING 127\.0\.0\.1:([0-9]{1,5})\r?\n", line)
        if address is None or not 0 < int(address[1]) <= 65535:
            raise ValueError("Missing Babel loopback listener")
        port = int(address[1])
        return await drive(SMOKE, offers, lambda operation: rootdse(port, operation))
    finally:
        if process.returncode is None:
            try:
                process.terminate()
            except ProcessLookupError:
                pass  # The bounded server may already have handled its last connection.
        try:
            await asyncio.wait_for(process.wait(), timeout=3)
        except TimeoutError:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            await asyncio.wait_for(process.wait(), timeout=3)


BUCKETS_US = (100, 250, 500, 1000, 2500, 5000, 10_000, 25_000, 50_000, 100_000, 500_000)


def distribution(values: list[int]) -> dict[str, Any]:
    ordered = sorted(values)
    count = len(ordered)
    percentiles = {
        f"p{p}_us": ordered[(count * p + 99) // 100 - 1] if count else None for p in (50, 95, 99)
    }
    buckets: dict[str, int] = {}
    previous = -1
    for bound in BUCKETS_US:
        buckets[str(bound)] = sum(previous < value <= bound for value in ordered)
        previous = bound
    buckets["+inf"] = sum(value > previous for value in ordered)
    return {
        "count": count,
        **percentiles,
        "max_us": ordered[-1] if count else None,
        "histogram_us_inclusive_upper_bounds": buckets,
    }


def summarize(samples: list[Sample], duration_s: int) -> dict[str, Any]:
    counts: dict[str, int] = {
        label: sum(sample.outcome == label for sample in samples) for label in OUTCOMES
    }
    completed = counts["succeeded"] + counts["denied"]
    return {
        "offered": len(samples),
        "started": sum(s.queue_us is not None for s in samples),
        "completed": completed,
        **counts,
        "timed_out_before_start": sum(
            s.outcome == "timed_out" and s.queue_us is None for s in samples
        ),
        "offered_per_s": len(samples) / duration_s,
        "completed_per_s": completed / duration_s,
        "queue_us": distribution([s.queue_us for s in samples if s.queue_us is not None]),
        "end_to_end_us": distribution([s.end_to_end_us for s in samples]),
        "end_to_end_by_outcome": {
            label: distribution([s.end_to_end_us for s in samples if s.outcome == label])
            for label in OUTCOMES
        },
    }


def host_details(label: str) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "label": label,
        "os_kernel": platform.platform(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "logical_cpus": os.cpu_count(),
        "cpu_model": platform.processor() or None,
        "visible_memory_kib": None,
    }
    if platform.system() == "Linux":
        fields["os_release"] = platform.freedesktop_os_release()["PRETTY_NAME"]
        cpu = re.search(r"^model name\s*:\s*(.+)$", Path("/proc/cpuinfo").read_text(), re.M)
        mem = re.search(r"^MemTotal:\s+(\d+)", Path("/proc/meminfo").read_text(), re.M)
        fields["cpu_model"] = cpu[1] if cpu else fields["cpu_model"]
        fields["visible_memory_kib"] = int(mem[1]) if mem else None
    return fields


def report(binary: Path, revision: str, seed: str, run_id: str, host: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="babel-workload-") as temporary:
        dataset = Path(temporary) / "dataset"
        manifest = generate(dataset, seed=seed, source_revision=revision, profile=PROFILES["smoke"])
        audit = verify(dataset)
    offers = schedule(SMOKE, seed)
    binary_sha256 = hashlib.sha256(binary.read_bytes()).hexdigest()
    clock = time.get_clock_info("monotonic")
    started = datetime.now(UTC)
    begin = time.monotonic()
    samples, peak, peak_active = asyncio.run(run_binary(binary, offers))
    operations = {
        name: summarize([s for s in samples if s.operation == name], SMOKE.duration_s)
        for name in OPERATIONS
    }
    return {
        "schema_version": 1,
        "requirement": "P00-09",
        "run_id": run_id,
        "started_at_utc": started.isoformat(),
        "elapsed_s_including_startup_and_drain": round(time.monotonic() - begin, 6),
        "source_revision": revision,
        "binary_sha256": binary_sha256,
        "dataset": {
            "audit": audit,
            "generator_version": manifest["generator_version"],
            "input_sha256": manifest["input_sha256"],
            "files": manifest["files"],
            "loaded_into_server": False,
        },
        "profile": asdict(SMOKE),
        "site": "local-loopback",
        "schedule_sha256": hashlib.sha256(encoded([asdict(offer) for offer in offers])).hexdigest(),
        "host": host_details(host),
        "clock": {"implementation": clock.implementation, "resolution_s": clock.resolution},
        "warmup_s": 0,
        "cache_state": "fresh process; host caches uncontrolled",
        "peak_outstanding": peak,
        "peak_inflight": peak_active,
        "operations": operations,
        "unrun": UNRUN,
        "unmeasured": [
            "server_cpu_and_working_set",
            "disk_io_and_fsync",
            "network_bytes_and_injected_delay",
            "replication_lag_and_audit_backlog",
            "token_bytes_and_storage_expansion",
            "cost_and_licensing",
        ],
    }


def check_smoke(data: dict[str, Any]) -> bool:
    """Check the small smoke contract without making timing-percentile thresholds."""
    base, denial = (data["operations"][name] for name in OPERATIONS)
    total = SMOKE.duration_s * SMOKE.rate_per_s
    counts_ok = all(
        row["offered"] == row["started"] == row["completed"] == count == row[terminal]
        and sum(row[label] for label in OUTCOMES) == count
        and row["timed_out_before_start"] == 0
        and row["queue_us"]["count"] == row["end_to_end_us"]["count"] == count
        and all(
            summary["count"] == sum(summary["histogram_us_inclusive_upper_bounds"].values())
            for summary in (
                row["queue_us"],
                row["end_to_end_us"],
                *row["end_to_end_by_outcome"].values(),
            )
        )
        and all(row["end_to_end_by_outcome"][label]["count"] == row[label] for label in OUTCOMES)
        for row, count, terminal in (
            (base, total * 4 // 5, "succeeded"),
            (denial, total // 5, "denied"),
        )
    )
    return bool(
        counts_ok
        and 0 < data["peak_inflight"] <= SMOKE.inflight_limit
        and data["peak_inflight"] <= data["peak_outstanding"] <= SMOKE.outstanding_limit
        and data["dataset"]["audit"]["source_revision"] == data["source_revision"]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--seed", default="babel-ldap-smoke-v1")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--host-label", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = report(args.binary, args.source_revision, args.seed, args.run_id, args.host_label)
    passed = check_smoke(evidence)
    evidence["status"] = "passed" if passed else "failed"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as stream:
        stream.write(encoded(evidence))
    if not passed:
        raise SystemExit(f"RootDSE workload smoke failed; see {args.output}")
