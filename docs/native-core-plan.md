# Native AD-compatible core: implementation plan

Decision: build and maintain Babel's own AD-compatible directory/domain core.
Samba AD DC will not be a required runtime, bundled domain controller or source
of persistent directory state. This is an explicit architecture direction from
the owner, not a claim that an independent domain controller already exists.
The existing CI and product/security/endpoint roadmaps remain in place.

## Scope and reuse boundary

The first production contract is unchanged: Linux-hosted identity/password
management, Windows domain join, Kerberos/LDAP, AD DNS discovery, GPO/SYSVOL,
trusts, schema/functional levels, multi-site replication and recovery for 10,000
identities across three sites. Partial laboratory milestones are development
previews, not a reduced first-production release.

A native core does not mean writing cryptography, TLS, storage engines or every
protocol utility from scratch. Evaluate maintained libraries with suitable
licenses and supported security properties. Babel owns its identity model,
authorization, protocol integration, persistence format, replication semantics
and conformance tests. Library reuse must not introduce an undeclared dependency
on Samba's domain database, administration tools or daemon behavior.

Microsoft AD in an isolated licensed lab is the interoperability reference.
Samba can be an optional secondary behavioral comparison, never a substitute
for Windows client tests or a requirement to run Babel. Use published protocol
specifications and document observed behavior; reference implementations do not
grant permission to copy their source or fixtures. Review specification terms,
dependency licenses and relevant distribution/patent obligations before reuse.

## Dependency-ordered milestones before the first vertical slice

These subdivide Phases 0–1 of the [main roadmap](roadmap.md). They do not add
finished functionality or claim that the current tooling CI covers a server.

| Milestone | Deliverable | Required evidence / next-step dependency |
| --- | --- | --- |
| N-00 — Compatibility contract and lab | Versioned protocol/operation matrix, selected Windows builds and functional levels, synthetic fixtures, private reporting and project-license decision | Each AD/SEC/PLAT/IAM requirement maps to a named operation and test owner; disposable Windows reference and Linux host networking, DNS/time and cleanup are reproducible |
| N-01 — Core/toolchain and parser boundaries | Memory-safe core skeleton, explicit public/internal error types, bounded codecs, cancellation/resource budgets, reviewed library inventory and crypto/key-provider interfaces | Language/toolchain ADR, locked builds, lint/types/tests, SAST/dependency/SBOM checks and real parser-fuzz smoke jobs added before the scope guard accepts source; no custom cryptography |
| N-02 — Identity model and durable storage | SID/GUID identity, normalized DN/schema/attributes, group/ACL model, atomic mutations, indexes, durable journal, versioned formats and recovery metadata | Property/negative tests for identity preservation, Unicode/DN collisions, authorization, nested groups, crash consistency and versioned snapshot round-trip; no reliance on a Samba database |
| N-03 — Discovery and bounded read-only directory | AD DNS/SRV/DC-locator discovery slice and LDAP RootDSE/search subset in an explicitly isolated lab | Actual supported client queries, malformed input limits, referral/paging behavior for the declared subset, restricted anonymous results; no domain-join claim from a successful LDAP query |
| N-04 — Authentication and authorized writes | Reviewed Kerberos integration, principal/key lifecycle, applicable PAC handling, secure LDAP bind and ACL-checked account/password changes | Real client authentication and denied operations, replay/downgrade/key-rotation tests, redacted audit and durable write recovery; password and ticket formats reviewed before persistent use |
| N-05 — Windows membership and administration slice | Required SMB/RPC/Netlogon membership paths, computer-account secure-channel/rotation, minimal delegated administration API/UI | Windows domain join, login, password change, machine-password rollover and negative secure-channel tests against native Linux-hosted services |
| N-06 — Initial GPO and SYSVOL slice | Policy objects, file permissions/version agreement, supported policy creation/application and reconciliation | Real Windows resultant policy, policy filtering and a verified change/revert across directory and SYSVOL; no claim of DFS-R/complete GPO coverage from file copying alone |

N-03 and parser experiments may proceed against synthetic data while N-02 is
being designed, but production credential-bearing mutations cannot bypass the
authorization/durability gates. Broader AD protocol behavior, functional levels,
trusts and migration complete Phase 2; replication/fault recovery completes Phase
3. Do not expand early UI features faster than the underlying security contract.

## Decisions that must precede persistent credentials or multi-controller writes

- Define stable SID/GUID allocation, schema extension rules, DN normalization,
  ACL evaluation/inheritance and group nesting bounds. User renames must not
  change identity or erase permission/trust relationships.
- Define password/verifier and Kerberos principal/key representations, encryption
  at rest, key custody/rotation and crash recovery using reviewed protocols and
  libraries. Never invent a new password format and call it AD-compatible.
- Specify the storage transaction boundary and which operations are durably
  acknowledged. Separate local recovery journaling from the distributed change
  model; a durable database alone is not AD replication.
- Design object/attribute change metadata, origin IDs, conflict ordering,
  tombstones/garbage collection, replication cursors, schema changes, urgent
  revocation behavior and clock-skew handling before fixing a disk format.
- Map native metadata and authentication to MS-DRSR and MS-ADTS requirements,
  including invocation IDs, USN/rollback handling, replication authorization,
  naming contexts, FSMO and global catalog behavior. Generic database Raft or
  a custom change feed is not automatically a compatible multi-master AD model.
- Establish versioned backup/export and upgrade contracts preserving identities,
  ACLs, policies, keys and replication recovery metadata. Rehearse upgrades and
  rollback/forward recovery; do not describe credentials as ordinary CSV data.

The initial lab may be single-controller; that must not silently establish a
storage format that makes the required multi-controller contract impossible.
Any irreversible model decision requires explicit design review and fixtures
covering upgrade/recovery before a public preview stores valuable credentials.

## Native-core conformance and security gates

Track exact specification revision, operation, client/build, expected behavior,
observed result and test artifact. Failed, unsupported, skipped and unrun cases
remain visible; only passing implemented operations count as supported.

| Area | Required validation |
| --- | --- |
| LDAP / directory / access | AD schema and controls, paging/referrals, GC, ACL filtering, denied reads/writes, stable identifiers, bounded nesting and filter/parser abuse |
| Kerberos / password / key lifecycle | AS/TGS and PAC behavior, SPNs, supported encryption types, delegation, replay, clock skew, password changes/resets, service/trust/ticket-signing rotation and revocation limits |
| DNS / time / membership | Secure discovery/updates, client DC locator, machine accounts, Netlogon, SMB/RPC signing/sealing, credential/secure-channel rollover and unsupported-client rejection |
| Policy delivery | GPO directory/file consistency, inheritance/filtering, SYSVOL ACLs and application on real clients, including interrupted updates and recovery |
| Multi-controller / trusts | DRS interoperability for the selected profile, concurrent writes, partitions/rejoin, deletions, topology/FSMO, forest trusts, SID filtering, schema/functional-level changes and migration |
| Linux operations / durability | Fresh install, reboot, crash/restart, disk exhaustion, encrypted isolated restore, upgrades, safe failure and 10k/three-site mixed-load qualification |

Property-based and fuzz tests cover untrusted parser/state-machine boundaries;
authorization tests exercise denied operations as well as positive paths.
Independent review must examine the integrated credential/authorization and
replication design, not just dependency scanner results. A standards checklist
or a green unit suite cannot replace interoperability testing.

## Portability and management boundaries

Linux is still the server host target. The server's language does not guarantee
all-OS hosting or all-client compatibility. Windows/Linux client behavior and
future macOS clients are separate supported-version matrices. Remote-support,
patch and EDR agents still require platform APIs, packaging and signing tests.

Keep administration, telemetry and endpoint execution behind versioned service
interfaces with explicit authorization. Their service accounts do not get direct
raw-store or replication-secret access. Only core-owned mutation paths may
change directory security state; the control plane is not an alternate database
writer. Authentication must continue when the UI or endpoint modules stop.

## First implementation change

After the N-00 lab/contract and N-01 toolchain/library design are reviewable,
introduce the smallest bounded protocol/parser core with its executable build,
unit/property tests, fuzz smoke, SAST/dependency and packaging jobs. Extend
`check_ci_scope.py` only in that same reviewed change. Start the read-only
LDAP/discovery slice after the identity-model design; label each implemented
operation precisely. Do not ship a placeholder authentication server or bypass
the new CI guard merely to create an application skeleton.

This document changes the architecture and delivery sequence. No native server
source, Windows lab, storage engine or cryptographic implementation is supplied
by this planning change, and no additional production gate is marked passed.
