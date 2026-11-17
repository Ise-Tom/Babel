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
| P02-01 | Complete domain/forest lifecycle, naming contexts and schema/object semantics. | Synthetic import/export and reference queries compare IDs, object attributes, ACLs and schema; incompatible operations have explicit failures. |
| P02-02 | Complete account and password lifecycle, fine-grained policy and delegated recovery. | User/admin changes, history/lockout/expiry, disable/delete/restore and denied actions pass through every supported protocol/API path. |
| P02-03 | Complete Kerberos/PAC, SPN and delegation behavior for the supported matrix. | Real client/service AS/TGS and delegation cases pass; replay, wrong key, invalid PAC, expired tickets and weak-encryption downgrade are rejected. |
| P02-04 | Complete LDAP controls, GC, paging/referrals and attribute-level authorization. | RSAT and LDAP clients agree with the reference for selected controls; unauthorized attributes never appear in search or error output. |
| P02-05 | Complete secure DNS updates, DC locator and site/subnet discovery. | Signed updates, stale records, wrong-site discovery and DNS failure tests produce the declared outcomes on supported clients. |
| P02-06 | Complete SMB/RPC/Netlogon, SAMR and LSA membership/administration paths. | Client join/rejoin, secure-channel reset and service-account operations pass; signing/sealing and least-privilege rejection are verified. |
| P02-07 | Complete GPO/SYSVOL creation, inheritance/filtering and supported delivery/replication semantics. | Actual resultant policy and scripts match the reference; filesystem and directory permissions/versions remain reconciled after failures. |
| P02-08 | Implement qualified domain/forest functional levels and FSMO transfer/seizure semantics. | Unsupported levels are rejected; role handoff, failed holder and schema upgrade tests preserve a recoverable authoritative state. |
| P02-09 | Complete trusts and migration/coexistence with SID filtering and selective authentication. | Two reference forests exercise permitted/denied cross-domain access, trust removal and a rehearsed migration/recovery path. |
| P02-10 | Publish an operation-level compatibility report without unsupported universal-OS claims. | Every AD contract row has real-client evidence with exact builds/spec revisions and no unexplained failure, skip or unrun acceptance case. |

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
