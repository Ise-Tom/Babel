# Phase 1 development progress

Status: native parser/RootDSE lab implemented; bounded filter extension in development;
Phase 1 acceptance
is **not complete**. The [phase specification](phases/phase-01.md) remains the
normative contract. [ADR 0001](adr/0001-native-ldap-lab.md) defines the narrow
implementation, resource bounds, toolchain choice and outstanding prerequisites.

## Implementation map

| Requirement | Current evidence scope | Remaining gate |
| --- | --- | --- |
| P01-01 | Rust workspace, pinned compiler/locks, formatting/Clippy, generated parser tests, sanitizer fuzz, dependency/license/SBOM and packaging gates | All later native components need corresponding checks; no general security assessment |
| P01-02 | Not implemented | Stable SID/GUID/schema/ACL and denied-state invariants |
| P01-03 | Not implemented; lab has no state | Transactional store/journal and kill/recovery tests after design approval |
| P01-04 | RootDSE base-search subset; bounded presence/objectClass equality/boolean filter extension exercised by ldap3 in the development PR | DNS, general directory/schema/matching rules and Windows reference-client evidence |
| P01-05 | Credential binds explicitly rejected, not authenticated | Reviewed Kerberos/PAC/password/key lifecycle, secure transport and actual authentication |
| P01-06 | Not implemented | Windows domain membership, secure channel and machine credential rollover |
| P01-07 | Not implemented | Policy directory/SYSVOL state and actual client application/recovery |
| P01-08 | Not implemented | Delegated account/group/password API/CLI/UI and authorization |
| P01-09 | Loopback, allocation/request/time limits and static diagnostics tested | Linux service packaging/install/reboot, TLS, DNS/time preflight and role privilege model |
| P01-10 | Supported subset/limitations are explicit in ADR, CLI and tests | Continue per-operation inventory as implementation grows; no production claims |

## Build, run and verify

Install Rust through its supported rustup route with normal TLS/checksum
verification. `rust-toolchain.toml` activates the exact compiler/components.
On this cloud instance tools were installed under `/workspace/.babel-tools`;
source `/workspace/.babel-tools/env` if cargo is not on PATH. Other development
machines use their normal rustup installation, not this cloud-specific location.

From the repository root:

```sh
cargo build --workspace --locked
cargo fmt --all --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --all-targets --locked
# Use the hash-locked Python tooling environment described in the README:
python native/babel-ldap/tests/smoke_ldap.py target/debug/babel-ldap
cargo run --locked -p babel-ldap -- --listen 127.0.0.1:1389
```

The filter extension and its limits are described in
[ADR 0002](adr/0002-bounded-rootdse-filters.md). The manual listener is a loopback lab endpoint; stop it with Ctrl-C. An
independent client can ask the empty DN for `supportedLDAPVersion`/`vendorName`
using a base `(objectClass=*)` search. Do not expose it publicly or send real
credentials. It cannot join a computer, serve accounts or replace AD.

## CI and evidence boundaries

The native reusable workflow pins compiler/fuzz/tool versions and runs build,
format/Clippy, unit/property/transport tests, independent LDAP smoke, instrumented
core line coverage, bounded sanitizer fuzz and dependency/license/source audit.
It produces native CycloneDX reports and an internal lab-binary archive/checksum.
These are development evidence, not published installable product releases.
The existing aggregate CI gate waits for native jobs too; new source trees stay
rejected unless explicitly registered alongside their checks.

Core line coverage is gated at 90% excluding test/CLI dispatch files. The actual
lab process is separately exercised by the independent client and negative CLI
checks; protocol/security scenarios matter beyond percentages. Fuzzing uses
synthetic corpus only, with a short PR budget and a longer scheduled budget;
passing it does not prove absence of parser vulnerabilities.

D-01/D-02/D-04/D-05/D-06 and the Windows lab remain open where specified in the
[decision register](decisions.md). No identity/key/storage format, release
license, Windows conformance result or production hardware capacity is invented.
