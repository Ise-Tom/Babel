# Phase 15 — General server-to-device file delivery

Status: specified; product acceptance not demonstrated.
Owner roles: file-delivery/agent maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires separate upload rights and qualified endpoint identity/transport. Upload is not remote execution, patch approval or permission to retrieve user files. This phase covers Linux-server-to-Windows/Linux-device delivery.

## Design and interfaces

An uploader stages content in protected Linux storage, previews fixed device scope/destination/digest/expiry and requests approval for sensitive/bulk targets. Authenticated relays stream resumable bounded chunks. The endpoint validates authority and destination at finalization, stages to a safe temporary path and atomically commits where supported; execution is a separate authorized operation.

## Data and lifecycle

Keep content identity separate from filename, immutable target snapshots, transfer offsets, authorized destination, ownership/overwrite policy and receipts. Record staged/partial/verified/failed/expired states and cleanup timers. Do not log confidential file bytes; device-to-server forensic retrieval needs a separate permission/policy.

## Security and failure handling

Defend against traversal, symlink/reparse-point races, protected startup/system destinations, stale recipient expansion, quota exhaustion and malicious content. Hashes rely on authenticated metadata; scanners do not prove harmlessness. Neither upload nor overwrite may bypass signed updater or OS privilege boundaries.

## Capacity and operations

Initial qualification profile: 250 concurrent transfers fleet-wide with 50 x 1-GiB payloads plus small files, under per-site bandwidth/quota limits. Ratify completion-time expectations from actual links; a 20-Mbit/s site cannot satisfy arbitrary short deadlines. Test large file/offset bounds, interruption and disk pressure on real filesystems.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P15-01 | Authorize exact file content, device scope, destination and expiry. | Target/digest/path changes require renewed approval; upload-only and cross-group operators cannot gain execution, patch or retrieval rights. |
| P15-02 | Protect staging and source/recipient authenticity. | Wrong sender/device, tampered metadata, unauthenticated hash substitution and untrusted TLS are rejected; staged confidential files are access-restricted. |
| P15-03 | Validate destinations at open/finalization without traversal/race bypass. | Real Windows reparse and Linux symlink/rename race tests cannot escape allowed directories or overwrite privileged startup/system files. |
| P15-04 | Apply explicit ownership, ACL and overwrite policy. | Default deny for privileged locations; approved overwrite preserves declared permissions and cannot convert a data upload into executable persistence. |
| P15-05 | Provide resumable bounded authenticated transfers. | Corrupt/reordered/replayed chunks, offset overflow, connection loss and retries cannot finalize incorrect or unauthorized content. |
| P15-06 | Finalize atomically where supported and report verified receipt. | Partial files are never treated as delivered; unsupported atomic behavior is visible and staged fallback is tested with interrupted finalization. |
| P15-07 | Enforce quotas, bandwidth, cancellation and stale-content cleanup. | Full disk, expired/cancelled jobs and abandoned staged data remain bounded; reconnect revalidates authority before continuing. |
| P15-08 | Apply explicit file-content and malware policy without automatic execution. | Type/size/scanning failures block according to policy; detection limits are documented and uploads cannot silently launch installers/scripts. |
| P15-09 | Provide privacy-safe audit and separate retrieval policy. | Operator/device/path/digest/outcome are auditable without raw contents; uploading never grants access to user files or unsolicited endpoint surveillance. |
| P15-10 | Qualify transfer recovery and mixed-load resource isolation. | Concurrent representative real filesystem transfers survive agent/controller restarts and malicious paths without directory SLO regression. |

## Evidence and exit

For every P15 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 14 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply. Requires Phase 05/06 supported Linux deployment and recovery, plus Phase 07 identity/authorization and Phase 10 agent/update assurance.

Traceability: FILE-01, FILE-02, FILE-03, FILE-04, FILE-05

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
