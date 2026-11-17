# Native-core implementation dependencies

Babel owns its native AD-compatible directory/domain core. Samba AD DC, its
persistent database and administration tools are not required at runtime.
Reviewed protocol/TLS/crypto/storage libraries are permitted; writing custom
cryptography or an entire storage engine is not the meaning of native ownership.

The full design is now in [architecture](architecture.md), [Phase 0](phases/phase-00.md),
[Phase 1](phases/phase-01.md) and subsequent [phase specifications](phases/README.md).
This map preserves N-00–N-06 terminology while replacing summary-only planning
with explicit state, security, capacity and acceptance requirements.

| Native milestone | Detailed phase design and dependency | Acceptance boundary |
| --- | --- | --- |
| N-00 | Phase 0 contract, reference lab, ownership/license and evidence model | Exact supported client/protocol matrix; synthetic isolated Windows/Linux lab |
| N-01 | Phase 0 toolchain/library ADR, then Phase 1 bounded native core | Locked build, lint/types/property/parser-fuzz/security/packaging jobs exist before scope extension |
| N-02 | Phase 0 identity/storage/replication design, then Phase 1 transactional model | Stable SID/GUID/schema/ACL and local durable-journal invariants with crash/negative tests |
| N-03 | Phase 1 read-only discovery/LDAP subset | Real declared client operations, bounded parser/query behavior; not a domain-join claim |
| N-04 | Phase 1 reviewed Kerberos/key lifecycle and authorized writes | Actual auth/password flows, replay/downgrade/rotation and denied-operation evidence |
| N-05 | Phase 1 Windows membership and delegated administration | Real computer secure-channel/machine-key lifecycle, login and UI/API/CLI authorization |
| N-06 | Phase 1 initial GPO/SYSVOL slice | Actual policy application/revert and recoverable directory/file permissions/version agreement |

Only isolated synthetic read-only/parser experiments can overlap unfinished
storage design. Valuable credentials and multi-controller writes require approved
state/metadata/key/upgrade decisions. Phases 2–3 complete the AD operation matrix,
trusts, functional levels, replication and failure recovery. Phases 4–5 qualify
and release the full first-production contract; partial previews never reduce it.

Use the [decision register](decisions.md) for store/toolchain/DRS/GPO uncertainties.
Generic database consensus or a copied SYSVOL tree does not prove compatible
AD replication. Fixed state formats and trust/key/schema transitions require
versioning, reviewed invariants, upgrade and clean-room recovery evidence.

The server remains Linux-hosted; language portability does not imply every-OS
hosting/client support. Administration and later endpoint components use scoped
core APIs, not raw-store access. The first implementation is described in [Phase 1 progress](phase-01-progress.md);
this dependency plan itself supplies no production conformance evidence. See [validation](validation-plan.md) before claiming a
native operation or release gate is supported.
