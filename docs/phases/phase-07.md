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
| P07-01 | Secure privileged passkey/hardware-key enrollment. | Origin/replay/unauthorized enrollment fails; factors bind to intended identities with audited registration. |
| P07-02 | Implement time-bounded just-in-time/just-enough privileges. | Grant expiry remains enforced after worker restart; tests cover nested groups, stale sessions/tickets and delayed replication with declared limits. |
| P07-03 | Separate requester/approver/executor for high-risk actions. | UI/API/bulk operations reject self-approval and scope substitution; signed-off target/content changes require reapproval. |
| P07-04 | Provide scoped managed service credential lifecycles. | Qualified gMSA/keytab retrieval, rotation and offline/reconnect behavior work on Windows/Linux services; unauthorized readers and secret logging fail. |
| P07-05 | Implement hardened password/self-service and lifecycle workflows. | Spray, enumeration, recovery impersonation and unauthorized reset/group request tests fail; breach checks do not export raw passwords. |
| P07-06 | Provide effective-permission and privilege-path views. | Displayed paths match ACL/trust/group decisions without exposing protected relationships to unauthorized viewers. |
| P07-07 | Govern GPO changes through diffs, preview and approval. | Approved content/scope matches committed policy; out-of-band edits and directory/SYSVOL conflicts are detected. |
| P07-08 | Provide monitored break-glass and privileged-workstation guidance. | A rehearsed IdP/provider outage preserves audited emergency access with separate custody and post-use rotation, without permanent hidden bypass. |
| P07-09 | Enforce exception ownership and expiration. | Expired/unowned grants and exceptions fail closed with visible review and renewal decisions. |
| P07-10 | Qualify advanced privilege features without weakening baseline defaults. | Negative/auth-strength/latency/recovery evidence covers selected feature IDs and mixed load; new security service failures cannot silently bypass MFA. |
| P07-11 | Secure factor replacement and privileged recovery. | Lost-factor/replacement and impersonation cases pass without SMS-only Tier 0 or hidden permanent bypass. |
| P07-12 | Provide scoped local-administrator credential retrieval and rotation. | LAPS/platform-equivalent retrieval, rotation and offline recovery respect device/reader boundaries and redact secret material. |
| P07-13 | Implement access-review decisions and effective revocation. | Owned reviews produce auditable retain/remove decisions and verify grant removal including stale sessions and replication limits. |
| P07-14 | Stage GPO rollout by OU and verify actual client revert. | Pilot/target resultant policy is measured; failures pause expansion and revert restores real client behavior. |
| P07-15 | Qualify accessible privileged policy workflows and bulk simulation. | Keyboard/screen-reader users can preview, approve and diagnose exact-scope changes without hidden omission or unsafe defaults. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P07-01`: separately verify `P07-11`.
- `P07-04`: separately verify `P07-12`.
- `P07-06`: separately verify `P07-13`.
- `P07-07`: separately verify `P07-14`.
- `P07-09`: separately verify `P07-15`.

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
