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
