# Security response readiness for solo development

Status: **timing amendment approved for PR review, not a requirement acceptance**.
The [P00-17 drill, offline rehearsal and exact timing decision packet](validation/p00-17.md)
is prepared for review. Its simulated records and available report form do not
meet the live-drill or backup requirement.
Ise-Tom is the current development owner. No backup responder, verified private
receipt or supported production service is claimed. On 19 November 2026, a
read-only GitHub API check reported private vulnerability reporting enabled.
Configuration alone does not test notification delivery, owner access or response.
No report or message was submitted.

## Original gate and approved timing amendment

Before this amendment, P00-17 required an actual private intake drill and a
real backup contact; `SECURITY.md` required two contacts before public previews.
Those original rules remain in force on main until the approved amendment
merges. A second
developer is not necessary for a backup role, but a genuinely available second
person is necessary to claim backup coverage. An assistant is not that person.

| Decision | Current requirement | Proposed solo-development timing |
| --- | --- | --- |
| Phase 0 | Live intake drill and real backup demonstrate receipt/escalation | Review intake, custody, triage and owner-absence process; record untested routing and sole-responder risk |
| Experimental preview | Two contacts and tested reporting route before public previews | Clearly unsupported development preview; visible sole-responder limitation, tested private route before soliciting external testers |
| Supported production release | Independent assessment and operational response remain required | Mandatory verified receipt/escalation drill and genuinely available backup before supported production; no silent exception |

Ise-Tom approved the exact timing decision in the [decision record](validation/p00-17-timing-review.md#owner-decision-record).
The canonical policy change is in this review branch. P00-17 is not accepted;
approval does not turn enabled reporting into passing evidence or authorize a
synthetic report.

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
disclosure. Do not grant general deployment/domain authority just to read reports;
review least-privilege access and recovery custody separately. No contact details
should be invented or exposed by this document.

## Drill record to complete after explicit authorization

Use a clearly labeled benign synthetic report, no real vulnerability or secret.
Retain the private report identifier, UTC submission/receipt/acknowledgment times,
verified recipients, notification/access outcome, backup acceptance and escalation
result, closure and follow-up. Publish only redacted outcome metadata. A missing
acknowledgment or unavailable backup is a failed/incomplete drill, never a pass.
Each participant must verify their own receipt. The current record is **unrun**;
no private identifier, recipient or successful escalation is recorded.

The proposal is tracked separately from the completed P00-07 threat/boundary
design. It does not claim independent assessment, real incident response or
whole-phase acceptance.
