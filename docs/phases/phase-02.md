# Phase 02 — Complete directory and AD interoperability contract

Status: specified; product acceptance not demonstrated.
Owner roles: protocol/conformance maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires the native slice, reviewed credential model and reference lab. Complete AD-01–AD-10 and IAM-01 operations; no missing protocol is silently deferred beyond first production.

## Design and interfaces

Protocol adapters share one identity/ACL/schema authority across LDAP/GC, Kerberos/PAC, DNS, SMB/RPC/Netlogon and GPO. A forest/domain capability model exposes only qualified functional levels. Trust evaluation handles external identity namespaces explicitly. Test the replication wire/metadata contract here, then qualify distributed failure behavior in Phase 3.

## Data and lifecycle

Define naming contexts, schema updates, principal/SPN uniqueness, SID history constraints, trust records, FSMO ownership and policy versions. Migration preserves identities and permission relationships through a supported mapping; password/key migration depends on supported secure mechanisms, not generic CSV export.

## Security and failure handling

Cover protocol downgrade, forged PAC/trust claims, unsafe delegation, LDAP ACL leaks and malicious GPO content. Reject unqualified feature levels. Trust and schema mutations need elevated approval and auditable state transitions. A failing reference comparison remains a blocker even if native unit tests pass.

## Capacity and operations

Exercise full object dataset, group nesting, indexed/paged searches and bounded unindexed queries. Report operation/client coverage independently from throughput. Coexistence tests use disposable independent forests; production credentials never enter public CI.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P02-01 | Complete domain/forest lifecycle and naming contexts. | Reference creation/removal and queries preserve forest/domain boundaries and reject incompatible transitions. |
| P02-02 | Complete account lifecycle through supported protocol/API paths. | Create/disable/delete/restore and membership changes preserve identity, rights and audit across supported clients. |
| P02-03 | Complete Kerberos AS/TGS, SPNs and service authentication. | Real flows enforce declared encryption/time policy and reject replay, expiry, wrong keys and downgrade. |
| P02-04 | Complete LDAP controls, paging and referrals. | RSAT/LDAP clients agree with reference continuation/referral/control semantics; unsupported controls fail explicitly. |
| P02-05 | Complete authenticated secure DNS updates. | Signed authorized updates work; unsigned/replayed/wrong-owner changes and stale-record substitution fail. |
| P02-06 | Complete protected Netlogon membership and secure-channel paths. | Join/rejoin, machine-secret rollover and reset verify signing/sealing, identity and least privilege. |
| P02-07 | Complete GPO objects, linking, inheritance and filtering. | Actual Windows resultant policy/script selection matches reference behavior and denies unauthorized edits. |
| P02-08 | Implement qualified functional levels and schema transitions. | Unsupported levels and interrupted incompatible changes cannot leave false capability advertisements. |
| P02-09 | Complete forest/domain trusts and cross-domain authorization. | Two reference forests verify creation/removal, SID filtering, selective authentication and denied access. |
| P02-10 | Publish an operation-level compatibility report without unsupported universal-OS claims. | Every AD contract row has real-client evidence with exact builds/spec revisions and no unexplained failure, skip or unrun acceptance case. |
| P02-11 | Complete schema/class/attribute matching semantics. | Reference import/export and mutations compare encodings, matching rules and invalid-class/value rejection. |
| P02-12 | Complete stable identity and object security-descriptor semantics. | Reference ACL/object tests preserve GUID/SID through rename/restore and verify inherited/object-specific allowed and denied access. |
| P02-13 | Complete password history, expiry, lockout and fine-grained policy. | User/admin changes enforce effective policy; weak passwords and inconsistent protocol enforcement are rejected. |
| P02-14 | Complete delegated password recovery authorization. | Authorized recovery works; impersonation, enumeration and unauthorized reset/group escalation fail with redacted audit. |
| P02-15 | Complete PAC construction and validation. | Real service/reference cases verify signatures and required authorization data; forged/malformed/mismatched PACs fail. |
| P02-16 | Complete supported constrained-delegation behavior. | Permitted delegation succeeds; unintended audiences, unapproved targets and escalation variants fail on actual services. |
| P02-17 | Complete global catalog and partial attribute sets. | Cross-domain searches return authorized partial attributes with correct naming-context and freshness behavior. |
| P02-18 | Complete attribute-level LDAP authorization and error filtering. | Protected attributes/existence do not leak through results, errors, paging or referrals. |
| P02-19 | Complete site/subnet placement, DC locator and discovery failover. | Real clients select eligible sites/DCs and recover from stale DNS, wrong-site answers and server loss within declared bounds. |
| P02-20 | Complete SAMR/LSA and required administrative RPC operations. | Supported RSAT/service-account calls agree with reference; unauthorized enumeration, escalation and unsupported opnums fail. |
| P02-21 | Complete required SMB transport and share protection. | Supported negotiation/signing/sealing and share access pass; downgrade, wrong recipient and unauthorized reads/writes fail. |
| P02-22 | Complete SYSVOL ACL/version consistency and qualified delivery. | Directory/filesystem permissions and versions reconcile after failure; actual policy files arrive through declared delivery/replication. |
| P02-23 | Implement FSMO/RID ownership, transfer and seizure. | Handoff, failed-holder recovery and RID range tests prevent duplicate authority/allocation and preserve recoverable state. |
| P02-24 | Complete migration and coexistence with rehearsed recovery. | Identity/permission/key mappings preserve cutover behavior; interrupted migration recovers without duplicate principals or credential exposure. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P02-01`: separately verify `P02-11`, `P02-12`.
- `P02-02`: separately verify `P02-13`, `P02-14`.
- `P02-03`: separately verify `P02-15`, `P02-16`.
- `P02-04`: separately verify `P02-17`, `P02-18`.
- `P02-05`: separately verify `P02-19`.
- `P02-06`: separately verify `P02-20`, `P02-21`.
- `P02-07`: separately verify `P02-22`.
- `P02-08`: separately verify `P02-23`.
- `P02-09`: separately verify `P02-24`.

## Evidence and exit

For every P02 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 01 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: AD-01, AD-02, AD-03, AD-04, AD-05, AD-06, AD-07, AD-08, AD-09, AD-10, IAM-01, SEC-01, SEC-02, SEC-03, SEC-06, SEC-07, SEC-08

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
