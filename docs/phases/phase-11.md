# Phase 11 — Endpoint inventory and patch-control foundation

Status: specified; product acceptance not demonstrated.
Owner roles: endpoint/inventory maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires stable scoped identity APIs and independent endpoint service credentials. Introduce Linux-hosted inventory/catalog/control services and signed Windows/Linux agents; do not add arbitrary remote execution to inventory.

## Design and interfaces

Agents enroll through short-lived approved credentials, obtain unique mutual-TLS identities and report bounded signed/authenticated observations. Inventory builds materialized device/software/update views with provenance and freshness. Vendor catalog workers normalize applicability/dependencies/supersedence without authorizing deployment. Site relays cache content, not approval authority.

## Data and lifecycle

Device identity is distinct from hostname and human identity; track enrollment/revocation, agent versions, OS/build, installed packages, reboot state and observation age. Retain catalog source/signature/revision and device-to-applicability evidence. Minimize user/process data and apply deletion/retention policy.

## Security and failure handling

Detect cloned/stolen enrollment, malicious attributes, forged telemetry and catalog poisoning. Separate low-privilege communication from later privileged package execution. Vendor signatures/TLS remain enabled. Competing patch managers and licensing/redistribution constraints must be discovered before deployment.

## Capacity and operations

Initial fleet target is 10k computers across three sites, independently of human identities. Inventory freshness target is 99% of continuously connected devices within 15 minutes. Define agent resource budgets and publish unsupported/EOL/stale states; do not infer fleet health from successful server requests.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P11-01 | Define a supported endpoint/agent/application update matrix. | Exact Windows editions/builds, Linux releases/architectures and selected third-party products have native-engine feasibility and licensing evidence. |
| P11-02 | Enroll agents with unique authenticated device identity. | Wrong identities, cloned/replayed tokens and unauthorized enrollment fail without embedded domain-admin secrets. |
| P11-03 | Collect bounded native hardware/software inventory. | Inventory matches actual OS/package tools; malformed/oversized payloads cannot exhaust endpoint or controller resources. |
| P11-04 | Authenticate update applicability and native backport/version rules. | Vendor signatures and native version/backport fixtures yield correct applicability beyond string matching. |
| P11-05 | Maintain explicit dynamic-target attributes and provenance. | Approved device/OU/tag mappings resist spoofed inventory and unauthorized cross-group changes; hostname reuse does not inherit device authority. |
| P11-06 | Detect competing update authorities and unsupported endpoints. | WSUS/Intune/native locks and EOL products surface actionable conflicts; the service does not race another manager into unsupported state. |
| P11-07 | Separate agent communication and privileged action boundaries. | A malicious inventory payload cannot execute a command, read arbitrary files or gain package-install/EDR/support rights. |
| P11-08 | Design authenticated content staging. | Source/recipient/signature/digest and partial-content checks reject tamper before distribution. |
| P11-09 | Define inventory privacy, access and retention. | Fields, reader roles and expiry are documented and tested against unauthorized collection/export. |
| P11-10 | Deliver a recoverable Linux-hosted management foundation. | Controller/agent restart, certificate expiry and provider outage preserve device identity and show stale state without affecting domain login. |
| P11-11 | Rotate, revoke and rescue device enrollment credentials. | Real certificate rotation/revocation/recovery preserve identity and audited custody without accepting stale authority. |
| P11-12 | Report inventory freshness, reboot and unsupported observations. | Missing/stale/unknown/unsupported states stay distinct; reboot/pending transaction status agrees with native endpoint reality. |
| P11-13 | Resolve update supersedence, prerequisites and dependencies. | Conflicting/superseded/prerequisite/known-issue fixtures select supported remediation order and reject unsafe combinations. |
| P11-14 | Qualify site caching and relay authority separation. | Poisoned metadata, eviction/retry and recipient tests retain verification; holding payload never authorizes installation. |
| P11-15 | Budget inventory/controller/agent capacity and freshness. | 10k simulation plus representative real devices reports resource/storage overhead and truthful freshness denominators. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P11-02`: separately verify `P11-11`.
- `P11-03`: separately verify `P11-12`.
- `P11-04`: separately verify `P11-13`.
- `P11-08`: separately verify `P11-14`.
- `P11-09`: separately verify `P11-15`.

## Evidence and exit

For every P11 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 10 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply. Requires Phase 05/06 supported Linux deployment and recovery, plus Phase 07 identity/authorization and Phase 10 agent/update assurance.

Traceability: PATCH-01, PATCH-02, PATCH-04, PATCH-08, PATCH-14

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
