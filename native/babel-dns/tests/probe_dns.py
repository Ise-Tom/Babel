"""Exercise the Babel release DNS listener with BIND dig and nsupdate."""

import argparse
import hashlib
import json
import platform
import re
import selectors
import shutil
import subprocess  # nosec B404
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DOMAIN = "discovery.example.test."
LOCATOR = "_ldap._tcp.dc._msdcs." + DOMAIN
EAST = "dc-east." + DOMAIN
WEST = "dc-west." + DOMAIN
PROFILE = "babel-synthetic-dc-discovery-v1"
PROBE_DATAGRAMS = 18
HEADER = re.compile(r"^;; ->>HEADER<<- opcode: (\w+), status: (\w+), id:[ \t]+(\d+)$", re.M)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"{name} must be installed (BIND client tools)")
    return path


def run(args: list[str], *, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    # Invoke the selected local executable directly with fixed probe arguments.
    return subprocess.run(  # nosec B603
        args,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )


def query(
    dig: str,
    port: str,
    name: str,
    kind: str,
    status: str,
    answers: tuple[str, ...] = (),
    *,
    authoritative: bool = True,
    options: tuple[str, ...] = (),
) -> dict[str, Any]:
    started = time.monotonic_ns()
    result = run(
        [
            dig,
            "-r",
            "@127.0.0.1",
            "-p",
            port,
            "+qr",
            "+noedns",
            "+noadflag",
            "+norecurse",
            "+notcp",
            "+nocmd",
            "+nostats",
            "+tries=1",
            "+time=2",
            name,
            kind,
            *options,
        ]
    )
    output = result.stdout
    label = f"{name} {kind} {options}"
    require(result.returncode == 0, f"{label}: dig failed\n{output}\n{result.stderr}")
    headers = HEADER.findall(output)
    require(len(headers) == 2, f"{label}: expected the sent query and received response\n{output}")
    (_, _, sent_id), (opcode, actual, received_id) = headers
    require(
        (opcode, actual, received_id) == ("QUERY", status, sent_id),
        f"{label}: expected {status} for the matching QUERY\n{output}",
    )
    response = output[output.rindex(";; ->>HEADER<<-") :]
    flags_match = re.search(r"^;; flags: ([^;]*);", response, re.M)
    require(flags_match is not None, f"{label}: missing flags\n{output}")
    assert flags_match is not None
    flags = flags_match[1].split()
    require(
        "qr" in flags and ("aa" in flags) == authoritative and not {"ra", "tc"} & set(flags),
        f"{label}: unexpected authority, recursion or truncation flags\n{output}",
    )

    records = [line.split() for line in response.splitlines() if line and not line.startswith(";")]
    actual_answers = []
    authority = []
    for owner, ttl, record_class, record_type, *data in records:
        require(record_class == "IN", f"{label}: unexpected class\n{output}")
        if record_type == "SOA":
            authority.append((owner.lower(), ttl, data[-1]))
        else:
            require(
                (owner.lower(), record_type) == (name.lower(), kind) and 0 < int(ttl) <= 30,
                f"{label}: unexpected owner, type or lease TTL\n{output}",
            )
            actual_answers.append(" ".join(data))
    expected_authority = [(DOMAIN, "0", "0")] if authoritative and not answers else []
    require(
        sorted(actual_answers) == sorted(answers) and authority == expected_authority,
        f"{label}: expected answers {answers} and authority {expected_authority}\n{output}",
    )
    return {
        "query": {"name": name, "type": kind, "options": list(options)},
        "expected_rcode": status,
        "rcode": actual,
        "expected_answers": list(answers),
        "duration_ms": round((time.monotonic_ns() - started) / 1_000_000, 3),
        "authoritative": authoritative,
        "answers": sorted(actual_answers),
        "dig_query_and_reply": output.strip(),
        "result": "passed",
    }


def refuse_update(nsupdate: str, port: str) -> dict[str, Any]:
    lines = [
        f"zone {DOMAIN}",
        f"update delete {EAST} A",
        f"update add {EAST} 60 A 192.0.2.99",
        "send",
    ]
    command = "\n".join([f"server 127.0.0.1 {port}", *lines, ""])
    started = time.monotonic_ns()
    result = run([nsupdate, "-d", "-t", "2", "-r", "0"], stdin=command)
    output = result.stdout + result.stderr
    headers = HEADER.findall(output)
    require(
        result.returncode != 0
        and len(headers) == 2
        and headers[0][:2] == ("UPDATE", "NOERROR")
        and headers[-1] == ("UPDATE", "NOTIMP", headers[0][2]),
        f"nsupdate did not observe an explicit UPDATE refusal\n{output}",
    )
    return {
        "commands": lines,
        "expected_rcode": "NOTIMP",
        "rcode": headers[-1][1],
        "duration_ms": round((time.monotonic_ns() - started) / 1_000_000, 3),
        "nsupdate_query_and_reply": output.strip().replace(f"127.0.0.1#{port}", "127.0.0.1#<port>"),
        "result": "passed",
    }


def probe(binary: Path, dig: str, nsupdate: str) -> list[dict[str, Any]]:
    refused = run([str(binary), "--listen", "0.0.0.0:0"])
    require(
        refused.returncode != 0 and "loopback" in refused.stderr,
        "non-loopback listener unexpectedly started",
    )
    # This process serves only the declared loopback fixture.
    with subprocess.Popen(  # nosec B603
        [str(binary), "--listen", "127.0.0.1:0", "--max-datagrams", str(PROBE_DATAGRAMS)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    ) as process:
        try:
            assert process.stdout is not None
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                require(bool(selector.select(timeout=3)), "DNS listener did not start")
                address = process.stdout.readline().strip()
            match = re.fullmatch(r"LISTENING 127\.0\.0\.1:(\d+)", address)
            require(match is not None, f"unexpected DNS listener address: {address}")
            assert match is not None
            port = match[1]
            east_srv = "0 0 389 " + EAST
            west_srv = "0 0 389 " + WEST
            cases = [
                query(dig, port, LOCATOR.upper(), "SRV", "NOERROR", (east_srv, west_srv)),
                query(
                    dig,
                    port,
                    "_ldap._tcp.east._sites.dc._msdcs." + DOMAIN,
                    "SRV",
                    "NOERROR",
                    (east_srv,),
                ),
                query(
                    dig,
                    port,
                    "_ldap._tcp.west._sites.dc._msdcs." + DOMAIN,
                    "SRV",
                    "NOERROR",
                    (west_srv,),
                ),
                query(dig, port, EAST, "A", "NOERROR", ("192.0.2.10",)),
                query(dig, port, EAST, "AAAA", "NOERROR", ("2001:db8::10",)),
                query(dig, port, WEST, "A", "NOERROR", ("192.0.2.20",)),
                query(dig, port, WEST, "AAAA", "NOERROR", ("2001:db8::20",)),
                query(dig, port, "dc-stale." + DOMAIN, "A", "NXDOMAIN"),
                query(dig, port, "dc-ineligible." + DOMAIN, "AAAA", "NXDOMAIN"),
                query(dig, port, "dc-invalid." + DOMAIN, "A", "NXDOMAIN"),
                query(
                    dig, port, "_ldap._tcp.unknown._sites.dc._msdcs." + DOMAIN, "SRV", "NXDOMAIN"
                ),
                query(dig, port, LOCATOR, "A", "NOERROR"),
                query(dig, port, EAST, "TXT", "NOTIMP", authoritative=False),
                query(
                    dig,
                    port,
                    EAST,
                    "A",
                    "NOTIMP",
                    authoritative=False,
                    options=("-c", "CH"),
                ),
                query(
                    dig,
                    port,
                    EAST,
                    "A",
                    "NOTIMP",
                    authoritative=False,
                    options=("+edns=0", "+nocookie"),
                ),
                query(dig, port, "outside.example.test.", "A", "REFUSED", authoritative=False),
                refuse_update(nsupdate, port),
                query(dig, port, EAST, "A", "NOERROR", ("192.0.2.10",)),
            ]
            require(process.wait(timeout=3) == 0, "DNS listener did not exit cleanly")
            return cases
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", args.revision):
        parser.error("--revision must be a full Git commit")
    binary = args.binary.resolve()
    dig, nsupdate = tool("dig"), tool("nsupdate")
    script = Path(__file__).resolve()
    stamp = datetime.now(UTC).isoformat(timespec="seconds")
    cases = probe(binary, dig, nsupdate)
    report = {
        "profile": PROFILE,
        "source_revision": args.revision,
        "started_at_utc": stamp,
        "binary_sha256": sha256(binary),
        "probe_sha256": sha256(script),
        "cargo_lock_sha256": sha256(script.parents[3] / "Cargo.lock"),
        "source_sha256": {
            name: sha256(script.parents[1] / name) for name in ("src/lib.rs", "src/main.rs")
        },
        "host": {
            "os": platform.freedesktop_os_release()["PRETTY_NAME"],
            "kernel": platform.release(),
            "architecture": platform.machine(),
        },
        "tools": {
            "python": platform.python_version(),
            "dig": run([dig, "-v"]).stdout.strip(),
            "nsupdate": run([nsupdate, "-V"]).stdout.strip(),
        },
        "transport": "loopback UDP",
        "non_loopback_listener": "refused",
        "result": "passed",
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{PROFILE}: {len(cases)} independent client checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
