"""Independent OpenSSL/loopback probe; ephemeral synthetic keys, no AD/client conformance."""

import json
import os
import select
import socket
import subprocess  # nosec B404
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, ClassVar

BINARY = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) > 1
    else Path("target/debug/babel-tls-lab").resolve()
)
REQUEST = b"BABEL-TLS-LAB\n"


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

    def start(self, server: str = "server") -> tuple[subprocess.Popen[bytes], str]:
        process = subprocess.Popen(
            [
                str(BINARY),
                str(self.root / f"{server}.der"),
                str(self.root / f"{server}-key.der"),
                str(self.root / "trusted.der"),
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
    ) -> None:
        process, address = self.start(server)
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
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary: dict[str, Any] = {
        "scope": "synthetic TLS transport only; no AD/Windows conformance",
        "tests": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "openssl": command(["openssl", "version"]).stdout.decode().strip(),
    }
    target = os.environ.get("BABEL_TLS_REPORT")
    if target:
        Path(target).write_text(json.dumps(summary, indent=2) + "\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
