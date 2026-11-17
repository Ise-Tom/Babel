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
| P11-02 | Enroll agents with unique revocable mutual authentication. | Replay/cloned tokens, wrong device identities and revoked certificates fail; enrollment/rotation/rescue are audited without embedded domain-admin secrets. |
| P11-03 | Collect trustworthy bounded hardware/software/update inventory. | Compare actual OS/native package tools and reboot state; missing/stale/unknown/unsupported observations remain distinguishable. |
| P11-04 | Build an authenticated applicability/supersedence/dependency catalog. | Vendor signatures/backports/prerequisites and known-issue fixtures yield correct applicable/not-applicable results beyond version-string matching. |
| P11-05 | Maintain explicit dynamic-target attributes and provenance. | Approved device/OU/tag mappings resist spoofed inventory and unauthorized cross-group changes; hostname reuse does not inherit device authority. |
| P11-06 | Detect competing update authorities and unsupported endpoints. | WSUS/Intune/native locks and EOL products surface actionable conflicts; the service does not race another manager into unsupported state. |
| P11-07 | Separate agent communication and privileged action boundaries. | A malicious inventory payload cannot execute a command, read arbitrary files or gain package-install/EDR/support rights. |
| P11-08 | Design authenticated content staging/site caching. | Poisoned cache/metadata, wrong recipient and signature failures are rejected; relay possession of payload never authorizes installation. |
| P11-09 | Set inventory privacy, retention and capacity budgets. | Fields/roles/retention are documented; 10k fleet simulation plus representative real endpoints reports freshness, resource and storage overhead. |
| P11-10 | Deliver a recoverable Linux-hosted management foundation. | Controller/agent restart, certificate expiry and provider outage preserve device identity and show stale state without affecting domain login. |

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
