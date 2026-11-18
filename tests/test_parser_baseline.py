"""Observe a declared compiler/platform/binary without inventing AD or fuzz results."""

import copy
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import qualify_parser_baseline as baseline  # noqa: E402

COMPILER = (
    "rustc 1.100.0 (synthetic test fixture)\nrelease: 1.100.0\n"
    "host: x86_64-unknown-linux-gnu\ncommit-hash: " + "a" * 40 + "\nLLVM version: fixture\n"
)
ELF = (
    "Type: DYN (Position-Independent Executable file)\n"
    " GNU_RELRO 0x1 0x2 R 0x1\n GNU_STACK 0x0 0x0 RW 0x1\n"
    "(FLAGS) BIND_NOW\n(FLAGS_1) Flags: NOW PIE\n"
    "(NEEDED) Shared library: [libc.so.6]\n"
)


class ParserBaseline(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in (
            "rust-toolchain.toml",
            "Cargo.toml",
            "Cargo.lock",
            "deny.toml",
            "fuzz/Cargo.toml",
            "fuzz/Cargo.lock",
            "native/babel-ldap/Cargo.toml",
            "native/babel-ldap/src/lib.rs",
            "native/babel-ldap/src/main.rs",
        ):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
        self.binary = self.root / "synthetic-elf"
        self.binary.write_bytes(b"\x7fELF\x02\x01" + b"\0" * 10 + b"\x03\x00\x3e\x00")
        self.meta = {
            "packages": [
                {
                    "id": "parser",
                    "name": "babel-ldap",
                    "source": None,
                    "license": "Apache-2.0",
                    "links": None,
                    "dependencies": [{"kind": "dev"}],
                    "targets": [{"kind": ["lib"]}, {"kind": ["bin"]}],
                }
            ],
            "resolve": {"nodes": [{"id": "parser", "deps": []}]},
        }
        self.compiler = COMPILER
        self.elf = ELF
        self.os = {"ID": "ubuntu", "VERSION_ID": "24.04", "PRETTY_NAME": "Synthetic Ubuntu fixture"}

    def collect(self):
        return baseline.collect(
            self.root,
            self.meta,
            self.compiler,
            self.elf,
            "GNU readelf fixture\n",
            self.binary,
            self.os,
            "b" * 40,
            "synthetic-runner",
        )

    def test_supported_hosts_retain_exact_source_inputs_and_binary_not_product_claims(self):
        report = self.collect()
        self.assertEqual(report["source_revision"], "b" * 40)
        self.assertEqual(report["parser_runtime_crates"], [])
        self.assertEqual(report["system_shared_libraries"], ["libc.so.6"])
        self.assertEqual(report["product_ad_conformance"], "unrun")
        self.assertEqual(report["owner_acceptance"], "not_inferred")
        self.assertEqual(len(report["input_sha256"]), 7)
        self.os.update(ID="debian", VERSION_ID="13", DEBIAN_VERSION_FULL="fixture")
        self.assertEqual(self.collect()["host"]["DEBIAN_VERSION_FULL"], "fixture")
        self.binary.write_bytes(self.binary.read_bytes() + b"fixture")
        self.assertNotEqual(report["binary_sha256"], self.collect()["binary_sha256"])

    def test_compiler_platform_and_host_drift_do_not_qualify(self):
        for key, value in (("ID", "windows"), ("VERSION_ID", "26.04")):
            old = self.os[key]
            self.os[key] = value
            with self.assertRaisesRegex(ValueError, "Host"):
                self.collect()
            self.os[key] = old
        for before, after in (
            ("release: 1.100.0", "release: 1.99.0"),
            ("x86_64-unknown-linux-gnu", "aarch64-unknown-linux-gnu"),
            ("a" * 40, "main"),
            ("LLVM version: fixture", ""),
        ):
            self.compiler = COMPILER.replace(before, after)
            with self.subTest(before=before), self.assertRaises(ValueError):
                self.collect()

    def test_changed_toolchain_components_and_release_overflow_policy_fail(self):
        path = self.root / "rust-toolchain.toml"
        original = path.read_text()
        for before, after in (("1.100.0", "1.99.0"), ('"clippy", ', "")):
            path.write_text(original.replace(before, after))
            with self.assertRaises(ValueError):
                self.collect()
        path.write_text(original)
        path = self.root / "Cargo.toml"
        path.write_text(
            path.read_text().replace("overflow-checks = true", "overflow-checks = false")
        )
        with self.assertRaisesRegex(ValueError, "overflow"):
            self.collect()

    def test_runtime_build_ffi_and_source_expansions_need_requalification(self):
        original = copy.deepcopy(self.meta)
        for key, value in (
            ("source", "git+unreviewed"),
            ("license", None),
            ("links", "ffi"),
            ("dependencies", [{"kind": None}]),
            ("dependencies", [{"kind": "build"}]),
            ("targets", [{"kind": ["custom-build"]}]),
        ):
            self.meta = copy.deepcopy(original)
            self.meta["packages"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.collect()
        self.meta = original
        self.meta["resolve"]["nodes"][0]["deps"] = [
            {"pkg": "foreign", "dep_kinds": [{"kind": None}]}
        ]
        self.meta["resolve"]["nodes"].append({"id": "foreign", "deps": []})
        with self.assertRaisesRegex(ValueError, "closure"):
            self.collect()
        self.meta["packages"] = []
        with self.assertRaisesRegex(ValueError, "metadata"):
            self.collect()

    def test_both_crate_roots_keep_the_unsafe_prohibition(self):
        for name in ("lib.rs", "main.rs"):
            path = self.root / "native/babel-ldap/src" / name
            original = path.read_text()
            path.write_text(original.replace("#![forbid(unsafe_code)]", "#![allow(unsafe_code)]"))
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "unsafe"):
                self.collect()
            path.write_text(original)

    def test_missing_linked_oversized_wrong_arch_and_non_pie_binaries_fail(self):
        original = self.binary.read_bytes()
        for raw in (
            b"",
            b"not an ELF" * 3,
            original[:18] + b"\xb7\x00",
            original[:16] + b"\x02\x00" + original[18:],
        ):
            self.binary.write_bytes(raw)
            with self.assertRaises(ValueError):
                self.collect()
        self.binary.unlink()
        self.binary.symlink_to(self.root / "Cargo.toml")
        with self.assertRaisesRegex(ValueError, "Regular"):
            self.collect()
        self.binary.unlink()
        with self.assertRaisesRegex(ValueError, "Regular"):
            self.collect()
        with self.binary.open("wb") as stream:
            stream.truncate(64 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(ValueError, "size"):
            self.collect()

    def test_pie_relro_immediate_binding_and_nonexec_stack_cannot_disappear(self):
        for before, after in (
            ("Type: DYN", "Type: EXEC"),
            ("NOW PIE", "NOW"),
            ("GNU_RELRO", "OTHER"),
            ("BIND_NOW", "OTHER"),
            ("GNU_STACK", "OTHER"),
            (" RW ", " RWE "),
        ):
            self.elf = ELF.replace(before, after)
            if before == "BIND_NOW":
                self.elf = self.elf.replace("NOW PIE", "PIE")
            with self.subTest(before=before), self.assertRaises(ValueError):
                self.collect()
        self.elf = ELF.replace("(FLAGS) BIND_NOW\n", "")
        self.assertIn("full_RELRO", self.collect()["protections"])
        self.elf = ELF + " GNU_STACK 0 0 RW 1\n"
        with self.assertRaises(ValueError):
            self.collect()

    def test_source_revision_and_elf_inspector_cannot_be_unknown(self):
        for revision, inspector in (
            ("main", "GNU readelf fixture"),
            ("b" * 40, "unreviewed inspector"),
        ):
            with self.assertRaises(ValueError):
                baseline.collect(
                    self.root,
                    self.meta,
                    COMPILER,
                    ELF,
                    inspector,
                    self.binary,
                    self.os,
                    revision,
                    "fixture",
                )
