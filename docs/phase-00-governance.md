# Phase 0 upgrade, recovery and scope governance

Status: proposed design; no runtime upgrade or clean-domain restore is accepted.
The current sole maintainer reviews changes through PRs and up-to-date CI. This
process does not require a second-person development approval. Independent
production review and operational coverage remain separately required evidence.

## Change record and acceptance

Every change names affected global/Pxx IDs, owner, exact scope, security/capacity
impact, format/protocol/API compatibility, tests, evidence invalidation and recovery.
Update the dashboard in the same PR with implementation, verification, limitations
and encountered development problems. Requirements keep stable IDs; extra substeps
follow actual scope rather than an equal quota per phase. Only the owner’s explicit
acceptance, with pinned evidence and exact scope, changes accepted counts.

Record a compatibility exception with ID, owner, exact operation/client/site/scope,
reason, compensating control, activation/expiry in UTC, review disposition and
production impact. Expiry disables the exception or blocks release; it cannot
silently renew. No exception may remove AD-01–AD-10, IAM-01, OPS-01, UX-01 or baseline
security from the first-production contract. Unknown/unrun remains visible and
cannot be converted to passing by a scope edit. Amend the matrix/digest and rerun
affected observations after intentional scope changes.

## Irreversible transitions and worked recovery cases

| Transition | Entry / forward action | Failure and recovery contract |
| --- | --- | --- |
| Local schema/SQL migration | Version capability check, exclusive bounded migration authority, coherent tested backup and dry-run compatibility | Interrupted migration yields old complete state or declared new state; record checkpoint/version, stop serving incompatible writes and resume or restore. Reverting the binary is not data rollback |
| Credential encryption/key rotation | Versioned key classes and access, recovery escrow/custody, dual-read interval and explicit cutover | Provider loss blocks affected operations; never write plaintext or silently select a weaker key. Prove retained data recovery before retiring the old key |
| Restore a whole domain/DC | Validate directory/SYSVOL/keys/schema/replica metadata as one coherent backup; start isolated | Quarantine stale invocation/USN state; qualified epoch/rejoin and credential revocation reconciliation precede service. A VM snapshot alone is insufficient |
| Domain/forest level or schema extension | Compare approved functional/profile support across every eligible DC and client | Refuse unsupported/unrehearsed transitions; document irreversibility. A rejected operation changes no advertised level or partial schema |
| Storage engine/record encoding | Versioned export/import, stable GUID/SID and descriptor/matching invariants, complete audit/checkpoint mapping | Compare identities/ACLs/counts and restore test before cutover; retain encrypted original until verified recovery. Adapter isolation reduces coupling but does not make migration trivial |
| GPO/SYSVOL publication | Stage content/ACL/directory version, verify and publish using a recoverable state machine | Interrupted file/SQL writes remain explicitly incomplete; reconcile/revert without serving a falsely coherent policy |

Before valuable credentials or irreversible formats, the corresponding design,
key/durability review and failure cases need executable qualification. The synthetic
PostgreSQL experiment only covers its documented local transaction/process-crash
subset. It cannot authorize production credential storage or AD replica restore.

## Phase 0 review sequence

Review the 2016 initial functional scope and explicit non-Windows client matrix;
pin exact image/package/spec versions with rights; provision the isolated lab twice;
exercise private intake/backup contact; qualify dependency choices and worked state
cases; then inspect evidence outcomes and workload assumptions requirement by
requirement. Accept a design scope explicitly where appropriate, while keeping
unrun real-client and infrastructure requirements blocked. Whole Phase 0 exit
requires all its stated acceptance evidence and an explicit separate phase decision.
No acceptance is prefilled by these documents.

## Completed Phase 0 contract and executable consistency checks

The original P00-10 design gate is now complete and submitted for explicit owner
validation in the [criterion packet](validation/p00-10.md). Runtime upgrade,
secret rotation and domain recovery are **unrun implementation gates**, rather
than evidence this design checker manufactures. The requirements themselves have
not been narrowed. See the [functional-level profile](functional-level-profile.md)
for the selected levels and transition review.

The [versioned contract](../lab/phase0-contract.json) contains all six worked
changes above. Each names its scope/owner/requirements; security, capacity, format,
protocol and API impact; forward checkpoint; interruption; recovery controls;
evidence invalidation/reruns; production impact; and proposed review disposition.
For example, an interrupted key rotation denies secret operations and retains both
recoverable encrypted generations; an incomplete GPO publication stays hidden
until directory/SYSVOL content, ACLs and versions reconcile. These are normative
outcomes to implement and test, not claims that those operations currently run.

[Required CI](../.github/workflows/ci.yml) runs the
[planning checker](../scripts/check_phase0_contract.py), which rejects omitted
recovery material, unsupported level declarations, binary-revert-only recovery,
rewritten runtime outcomes and incomplete evidence-invalidation rules. It emits
source revision, exact contract/matrix SHA-256, check time and the six reviewed
change families in a retained `phase0-contract-evidence` artifact. The usual
strict lint/type/security and branch-coverage checks also cover this tool.

An active scope exception must identify operation, client, site, owner, scope,
reason, compensating control, explicit review evidence and production impact.
UTC activation is inclusive and expiry exclusive; inactive/expired entries fail
CI and never renew. No current exception exists. No first-production global
baseline ID may be waived; unknown IDs and phase-gate waivers are rejected. No
exception may rewrite observations as passing.
A changed source/profile/schema/key class/scope/expected result invalidates its
affected evidence and requires fresh cases; keeping an old hash is not revalidation.

This checker validates **review material and consistency**. It does not verify
that prose is sufficient, authenticate a named reviewer or escrow, grant Tier 0
access, enact a change, or prove runtime recovery. The owner reviews the actual
PR/evidence using the established solo-maintainer process. Future runtime command
handlers must enforce their own authority, version/checkpoint and fail-closed
state machines. Owner acceptance of P00-10 remains a separate dated decision;
Phase 0 exit and production approval are never inferred from a passing record.
