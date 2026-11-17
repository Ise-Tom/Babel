# Phase 12 — Controlled patch campaigns and verified installation

Status: specified; product acceptance not demonstrated.
Owner roles: patch/agent and operations maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires inventory/applicability and secure agent enrollment. The privileged executor accepts approved typed package operations only; general shell/file support arrives in separately authorized later phases.

## Design and interfaces

An operator snapshots target membership and selected package digests, obtains approvals, then schedules canary/pilot/production rings. Agents revalidate job scope/expiry/cancellation, preflight native updater constraints, install and report post-reboot verification. A durable controller reconciles missing acknowledgments instead of assuming success; relays distribute authenticated content under bandwidth limits.

## Data and lifecycle

Persist immutable campaign approval scope, ring membership, deadlines/windows/time zones, package/supersedence versions, attempts and separate downloaded/installed/reboot-pending/verified/unknown states. Content stages atomically where supported. Preserve cancellation/revocation epochs and audit provider-independent execution receipts.

## Security and failure handling

Prevent approval scope substitution, replayed offline jobs, poisoned packages, mass forced reboot and updater lock bypass. Never auto-promote a ring with insufficient reporting. A patch may be irreversible: every supported update class has uninstall, restore/reimage or forward-fix instructions rather than a generic rollback promise.

## Capacity and operations

Use configurable per-site/download/install concurrency and native workload health checks. DC maintenance is serialized by fault domain, protecting surviving DNS/KDC/replication. Real Windows/Linux VM reboot cycles validate schedule/DST and state recovery; containers alone cannot qualify OS/kernel updates.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P12-01 | Approve exact targets, content and risk before scheduling. | Changing membership/digest/privileged scope requires reapproval; self-approval, cross-group API calls and stale authorization fail. |
| P12-02 | Implement gated canary/pilot/production rings. | Bad patch/health/error-rate fixtures pause later rings; missing report coverage cannot count as promotion success. |
| P12-03 | Enforce maintenance/deadline/reboot policy with user notice. | DST/time-zone, sleep/offline devices, active sessions, grace/deferral and forced reboot scenarios match explicit approved policy. |
| P12-04 | Run disk/power/prerequisite/lock and application-health preflight. | Blocked devices are reported separately; competing native transactions and unsupported reboot suppression are not overridden silently. |
| P12-05 | Deliver verified packages through throttled resumable site caches. | Vendor signatures plus approved digests survive retries/proxies; tamper, replay, incomplete files and quota failures block installation. |
| P12-06 | Revalidate typed job authority immediately before privileged execution. | Expired/cancelled jobs cannot run after reconnect; duplicate IDs and lost replies cannot cause repeated install or arbitrary command execution. |
| P12-07 | Verify actual installation, reboot and post-patch health. | Native version/state and health checks confirm remediation; exit zero, downloaded content or offline silence alone never counts as verified. |
| P12-08 | Provide update-class-specific failure recovery. | Uninstall works where supported; irreversible kernel/application/state changes follow tested restore/reimage/forward-fix with recorded limitations. |
| P12-09 | Provide emergency prioritization and controlled overrides. | Known-exploited/exposed asset priority is explainable; override scope, expiry, independent approval and audit prevent unlimited emergency privilege. |
| P12-10 | Protect identity-service availability during server patching. | A controller rollout cannot reboot all site DCs together; induced auth/replication health failure pauses and recovers the campaign. |

## Evidence and exit

For every P12 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 11 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply. Requires Phase 05/06 supported Linux deployment and recovery, plus Phase 07 identity/authorization and Phase 10 agent/update assurance.

Traceability: PATCH-01, PATCH-02, PATCH-03, PATCH-04, PATCH-05, PATCH-06, PATCH-07, PATCH-08, PATCH-09, PATCH-10, PATCH-11, PATCH-12, PATCH-13, PATCH-14, PATCH-15

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
