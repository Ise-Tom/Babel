# Phase 16 — Native endpoint detection and response

Status: specified; product acceptance not demonstrated.
Owner roles: endpoint detection/security maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires secure agent lifecycle and separately authorized security-response roles. Native telemetry/detection must be implemented; SIEM ingestion alone is not Babel EDR. Detection and prevention modes remain distinct.

## Design and interfaces

OS-specific sensor modules collect bounded process/network/file/security observations into local protected buffers, then send provenance-tagged events through authenticated Linux-hosted ingestion. Versioned rules correlate telemetry into alerts/cases. An independent response authorizer issues typed expiring process/file/isolation actions; patch/support roles cannot mint them.

## Data and lifecycle

Track device/boot/process identity and rule/sensor version to avoid PID-reuse confusion. Store event sequence/gaps, provenance, evidence custody and case/action history with privacy-scoped retention. Separate raw telemetry, enriched alerts and collected evidence; never capture credentials/memory/user files indiscriminately.

## Security and failure handling

Use supported Windows telemetry/security APIs and Linux audit/eBPF interfaces, qualified by exact OS/kernel. Kernel drivers require justification, independent review and platform signing; do not disable Secure Boot/protections. Root/kernel compromise may defeat the sensor. False positives cannot trigger unlimited fleet-wide containment.

## Capacity and operations

Provisional fleet model for Phase 17: 2 events/device/s steady and 20/device/s five-minute burst, average 500-byte event envelope before indexing/replication. At 10k devices, steady raw input is ~10 MB/s/~864 GB/day. Set raw/alert/evidence retention and provider sizing from measured cost, loss and detection value.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P16-01 | Ship a dedicated securely enrolled signed sensor/agent module. | Per-device identity/revocation, staged signed updates and authorized rescue/uninstall pass; module rights are isolated from support and patch executors. |
| P16-02 | Qualify supported telemetry on real endpoint OS/kernel builds. | Process lineage/hashes, network, file and selected persistence/security events match fixture ground truth; unavailable sources/blind spots are explicit. |
| P16-03 | Preserve stable event/process provenance and loss visibility. | PID reuse, clock changes, reconnect duplicates, reordered events and buffer overflow cannot silently corrupt identity or claim complete healthy telemetry. |
| P16-04 | Implement signed/versioned bounded detection and indicator rules. | Labeled malicious/benign synthetic scenarios measure precision/recall and alert delay; costly/untrusted rules cannot exhaust endpoint resources. |
| P16-05 | Provide privacy-scoped investigation and evidence collection. | Case/timeline/collection actions require scope and audit; evidence hashes/provenance/retention and denied-reader tests pass without blanket memory/credential extraction. |
| P16-06 | Implement typed authorized process/file containment and quarantine. | Wrong process generation, expired/replayed jobs, protected system targets and unauthorized analysts are rejected; quarantine limitations are documented. |
| P16-07 | Provide recoverable device isolation and bounded automated response. | Narrow authenticated rescue paths survive isolation; two-person/mass-action limits and false-positive tests prevent fleet/DC lockout; release-from-isolation is rehearsed. |
| P16-08 | Operate offline buffering and trusted cached rules safely. | Disk/memory quotas, encryption/access controls, sequence gaps and reconnect backpressure preserve visibility; outages do not stall domain login or fill disks indefinitely. |
| P16-09 | Detect sensor tamper and define realistic protection boundaries. | Stopped/stale sensors, changed policy and signer failure alert with provenance; root/kernel control is not claimed containable by local tamper protection. |
| P16-10 | Qualify detection/prevention behavior and external response integrations. | Real endpoint performance, false positives/negatives, benign safety and SIEM/SOAR connector replay/authorization tests pass before enforcement is enabled. |

## Evidence and exit

For every P16 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 15 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply. Requires Phase 05/06 supported Linux deployment and recovery, plus Phase 07 identity/authorization and Phase 10 agent/update assurance.

Traceability: EDR-01, EDR-02, EDR-03, EDR-04, EDR-05, EDR-06, EDR-07, EDR-08

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
