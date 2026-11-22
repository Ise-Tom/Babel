# Security response readiness for solo development

Status: **timing amendment merged in PR #42; amended P00-17 Phase 0 process design accepted**.
The [P00-17 drill, offline rehearsal and exact timing decision packet](validation/p00-17.md)
supports the accepted Phase 0 process design. Its simulated records and
available report form do not meet the live-drill or backup requirement.
The [amended criterion review](validation/p00-17-design-review.md) maps each
Phase 0 process obligation to the runbook and fresh offline evidence.
Ise-Tom is the current development owner. No backup responder, verified private
receipt or supported production service is claimed. On 19 November 2026, a
read-only GitHub API check reported private vulnerability reporting enabled.
Configuration alone does not test notification delivery, owner access or response.
No report or message was submitted.

## Effective timing and roles

The [effective P00-17](phases/phase-00.md) is a process-design review. A live
owner-receipt drill is required before soliciting external preview users; the
[P05-04](phases/phase-05.md) production gate also requires a real backup with
independently verified private access, receipt and owner-absence escalation.
A second developer is not necessary for the backup role, but a genuinely
available second person is necessary. An assistant is not that person.

| Milestone | Effective requirement | Evidence limit |
| --- | --- | --- |
| Phase 0 | Review intake, custody, acknowledgment, escalation, failure handling and live-drill plan with a benign offline rehearsal | Design evidence does not prove live receipt or backup coverage |
| Before soliciting external preview users | State unsupported/sole-responder status; run and privately close an authorized live report with independently verified owner notification, receipt and acknowledgment | A form or simulated event cannot pass; a failed route blocks solicitation |
| Before supported production | Two genuinely available contacts, each with verified private access and receipt; backup demonstrates owner-absence escalation; live drill, assessment and recovery evidence remain current | An untested nominee or owner-dependent escalation cannot pass P05-04 |

Ise-Tom approved the timing decision in the [decision record](validation/p00-17-timing-review.md#owner-decision-record), and [PR #42](https://github.com/Ise-Tom/Babel/pull/42) merged it. Ise-Tom separately accepted the amended P00-17 [process-design scope](validation/p00-17-design-review.md#owner-acceptance-of-the-amended-phase-0-scope) on 23 November 2026. Neither decision turns enabled reporting into live receipt or authorizes a synthetic report.

| Role | Process responsibility | Current evidence |
| --- | --- | --- |
| Reporter | Uses only the private route after exact authorization, supplies synthetic data, retains submission confirmation and private report ID | Draft and reporter-side form observation only; no submission |
| Owner — Ise-Tom | Checks notification independently, opens/acknowledges privately, triages, protects the record and closes the drill | Named accountable owner; notification/open/acknowledgment unrun |
| Backup — future consenting person | Confirms limited private access and receipt, can acknowledge and coordinate escalation when the owner is absent | Role defined; no person appointed, contacted or tested |
| Independent escalation verifier — designated for a future drill | Triggers the agreed private backup route while the owner is unavailable and records the observed result | Role defined; no person appointed or exercise run |

## Intake and custody process

1. Report through GitHub private vulnerability reporting. If it is unavailable,
   request a private contact without public vulnerability details and wait for the
   channel. Do not solicit public secrets, captures or production directory data.
2. The owner checks private report access and triages affected commit/version,
   exposure and reproduction with synthetic data. Treat attachments as hostile;
   avoid privileged execution, public CI artifacts and third-party upload services.
3. Record severity, scope, confidentiality and an acknowledgment in the private
   record. Existing two-working-day acknowledgment/seven-day update targets are
   proposed targets; there is no active response SLA or supported version today.
4. Reproduce in an isolated owned lab, contain exposure and prepare a tested fix.
   Credential/key compromise requires rotation and clean recovery guidance where
   applicable. Avoid placing exploit details or private evidence in public PRs.
5. Agree disclosure timing privately, publish a coordinated advisory when ready,
   identify affected/fixed revisions and document operator recovery. Track follow-up
   regressions and reopen incomplete remediation instead of assuming a code patch
   cures an already compromised domain.

## Sole-owner absence and future continuity

The owner remains the only accountable contact. Notifications and stored drafts
are not backup coverage. During a planned absence, announce reduced availability
without secrets, keep experimental support limits visible and avoid soliciting
new users on a promise of prompt response. If intake access is lost, establish a
verified private route before inviting sensitive submissions. An unsupported
preview must not be promoted to a supported production release while receipt,
backup coverage or incident recovery remain unverified.

A future backup must explicitly agree to the role, have tested private access,
know the escalation/absence procedure and be able to coordinate containment and
disclosure. An independent verifier must be able to trigger the backup route
without the owner initiating or forwarding it; the owner reviews the record
after returning. Do not grant general deployment/domain authority just to read
reports; review least-privilege access and recovery custody separately. No
contact details should be invented or exposed by this document.

## Drill record to complete after explicit authorization

Use a clearly labeled benign synthetic report, no real vulnerability or secret.
Retain the private report identifier, UTC submission/receipt/acknowledgment times,
verified recipients, notification/access outcome, backup acceptance and escalation
result, closure and follow-up. Publish only redacted outcome metadata. A missing
acknowledgment or unavailable backup is a failed/incomplete drill, never a pass.
Each participant must verify their own receipt. The current record is **unrun**;
no private identifier, recipient or successful escalation is recorded.

This process design is tracked separately from the completed P00-07 threat/
boundary design. It does not claim independent assessment, real incident
response or whole-phase acceptance.
