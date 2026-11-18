# Phase 00 — Contract, native-core design and laboratory

Status: specified; product acceptance not demonstrated.
Owner roles: Ise-Tom is the current accountable development owner (product/security/protocol); independent production review and backup incident coverage remain unassigned.

See [current Phase 0 work and remaining evidence](../phase-00-progress.md).

## Scope and entry

Enter from the accepted native-core direction. Exit is a reviewed design/lab contract, not a functioning domain controller. Inventory, licensing and the security reporting route precede public previews.

## Design and interfaces

A conformance runner orchestrates disposable Linux Babel hosts and licensed Windows reference/client VMs on isolated networks. Specification operations and client builds are versioned inputs; observations become redacted evidence. Rust is the proposed native server baseline; a toolchain/library ADR must qualify it before source is admitted. Python remains test tooling. The management API is a separate authorization boundary, not a direct store writer.

## Data and lifecycle

Own stable object GUID/SID identity, normalized DN/schema, attribute change metadata, security descriptors, principal/key records and journal/snapshot versions. Document transaction and replication boundaries before credentials persist. Select the storage engine through crash/locking/index benchmarks; no Samba database import is the native storage design.

## Security and failure handling

Use synthetic forests, isolated DNS/time and lab-only credentials. Do not bridge lab domains to production. Review crypto/library/specification licensing; selecting a native core does not authorize copying code or designing new cryptography. Lost lab state must be recreatable without real identity data.

## Capacity and operations

The baseline dataset is 10k users, 10k computers and 2k groups across three sites/six DCs. Record host hardware and test costs. Lab bootstrap is noninteractive and repeatable; provisioning failures retain redacted diagnostics and destroy scoped test resources.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P00-01 | Define the protocol-operation matrix and operation ownership. | Every AD operation maps to expected positive/negative behavior and an owner; unknown operations remain visible. |
| P00-02 | Define stable identities, authorization order, schema rules and local commit semantics. | Design review covers rename, DN collision, ACL inheritance, nested groups, concurrent updates and durable acknowledgment boundaries. |
| P00-03 | Define attribute replication/versioning and restore epochs before fixing a disk format. | Worked partition/delete/conflict/rollback examples specify observable outcomes and map to MS-ADTS/MS-DRSR. |
| P00-04 | Qualify the memory-safe toolchain and parser baseline. | Record supported platforms, alternatives, license/advisory maintenance and locked build/fuzz/security jobs. |
| P00-05 | Provide a disposable Windows reference and Linux host lab with reproducible DNS/time. | Two fresh deployments run discovery probes, isolate egress, clean up resources and publish exact image/build identifiers. |
| P00-06 | Establish the project license and contributor terms. | Record owner license/DCO decisions, contribution terms and third-party notice/redistribution obligations before distribution; do not invent certification. |
| P00-07 | Establish Tier 0 boundaries, review ownership and threats. | Every boundary has misuse cases and accountable review; solo development review is not independent production assessment. |
| P00-08 | Version the compatibility/evidence schema and requirement traceability. | Evidence records commit, test/client/spec revision, requirement, outcome and redacted artifacts; skipped/unrun are never passing. |
| P00-09 | Approve the target workload, fault profiles and performance measurement method. | Reviewed load model includes mixed successful/denied requests, cold cache, WAN loss/latency, partial outages and hardware costs. |
| P00-10 | Specify upgrade, recovery and scope-change governance. | Irreversible schema/key/storage decisions require review and recovery examples; scope exceptions have owner, expiry and production impact. |
| P00-11 | Define the domain/forest functional-level profile. | Review supported levels, transitions and incompatible behavior; do not advertise unqualified levels. |
| P00-12 | Pin exact Windows, Linux and macOS platform profiles. | Edition, architecture, OS/build, package and image identifiers are explicit; missing profiles cannot qualify compatibility. |
| P00-13 | Qualify the TLS library/provider and channel boundary. | Review exact versions/features, key custody, certificate, downgrade, channel-binding and provider-loss cases; no custom cryptography. |
| P00-14 | Qualify Kerberos/PAC dependencies and cryptographic maintenance. | Review AES/PAC/replay/delegation support, licenses, FFI/unsafe boundaries and upstream maintenance; generic Kerberos is not AD conformance. |
| P00-15 | Qualify the storage driver and transactional interface. | Review versions, parameterization, cancellation, commit/error mapping and recovery before credentials or stable formats persist. |
| P00-16 | Review specification and reference-fixture use rights. | Pin document revisions and use/redistribution obligations separately from project licensing; unclear image/fixture rights block distribution. |
| P00-17 | Exercise private vulnerability intake and backup response coverage. | A synthetic private intake drill and real backup contact demonstrate receipt/escalation; no contact, SLA or exercise is invented. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P00-01`: separately verify `P00-11`, `P00-12`.
- `P00-04`: separately verify `P00-13`, `P00-14`, `P00-15`.
- `P00-06`: separately verify `P00-16`.
- `P00-07`: separately verify `P00-17`.

## Evidence and exit

For every P00 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

None beyond the owner-approved native-core scope and existing CI.

Traceability: PLAT-01, PLAT-02, PLAT-03, AD-01, AD-02, AD-03, AD-04, AD-05, AD-06, AD-07, AD-08, AD-09, AD-10, IAM-01, OPS-01, UX-01, SEC-01, SEC-02, SEC-03, SEC-04, SEC-05, SEC-06, SEC-07, SEC-08, SEC-09, SEC-10, SEC-11

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
