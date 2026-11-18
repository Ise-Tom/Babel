# Phase 13 — Production patch fleet, compliance and resilience

Status: specified; product acceptance not demonstrated.
Owner roles: fleet/patch operations maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires controlled real-endpoint deployment and recovery tests. Qualify the patch module as a production service independent of the directory release; simulated command throughput alone is insufficient.

## Design and interfaces

Durable workers coordinate inventory, campaigns, relays, compliance materializations and change-ticket integrations. APIs expose reconciliation and progress with clear data age. Redundant control services recover pending state from durable storage; workload priority preserves directory/control and emergency stop over bulk transfers.

## Data and lifecycle

Keep approved versus actual target coverage, missing/failed/unknown endpoints, verification age, SLA/exception ownership and expiry. Immutable audit ties vendor catalog version to approved package and per-device execution. Backup recovery reconciles device reality before resuming pending jobs.

## Security and failure handling

Controller compromise is a fleet-wide privileged threat. Test dispatch stop, issuer/agent revocation, trusted catalog restore, queued-job inspection and reenrollment. Offline completion/stop is bounded by reconnect and expiry; do not declare all devices immediately stopped or remediated.

## Capacity and operations

Qualify 10k enrolled computers/three sites: 99% healthy connected inventory <=15 min, p95 authorized job acknowledgment <=60 s excluding scheduled waiting/install. Test 10k reconnect, baseline WAN/degraded/24-hour partition, realistic payloads and mixed inventory/patch/report traffic without directory SLO regression.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P13-01 | Qualify real OS/application remediation plus large-fleet orchestration. | Publish exact platform/device counts and real versus simulated roles; containers/simulators cannot replace native install/reboot evidence. |
| P13-02 | Meet inventory freshness with transparent denominators. | Connected/stale/offline/unsupported categories stay explicit; >=99% targets cannot hide unexplained failures or missing agents. |
| P13-03 | Bound reconnect storms, work queues and retries. | 10k-agent recovery after controller/site outage preserves authorization/cancellation, avoids duplicate installs and publishes convergence and queue metrics. |
| P13-04 | Budget payload bandwidth and relay storage from real package sizes. | Transfer tests measure cache hits/misses/eviction/retries under configured site limits; control API rate is not reported as distribution throughput. |
| P13-05 | Produce truthful compliance/SLA and exception reports. | Missing/stale/offline/unverified/EOL devices cannot appear compliant; risk-based overdue time and exception expiry are reproducible from raw receipts. |
| P13-06 | Provide delegated patch UI/API/CLI workflows. | Role/target/approval/audit behavior agrees across clients and rejects unauthorized scopes. |
| P13-07 | Recover controller/relay state and interrupted upgrades safely. | Backups, expired certificates, full disks and process failures reconcile endpoint reality before resuming approved campaigns. |
| P13-08 | Rehearse compromised-controller containment and recovery. | Stop dispatch, revoke/rotate trust, inspect queue/catalog, recover signing/enrollment and reinstall trusted agents through a documented rescue process. |
| P13-09 | Qualify agent/controller version skew. | Declared old/new combinations preserve identity, typed jobs/cancellation and truthful unsupported state. |
| P13-10 | Release the patch service with owned operating limits. | Independent review, resource/storage/retention sizing, failure runbooks and mixed-load no-directory-SLO-regression evidence are approved before production. |
| P13-11 | Measure job acknowledgment separately from execution. | p95 ack reports retain dropped/unexplained requests; controller acceptance is never verified endpoint remediation. |
| P13-12 | Integrate ticket systems without granting execution authority. | Outages, duplicate tickets and replayed external events cannot widen permissions or report false completion. |
| P13-13 | Roll out signed agent upgrades with pause and recovery. | Staged upgrades reject bad signatures, pause bad versions and retain tested rollback/forward-recovery. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P13-02`: separately verify `P13-11`.
- `P13-06`: separately verify `P13-12`.
- `P13-09`: separately verify `P13-13`.

## Evidence and exit

For every P13 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 12 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply. Requires Phase 05/06 supported Linux deployment and recovery, plus Phase 07 identity/authorization and Phase 10 agent/update assurance.

Traceability: PATCH-01, PATCH-02, PATCH-03, PATCH-04, PATCH-05, PATCH-06, PATCH-07, PATCH-08, PATCH-09, PATCH-10, PATCH-11, PATCH-12, PATCH-13, PATCH-14, PATCH-15

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
