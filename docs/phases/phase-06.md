# Phase 06 — Sustained operations and maintenance

Status: specified; product acceptance not demonstrated.
Owner roles: support/security operations owners; named accountable owners must be assigned before execution.

## Scope and entry

Requires the first production release and staffed support/security ownership. Operate a maintained product; ongoing vulnerability, expiry and recovery work does not wait for advanced features.

## Design and interfaces

Separate telemetry/alerting, release-channel service, support intake and backup validation from authentication. Maintain a supported-version registry and vulnerability triage queue. Operators reconcile observed service state with declared configuration and receive specific diagnostic actions.

## Data and lifecycle

Version runbooks, advisory mappings, support windows, exception expiry and drill outcomes. Retain privacy-scoped logs according to policy. Preserve immutable backup copies and signing/recovery continuity across maintainer turnover.

## Security and failure handling

Triage upstream and native-core vulnerabilities with impact-specific mitigations. Expired keys/certificates and stale replicas must alert before outages where possible. Define supplier/maintainer compromise and disclosure procedures; no diagnostics dump passwords or production directory exports.

## Capacity and operations

Measure 99.95% monthly per-healthy-site authentication availability, using synthetic online ticket/login probes and a documented denominator. Quarterly isolated restore drills must meet the full-domain RPO/RTO; monitor actual scheduled security runs and alert storage/bandwidth growth.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P06-01 | Maintain explicit supported versions and security-update commitments. | Published matrix identifies release support/EOL and upgrade paths; advisory intake reaches accountable maintainers. |
| P06-02 | Monitor online authentication, DNS/time, replication, certificates and capacity. | Synthetic fault injection produces timely actionable alerts; cached offline login and missing telemetry do not count as online service success. |
| P06-03 | Operate vulnerability triage and coordinated disclosure. | Exercises prove private report receipt, severity/impact assessment, patch/mitigation tracking and secure publication without premature sensitive details. |
| P06-04 | Run regular independent backup verification and restore drills. | Quarterly full-dataset isolated restores meet <=1 h RPO/<=4 h RTO and include credentials, SYSVOL and recovery-key access. |
| P06-05 | Manage expiry and security exception debt. | Certificate/key/legacy-protocol exceptions have owners and expiry; expired/unowned exceptions cannot silently continue. |
| P06-06 | Provide privacy-safe support diagnostics. | Export is explicitly scoped/redacted and access-audited; credential material, arbitrary user data and complete environments are excluded. |
| P06-07 | Keep capacity and reliability reports with meaningful error budgets. | Monthly site-level availability and growth trends include exclusions/outages and remediation; breaches generate owned corrective work. |
| P06-08 | Maintain dependency/tool/signing updates and reproducible update checks. | Daily/periodic scans actually run, stale results alert, signatures stay verified and urgent advisories do not wait for routine schedules. |
| P06-09 | Rehearse maintainer/provider loss and emergency service recovery. | Separate contacts, signing recovery and backup custody restore operations without a single absent administrator or failed domain provider. |
| P06-10 | Decommission data and versions through controlled retention policy. | Removal preserves required evidence/backup holds while preventing indefinite unnecessary identity data retention; migrations are auditable. |

## Evidence and exit

For every P06 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 05 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: OPS-01, SEC-09, SEC-10, SEC-11

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
