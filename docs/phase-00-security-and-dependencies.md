# Phase 0 security ownership and dependency qualification

Status: the owner accepted the P00-07 boundary, threat and ownership design on
22 November 2026. Independent assessment and supported operation remain open.
Current accountable development owner is **Ise-Tom**, the repository owner. The solo
PR policy requires owner diff review plus CI; it does not claim independent review.
No additional maintainer, security mailbox or private report exercise is invented.

## Boundary ownership and misuse evidence

| Boundary / Tier 0 exposure | Current accountable owner | Required misuse/failure evidence |
| --- | --- | --- |
| Client → LDAP/KDC/DNS/SMB/RPC/core; directory identities/ACLs | Ise-Tom; protocol/security role | T-01–T-05: malformed budgets, downgrade/replay, wrong ACL and unauthorized policy publication |
| API/browser → core; delegated and recovery authority | Ise-Tom; management/security role | T-06/T-11: CSRF, scope substitution, stale grants, reset/enrollment abuse and denied actions |
| Core → PostgreSQL/key custody; verifiers/journal/audit | Ise-Tom; storage/security role | T-02/T-03/T-09/T-20: auth/write race, credential leak, missing keys and no false success on disk/audit failure |
| DC → peer/restore; replica keys, RID and invocation identity | Ise-Tom; replication/recovery role | T-08/T-09: forged replication, partition/reorder, stale restore, lingering objects and key-rotation recovery |
| Source/dependency → build/update consumer; signing authority | Ise-Tom; release role | T-10: pinned inputs, least privilege, failed provenance, replay and unauthorized ref changes |
| Future IdP/CA/device/relay/agent services | Ise-Tom; module ownership until assigned | T-07/T-12–T-19: external issuer/SSRF, enrollment replay, unsafe dispatch/upload, consent and telemetry gaps |

Threat IDs refer to the [shared threat register](threat-model.md). Record exposure,
asset, actor/precondition, misuse scenario, mitigation, executable test and residual
risk per implementation. An unimplemented boundary is not considered secured.
Directory administrators do not automatically control backup custody, release
signing or fleet response authority. The current single maintainer is a project
bus-factor risk, not a production separation-of-duty implementation.

## Vulnerability intake and incident exercise

GitHub private reporting is enabled, but no submission/response drill has occurred.
Before accepting a preview as supported: verify owner access, submit a benign
clearly labeled **synthetic** private drill, confirm receipt privately, check access
and notification behavior, close the drill and record only redacted metadata.
Do not create public vulnerability examples or send private reports without an
explicit owner-authorized drill. No test message was sent by this work.

Assign and exercise a real backup security contact before claiming P00-17 complete;
a GitHub username alone does not prove availability or a private channel. The
proposed two-working-day acknowledgment/seven-day update targets in [SECURITY.md](../SECURITY.md)
are not active SLAs. Record time/owner/escalation, safe reproduction, severity,
affected commits, containment, fix/retest, coordinated disclosure and advisory.
A suspected domain compromise requires clean recovery and credential/key rotation;
a code patch alone is insufficient. Independent production assessment and response
coverage remain gates even though daily development uses solo approvals.

## Dependency and rights register

| Component | Current decision / alternatives | Qualification required before broader use |
| --- | --- | --- |
| Native toolchain/parser | [Owner-accepted P00-04 packet](validation/p00-04.md): Rust 1.100.0 Linux x86_64 GNU parser baseline, debug/release/overflow/client/fuzz/audit and actual compiler/ELF evidence | New targets/dependencies require requalification. Native AD behavior remains open |
| TLS | [Owner-accepted P00-13 provider/channel review](validation/p00-13.md) for the Rustls 0.23.46/ring 0.17.14 standalone Linux lab described in [ADR 0006](adr/0006-tls-qualification-lab.md) | Native LDAP/SASL/EPA, general revocation freshness/OCSP, protected product key custody, real OS clients and concurrency retain their implementation/qualification gates |
| Kerberos/PAC | [Owner-accepted P00-14 decision](validation/p00-14.md) selects signed MIT krb5 1.22.3 for a bounded Linux AES/PAC/replay qualification profile | Rust FFI, product replay/key custody, AD PAC/S4U/PKINIT and real Windows/Linux/macOS conformance are separate unrun integration gates |
| PostgreSQL | Owner selected backend family; PostgreSQL 18.7/psql SQL experiment and [tokio-postgres 0.7.18/Tokio 1.54.1 profile](validation/p00-15.md) now completes the Phase 0 driver review with typed/bounded operations, dropped-future safety, reply-loss/idempotency and process-crash evidence | The owner validated the full P00-15 gate on 18 November 2026. Native AD adapter/authorization, service auth provisioning, host/disk/backup/upgrade and key custody remain subsequent implementation/qualification gates |
| DNS/SMB/RPC | Production parsers/transports not selected; reuse reviewed libraries where suitable without requiring Samba | Exact supported operation/encoding/signing/sealing matrix, adversarial bounds, licenses and fuzz/reference evidence |
| Python / TypeScript | Current test/report tooling and dashboard, not native domain-server language | Hash-locked/pinned dependencies and current CI; tool/compiler changes must preserve security checks |
| Platform agents | Separate later Linux/macOS/Windows qualification | Updater/sensor/driver/consent/signing/privacy requirements; no generic privileged shell as policy engine |

Every dependency decision records upstream/source and immutable version/digest,
license/notice and redistribution/linking obligations, advisory status/date,
maintenance/EOL/support policy, transitive features, unsafe/FFI/crypto/provider
surface, alternatives and a removal/upgrade plan. A green current advisory scan
is time-bound evidence, not a lifetime security guarantee. Existing SBOM/license
jobs cover their registered scope only.

The internal native archive now retains actual project, selected runtime-crate
and Rust-library notice texts with a digest manifest and extraction verification.
This closes the former lab-binary notice-packaging gap for that artifact; it does
not finish protocol/fixture rights, binary-link analysis or product distribution
qualification. See ADR 0006 for the reviewed permissive terms and exact boundary.

The project license is Apache-2.0 with DCO, as selected by the owner. The protocol
matrix lists public reference locations **without copying specification text**;
exact revision/byte pins and a reference-use review are now recorded, while
patent/program/image/fixture clearance remains unresolved. Consult actual terms for
each selected Microsoft/RFC reference, redistributed fixtures, SDK/library and
Windows image. This document is not a legal clearance or permission to redistribute
licensed VM images. Keep public evidence synthetic and retain notices; do not
import another directory server's code/database as the native implementation.

The complete [P00-06 contribution/redistribution register](licensing-and-redistribution.md)
now records the existing owner decision, actual terms and enforced artifact handling.
The owner accepted its Phase 0 scope on 22 November 2026. P00-16 remains open.


The [complete boundary register](../lab/state-security-contract.json) expands the
summary table into eleven separately owned boundaries with all twenty threat IDs,
assets/misuse/denial/fault/residual-risk and implementation-gate bindings. See the
[full P00-07 criterion packet](validation/p00-07.md). Exact protocol reference
editions and the remaining P00-16 rights gaps are recorded in the
[reference-use review](reference-use-review.md); no image/patent grant is inferred.

The [solo response-readiness runbook](security-response-readiness.md) documents
intake, custody, owner absence and the live-drill plan. The merged timing
amendment and explicit owner decision accept only P00-17's Phase 0 process
design. A verified live owner-receipt drill is required before soliciting
external preview users, and real backup/owner-absence escalation remains a
P05-04 supported-production gate. No private report or contact was authorized;
neither operational gate has passed.
