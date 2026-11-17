# Phase 07 — Strong identity and privileged administration

Status: specified; product acceptance not demonstrated.
Owner roles: identity/security and UX maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires baseline MFA, ACL/RBAC, audit and recovery. Advanced controls extend first-release safety; any feature selected in the first-production profile is gated earlier.

## Design and interfaces

An authorization/policy service evaluates identity strength, approved role, target scope, grant expiry and separation of duties before invoking core operations. Managed credential providers expose retrieval/rotation only to scoped principals. Approval and access-review services are control-plane functions; their failure cannot grant permanent privilege.

## Data and lifecycle

Persist grant/request/approval identity, immutable scope, expiry, credential retrieval audit and exception state. Ticket/session caches have independent revocation limits, made visible to operators. Never store reusable admin credentials in browser state or shared endpoint agents.

## Security and failure handling

Protect enrollment/recovery against account takeover, fatigue and self-approval. Require phishing-resistant privileged web authentication and define break-glass custody. Test scoped LAPS/gMSA/keytab support against the exact native-core/client profile; do not simulate interoperability with shared plaintext secrets.

## Capacity and operations

Use the 10k identity dataset with nested delegation/access-review workloads. Set grant/session lifetimes and a measurable enforcement/revocation bound in the support profile; record stale-ticket and partition limits. Approval/credential provider outage behavior must be explicit and fail closed for new privileged grants.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P07-01 | Provide secure passkey/hardware-key enrollment and recovery for privileged access. | Origin/replay/unauthorized enrollment tests fail; multiple factors, replacement and recovery are audited with no SMS-only Tier 0 bypass. |
| P07-02 | Implement time-bounded just-in-time/just-enough privileges. | Grant expiry remains enforced after worker restart; tests cover nested groups, stale sessions/tickets and delayed replication with declared limits. |
| P07-03 | Separate requester/approver/executor for high-risk actions. | UI/API/bulk operations reject self-approval and scope substitution; signed-off target/content changes require reapproval. |
| P07-04 | Provide scoped managed Windows/Linux service and local-admin credential lifecycles. | Qualified LAPS/gMSA/keytab retrieval, rotation, offline behavior and denied readers pass; secrets never appear in logs or broad inventory. |
| P07-05 | Implement hardened password/self-service and lifecycle workflows. | Spray, enumeration, recovery impersonation and unauthorized reset/group request tests fail; breach checks do not export raw passwords. |
| P07-06 | Provide effective-permission and privilege-path views with access reviews. | Results match actual ACL/trust/nested-group decisions; unauthorized viewers cannot enumerate protected relationships. |
| P07-07 | Govern GPO changes through diffs, preview, approval and staged OU rollout. | Version/SYSVOL consistency, out-of-band edits and resultant-policy comparisons are validated; revert restores real client behavior. |
| P07-08 | Provide monitored break-glass and privileged-workstation guidance. | A rehearsed IdP/provider outage preserves audited emergency access with separate custody and post-use rotation, without permanent hidden bypass. |
| P07-09 | Enforce exception ownership, expiration and accessible policy workflows. | Expired grants/exceptions fail closed; keyboard/screen-reader and policy-simulation journeys include safe bulk-change previews. |
| P07-10 | Qualify advanced privilege features without weakening baseline defaults. | Negative/auth-strength/latency/recovery evidence covers selected feature IDs and mixed load; new security service failures cannot silently bypass MFA. |

## Evidence and exit

For every P07 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 06 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: A-01, A-03, A-04, A-05, A-06, B-01, B-02, B-03, B-04, B-05, B-06, C-01, C-02, C-03, C-04, C-05, D-01, D-02, D-03, D-04, L-02, L-03, L-04, L-05, L-06

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
