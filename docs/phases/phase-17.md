# Phase 17 — Joint fleet qualification and endpoint service release

Status: specified; product acceptance not demonstrated.
Owner roles: fleet/security/performance reviewers; named accountable owners must be assigned before execution.

## Scope and entry

Requires accepted remote, file, patch and EDR capabilities on their supported platform matrices. This qualifies their interaction at 10k computer endpoints/three sites; no enrollment-count claim implies 10k active desktop sessions.

## Design and interfaces

Independent Linux-hosted broker, inventory/patch workers, transfer relays and telemetry pipeline use priority queues, quotas and scoped service identities. A common device registry supplies identity/revocation without merging execution permissions. Supervisors expose partial failure/unknown state and preserve independently recoverable management channels.

## Data and lifecycle

Correlate event/job/session/action IDs and per-service state without building a shared unrestricted raw credential store. Reconcile actual endpoint installation/isolation/session state after controller recovery. Apply module-specific raw/alert/recording/file retention and explicitly budget storage/index/replica amplification.

## Security and failure handling

Assess compromised controller/relay/operator/sensor, stolen enrollment, malicious rules/content, mass action and false-positive containment. Emergency stop revokes connected authority within declared bounds; offline jobs require expiry/reapproval on reconnect. Core directory availability must remain independent of all endpoint modules.

## Capacity and operations

Joint target: 10k agents, 50 desktops, 100 terminals, 250 transfers and mixed patch/inventory plus EDR 20k events/s steady/200k burst. Apply baseline WAN loss/latency and 24-hour site disconnection. These are provisional targets: ratify or change through a reviewed capacity ADR before release, never silently lower thresholds after failing.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P17-01 | Run the combined supported-endpoint and directory workload. | Reports identify real versus simulated endpoints/sessions, platform counts, traffic mix and exact build/rule versions; all individual contracts remain satisfied. |
| P17-02 | Qualify aggregate concurrency, latency and resource budgets. | 50 desktop/100 terminal/250 transfer and EDR steady/burst profiles publish CPU/RAM/disk/IOPS/network/retention sizing, cost and endpoint overhead. |
| P17-03 | Preserve authentication/replication SLOs under endpoint pressure. | Telemetry floods, relay misses, large transfers and reconnect storms cannot starve core directory services within approved resource isolation limits. |
| P17-04 | Recover from site/provider/control-plane failures. | 24-hour partition, clock/DNS faults, full disks, expired issuers and 10k reconnect preserve authorization, bounded queues and truthful unknown state. |
| P17-05 | Reconcile pending/partial operations after backup/upgrade recovery. | Actual endpoint patch/file/isolation/session states are verified before replay; duplicate, cancelled and expired jobs cannot gain fresh authority. |
| P17-06 | Exercise cross-module privilege and compromise boundaries independently. | Support/upload/patch/EDR roles cannot exchange execution authority; external review includes enrollment, brokers, privileged executors, signing and recovery. |
| P17-07 | Rehearse emergency stop and fleet trust recovery. | Stop dispatch, revoke/rotate identities and rules, inspect queues and reenroll through an independent rescue path; offline stop limits and irreversible actions are explicit. |
| P17-08 | Qualify privacy and usability for real operator workflows. | Notice/consent/recording/evidence retention and accessible triage/patch/support journeys pass; missing data cannot appear as healthy/compliant. |
| P17-09 | Release immutable versioned endpoint services and agents safely. | Signed artifacts, SBOM/provenance, staged agent upgrades/version skew and supported Linux/Windows packages pass with defined rollback/forward-recovery. |
| P17-10 | Publish final endpoint service readiness and ownership. | All PATCH/REMOTE/FILE/EDR and selected security gates have current evidence, operator/support owners and known limits; no unrun acceptance is labeled production ready. |

## Evidence and exit

For every P17 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 16 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply. Requires Phase 05/06 supported Linux deployment and recovery, plus Phase 07 identity/authorization and Phase 10 agent/update assurance.

Traceability: PATCH-01, PATCH-02, PATCH-03, PATCH-04, PATCH-05, PATCH-06, PATCH-07, PATCH-08, PATCH-09, PATCH-10, PATCH-11, PATCH-12, PATCH-13, PATCH-14, PATCH-15, REMOTE-01, REMOTE-02, REMOTE-03, REMOTE-04, REMOTE-05, REMOTE-06, FILE-01, FILE-02, FILE-03, FILE-04, FILE-05, EDR-01, EDR-02, EDR-03, EDR-04, EDR-05, EDR-06, EDR-07, EDR-08

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
