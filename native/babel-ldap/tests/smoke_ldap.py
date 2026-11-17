"""Independent ldap3 client exercises the built lab server on an ephemeral port."""

import selectors
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

from ldap3 import BASE, NONE, SUBTREE, Connection, Server  # type: ignore[import-untyped]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def connect(server: Server) -> Connection:
    connection = Connection(server, receive_timeout=2, raise_exceptions=False)
    require(connection.bind(), "anonymous lab bind failed")
    return connection


def check_root(server: Server) -> None:
    connection = connect(server)
    try:
        require(
            connection.search(
                "",
                "(objectClass=*)",
                BASE,
                attributes=["supportedLDAPVersion", "vendorName", "vendorVersion"],
            ),
            "RootDSE search failed",
        )
        entries = [item for item in connection.response if item["type"] == "searchResEntry"]
        require(len(entries) == 1 and entries[0]["dn"] == "", "wrong RootDSE entry")
        attributes = entries[0]["attributes"]
        require(attributes["supportedLDAPVersion"] == ["3"], "incorrect LDAP version")
        require(attributes["vendorName"] == ["Babel"], "incorrect vendor")
        require("supportedCapabilities" not in attributes, "unexpected AD capability claim")
    finally:
        connection.unbind()


def run(binary: Path) -> None:
    for args in (["--listen", "0.0.0.0:0"], ["--max-connections", "0"]):
        result = subprocess.run([str(binary), *args], capture_output=True, timeout=5, check=False)
        require(result.returncode != 0, "unsafe lab configuration accepted")
    with tempfile.TemporaryFile(mode="w+t") as diagnostics:
        process = subprocess.Popen(
            [str(binary), "--listen", "127.0.0.1:0", "--max-connections", "5"],
            stdout=subprocess.PIPE,
            stderr=diagnostics,
            text=True,
        )
        try:
            require(process.stdout is not None, "startup stream missing")
            if process.stdout is None:
                raise RuntimeError("startup stream missing")
            with selectors.DefaultSelector() as ready:
                ready.register(process.stdout, selectors.EVENT_READ)
                require(bool(ready.select(timeout=5)), "lab server startup timed out")
                address = process.stdout.readline().strip()
            require(address.startswith("LISTENING 127.0.0.1:"), "unsafe or missing listener")
            port = int(address.rsplit(":", 1)[1])
            server = Server("127.0.0.1", port=port, get_info=NONE, connect_timeout=2)
            check_root(server)

            credential = Connection(
                server,
                user="cn=admin",
                password="lab-fixture",
                receive_timeout=2,
                raise_exceptions=False,
            )
            try:
                require(not credential.bind(), "credential authentication unexpectedly succeeded")
                require(credential.result["result"] == 53, "credential rejection code incorrect")
            finally:
                credential.unbind()

            connection = connect(server)
            try:
                require(
                    not connection.search("dc=example", "(objectClass=*)", BASE),
                    "directory objects unexpectedly exist",
                )
                require(connection.result["result"] == 32, "missing object code incorrect")
                require(
                    not connection.search("", "(objectClass=*)", SUBTREE),
                    "unsupported subtree search succeeded",
                )
                require(connection.result["result"] == 53, "subtree rejection incorrect")
            finally:
                connection.unbind()

            with socket.create_connection(("127.0.0.1", port), timeout=2) as malformed:
                malformed.sendall(bytes.fromhex("3084ffffffff"))
                require(malformed.recv(1) == b"", "oversized declaration was not rejected")
            check_root(server)  # malformed peer did not kill the lab process
            require(process.wait(timeout=5) == 0, "lab server did not exit cleanly")
            diagnostics.seek(0)
            require("lab-fixture" not in diagnostics.read(), "credential leaked in diagnostics")
            require("lab-fixture" not in process.stdout.read(), "credential leaked in stdout")
            print("LDAP smoke passed: RootDSE, credential/scope denial, malformed-peer recovery")
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
            if process.stdout is not None:
                process.stdout.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: smoke_ldap.py /absolute/path/to/babel-ldap")
    run(Path(sys.argv[1]).resolve())
