"""Independent ldap3 probe for the release directory-read listener."""

import argparse
import hashlib
import json
import platform
import re
import selectors
import socket
import subprocess  # nosec B404
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from functools import partial
from importlib.metadata import version
from pathlib import Path
from typing import Any

from ldap3 import BASE, DEREF_ALWAYS, DEREF_NEVER, LEVEL, NONE, SUBTREE, Connection, Server  # type: ignore[import-untyped]
from ldap3.operation.search import search_operation  # type: ignore[import-untyped]
from ldap3.protocol.rfc4511 import LDAPMessage, ProtocolOp  # type: ignore[import-untyped]
from pyasn1.codec.ber.encoder import encode  # type: ignore[import-untyped]

CONTEXT = "DC=babel,DC=test"
ALICE = "CN=Alice," + CONTEXT
BOB = "CN=Bob," + CONTEXT
READERS = "CN=Readers," + CONTEXT
WORKSTATION = "CN=Workstation," + CONTEXT
PAGED = "1.2.840.113556.1.4.319"
MANAGE_DSA_IT = "2.16.840.1.113730.3.4.2"
PROFILE = "babel-synthetic-ldap-read-v1"
DEFAULT_FILTER = "(objectClass=*)"
CHILDREN = [ALICE, BOB, READERS, WORKSTATION]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


@contextmanager
def connect(server: Server) -> Iterator[Connection]:
    conn = Connection(
        server,
        receive_timeout=2,
        auto_referrals=False,
        check_names=False,
        return_empty_attributes=False,
    )
    require(conn.bind(), "anonymous LDAPv3 bind failed")
    try:
        yield conn
    finally:
        conn.unbind()


def search(
    conn: Connection,
    cases: list[dict[str, Any]],
    scenario: str,
    base: str,
    scope: str,
    dns: list[str],
    *,
    expression: str = DEFAULT_FILTER,
    attrs: tuple[str, ...] = ("1.1",),
    expected_attrs: list[dict[str, list[str]]] | None = None,
    code: int = 0,
    matched: str = "",
    deref: str = DEREF_NEVER,
    size_limit: int = 0,
    types_only: bool = False,
    paging: tuple[int, bytes] | None = None,
    continued: bool | None = None,
    controls: list[tuple[str, bool, bytes | None]] | None = None,
) -> bytes:
    started = time.monotonic()
    conn.search(
        base,
        expression,
        scope,
        dereference_aliases=deref,
        attributes=list(attrs),
        size_limit=size_limit,
        types_only=types_only,
        controls=controls,
        paged_size=None if paging is None else paging[0],
        paged_criticality=True,
        paged_cookie=None if paging is None else paging[1],
    )
    actual = conn.result
    entries = [
        {
            "dn": item["dn"],
            "attributes": {
                name: [value.decode("utf-8") for value in (values or [])]
                for name, values in item["raw_attributes"].items()
            },
        }
        for item in conn.response
        if item["type"] == "searchResEntry"
    ]
    require(
        actual["result"] == code
        and actual["dn"] == matched
        and [entry["dn"] for entry in entries] == dns
        and not actual.get("referrals")
        and len(entries) == len(conn.response),
        f"{scenario}: unexpected status, matched base, entries or referrals ({actual['result']})",
    )
    if expected_attrs is None:
        expected_attrs = [{} for _ in dns]
    require(
        [entry["attributes"] for entry in entries] == expected_attrs,
        f"{scenario}: unexpected attributes: {entries}",
    )
    response_control = actual.get("controls", {}).get(PAGED)
    cookie = b"" if response_control is None else response_control["value"]["cookie"]
    if continued is not None:
        require(
            response_control is not None and len(cookie) == (16 if continued else 0),
            f"{scenario}: missing or wrong paging disposition",
        )
    else:
        require(response_control is None, f"{scenario}: unexpected paging control")
    cases.append(
        {
            "scenario": scenario,
            "request": {
                "base": base,
                "scope": scope,
                "filter": expression,
                "attributes": list(attrs),
                "deref": deref,
                "types_only": types_only,
                "size_limit": size_limit,
                "paging": None
                if paging is None
                else {"size": paging[0], "cookie_bytes": len(paging[1])},
                "controls": [
                    {"oid": oid, "critical": critical, "value_bytes": len(value or b"")}
                    for oid, critical, value in (controls or [])
                ],
            },
            "expected_code": code,
            "result_code": actual["result"],
            "matched_dn": actual["dn"],
            "entries": entries,
            "referrals": [],
            "page_cookie_bytes": None if response_control is None else len(cookie),
            "duration_ms": round((time.monotonic() - started) * 1000, 3),
            "result": "passed",
        }
    )
    return bytes(cookie)


def reads(server: Server, cases: list[dict[str, Any]]) -> None:
    with connect(server) as conn:
        check = partial(search, conn, cases)
        check(
            "rootdse",
            "",
            BASE,
            [""],
            attrs=("supportedLDAPVersion", "vendorName", "namingContexts", "supportedCapabilities"),
            expected_attrs=[{"supportedLDAPVersion": ["3"], "vendorName": ["Babel"]}],
        )
        check(
            "base-projection",
            ALICE.lower(),
            BASE,
            [ALICE],
            expression="(&(objectClass=USER)(cn=ALICE)(uidNumber=1001))",
            attrs=("CN", "displayName", "uidNumber", "objectGUID", "objectSid"),
            expected_attrs=[
                {"cn": ["Alice"], "displayName": ["Alice Example"], "uidNumber": ["1001"]}
            ],
        )
        check(
            "apex-base",
            CONTEXT,
            BASE,
            [CONTEXT],
            attrs=("*",),
            expected_attrs=[{"objectClass": ["domain"], "dc": ["babel"]}],
        )
        check("onelevel", CONTEXT, LEVEL, CHILDREN)
        check("subtree", CONTEXT, SUBTREE, [CONTEXT, *CHILDREN])
        check("leaf-onelevel", ALICE, LEVEL, [])
        check(
            "leaf-subtree",
            WORKSTATION,
            SUBTREE,
            [WORKSTATION],
            attrs=("dnsHostName",),
            expression="(dnsHostName=WORKSTATION.babel.test)",
            expected_attrs=[{"dnsHostName": ["workstation.babel.test"]}],
        )
        check(
            "types-only",
            ALICE,
            BASE,
            [ALICE],
            types_only=True,
            attrs=("cn", "displayName", "objectSid"),
            expected_attrs=[{"cn": [], "displayName": []}],
        )
        check(
            "boolean-filter",
            CONTEXT,
            LEVEL,
            [ALICE, READERS],
            expression="(|(description=Public fixture)(&(objectClass=group)(description=*)))",
        )
        check(
            "description-exact",
            ALICE,
            BASE,
            [],
            expression="(description=public fixture)",
        )
        check(
            "invalid-integer-assertion",
            CONTEXT,
            LEVEL,
            [],
            expression="(!(uidNumber=01001))",
        )
        check(
            "unreadable-filter-attribute",
            CONTEXT,
            SUBTREE,
            [],
            expression="(!(objectGUID=*))",
        )
        check(
            "unsupported-filter",
            CONTEXT,
            SUBTREE,
            [],
            expression="(|(objectClass=*)(cn=Al*))",
            code=53,
        )
        check(
            "unsupported-target",
            "DC=external,DC=test",
            BASE,
            [],
            code=32,
        )
        check(
            "missing-leaf",
            "CN=Missing," + CONTEXT,
            BASE,
            [],
            code=32,
            matched=CONTEXT,
        )
        check(
            "invalid-base",
            "CN=Invalid!,DC=babel,DC=test",
            BASE,
            [],
            code=34,
        )
        check(
            "alias-deref-refused",
            CONTEXT,
            BASE,
            [],
            code=53,
            deref=DEREF_ALWAYS,
        )
        check(
            "referral-control-critical",
            CONTEXT,
            SUBTREE,
            [],
            code=12,
            controls=[(MANAGE_DSA_IT, True, None)],
        )
        check(
            "referral-control-noncritical",
            "DC=external,DC=test",
            BASE,
            [],
            code=32,
            controls=[(MANAGE_DSA_IT, False, None)],
        )
        check("size-limit", CONTEXT, LEVEL, [ALICE], code=4, size_limit=1)


def pages(server: Server, cases: list[dict[str, Any]]) -> None:
    with connect(server) as conn:
        check = partial(search, conn, cases)
        first = check(
            "page-one",
            CONTEXT,
            LEVEL,
            CHILDREN[:2],
            paging=(2, b""),
            continued=True,
        )
        check(
            "changed-query-cookie",
            CONTEXT,
            LEVEL,
            [],
            code=53,
            expression="(objectClass=user)",
            paging=(2, first),
        )
        second = check(
            "page-two",
            CONTEXT,
            LEVEL,
            [READERS],
            paging=(1, first),
            continued=True,
        )
        check("replayed-cookie", CONTEXT, LEVEL, [], code=53, paging=(2, first))
        check(
            "last-page",
            CONTEXT,
            LEVEL,
            [WORKSTATION],
            paging=(2, second),
            continued=False,
        )
        check("completed-cookie", CONTEXT, LEVEL, [], code=53, paging=(2, second))
        limited = check(
            "limited-first-page",
            CONTEXT,
            LEVEL,
            CHILDREN[:2],
            size_limit=3,
            paging=(2, b""),
            continued=True,
        )
        check(
            "limited-terminal-page",
            CONTEXT,
            LEVEL,
            [READERS],
            code=4,
            size_limit=3,
            paging=(2, limited),
            continued=False,
        )
        check(
            "oversized-page",
            CONTEXT,
            LEVEL,
            [],
            code=11,
            paging=(5, b""),
        )
        check("empty-cookie-cancel", CONTEXT, LEVEL, [], code=2, paging=(0, b""))
        check(
            "malformed-page-control",
            CONTEXT,
            LEVEL,
            [],
            code=2,
            controls=[(PAGED, True, b"\x30\x00")],
        )
        check(
            "missing-page-value",
            CONTEXT,
            LEVEL,
            [],
            code=2,
            controls=[(PAGED, True, None)],
        )
        cancelled = check(
            "start-cancelled-page",
            CONTEXT,
            LEVEL,
            [ALICE],
            paging=(1, b""),
            continued=True,
        )
        check(
            "cancel-page",
            CONTEXT,
            LEVEL,
            [],
            paging=(0, cancelled),
            continued=False,
        )
        check(
            "cancelled-cookie",
            CONTEXT,
            LEVEL,
            [],
            code=53,
            paging=(1, cancelled),
        )
        crossing = check(
            "start-connection-local-page",
            CONTEXT,
            LEVEL,
            [ALICE],
            paging=(1, b""),
            continued=True,
        )
    with connect(server) as conn:
        check = partial(search, conn, cases)
        own = check(
            "new-connection-page",
            CONTEXT,
            LEVEL,
            [ALICE],
            paging=(1, b""),
            continued=True,
        )
        check(
            "cross-connection-cookie",
            CONTEXT,
            LEVEL,
            [],
            code=53,
            paging=(1, crossing),
        )
        check(
            "new-connection-own-cookie",
            CONTEXT,
            LEVEL,
            [BOB, READERS, WORKSTATION],
            paging=(3, own),
            continued=False,
        )


def malformed_filter(port: int, cases: list[dict[str, Any]]) -> None:
    request = search_operation(
        CONTEXT,
        DEFAULT_FILTER,
        LEVEL,
        DEREF_NEVER,
        ["cn"],
        0,
        0,
        False,
        False,
        True,
    )
    operation = ProtocolOp()
    operation["searchRequest"] = request
    message = LDAPMessage()
    message["messageID"] = 1
    message["protocolOp"] = operation
    valid = bytes(encode(message))
    field = b"\x87\x0bobjectClass"
    require(valid.count(field) == 1, "ldap3 encoded a different presence filter")
    invalid = valid.replace(field, b"\x88\x0bobjectClass")
    with socket.create_connection(("127.0.0.1", port), timeout=2) as connection:
        connection.sendall(invalid)
        require(connection.recv(1) == b"", "malformed filter did not close the connection")
    cases.append(
        {
            "scenario": "malformed-filter-tag",
            "request": {"base": CONTEXT, "scope": LEVEL, "wire_hex": invalid.hex()},
            "response": "closed without a search entry or result",
            "result": "passed",
        }
    )


def probe(binary: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with (
        tempfile.TemporaryFile(mode="w+t") as diagnostics,
        subprocess.Popen(  # nosec B603
            [str(binary), "127.0.0.1:0", "4"],
            stdout=subprocess.PIPE,
            stderr=diagnostics,
            text=True,
        ) as process,
    ):
        try:
            assert process.stdout is not None
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                require(bool(selector.select(timeout=4)), "LDAP listener startup timed out")
                address = process.stdout.readline().strip()
            match = re.fullmatch(r"LISTENING 127\.0\.0\.1:(\d+)", address)
            require(match is not None, "LDAP listener did not bind to loopback")
            assert match is not None
            port = int(match[1])
            server = Server("127.0.0.1", port=port, get_info=NONE, connect_timeout=2)
            reads(server, cases)
            pages(server, cases)
            malformed_filter(port, cases)
            require(process.wait(timeout=4) == 0, "LDAP listener did not exit cleanly")
            diagnostics.seek(0)
            require(
                diagnostics.read().strip()
                == "Lab connection closed: invalid, unsupported or expired session",
                "unexpected listener diagnostic",
            )
        finally:
            if process.poll() is None:
                process.kill()
    return cases


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", args.revision):
        parser.error("--revision must be a full Git revision")
    binary = args.binary.resolve()
    started = datetime.now(UTC).isoformat(timespec="seconds")
    cases = probe(binary)
    root = Path(__file__).resolve().parents[3]
    report = {
        "profile": PROFILE,
        "source_revision": args.revision,
        "started_at_utc": started,
        "binary_sha256": sha256(binary),
        "probe_sha256": sha256(Path(__file__).resolve()),
        "cargo_lock_sha256": sha256(root / "Cargo.lock"),
        "host": {
            "os": platform.freedesktop_os_release()["PRETTY_NAME"],
            "kernel": platform.release(),
            "architecture": platform.machine(),
        },
        "client": {
            "ldap3": version("ldap3"),
            "pyasn1": version("pyasn1"),
            "python": platform.python_version(),
        },
        "result": "passed",
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{PROFILE}: {len(cases)} LDAP client checks passed")


if __name__ == "__main__":
    main()
