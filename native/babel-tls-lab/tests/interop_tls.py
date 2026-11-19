"""Independent OpenSSL/loopback probe; ephemeral synthetic keys, no AD/client conformance."""

import hashlib
import json
import os
import re
import select
import socket
import ssl
import subprocess  # nosec B404
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, ClassVar

BINARY = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) > 1
    else Path("target/debug/babel-tls-lab").resolve()
)
REQUEST = b"BABEL-TLS-LAB\n"
ROOT = Path(__file__).resolve().parents[3]
REQUIRED_BOUNDARY_METHODS = {
    "test_current_crl_accepts_unrevoked_and_rejects_revoked_clients",
    "test_expired_unknown_and_bad_signature_revocation_data_fail_closed",
    "test_bad_or_missing_crl_is_not_a_revocation_bypass",
    "test_certificate_replacement_is_observed_in_the_same_running_process",
    "test_invalid_replacement_cannot_produce_a_second_verified_exchange",
    "test_private_key_loss_permissions_and_mismatch_prevent_startup",
    "test_independent_tls_exporter_and_wrong_truncated_or_replayed_bindings",
    "test_tls12_does_not_advertise_the_tls13_binding_profile",
}


def command(args: list[str], *, data: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, input=data, capture_output=True, check=False, timeout=10)  # nosec B603 - fixed synthetic tool arguments


class OpenSSLQualification(unittest.TestCase):
    temp: ClassVar[tempfile.TemporaryDirectory[str]]
    root: ClassVar[Path]

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="babel-tls-qualification-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.ca("trusted")
        cls.ca("stranger")
        for name, server, issuer, purpose, days in (
            ("server", True, "trusted", "serverAuth", 1),
            ("server-rsa", True, "trusted", "serverAuth", 1),
            ("client-rsa", False, "trusted", "clientAuth", 1),
            ("future-client", False, "trusted", "clientAuth", -2),
            ("client", False, "trusted", "clientAuth", 1),
            ("foreign", False, "stranger", "clientAuth", 1),
            ("expired-client", False, "trusted", "clientAuth", -1),
            ("expired-server", True, "trusted", "serverAuth", -1),
            ("wrong-client-purpose", False, "trusted", "serverAuth", 1),
            ("wrong-server-purpose", True, "trusted", "clientAuth", 1),
        ):
            cls.leaf(name, server, issuer, purpose, days)
        # A dedicated client is revoked; the normal positive client remains valid.
        cls.leaf("revoked", False, "trusted", "clientAuth", 1)
        cls.checked(
            [
                "openssl",
                "ca",
                "-batch",
                "-config",
                str(cls.root / "client.cnf"),
                "-revoke",
                str(cls.root / "revoked.pem"),
            ]
        )
        for name, issuer, dates in (
            ("valid", "trusted", ["-crldays", "1"]),
            (
                "expired",
                "trusted",
                ["-crl_lastupdate", "20000101000000Z", "-crl_nextupdate", "20010101000000Z"],
            ),
            ("foreign", "stranger", ["-crldays", "1"]),
        ):
            config = cls.root / ("client.cnf" if issuer == "trusted" else "foreign.cnf")
            cls.checked(
                [
                    "openssl",
                    "ca",
                    "-gencrl",
                    "-config",
                    str(config),
                    *dates,
                    "-out",
                    str(cls.root / f"{name}-crl.pem"),
                ]
            )
            cls.checked(
                [
                    "openssl",
                    "crl",
                    "-in",
                    str(cls.root / f"{name}-crl.pem"),
                    "-outform",
                    "DER",
                    "-out",
                    str(cls.root / f"{name}-crl.der"),
                ]
            )
        raw = bytearray((cls.root / "valid-crl.der").read_bytes())
        raw[-1] ^= 1
        (cls.root / "tampered-crl.der").write_bytes(raw)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    @classmethod
    def checked(cls, args: list[str]) -> None:
        if command(args).returncode:
            raise RuntimeError("Synthetic OpenSSL fixture setup failed")

    @classmethod
    def ca(cls, name: str) -> None:
        cls.checked(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "ec",
                "-pkeyopt",
                "ec_paramgen_curve:P-256",
                "-noenc",
                "-keyout",
                str(cls.root / f"{name}.key"),
                "-out",
                str(cls.root / f"{name}.pem"),
                "-days",
                "2",
                "-subj",
                f"/CN=Babel-Lab-{name}",
                "-addext",
                "basicConstraints=critical,CA:TRUE",
                "-addext",
                "keyUsage=critical,keyCertSign,cRLSign",
            ]
        )
        cls.checked(
            [
                "openssl",
                "x509",
                "-in",
                str(cls.root / f"{name}.pem"),
                "-outform",
                "DER",
                "-out",
                str(cls.root / f"{name}.der"),
            ]
        )

        (cls.root / f"{name}-index").write_text("")
        (cls.root / f"{name}-serial").write_text("1000\n")
        (cls.root / f"{name}-crlnumber").write_text("1000\n")
        (cls.root / f"{name}-certs").mkdir()

    @classmethod
    def leaf(cls, name: str, server: bool, issuer: str, purpose: str, days: int) -> None:
        key, csr, cert = (cls.root / f"{name}.{suffix}" for suffix in ("key", "csr", "pem"))
        algorithm = (
            ["-newkey", "rsa:2048"]
            if name.endswith("-rsa")
            else ["-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:P-256"]
        )
        cls.checked(
            [
                "openssl",
                "req",
                "-new",
                *algorithm,
                "-noenc",
                "-keyout",
                str(key),
                "-out",
                str(csr),
                "-subj",
                f"/CN=Babel-Lab-{name}",
            ]
        )
        config = cls.root / f"{name}.cnf"
        config.write_text(
            "[ca]\ndefault_ca=issuer\n[issuer]\n"
            f"database={cls.root / (issuer + '-index')}\nserial={cls.root / (issuer + '-serial')}\n"
            f"new_certs_dir={cls.root / (issuer + '-certs')}\n"
            f"crlnumber={cls.root / (issuer + '-crlnumber')}\n"
            f"certificate={cls.root / (issuer + '.pem')}\n"
            f"private_key={cls.root / (issuer + '.key')}\n"
            "default_md=sha256\ndefault_days=1\npolicy=identity\nunique_subject=no\nx509_extensions=leaf\n"
            "[identity]\ncommonName=supplied\n[leaf]\nbasicConstraints=critical,CA:FALSE\n"
            f"keyUsage=critical,digitalSignature\nextendedKeyUsage={purpose}\n"
            f"subjectAltName=DNS:{'babel' if server else 'client'}.example.test\n"
        )
        dates = (
            ["-startdate", "20000101000000Z", "-enddate", "20010101000000Z"]
            if days == -1
            else ["-startdate", "20500101000000Z", "-enddate", "20510101000000Z"]
            if days == -2
            else ["-days", str(days)]
        )
        cls.checked(
            [
                "openssl",
                "ca",
                "-batch",
                "-notext",
                "-config",
                str(config),
                "-in",
                str(csr),
                "-out",
                str(cert),
                *dates,
            ]
        )
        cls.checked(
            [
                "openssl",
                "x509",
                "-in",
                str(cert),
                "-outform",
                "DER",
                "-out",
                str(cls.root / f"{name}.der"),
            ]
        )
        cls.checked(
            [
                "openssl",
                "pkcs8",
                "-topk8",
                "-nocrypt",
                "-in",
                str(key),
                "-outform",
                "DER",
                "-out",
                str(cls.root / f"{name}-key.der"),
            ]
        )
        key.chmod(0o600)
        (cls.root / f"{name}-key.der").chmod(0o600)

    def start(
        self, server: str = "server", options: list[str] | None = None
    ) -> tuple[subprocess.Popen[bytes], str]:
        process = subprocess.Popen(
            [
                str(BINARY),
                str(self.root / f"{server}.der"),
                str(self.root / f"{server}-key.der"),
                str(self.root / "trusted.der"),
                *(options or []),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )  # nosec B603 - fixed loopback lab binary and synthetic fixture paths
        self.addCleanup(self.stop, process)
        if process.stdout is None or not select.select([process.stdout], [], [], 5)[0]:
            self.fail("Lab did not announce a bounded listener")
        address = process.stdout.readline().decode().strip().removeprefix("LISTEN ")
        self.assertTrue(address.startswith("127.0.0.1:"), "Lab must bind only loopback")
        return process, address

    @staticmethod
    def stop(process: subprocess.Popen[bytes]) -> None:
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=3)

    def probe(
        self,
        *,
        server: str = "server",
        client: str | None = "client",
        hostname: str = "babel.example.test",
        ca: str = "trusted",
        flags: list[str] | None = None,
        message: bytes = REQUEST,
        allowed: bool = False,
        crl: str | None = None,
    ) -> None:
        process, address = self.start(
            server, ["--crl", str(self.root / f"{crl}-crl.der")] if crl else None
        )
        args = [
            "openssl",
            "s_client",
            "-quiet",
            "-connect",
            address,
            "-servername",
            hostname,
            "-verify_hostname",
            hostname,
            "-verify_return_error",
            "-CAfile",
            str(self.root / f"{ca}.pem"),
            *(flags or ["-tls1_3"]),
        ]
        if client:
            args += [
                "-cert",
                str(self.root / f"{client}.pem"),
                "-key",
                str(self.root / f"{client}.key"),
            ]
        result = command(args, data=message)
        out, error = process.communicate(timeout=6)
        self.assertNotIn(b"PRIVATE KEY", out + error)
        if allowed:
            self.assertEqual(
                result.returncode, 0, "Independent TLS client rejected a positive case"
            )
            self.assertEqual(process.returncode, 0, "Positive lab exchange failed")
            self.assertIn(b"verified lab session", result.stdout)
            self.assertIn(b"VERIFIED", out)
        else:
            self.assertNotEqual(process.returncode, 0, "Negative case reached verified lab success")
            self.assertNotIn(b"VERIFIED", out)
            self.assertNotIn(b"verified lab session", result.stdout)

    def test_tls13(self) -> None:
        self.probe(allowed=True)

    def test_tls12(self) -> None:
        self.probe(flags=["-tls1_2"], allowed=True)

    def test_current_crl_accepts_unrevoked_and_rejects_revoked_clients(self) -> None:
        for version in ("-tls1_2", "-tls1_3"):
            self.probe(flags=[version], crl="valid", allowed=True)
            self.probe(flags=[version], crl="valid", client="revoked")

    def test_expired_unknown_and_bad_signature_revocation_data_fail_closed(self) -> None:
        for crl in ("expired", "foreign", "tampered"):
            self.probe(crl=crl)

    def test_bad_or_missing_crl_is_not_a_revocation_bypass(self) -> None:
        path = self.root / "invalid-crl.der"
        for data in (None, b"", b"bad CRL", b"x" * 16385):
            if data is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(data)
            result = command(
                [
                    str(BINARY),
                    str(self.root / "server.der"),
                    str(self.root / "server-key.der"),
                    str(self.root / "trusted.der"),
                    "--crl",
                    str(path),
                ]
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(b"LISTEN", result.stdout)

    def test_certificate_replacement_is_observed_in_the_same_running_process(self) -> None:
        process, address = self.start(
            options=[
                "--replace",
                str(self.root / "server-rsa.der"),
                str(self.root / "server-rsa-key.der"),
                "--crl",
                str(self.root / "valid-crl.der"),
            ]
        )
        context = ssl.create_default_context(cafile=str(self.root / "trusted.pem"))
        context.load_cert_chain(str(self.root / "client.pem"), str(self.root / "client.key"))
        host, port = address.split(":")
        for name in ("server", "server-rsa"):
            with socket.create_connection((host, int(port)), timeout=3) as socket_peer:
                with context.wrap_socket(socket_peer, server_hostname="babel.example.test") as peer:
                    actual = peer.getpeercert(binary_form=True)
                    self.assertTrue(
                        actual is not None
                        and hashlib.sha256(actual).digest()
                        == hashlib.sha256((self.root / f"{name}.der").read_bytes()).digest()
                    )
                    peer.sendall(REQUEST)
                    self.assertEqual(peer.recv(64), b"verified lab session\n")
                    while peer.recv(64):
                        pass
        out, error = process.communicate(timeout=3)
        self.assertEqual(process.returncode, 0)
        self.assertEqual(out.count(b"VERIFIED"), 2)
        self.assertNotIn(b"PRIVATE KEY", out + error)

    def test_private_key_loss_permissions_and_mismatch_prevent_startup(self) -> None:
        path = self.root / "unusable-key.der"
        for mode in ("missing", "public", "symlink", "mismatch"):
            path.unlink(missing_ok=True)
            if mode == "public":
                path.write_bytes((self.root / "server-key.der").read_bytes())
                path.chmod(0o644)
            elif mode == "symlink":
                path.symlink_to(self.root / "server-key.der")
            elif mode == "mismatch":
                path.write_bytes((self.root / "client-key.der").read_bytes())
                path.chmod(0o600)
            result = command(
                [
                    str(BINARY),
                    str(self.root / "server.der"),
                    str(path),
                    str(self.root / "trusted.der"),
                ]
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(b"LISTEN", result.stdout)
            self.assertNotIn(b"PRIVATE KEY", result.stderr)

    def test_invalid_replacement_cannot_produce_a_second_verified_exchange(self) -> None:
        process, address = self.start(
            options=[
                "--replace",
                str(self.root / "server-rsa.der"),
                str(self.root / "client-key.der"),
            ]
        )
        context = ssl.create_default_context(cafile=str(self.root / "trusted.pem"))
        context.load_cert_chain(str(self.root / "client.pem"), str(self.root / "client.key"))
        host, port = address.split(":")
        with socket.create_connection((host, int(port)), timeout=3) as raw:
            with context.wrap_socket(raw, server_hostname="babel.example.test") as peer:
                peer.sendall(REQUEST)
                self.assertEqual(peer.recv(64), b"verified lab session\n")
                while peer.recv(64):
                    pass
        out, error = process.communicate(timeout=3)
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(out.count(b"VERIFIED"), 1)
        self.assertNotIn(b"PRIVATE KEY", out + error)

    def binding_probe(self, mode: str, replay: bytes | None = None) -> bytes:
        process, address = self.start(options=["--crl", str(self.root / "valid-crl.der")])
        args = [
            "openssl",
            "s_client",
            "-connect",
            address,
            "-servername",
            "babel.example.test",
            "-verify_hostname",
            "babel.example.test",
            "-verify_return_error",
            "-CAfile",
            str(self.root / "trusted.pem"),
            "-cert",
            str(self.root / "client.pem"),
            "-key",
            str(self.root / "client.key"),
            "-ign_eof",
            "-tls1_3",
            "-keymatexport",
            "EXPORTER-Channel-Binding",
            "-keymatexportlen",
            "32",
        ]
        client_process = subprocess.Popen(
            args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )  # nosec B603
        self.addCleanup(self.stop, client_process)
        assert client_process.stdout is not None and client_process.stdin is not None
        data = b""
        deadline = time.monotonic() + 2
        match = None
        while time.monotonic() < deadline and len(data) < 65536:
            if not select.select(
                [client_process.stdout], [], [], max(0, deadline - time.monotonic())
            )[0]:
                break
            chunk = os.read(client_process.stdout.fileno(), 4096)
            if not chunk:
                break
            data += chunk
            match = re.search(rb"Keying material: ([0-9a-fA-F]{64})", data)
            if match:
                break
        self.assertIsNotNone(match, "Independent client did not produce bounded exporter evidence")
        assert match is not None
        binding = bytes.fromhex(match.group(1).decode())
        sent = binding if mode == "matching" else replay if mode == "replay" else b"\0" * 32
        assert sent is not None
        payload = b"BABEL-TLS-CB\n" + sent
        if mode == "truncated":
            payload = payload[:-1]
        client_process.stdin.write(payload)
        client_process.stdin.flush()
        response, _ = client_process.communicate(timeout=5)
        out, error = process.communicate(timeout=3)
        self.assertNotIn(binding.hex().encode(), out + error)
        if mode == "matching":
            self.assertEqual(process.returncode, 0)
            self.assertIn(b"verified lab session", response)
        else:
            self.assertNotEqual(process.returncode, 0)
            self.assertNotIn(b"VERIFIED", out)
            self.assertNotIn(b"verified lab session", response)
        return binding

    def test_independent_tls_exporter_and_wrong_truncated_or_replayed_bindings(self) -> None:
        original = self.binding_probe("matching")
        self.binding_probe("wrong")
        self.binding_probe("truncated")
        self.binding_probe("replay", original)

    def test_tls12_does_not_advertise_the_tls13_binding_profile(self) -> None:
        self.probe(flags=["-tls1_2"], message=b"BABEL-TLS-CB\n" + b"\0" * 32)

    def test_missing_client(self) -> None:
        self.probe(client=None)

    def test_rsa_certificates_tls12_and_tls13(self) -> None:
        for version in ("-tls1_2", "-tls1_3"):
            self.probe(server="server-rsa", client="client-rsa", flags=[version], allowed=True)

    def test_future_client(self) -> None:
        self.probe(client="future-client")

    def test_untrusted_client(self) -> None:
        self.probe(client="foreign")

    def test_expired_client(self) -> None:
        self.probe(client="expired-client")

    def test_wrong_client_purpose(self) -> None:
        self.probe(client="wrong-client-purpose")

    def test_wrong_server_identity(self) -> None:
        self.probe(hostname="wrong.example.test")

    def test_untrusted_server(self) -> None:
        self.probe(ca="stranger")

    def test_expired_server(self) -> None:
        self.probe(server="expired-server")

    def test_wrong_server_purpose(self) -> None:
        self.probe(server="wrong-server-purpose")

    def test_tls11(self) -> None:
        self.probe(flags=["-tls1_1", "-cipher", "DEFAULT:@SECLEVEL=0"])

    def test_unapproved_cipher(self) -> None:
        self.probe(flags=["-tls1_3", "-ciphersuites", "TLS_CHACHA20_POLY1305_SHA256"])

    def test_wrong_application_message(self) -> None:
        self.probe(message=b"not a directory request\n")

    def test_application_budget(self) -> None:
        self.probe(message=b"x" * 65 + b"\n")

    def test_authenticated_idle_deadline(self) -> None:
        self.probe(message=b"")

    def test_plaintext_and_idle_connections_are_bounded(self) -> None:
        for payload in (b"not TLS\n", b""):
            process, address = self.start()
            host, port = address.split(":")
            with socket.create_connection((host, int(port)), timeout=3) as peer:
                if payload:
                    peer.sendall(payload)
                out, error = process.communicate(timeout=5)
            self.assertNotEqual(process.returncode, 0)
            self.assertNotIn(b"VERIFIED", out)
            self.assertNotIn(b"PRIVATE KEY", error)

    def test_scope_and_configuration_rejection(self) -> None:
        result = command([str(BINARY), "--scope"])
        self.assertEqual(result.returncode, 0)
        self.assertIn(b"no LDAP", result.stdout)
        for content in (b"", b"synthetic-private-material", b"x" * 16385):
            path = self.root / "invalid.der"
            path.write_bytes(content)
            result = command([str(BINARY), str(path), str(path), str(path)])
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(b"LISTEN", result.stdout)
            self.assertNotIn(b"synthetic-private-material", result.stderr)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(OpenSSLQualification)
    methods = [
        test.id().rsplit(".", 1)[-1] for test in suite if isinstance(test, unittest.TestCase)
    ]
    if not REQUIRED_BOUNDARY_METHODS <= set(methods):
        raise SystemExit("TLS boundary qualification cases missing")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary: dict[str, Any] = {
        "schema_version": 1,
        "scope": "synthetic TLS transport only; no AD/Windows conformance",
        "tests": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "openssl": command(["openssl", "version"]).stdout.decode().strip(),
        "methods": methods,
        "skipped": len(result.skipped),
        "binary_sha256": hashlib.sha256(BINARY.read_bytes()).hexdigest(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "production_conformance": "unrun",
        "source_revision": command(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
        .stdout.decode()
        .strip(),
        "input_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in (
                "Cargo.lock",
                "native/babel-tls-lab/Cargo.toml",
                "native/babel-tls-lab/src/lib.rs",
                "native/babel-tls-lab/src/main.rs",
                "native/babel-tls-lab/src/budget_tests.rs",
                "native/babel-tls-lab/tests/handshake.rs",
                "fuzz/fuzz_targets/tls_record.rs",
            )
        },
    }
    target = os.environ.get("BABEL_TLS_REPORT")
    if target:
        Path(target).write_text(json.dumps(summary, indent=2) + "\n")
    raise SystemExit(0 if result.wasSuccessful() and not result.skipped else 1)
