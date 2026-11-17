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
| P00-01 | Define supported protocol operations, functional levels and exact Windows/Linux client editions/builds. | Reviewed matrix maps every AD requirement to expected positive/negative behavior and an owner; unknown/unsupported operations stay visible. |
| P00-02 | Define stable identities, authorization order, schema rules and local commit semantics. | Design review covers rename, DN collision, ACL inheritance, nested groups, concurrent updates and durable acknowledgment boundaries. |
| P00-03 | Define attribute replication/versioning and restore epochs before fixing a disk format. | Worked partition/delete/conflict/rollback examples specify observable outcomes and map to MS-ADTS/MS-DRSR. |
| P00-04 | Choose a memory-safe toolchain and reviewed TLS/Kerberos/storage/parser dependencies. | ADR records alternatives, supported platforms, license/CVE maintenance and locked build/fuzz/security jobs; no custom crypto accepted. |
| P00-05 | Provide a disposable Windows reference and Linux host lab with reproducible DNS/time. | Two fresh deployments run discovery probes, isolate egress, clean up resources and publish exact image/build identifiers. |
| P00-06 | Establish project license, contributor terms and specification-use review. | Owner decision and dependency obligations recorded before source distribution; missing decisions block release rather than receiving invented terms. |
| P00-07 | Establish Tier 0 identities, review ownership, vulnerability intake and an initial threat register. | Private report route and backup security contacts exercised; every boundary has misuse cases and review responsibility. |
| P00-08 | Version the compatibility/evidence schema and requirement traceability. | Evidence records commit, test/client/spec revision, requirement, outcome and redacted artifacts; skipped/unrun are never passing. |
| P00-09 | Approve the target workload, fault profiles and performance measurement method. | Reviewed load model includes mixed successful/denied requests, cold cache, WAN loss/latency, partial outages and hardware costs. |
| P00-10 | Specify upgrade, recovery and scope-change governance. | Irreversible schema/key/storage decisions require review and recovery examples; scope exceptions have owner, expiry and production impact. |

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
