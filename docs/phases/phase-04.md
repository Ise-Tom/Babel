# Phase 04 — Security, capacity and administrator qualification

Status: specified; product acceptance not demonstrated.
Owner roles: security/performance/accessibility reviewers; named accountable owners must be assigned before execution.

## Scope and entry

Requires full native protocol and multi-site behavior. This phase qualifies the first-production product, not merely the implementation team’s unit tests. All baseline SEC/PLAT/UX gates apply.

## Design and interfaces

Independent reviewers evaluate protocol/core, privileged management and operations boundaries. Load generators use versioned synthetic identities and mixed protocol/API traffic. Observability separates successful auth, expected denials, unexpected errors, replication and collector gaps. Usability sessions exercise the same production permissions and recovery paths.

## Data and lifecycle

Keep immutable test inputs, normalized result schemas and redacted attack/incident evidence. Store performance distributions and achieved load, not only averages. Publish accessibility findings and mitigation ownership without exposing participant data or credentials.

## Security and failure handling

Test credential abuse, parsers, ACLs, recovery, downgrade and trust/GPO attacks in isolated labs. No unexplained critical/high finding can be hidden as an accepted skip; any disposition needs a named security owner and explicit release impact. Resolve baseline safety defects before production even if an advanced defense is planned later.

## Capacity and operations

Combined baseline: 100 auth/s for 60 min plus 500/s five-minute burst; 500 indexed reads/s and 20 writes/s; p95/p99 <=100/300 ms LAN auth/read, p95 local writes <=500 ms, unexpected errors <0.1%. Run a 24-hour soak and one-DC-loss sustained profile with CPU <=70%/RAM <=80% headroom targets.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P04-01 | Run independent integrated assessment and threat review. | Scoped reproducible findings cover protocol, keys, UI/API, replication, supply chain and restore. |
| P04-02 | Enforce secure protocol defaults and scoped legacy exceptions. | Invalid TLS, anonymous sensitive reads, unsigned channels and weak crypto fail; exceptions carry scope/expiry/audit and cannot silently become defaults. |
| P04-03 | Measure the full mixed-load contract with real clients and reference requests. | Publish dataset, hardware, caches, concurrency, rates, percentiles and unexpected errors; each baseline target is met or release-blocking. |
| P04-04 | Qualify sustained operation through the full soak. | A 24-hour mixed-load soak shows bounded queues/storage and no unexplained credential/data corruption. |
| P04-05 | Demonstrate complete and privacy-preserving security audit. | For each privileged/auth/policy/key operation, expected events and denied cases are present, correlated and redacted; export loss is visible. |
| P04-06 | Qualify administrator journeys with representative users. | At least five admins achieve >=90% unassisted completion per declared journey, including delegation, policy, diagnosis and restore; publish time-on-task. |
| P04-07 | Qualify keyboard/screen-reader accessibility. | WCAG 2.2 AA audit and manual assistive-technology journeys pass across supported administration surfaces. |
| P04-08 | Test denial and recovery through UI, API and CLI consistently. | Role/session expiry, CSRF, unauthorized export/reset, recovery bypass and stale privilege tests preserve authorization and provide safe actionable errors. |
| P04-09 | Ratify production sizing and operating limits from results. | ADR records DC/backup/audit capacity, retention, bandwidth and expansion triggers; suggested 4-vCPU/16-GiB sizing is not treated as measured beforehand. |
| P04-10 | Produce a signed-off first-production readiness bundle. | Every baseline requirement maps to current passing evidence; outstanding exceptions, unsupported clients and residual risks are explicit and approved before Phase 5. |
| P04-11 | Remediate and independently retest assessment findings. | Each finding has an owner/severity/fix/retest/disposition; an assessment report alone cannot close qualification. |
| P04-12 | Qualify DC/site failure headroom under load. | Losing a DC/site at sustained traffic preserves declared SLO/resource bounds and publishes degraded-mode limits and failures. |
| P04-13 | Qualify dangerous-action previews and unsupported-setting handling. | Bulk/irreversible changes preview exact scope/consequences; unsupported settings and partial failures are never silently discarded. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P04-01`: separately verify `P04-11`.
- `P04-04`: separately verify `P04-12`.
- `P04-07`: separately verify `P04-13`.

## Evidence and exit

For every P04 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 03 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: PLAT-01, PLAT-02, PLAT-03, AD-01, AD-02, AD-03, AD-04, AD-05, AD-06, AD-07, AD-08, AD-09, AD-10, IAM-01, OPS-01, UX-01, SEC-01, SEC-02, SEC-03, SEC-04, SEC-05, SEC-06, SEC-07, SEC-08, SEC-09, SEC-10, SEC-11

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
