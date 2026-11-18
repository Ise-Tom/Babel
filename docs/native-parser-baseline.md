# Qualified native toolchain and bounded parser baseline

Status: **full P00-04 Phase 0 criterion packet complete; owner validation pending**.
The qualified baseline is `linux-x86_64-gnu-bounded-parser-v1`. It covers the
Rust toolchain and existing bounded BER/LDAP parser, not a functioning AD server.

## Platforms, versions and alternatives

| Input | Selected qualification boundary |
| --- | --- |
| Host / target | Linux x86_64, GNU ABI; Ubuntu 24.04 in required hosted CI and Debian 13 locally. Record actual OS/full Debian version, kernel, runner image version and binary/compiler hashes. No ARM, musl or Windows/macOS server build is qualified |
| Compiler | Rust 1.100.0, edition 2024; rustfmt, Clippy, LLVM tools and Rust docs pinned in `rust-toolchain.toml`. Capture actual compiler commit, host and LLVM version |
| Parser | `babel-ldap`; no normal/build crate dependencies or build scripts/FFI linkage. Both library and binary roots forbid unsafe Rust. Standard-library/libc internals remain an upstream trust boundary |
| Generated tests / independent client | Locked proptest 1.12.0; hash-locked ldap3 probe. Test-only dependencies are audited too |
| Sanitizer fuzz | nightly-2026-11-17, cargo-fuzz 0.13.2, locked libfuzzer-sys 0.4.13; bounded real decoder/responder/framing target with seed 1. Nightly is a test tool, not the shipping compiler |
| Security / coverage tools | cargo-deny 0.21.0, cargo-llvm-cov 0.9.1, hash/commit-pinned remaining CI tools. Record actual GNU readelf version used for ELF observations |

Rust was chosen for checked byte parsing, ownership/lifetimes and explicit
bounded allocation without a garbage collector. C/C++ would require substantially
more manual memory/lifetime review at the protocol boundary. Go is memory-safe
and suitable for some future agents, but adds GC/runtime budgeting and another
server toolchain; it is not required for the initial core. Python remains
orchestration/test tooling; TypeScript remains administration/dashboard tooling.
These are maintainability and boundary choices, not measured language benchmarks.
Rust does not supply AD semantics, authorization correctness or immunity to DoS.

Windows/Linux/macOS **client** compatibility is independent of the server compiler
target. Exact client platforms remain P00-12; TLS/provider and Kerberos/PAC choices
remain P00-13/P00-14, and the storage driver retains its accepted P00-15 profile.
Babel's TLS/provider and driver crates are separate qualified boundaries; their
existence does not make the dependency-free parser a claim of an all-memory-safe
server. In particular ring contains native C/assembly.

## Parser, optimized build and evidence

The existing parser/transport has 16-KiB frame limits, checked BER lengths, bounded
attribute/filter/depth/assertion work, finite session/request budgets, redacted
errors and denial of credentials/unsupported AD behavior. See
[ADR 0001](adr/0001-native-ldap-lab.md) and [ADR 0002](adr/0002-bounded-rootdse-filters.md)
for the exact implemented behavior and test cases.

Optimized workspace builds now keep integer overflow checks enabled. A real Rust
test executes overflowing nonconstant arithmetic and requires a visible failure
in **both debug and release**; explicit checked/wrapping protocol arithmetic still
requires code review. Independent ldap3/OpenSSL probes exercise release binaries.
The Linux parser executable must have PIE, full RELRO/immediate binding and an
explicit non-executable stack. These mitigations do not replace parser correctness.

The [collector](../scripts/qualify_parser_baseline.py) cross-checks the compiler
pin, host/target, release configuration, crate roots, actual Cargo normal/runtime
closure and built ELF. It rejects unreviewed parser runtime/build/FFI expansion,
changed toolchains/hosts or missing mitigations. The retained `parser-baseline.json`
binds source revision, manifests/lockfiles/policy hashes, exact binary and ELF report,
compiler/LLVM/readelf and host observations. It is a build observation; the
**passing full CI run** separately supplies actual unit/property/transport/client,
coverage, advisory/license/source and sanitizer-fuzz results. Synthetic collector
unit fixtures are never product observations.

Required CI runs debug and release parser tests, strict formatting/Clippy,
independent probes, >=90% library line coverage, both locked graph audits and
bounded sanitizer fuzz. A failed, skipped or cancelled prerequisite fails the
native/full aggregate gate. Fuzz run/time/RSS ceilings are budgets, not exhaustive
proof. Archive extraction reruns the real probes and verifies retained notices.

## Licenses, advisories and maintenance

Babel uses owner-selected Apache-2.0/DCO. Rust is distributed under its actual
MIT/Apache and bundled component terms; the standard-library copyright catalog
and referenced license texts travel with native lab artifacts. The actual GNU
system-runtime copyright/LGPL/GPL texts are also retained; those OS libraries
remain dynamically replaceable and are not copied into the archive. Development and
fuzz graph terms, including NCSA libFuzzer, remain in the audit. See the
[redistribution register](licensing-and-redistribution.md); a compiler choice does
not settle specification or reference-image rights.

Reviewed the [Rust 1.100.0 release](https://github.com/rust-lang/rust/releases/tag/1.100.0)
on 18 November 2026 (published 12 November). Its changed intermediate Cargo layout
requires retesting path-sensitive coverage/packaging tools; current probes verify
the actual artifacts. Its default use of packaged install lockfiles preserves the
intent of our explicitly versioned/locked tooling installs. The cited SGX library
soundness fix is not evidence about the selected GNU/Linux target. No blanket
compiler/platform vulnerability certification is claimed.

Ise-Tom owns current development maintenance: daily required Cargo advisory scans
and scheduled CI; weekly dependency proposals; prompt compiler/std/provider
security-release review through Rust release/security announcements and RustSec;
monthly review of manually pinned tools/nightly, OS support and license changes.
Cargo advisory scans do not cover every compiler, libc or base-image vulnerability.
Review those upstream/security inputs and rerun the full qualification before
updating or extending the profile; an unsupported/unmaintained profile must stop
being offered rather than silently retaining an obsolete pin.

Any new target, normal/build parser dependency, FFI/build script, toolchain,
release policy or relevant parser semantics requires scoped review, updated
notices and fresh build/negative/client/coverage/fuzz evidence. Profile checks are
review safeguards, not protection against a maintainer rewriting CI. No production
availability/capacity, credential handling or AD conformance is accepted here.
