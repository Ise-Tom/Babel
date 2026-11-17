# ADR 0001 — Rust bounded LDAP laboratory increment

Status: accepted for the initial non-credential-bearing parser/RootDSE slice.
This resolves only the toolchain boundary of D-03, not storage, key formats,
Windows interoperability, licensing or the rest of Phase 0/1.

## Decision and rationale

Use Rust 1.100.0 (edition 2024), pinned in `rust-toolchain.toml`, for the native
core's first bounded BER/LDAP implementation. It permits explicit checked byte
parsing and ownership with `unsafe` forbidden in this crate. No runtime crate
dependencies, TLS, cryptography or persistent data are introduced. The crate is
`publish = false`; project license selection and product release remain blocked
by D-01. Rust/std and development dependencies still have third-party obligations.

Use exact, locked proptest development dependencies for generated invariants,
pinned libFuzzer tooling/nightly for parser fuzzing, and an independent ldap3
client for real loopback protocol checks. These are test tools, not Python server
implementation. Review exact toolchain, compiler advisories and tooling pins
regularly; a pin prevents drift but does not make an old version safe forever.

## Implemented wire and transport boundaries

- LDAPv3 anonymous simple bind to public lab data only; any credential/SASL bind
  fails. Request objects/debug output never retain or echo DNs/password bytes.
- Base-scope empty-DN RootDSE search with `(objectClass=*)`, projected
  `objectClass`, `supportedLDAPVersion`, `vendorName` and `vendorVersion`.
  Explicit names are case-insensitive; `*`, `+`, `1.1` and `typesOnly` are tested.
- The development extension in [ADR 0002](0002-bounded-rootdse-filters.md) adds
  bounded presence/objectClass equality and AND/OR/NOT with Undefined semantics.
- No AD capability OIDs, naming contexts, StartTLS, schema, credentials, accounts,
  controls, general directory/schema matching or domain operations are advertised. Unknown
  controls/malformed requests close the session; unsupported operations never
  return a fabricated authentication or account success.
- Maximum 16 KiB total frame, four BER length octets, 64 attributes of 64 bytes,
  1,024-byte base/bind DNs; checked lengths before body allocation. The filter
  extension additionally enforces depth/node/assertion budgets before evaluation.
- Loopback-only single-active-connection service, five-second **total** session
  budget enforced on every read/write, 32 requests/session. Fragmented/coalesced
  TCP messages are supported. A slow/malformed client cannot create unbounded
  threads/queues or extend its deadline by sending one byte at a time.
- Diagnostics are static and credential-free. There is no persistent state.
  Plaintext loopback is limited to synthetic public lab traffic; production
  TLS/channel protections are not claimed. Never send real credentials here.

The lab service is a genuine read-only LDAP protocol endpoint, not a stub that
accepts passwords or claims to be a domain controller. Its sequential listener
and tiny limits deliberately provide no production availability/capacity promise.

## Evidence and progression

See [Phase 1 progress](../phase-01-progress.md) for actual checks and command
reproduction. Unit/negative/property, framing/deadline, independent-client,
coverage and sanitizer-fuzz jobs must pass before this source scope is admitted.
Cargo lock checks, dependency/license/source audit and native CycloneDX reports
cover both the core and fuzz graphs. Private unpublished workspace-license
exemption is explicit; it cannot authorize registry/public product distribution.

This is partial P01-01/P01-04/P01-09/P01-10 evidence. Stable identity/schema/ACL,
durable storage, DNS, authentication/key lifecycle, Windows membership and
GPO/SYSVOL remain unimplemented and cannot be marked passed. Windows reference
lab, storage/replication ADRs and crypto/key custody must precede valuable
credential-bearing writes. No security assessment or full AD conformance is
implied by this bounded subset.
