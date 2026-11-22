# P00-17 timing amendment — merged decision record

Status: **owner approved on 22 November 2026; merged in PR #42**.
The exact Phase 0 and `SECURITY.md` replacement wording comes from the
[P00-17 timing record](p00-17.md).
The effective [P05-04](../phases/phase-05.md) row makes the deferred operational
gate explicit. This decision did not authorize a report, appoint a backup, or
accept either requirement.

## Owner decision record

Ise-Tom answered **Approve** in the Phase 0 worker chat on 22 November 2026 to
this exact question:

> Approve the [exact P00-17 timing wording](https://github.com/Ise-Tom/Babel/blob/4c4431b2068bc1481aae53f341e282ba868a7345/docs/validation/p00-17.md#proposed-timing-decision--not-effective) and [prepared policy diff](C:/Users/Anxie/.codex/worktrees/phase0-security-response-timing/Babel/docs/validation/p00-17-timing-review.md)? Approval moves Phase 0 to process evidence, requires a live drill before soliciting preview users, and moves backup plus disclosure/version-policy gates to production under P05-04. Current policy stays until merge.

The answer approved only that timing amendment and the prepared P05-04 gate.
It does not authorize report submission or participant contact, and does not
accept P00-17 or P05-04. [PR #42](https://github.com/Ise-Tom/Babel/pull/42)
merged the amendment; the effective criteria are in the phase and security
policy files.

| Milestone | Effective evidence and gate |
| --- | --- |
| Phase 0 | Review the private-intake runbook and benign offline ledger rehearsal: reporter, owner and backup roles; custody, acknowledgment, escalation and incomplete states; an exact live-drill plan. The accessible form and simulated events remain insufficient as operational proof. |
| Before soliciting external preview users | State publicly that the preview is unsupported and only one responder is available. With separate authorization, run and privately close a benign live report; independently record owner notification, private receipt and acknowledgment, then publish only redacted outcome metadata. A failed route blocks solicitation until repaired. |
| Before supported production under P05-04 | Retain a live private report ID and independently verified owner notification, receipt, acknowledgment and closure. Appoint two genuinely available contacts, verify each one's private access and receipt, and exercise owner-absence escalation with the backup. Also complete the supported-version/disclosure policies, independent assessment, compromise containment, clean recovery and credential/key-rotation exercises required by `SECURITY.md`. Offline simulation or a nominal contact cannot pass. |

## Safeguard differences approved with the timing change

- The former Phase 0 row required a live private
  drill and a real backup for P00-17 acceptance. The amendment permits
  **process-design acceptance in Phase 0**, while moving both operational proofs
  to P05-04. No acceptance decision is implied by the amendment.
- The former `SECURITY.md` required two contacts before
  **public previews**. The effective text requires them before **supported
  production**. An unsupported preview may therefore have only one responder,
  with that limitation visible.
- The former policy also required embargo/coordinated-disclosure rules and a
  version support policy **before public previews**. The adopted text
  puts supported-version and coordinated-disclosure policies **before supported
  production**. That is an additional timing relaxation, beyond the second
  contact, and must be included in the owner's decision. It does not license
  concealing the preview's unsupported status or publishing private details.
- The adopted paragraphs would otherwise have deleted the existing report-content
  guidance and immediate triage/key-rotation guidance for critical exploited
  issues. The prepared `SECURITY.md` diff preserves both sentences unchanged
  as standalone paragraphs; this is not a relaxation of those safeguards.
- The amendment changes the preview checkpoint from **before public previews**
  to **before soliciting external preview users**. Publishing an experimental
  preview without inviting external users could occur before the live route
  check under the proposed wording; inviting users or reports cannot. This
  boundary must be intentional.

The two-working-day acknowledgment and seven-day update intervals remain
proposed targets, not current SLAs. Any support commitment needs staffed and
tested evidence. This timing decision alone did not accept P00-17 or qualify
the live preview/production gates.
