# ADR 0006 — Rustls transport qualification experiment

Date: 18 November 2026. Status: **implemented lab candidate, production selection
and P00-13 acceptance pending**. Applies to P00-04/P00-06/P00-13 and SEC-04/SEC-10.
Linux hosting and the native AD direction remain unchanged.

## Decision and alternatives

Qualify Rustls **0.23.46**, using its explicit **ring 0.17.14** provider, in a
standalone Rust experiment before integrating any directory transport. Cargo
locks versions and registry checksums; Rustls default features are disabled and
only `std`, `ring`, `tls12` enabled. `rustls-webpki 0.103.17` performs certificate
verification. Test-only `rcgen 0.14.10` generates synthetic identities; it is not
a product certificate authority. No custom cipher, TLS engine or verifier is used.

Rustls offers a Rust protocol implementation and explicit trust/provider APIs.
OpenSSL bindings offer a mature independent stack and broader provider options,
but add a C/FFI and system/build configuration boundary. Rustls with aws-lc-rs
offers another maintained provider and separately qualified FIPS options; those
build, distribution, platform and validation requirements have not been tested
here. Native OS TLS would require different hosting implementations. Ring keeps
this first Linux experiment bounded; it is not a final platform or HSM decision.

The exact upstream code is fetched from crates.io using Cargo.lock checksums:
[Rustls source](https://github.com/rustls/rustls),
[ring source](https://github.com/briansmith/ring), and
[WebPKI source](https://github.com/rustls/webpki). Cargo advisory/source/license
checks cover both workspace and fuzz graphs, including development dependencies.
These passing checks are dated evidence, not lifetime maintenance guarantees.
Review advisories on scheduled CI, keep compiler/provider pins current, review
breaking policy changes and rerun independent, property and fuzz tests on upgrades.
The isolated crate is removable without changing directory disk formats or LDAP.

## Implemented boundary

`babel-tls-lab` binds loopback on an ephemeral port, accepts one connection within
five seconds, and allows two seconds for the entire exchange. It accepts only the
fixed synthetic `BABEL-TLS-LAB` message and returns a fixed acknowledgment. There
are no accounts, directory operations, privileged actions or authentication grants.

Both TLS 1.2 and 1.3 are enabled with an explicit AES-GCM/ECDHE suite allowlist.
Client certificates are mandatory and verified against one explicitly supplied
CA. The independent client verifies the server CA, hostname and purpose. No
anonymous verifier, TLS 1.0/1.1, early data, session cache or session tickets are
enabled. This is a deliberately narrow lab profile; mandatory client certificates
and AES-only policy are **not** decisions about production LDAP compatibility.

DER inputs are 1–16,384 bytes, connection input/output each limited to 65,536
bytes, TLS buffering/fragments to 4,096 bytes, application request to 64 bytes and
individual socket reads to 8,192 bytes. Deadlines use a monotonic clock and are
reapplied to each socket operation. Errors are static and do not print keys or
request contents. The CLI reads bounded local DER files; it is not a production
secret loader, chain builder or multi-client service.

## Executed evidence and CI

- Seven Rust tests exercise mutual TLS, exact provider policy, certificate/key
  rejection, identity/trust/time/purpose failures, ciphertext tampering, transport
  budgets and property-generated invalid records. Exporter values agree across
  peers and differ by context; this is only a prerequisite for channel binding.
- Nineteen independent OpenSSL test methods include TLS 1.2/1.3 with EC and RSA
  leaf identities, missing/untrusted/expired/future/wrong-purpose clients,
  invalid server identity/trust/expiry/purpose, obsolete TLS and unapproved cipher
  rejection, application limits, idle/plaintext deadlines and redacted errors.
- The required native job runs release and instrumented probes, retains OpenSSL
  version/outcome reports, and separately requires 90% TLS-library line coverage.
  CLI dispatch and test code are excluded; the CLI is exercised by subprocess tests.
- The bounded sanitizer fuzzer feeds malformed TLS records into the real server
  state machine: 20,000 iterations/20 seconds per PR, 200,000/120 seconds scheduled,
  16-KiB input and 512-MiB RSS ceilings. Both are stop ceilings, not minimum work.

Run locally with the pinned Rust toolchain and installed OpenSSL:

```sh
cargo test --workspace --all-targets --locked
cargo build --workspace --release --locked
python native/babel-tls-lab/tests/interop_tls.py target/release/babel-tls-lab
cargo +nightly-2026-11-17 fuzz run tls_record -- -runs=20000 -max_total_time=20 -max_len=16384 -rss_limit_mb=512 -seed=1
```

Only synthetic temporary identities are used. OpenSSL generates keys under a
private temporary directory and removes them; Rust in-memory fixture validity
ranges are test conveniences, not approved certificate lifetime policy. Rejection
tests verify controls are enforced; they do not grant access or weaken verifiers.

## Rights and distribution

The actual selected runtime source terms were reviewed for this lab: Rustls is
Apache-2.0 OR ISC OR MIT; ring is Apache-2.0 AND ISC with additional bundled
copyright/permission texts; WebPKI and untrusted use ISC, subtle BSD-3-Clause,
and other selected crates MIT/Apache-2.0. ISC and BSD-3-Clause are added to the
reviewed permissive Cargo policy. BSD copyright, permission, disclaimer and
non-endorsement terms and all applicable notices must travel with distribution.
This does not allow other unreviewed license families or copying upstream code
without its terms. Full graph SPDX/advisory policy remains mandatory.

The experimental archive contains both lab binaries and a `notices/` tree with
the project LICENSE/NOTICE/DCO, actual nested dependency notice files and Rust's
`COPYRIGHT-library.html` plus its referenced license texts. The collector uses
the selected normal dependency closure from platform-filtered Cargo metadata;
the separate SBOM also covers development/fuzz dependencies. The generated
manifest retains package versions, SPDX expressions and file SHA-256/byte counts.
CI extracts the archive, verifies all notice bytes and reruns both lab probes.
The Rust catalog can list components not linked into these binaries; it is not
a binary-link inventory or legal clearance for future product packages.

## Unqualified production obligations

LDAPS/StartTLS negotiation, LDAP bind/signing policy and downgrade state handling
are not integrated. SASL/GSSAPI channel binding, Windows EPA and Kerberos tickets
need exact protocol/reference tests; matching a generic exporter does not satisfy
them. No Windows, macOS or domain-client compatibility is claimed, and all 60
Phase 0 conformance scenarios remain unrun.

Revocation/CRL/OCSP policy, certificate chains/rotation/reload, key zeroization and
encrypted custody, HSM/KMS/provider failure, entropy/clock fault behavior,
multi-tenant trust, production concurrency and capacity, supported CPU/OS builds
and independent security assessment remain open. Babel source forbids unsafe
Rust; ring contains native C/assembly, so this is not an all-memory-safe or FIPS
validation claim. Client OS trust/provider behavior requires separate evidence.
P00-13 and the broader dependency blocker stay in progress.
