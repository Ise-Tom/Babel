# Phase 01 — Native core and end-to-end development slice

Status: specified; product acceptance not demonstrated.
Owner roles: protocol/storage and management maintainers; named accountable owners must be assigned before execution.

The first bounded Rust LDAP lab increment has started; see
[implementation progress](../phase-01-progress.md) and [ADR 0001](../adr/0001-native-ldap-lab.md).
No full phase requirement is marked accepted by this source change.

## Scope and entry

Requires Phase 0 model/toolchain gates for the component being implemented. Deliver bounded N-01–N-06 increments; partial protocol previews use synthetic data and cannot be advertised as production AD.

## Design and interfaces

Bounded protocol listeners decode into typed operations, authenticate a principal, authorize through the core, commit atomically, then issue redacted audit events and replies. Storage and key providers sit behind narrow core-owned interfaces. LDAP/DNS read-only discovery comes before credential writes; Kerberos, secure membership and initial GPO follow their dependencies. A delegated management API drives the same operations as protocol requests.

## Data and lifecycle

Persist object/attribute versions and security descriptors with transactionally coupled journal entries. Preserve SID/GUID across rename/restore. Keep key material out of normal read APIs; stage SYSVOL content with a recoverable policy-version transition. Public errors do not expose internal principal/key representations.

## Security and failure handling

Reject oversized/recursive/malformed messages before unbounded allocation. Authenticate/authorize every credential-bearing mutation; denied operations do not change state. Simulate process termination and partial disk writes. Admin UI loss must not interrupt the protocol data plane.

## Capacity and operations

Use small deterministic fixtures initially, plus the full dataset for index/memory trend checks. Set explicit message/query/connection/nesting budgets in the implementation ADR. Services need systemd startup, DNS/time preflight and restart recovery on the proposed Linux baseline.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P01-01 | Add actual native source only with locked build, lint, types, unit/property tests and fuzz smoke. | The scope guard is extended in the same reviewed PR; clean Linux build plus malformed-input regression corpus passes. |
| P01-02 | Implement stable identity and schema primitives before mutations. | Preserve GUID/SID on rename and reject DN collisions, invalid classes and matching-rule violations. |
| P01-03 | Implement a transactionally durable local store. | Commit-boundary kills recover old or new complete state; never acknowledge an undurable mutation. |
| P01-04 | Implement the declared bounded LDAP discovery/read subset. | Real probes and negative paging/filter/referral tests pass; RootDSE is not domain join. |
| P01-05 | Integrate reviewed authentication and initial bind/AS/TGS flows. | Positive/denied authentication, replay, expiry and downgrade tests pass without credential disclosure. |
| P01-06 | Implement computer-account membership and secure-channel rollover. | A supported Windows client joins, logs in and rotates its machine password; unsigned/unauthorized membership requests fail. |
| P01-07 | Implement an initial GPO/SYSVOL delivery path with ACL/version consistency. | A Windows client applies and reverts a declared policy; interrupted writes recover without silently serving contradictory versions. |
| P01-08 | Provide delegated account/group/password administration through API/CLI. | Create/disable/reset/group actions require correct rights with consistent denied-action audit. |
| P01-09 | Package constrained Linux services and lifecycle health checks. | Clean install/reboot, DNS/time prerequisites and least-privilege file/port tests yield safe actionable errors. |
| P01-10 | Label and inventory development limitations. | Each public operation has a tested/unsupported status; lab credentials and incomplete protocol behavior cannot be promoted as a production release. |
| P01-11 | Implement ordered ACL, inheritance and nested-group authorization. | Allowed/denied tests cover ACE order, object/parent rights, inheritance, group cycles and bounded expansion before writes. |
| P01-12 | Implement versioned journal recovery and durable retry receipts. | State/journal/audit/idempotency commit together; lost replies and replay cannot skip committed changes or repeat mutations. |
| P01-13 | Implement DNS discovery and eligible DC locator records. | Clients discover only eligible DCs; stale/invalid records and unsupported updates fail explicitly. |
| P01-14 | Implement password changes and principal-key lifecycle. | Authorized/denied password operations enforce policy; key custody, rotation and redaction precede valuable credential storage. |
| P01-15 | Provide the minimal delegated administration UI. | Accessible UI journeys use the same authorized core operations; allowed/denied results agree with API/CLI. |
| P01-16 | Implement certificate configuration and TLS failure handling. | Missing/expired/untrusted certificates and unsafe channel settings stop affected operations without disabling verification. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P01-02`: separately verify `P01-11`.
- `P01-03`: separately verify `P01-12`.
- `P01-04`: separately verify `P01-13`.
- `P01-05`: separately verify `P01-14`.
- `P01-08`: separately verify `P01-15`.
- `P01-09`: separately verify `P01-16`.

## Evidence and exit

For every P01 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 00 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: PLAT-01, PLAT-02, PLAT-03, AD-01, AD-02, AD-03, AD-04, AD-05, AD-06, AD-08, IAM-01, UX-01, SEC-01, SEC-04, SEC-06, SEC-08

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
