# Phase 14 — Remote desktop and terminal access

Status: specified; product acceptance not demonstrated.
Owner roles: remote-support/security maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires unique device identity and separate support-operator roles; directory/patch membership alone does not authorize remote access. Qualify supported Windows/Linux desktop and terminal protocols before broad rollout.

## Design and interfaces

A Linux-hosted broker authenticates the operator with step-up, authorizes a target/time-bound session and requests endpoint consent or explicit unattended policy. Endpoint-initiated relay channels avoid default Internet-exposed RDP/SSH ports. Desktop/terminal engines honor OS session and elevation boundaries; the support executor is separate from allowlisted patch actions.

## Data and lifecycle

Persist actor/device/session IDs, approvals, consent/grant expiry, start/end and allowed channels. Keep credential custody explicit; a web MFA assertion is not a reusable RDP/SSH password. Recording/clipboard/drive redirection require separate policy; redacted audit is not unrestricted keystroke capture.

## Security and failure handling

Reject stolen/replayed session tokens, wrong devices, consent substitution and privilege escalation. Default to attended consent; unattended access requires explicit enrollment/device policy and scoped independent permission. Bound revocation/disconnect time and define outage behavior; broker-terminated encryption must not be labeled end-to-end.

## Capacity and operations

Initial joint-qualification target: 50 concurrent desktop and 100 terminal sessions fleet-wide, not 10k simultaneous desktops. Ratify resolution/codec/bitrate/latency and relay sizing before release. Network/broker outage must visibly end or safely suspend authority, not create indefinite sessions.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P14-01 | Qualify actual desktop sessions by supported endpoint platform. | Real Windows/Linux desktops including X11/Wayland have exact build/engine and unsupported-behavior evidence. |
| P14-02 | Require unique authenticated devices and scoped operator MFA/step-up. | Wrong-device, replayed/expired tokens and stolen low-privilege accounts cannot open a session or reuse a privileged endpoint credential. |
| P14-03 | Provide visible attended consent and immediate disconnect. | Denied/expired/misleading requests fail; local user sees operator identity and can terminate a session without a remote approval. |
| P14-04 | Gate unattended support separately with time/device boundaries. | No implicit permission from domain membership or patch role; expired device/operator grants fail and administrative access is audited. |
| P14-05 | Separate terminal, clipboard, transfer and recording channels. | Denied channels cannot be reenabled through protocol/API bypass or unrelated support grants. |
| P14-06 | Authenticate and encrypt broker/session transport. | Certificate, recipient and session-binding failures close connections while protecting device/operator credentials. |
| P14-07 | Enforce bounded revocation and outage session policy. | A connected session loses authority within a configured, tested <=60 s revocation target; offline/broker-failed cases follow explicit safe expiry rules. |
| P14-08 | Govern recording purpose, access and retention. | Recordings have explicit reader policy, expiry/deletion and protected evidence custody. |
| P14-09 | Handle reconnect, concurrent operators and privilege changes safely. | Session identity and consent are revalidated; no unnoticed takeover, indefinitely cached grant or unintended concurrent control survives switching/restart. |
| P14-10 | Qualify relay concurrency, bitrate and latency. | Real-session load publishes bounded resource/capacity limits without starving identity traffic. |
| P14-11 | Qualify terminal and headless access independently. | Real Windows/Linux terminal cases have declared engines and identity boundaries; desktop tests cannot qualify headless access. |
| P14-12 | Enforce elevation, lock-screen and OS security prompts. | Switching users and elevating require scoped authority/consent; remote support cannot suppress native security boundaries. |
| P14-13 | Qualify relay trust, content visibility and NAT/proxy paths. | Compromised relay tests document content visibility and prevent impersonation or silent encryption weakening. |
| P14-14 | Enforce recording notice, consent and sensitive-input boundaries. | Users see accurate recording policy; covert capture and indiscriminate credential/key logging fail tests. |
| P14-15 | Recover from compromised operators or support brokers. | Revocation, termination and independent rescue regain control without depending on the compromised broker. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P14-01`: separately verify `P14-11`.
- `P14-05`: separately verify `P14-12`.
- `P14-06`: separately verify `P14-13`.
- `P14-08`: separately verify `P14-14`.
- `P14-10`: separately verify `P14-15`.

## Evidence and exit

For every P14 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 13 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply. Requires Phase 05/06 supported Linux deployment and recovery, plus Phase 07 identity/authorization and Phase 10 agent/update assurance.

Traceability: REMOTE-01, REMOTE-02, REMOTE-03, REMOTE-04, REMOTE-05, REMOTE-06

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
