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
| P12-03 | Implement maintenance scheduling and user notice. | Time-zone/DST, sleep/offline and active-session cases follow approved schedules with visible grace/deferral notices. |
| P12-04 | Run disk/power and package-prerequisite preflight. | Insufficient capacity/power or missing dependencies block the device with actionable state rather than unsafe installation. |
| P12-05 | Verify approved package/vendor/content authenticity. | Signatures and approved digests reject tamper, replay and incomplete payloads before privileged installation. |
| P12-06 | Revalidate typed job authority before privileged execution. | Expired/cancelled/wrong-scope jobs cannot run after reconnect; no arbitrary command authority is exposed. |
| P12-07 | Verify actual native installation state. | Native versions/receipts confirm remediation; exit zero, downloaded bytes or offline silence cannot qualify success. |
| P12-08 | Provide update-class-specific failure recovery. | Uninstall works where supported; irreversible kernel/application/state changes follow tested restore/reimage/forward-fix with recorded limitations. |
| P12-09 | Prioritize emergency remediation by explainable exposure. | Known-exploited/exposed assets receive transparent priority without changing approved target/content authority. |
| P12-10 | Protect identity-service availability during server patching. | A controller rollout cannot reboot all site DCs together; induced auth/replication health failure pauses and recovers the campaign. |
| P12-11 | Enforce reboot, deadline and deferral policy. | Native reboot/deadline/forced-restart cases match explicit policy; unsupported reboot suppression is never silently asserted. |
| P12-12 | Check competing native transactions and application health. | Native locks and unhealthy application conditions remain visible; no racing update authority or silent unsupported override. |
| P12-13 | Distribute bounded resumable/throttled packages through site caches. | Retries/proxies, connection loss, quotas and hit/miss paths preserve content integrity within declared bandwidth limits. |
| P12-14 | Make installation retries and lost replies idempotent. | Duplicate IDs, ambiguous responses and restarts reconcile durable native results without repeated unauthorized installation. |
| P12-15 | Verify post-reboot/application health before campaign success. | Required restart is observed and service checks pass; pending reboot or unhealthy applications remain unverified/failed. |
| P12-16 | Control emergency overrides through scope, expiry and approval. | Independent approval and audit prevent emergency status from granting unlimited/permanent installation privilege. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P12-03`: separately verify `P12-11`.
- `P12-04`: separately verify `P12-12`.
- `P12-05`: separately verify `P12-13`.
- `P12-06`: separately verify `P12-14`.
- `P12-07`: separately verify `P12-15`.
- `P12-09`: separately verify `P12-16`.

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
