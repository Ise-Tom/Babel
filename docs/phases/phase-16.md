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
| P16-01 | Enroll a dedicated sensor module with isolated authority. | Per-device identity/revocation and module boundaries prevent unrestricted patch/support credential reuse. |
| P16-02 | Implement supported native telemetry sources. | Process/network/file and selected persistence/security sources use the exact declared OS/kernel interfaces. |
| P16-03 | Preserve stable event/process provenance and loss visibility. | PID reuse, clock changes, reconnect duplicates, reordered events and buffer overflow cannot silently corrupt identity or claim complete healthy telemetry. |
| P16-04 | Verify and execute bounded signed/versioned detection and indicator rules. | Untrusted/costly rules cannot bypass signing/version policy or exhaust endpoint CPU/memory. |
| P16-05 | Provide scoped investigation and collection actions. | Case/timeline/collection permissions are audited and denied across unauthorized assets without blanket credential/memory extraction. |
| P16-06 | Contain the authorized process generation safely. | PID reuse, protected targets and expired/replayed/wrong-scope actions fail with generation-aware receipts. |
| P16-07 | Implement recoverable network isolation. | Narrow authenticated rescue survives isolation and release is rehearsed on actual endpoints. |
| P16-08 | Operate offline buffering and trusted cached rules safely. | Disk/memory quotas, encryption/access controls, sequence gaps and reconnect backpressure preserve visibility; outages do not stall domain login or fill disks indefinitely. |
| P16-09 | Detect sensor tamper and define realistic protection boundaries. | Stopped/stale sensors, changed policy and signer failure alert with provenance; root/kernel control is not claimed containable by local tamper protection. |
| P16-10 | Qualify prevention safety and endpoint overhead. | Supported enforcement, benign-safety and real performance cases meet declared limits before enabling prevention. |
| P16-11 | Sign, stage, recover and uninstall the sensor securely. | Signed updates, authorized rescue/uninstall and staged rollback/forward-recovery work without stealth persistence. |
| P16-12 | Qualify telemetry ground truth and platform blind spots. | Real fixtures compare events/lineage/hashes against truth; missing sources and unsupported builds remain visible. |
| P16-13 | Measure labeled detection quality and alert delay. | Versioned malicious/benign scenarios publish precision/recall, latency and false positives/negatives; missing signals are not clean results. |
| P16-14 | Preserve evidence provenance, integrity and retention. | Artifacts retain hashes/source/custody and authorized retention; tampered/incomplete evidence and unauthorized readers are rejected. |
| P16-15 | Quarantine and recover files under separate authority. | Quarantine/release preserves provenance/scope and documents prior-execution limits and protected-file recovery. |
| P16-16 | Bound automated and mass-response blast radius. | Independent high-impact approvals and false-positive tests prevent fleet/DC lockout or unrestricted authority from one detection. |
| P16-17 | Integrate SIEM/SOAR without replaying response authority. | Duplicate/forged/replayed connector actions and stale external grants cannot bypass typed native response controls. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P16-01`: separately verify `P16-11`.
- `P16-02`: separately verify `P16-12`.
- `P16-04`: separately verify `P16-13`.
- `P16-05`: separately verify `P16-14`.
- `P16-06`: separately verify `P16-15`.
- `P16-07`: separately verify `P16-16`.
- `P16-10`: separately verify `P16-17`.

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
