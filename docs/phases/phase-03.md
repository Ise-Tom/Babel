# Phase 03 — Multi-site replication, durability and recovery

Status: specified; product acceptance not demonstrated.
Owner roles: replication/recovery maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires Phase 2 replication/identity/key contracts and a single-node store with proven crash behavior. Qualify six writable Linux DCs across three sites; independent replica state is not a shared database shortcut.

## Design and interfaces

Authenticated replicas exchange naming-context/attribute changes with origin identity, versions, cursors and bounded queues. Conflict decisions and tombstone handling follow the qualified AD contract; local transactions atomically store changes and replication progress. Operator workflows handle FSMO, topology, key rotation, backup epochs and replica replacement.

## Data and lifecycle

Persist per-replica invocation identity, USN/rollback safeguards, durable checkpoints and versioned snapshots. Backups include directory/SYSVOL consistency and required recovery metadata, encrypted under independently recoverable keys. Do not restore a stale VM and assume it is a safe replica.

## Security and failure handling

An unauthorized replica must not obtain credential material. Partitioned replicas cannot promise immediate global revocation. Quarantine inconsistent/restored replicas until validated; detect stale policies and expose unknown state. Exercise disk-full, clock skew, collector failure and key/certificate rotation without dropping verification.

## Capacity and operations

Qualify the baseline 50 ms WAN/1% loss and 150 ms degraded WAN plus a 24-hour partition. Targets: p99 convergence <=5 s in-site/<=60 s healthy inter-site, DC failover <=60 s, whole-domain RPO <=1 h/RTO <=4 h. Measure bounds under simultaneous directory load, not isolated replication.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P03-01 | Authenticate and authorize replication membership and secret access. | Unknown, revoked and insufficiently privileged replicas cannot read credential changes or alter membership; every enrollment is audited. |
| P03-02 | Apply change data and replication cursors atomically and idempotently. | Duplicate/reordered/interrupted exchanges do not lose acknowledged local transactions or skip unapplied remote changes. |
| P03-03 | Resolve concurrent scalar attribute and object naming changes. | Modify/modify and move/rename converge under qualified metadata rules despite reordered delivery. |
| P03-04 | Handle replication topology and naming contexts under loss. | Discovery and replication respect eligible sites/context boundaries during node/site loss and rejoin. |
| P03-05 | Expose replication freshness and revocation uncertainty. | A partition causes visible stale/unknown warnings with measured convergence; UI/API never claims instant global disable during disconnection. |
| P03-06 | Protect against unsupported rollback and stale replica reintroduction. | Restore old snapshots with conflicting invocation/progress metadata; reject/quarantine unsafe joins and follow a tested recovery path. |
| P03-07 | Create coherent encrypted directory/SYSVOL/key-metadata backups. | Manifests bind directory, policy, keys and replica epochs and reject partial/inconsistent snapshots. |
| P03-08 | Meet the online DC/client failover objective. | Fault drills measure DNS/DC failover <=60 seconds; offline cached login is not online service recovery. |
| P03-09 | Rotate TLS certificates and issuer trust safely. | Expiry, issuer loss and interrupted overlap reject unsafe trust without verification bypass. |
| P03-10 | Recover from local storage, process and queue exhaustion. | Disk-full, queue pressure and kills have bounded retries/memory and complete journal/audit outcomes. |
| P03-11 | Resolve linked membership, deletion/recycle and lingering-object conflicts. | Add/remove/delete/modify and tombstone-expiry cases converge without privilege resurrection or orphaned link authority. |
| P03-12 | Recover role/RID authority under transfer and seizure. | No duplicate holder/allocator survives recovery; a stale former owner cannot silently resume authoritative writes. |
| P03-13 | Restore full backups in a clean room with independent custody. | Recovery at target size works without the original domain or a sole directory-held key and verifies identity/ACL/policy/replica state. |
| P03-14 | Meet whole-domain disaster-recovery RPO/RTO. | Full-domain drills at target size prove RPO <=1 hour and RTO <=4 hours; breaches block qualification. |
| P03-15 | Rotate Kerberos, service, machine and trust credentials. | Actual clients verify intended overlap/rotation; compromised old keys do not remain valid indefinitely and recovery is explicit. |
| P03-16 | Recover from prolonged partitions, clock faults and degraded WAN. | A 24-hour partition/rejoin, asymmetric loss and skew retain bounded queues and publish stale-state/convergence/data-loss outcomes. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P03-03`: separately verify `P03-11`.
- `P03-04`: separately verify `P03-12`.
- `P03-07`: separately verify `P03-13`.
- `P03-08`: separately verify `P03-14`.
- `P03-09`: separately verify `P03-15`.
- `P03-10`: separately verify `P03-16`.

## Evidence and exit

For every P03 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 02 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: AD-07, AD-09, AD-10, OPS-01, PLAT-02, PLAT-03, SEC-06, SEC-09, SEC-11

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
