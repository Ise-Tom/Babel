# Phase 09 — Containment, key custody and compromise resilience

Status: specified; product acceptance not demonstrated.
Owner roles: security/platform/recovery maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires qualified replication/recovery, approved credential rotation and scoped response roles. Branch-controller and hardware-key features depend on an explicit native implementation, not assumed Samba behavior.

## Design and interfaces

A response orchestrator submits typed, scoped, expiring actions to authorized core/endpoint services. Quarantine separates suspect replicas/devices while preserving independent rescue paths. Key-provider interfaces expose only supported operations and key classes; HSM/KMS adoption is incremental and independently qualified.

## Data and lifecycle

Persist incident scope, approval/action identifiers, secret/key epochs, recovery provenance and replica quarantine reasons. Backups restore a reconciled security state: known revocations and compromised credentials are not silently resurrected. Read-only branch designs explicitly track which credentials may be cached.

## Security and failure handling

An automated alert cannot disable the entire domain or rotate every key unsupervised. Treat compromised writable DCs as domain compromise; isolation does not erase stolen keys. Root/kernel compromise can defeat local controls. Review hardware-provider outage and emergency access without silently accepting insecure software fallback.

## Capacity and operations

Measure containment/revocation by operation, including offline/stale-ticket limits. Run full-dataset clean-room compromise restores, one-site isolation and provider outage during mixed auth load. Preserve the baseline RPO/RTO and bound response queues; every high-risk operation has a tested abort/rescue path.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P09-01 | Implement typed response workflows with scoped approvals and idempotency. | Disable/quarantine/trust/key actions reject wrong scope, replay, expired approval and unauthorized API calls; execution and cancellation are audited. |
| P09-02 | Rehearse complete domain-compromise credential recovery. | Ticket-signing double rotation, service/machine/trust/admin keys and downstream effects are sequenced and verified in an isolated lab. |
| P09-03 | Quarantine and safely reintroduce suspect replicas. | A compromised/stale replica cannot contaminate clean state; evidence preservation, trust revocation, role recovery and controlled reenrollment are exercised. |
| P09-04 | Qualify read-only branch and password-cache exposure profiles. | Exact RODC/password-replication semantics, permitted caches, theft blast radius and credential reset behavior pass; writable state is never labeled read-only. |
| P09-05 | Qualify HSM/TPM/KMS integration per key class. | Supported key operations, latency, outage, backup/custody and provider recovery are tested; unsupported AD verifiers/keys are explicitly excluded. |
| P09-06 | Apply least-privilege host/service and network exposure profiles. | Capabilities, systemd sandboxing, LSM policies, RPC ranges and update paths pass functional/denied tests without a privileged-container default. |
| P09-07 | Maintain clean-room/offline backup recovery with split custody. | Independent recovery works after directory/provider loss and reconciles revoked identities, key epochs and directory/SYSVOL consistency. |
| P09-08 | Provide safe degraded modes for security-service outages. | MFA/audit/KMS/CA failures have explicit per-operation behavior; no silent auth bypass, unbounded audit flood or hidden evidence loss occurs. |
| P09-09 | Exercise ransomware, insider, maintainer and provider compromise playbooks. | Tabletops plus technical drills record response time, operator mistakes, evidence retained and follow-up fixes. |
| P09-10 | Validate compartmentalization under malicious and resource-exhaustion scenarios. | Noisy response/relay/query workloads cannot exceed approved blast radius or violate authentication SLOs without an explicit failed qualification. |

## Evidence and exit

For every P09 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 08 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: E-01, E-02, E-03, E-06, F-01, F-02, F-03, F-04, F-05, F-06, H-01, H-02, H-03, H-04, H-05, I-01, I-02, I-03, I-04, I-05

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
