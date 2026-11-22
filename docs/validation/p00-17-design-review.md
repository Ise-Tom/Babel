# P00-17 amended Phase 0 process-design review

Reviewed against [the effective P00-17 row](../phases/phase-00.md) on main
revision `f2ddab38760d3f830200e20949eda1149e51037d` (23 November 2026).
The timing amendment was merged in [PR #42](https://github.com/Ise-Tom/Babel/pull/42).
This packet assesses only the amended **Phase 0 process-design gate**. It does
not claim a submitted report, verified live receipt, a real backup, P05-04
production readiness, or P00-17 acceptance by the owner.

| Criterion element | Reviewed design evidence | Disposition / limit |
| --- | --- | --- |
| Private-intake runbook | [Runbook](../security-response-readiness.md) steps 1–5 define private route/fallback, triage, isolated synthetic reproduction, hostile-attachment custody, containment, disclosure and recovery. [Exact benign draft and ledger](p00-17.md#exact-benign-draft-for-an-authorized-live-drill) define the intended future exercise. | Design present. The report form was observed read-only; no report was submitted. |
| Reporter role | Runbook role table assigns private submission, synthetic content, confirmation and report ID after specific authorization. The [draft](p00-17.md#exact-benign-draft-for-an-authorized-live-drill) contains exact proposed fields. | Role present; no reporter is authorized to submit. The observed browser account is not an appointment. |
| Owner role | Runbook names Ise-Tom, with independent notification check, maintainer-side opening and private acknowledgment; [ledger](p00-17.md#live-drill-ledger-and-verification-roles) requires UTC evidence and closure. | Role present; actual notification, opening and acknowledgment unrun. |
| Backup role | Runbook defines a future consenting person with limited private access, independent receipt and ability to respond during owner absence. [P05-04](../phases/phase-05.md) requires two genuinely available contacts before production. | Role present as a design placeholder; no person appointed, available or tested. |
| Custody | Runbook excludes secrets and private evidence from public issues, CI and third-party upload; ledger keeps report URL/ID, account details and comments restricted, with only redacted outcomes public. | Custody plan present; no real private ledger exists. |
| Acknowledgment | Runbook records a private owner acknowledgment and timestamp; ledger distinguishes reporter confirmation, notification, owner opening and acknowledgment. Two-working-day/seven-day intervals are proposed targets, not active SLAs. | Process present; no live acknowledgment. |
| Escalation | Runbook assigns an independent verifier to trigger the private backup route while the owner is unavailable; backup responds directly and owner reviews later. Ledger records trigger, delivery, acknowledgment and failure path. | Owner-absence design present; no verifier, backup or live escalation appointed or exercised. |
| Failure handling | Route-unavailable fallback waits for a private channel; absent notification/open/acknowledgment or backup response stays failed/incomplete. The offline cases explicitly retain missing owner/backup states. | Failure rules present; no operational pass inferred. |
| Live-drill plan | [Draft and ledger](p00-17.md) define exact content, authorization, roles, UTC observations, closure and redaction. An owner-only route drill is due before soliciting external preview users; backup/owner-absence exercise remains due under P05-04 before supported production. | Plan present. Both operational checkpoints remain unrun and require separate authorization. |
| Benign offline recordkeeping rehearsal | [Fixture](../../lab/security-intake/offline-rehearsal.json), [validator](../../scripts/check_security_intake.py), [retained fresh result](../../lab/security-intake/evidence/review-f2ddab3-2026-11-23.json) and [negative tests](../../tests/test_security_intake.py). | Design rehearsal passes; `live_intake_and_backup_ready` remains `false`. Simulated actors and timestamps are not delivery or backup evidence. |

## Fresh reproducible review evidence

The dedicated worktree started at the reviewed main revision above. This PR
adds explicit simulated owner absence and independent escalation-trigger events
to the fixture and validator; the fixture and result carry that reviewed base
revision. On 23 November 2026, with Python 3.13, the following commands
completed locally:

```text
python scripts/check_security_intake.py --output lab/security-intake/evidence/review-f2ddab3-2026-11-23.json
python -m unittest discover -s tests -p test_security_intake.py -v
```

The validator returned `offline_complete_not_gate_evidence` for the complete
mock case; `incomplete:owner_opened,owner_acknowledged` for notification without
owner receipt; `incomplete:backup_role_accepted,backup_opened,owner_absence_observed,escalation_triggered,escalation_acknowledged`
for owner receipt without backup; and `incomplete:owner_acknowledged` for owner
opening without acknowledgment. It returned `live_intake_and_backup_ready: false`.
Both test methods passed; nine subtests rejected a fabricated live ID, invented
backup, missing case, false pass, wrong actor, duplicate event, missing trigger,
owner-triggered escalation and reversed timestamp.
The test also compares the retained result with a fresh validator call.

SHA-256 of exact execution inputs and retained output:

| File | SHA-256 |
| --- | --- |
| `lab/security-intake/offline-rehearsal.json` | `2c79699fd35ade76f44fbf7daf4a790b855f2a840b10ae62315d5b0717926ab7` |
| `scripts/check_security_intake.py` | `1c0081d9ef3f5ffc8524f6e510b2ddecc0967d2c96b0d72a8921493791002efb` |
| `lab/security-intake/evidence/review-f2ddab3-2026-11-23.json` | `19d721cfe89cd6bf2a33b9b2d703ec2902fa55ef4616a4585770f12029e99a9d` |

The validator checks the structure and expected classifications of synthetic
records. It cannot verify GitHub notifications, actual maintainer access,
human backup availability, or escalation during absence. CI must pass before
an owner decision on this packet. Approval would accept only P00-17's amended
Phase 0 **process-design** scope; it would not authorize the live drill or
accept the P05-04 production gate.
