# ADR 0003 — PostgreSQL as the first directory backend

Status: **backend family accepted by the project owner on 17 November 2026**.
The model and qualification plan below are proposed implementation contracts,
not accepted durability, authorization or AD replication evidence. No database,
credential write or multi-controller implementation is introduced by this ADR.

## Decision and alternatives

Use PostgreSQL behind a narrow Rust storage interface for the first durable
Babel directory. The owner explicitly selected this option in this conversation.
The backend provides mature local transactions, constraints, crash recovery and
backup tools. Babel owns directory identity, schema, authorization, logical change
metadata and AD wire behavior; database tables are not the public management API.

An embedded store reduces service footprint but makes indexing, backup, concurrent
access and recovery more application work. Building a new engine adds unnecessary
correctness/security work. Neither alternative is selected. PostgreSQL adds a
service, upgrade and resource budget; it must be included in Linux packaging and
failure tests. Engine-specific SQL belongs in the adapter so a future engine change
can use a versioned export/import path. That boundary reduces coupling; migration
would still require data, recovery and conformance qualification.

Each writable Babel DC owns independent local state and a PostgreSQL instance.
Three sites must not depend on one central database. PostgreSQL streaming/logical
replication is not Babel’s AD replication and does not qualify Windows DC
coexistence, FSMO/RID behavior or multi-master semantics. Optional database HA
must preserve the same logical DC identity and recovery rules; it does not create
an additional independently writable domain controller.

## Core ownership and transaction interface

Protocol and management requests authenticate and authorize through the same
core. An untrusted request cannot construct an authorized mutation or select raw
SQL. The adapter is not reachable directly by endpoint agents or the web UI.
Initial deployment uses a dedicated service identity and local Unix socket;
remote database exposure is outside this initial selection.

The proposed adapter operations are bounded snapshot reads, a local mutation
transaction, paginated change-journal reads, checkpoint inspection and controlled
snapshot export. Inputs/outputs carry typed IDs, expected object/security epochs,
operation identity, limits and a schema version. SQL queries are parameterized;
resource budgets, deadlines and cancellation are mandatory. Database errors map
to bounded public failures without SQL, DN/password material or key dumps.

Authorization reads and mutation writes share the transaction and relevant locks.
Lock the principal/policy epoch records before relying on them; local revocation
must serialize with the affected mutation. A stale request is reauthorized rather
than trusting a client-supplied privilege flag. This does not promise immediate
cross-site revocation during a network partition.

## Logical state before SQL schema freeze

| Record | Required invariant |
| --- | --- |
| Object | Immutable GUID; applicable SID immutable across rename; parent GUID and structured RDN; display name separate from qualified matching keys; class/schema version; lifecycle state; object/security epoch |
| Attribute | Schema ID, ordered/unordered value semantics, matching-rule version and per-attribute change metadata; credential material excluded from normal attributes/exports |
| Membership link | Stable source/target IDs, link identity and change/deletion metadata; reverse links derived consistently instead of independently editable copies |
| Security descriptor | Versioned owner/group/DACL/SACL representation with inheritance semantics owned by Babel; PostgreSQL role checks do not replace directory ACL checks |
| Local journal | Local USN, invocation identity, mutation ID, affected IDs and logical changes; state, journal and protected audit intent commit together |
| Replica progress | Naming context, source invocation/epoch and qualified cursors; incoming change application and progress commit together |
| RID allocation | Domain SID and owned RID ranges; transactional consumed/reserved state; no reissue on restart/restore and no invention of allocations when the authority is unavailable |
| Idempotency | Actor plus request identity, mutation digest and durable result, coupled to the mutation; reuse for a different operation fails; retention outlasts the declared retry window |

PostgreSQL UUID/collation/sequence behavior does not define AD wire semantics.
GUID binary/display conversion, SID encoding and every DN/schema matching key
need explicit fixtures; locale-sensitive SQL `lower()` is not AD name matching.
The schema must preserve forward/back link, tombstone/recycle and identity
semantics instead of relying on broad `ON DELETE CASCADE` behavior.

## Commit and journal ordering

A successful local mutation is acknowledged only after PostgreSQL reports a
synchronous durable commit with `fsync`, `full_page_writes` and
`synchronous_commit` enabled. Startup must reject unsafe effective settings.
Host/storage flush behavior still requires fault qualification; a database
setting alone does not prove hardware durability.

For the first prototype, serialize local writers through a transactional per-DC
allocator row acquired before other mutation locks. Allocate local USNs and
update state/journal/idempotency/audit intent in that same transaction, holding
the allocator lock until commit. This deliberate bottleneck makes ordering
reviewable; benchmark it against the existing workload/SLOs before optimizing.
Readers use bounded snapshots and must not bypass ACL or freshness semantics.

Do not use an ordinary PostgreSQL sequence as a committed replication watermark:
transaction A can obtain 100 and stall while B obtains/commits 101. Advancing a
consumer to 101 would then miss A when 100 commits later. With the proposed
transactional writer lock, B cannot commit a later local journal position before
A completes. Rollback exposes neither partial state nor a committed journal entry.
Origin metadata remains distinct from local USNs; a database sequence is not an
AD update vector or conflict resolver.

A commit response lost after durable commit is **unknown to the client**, not a
proven rollback. Retrying the same actor/request/mutation digest returns the
stored result after reauthorization. A new request identity can represent a new
operation; cross-DC idempotency/failover semantics need D-05 qualification.

## Failure and recovery qualification

| Experiment | Required result before the implementation is accepted |
| --- | --- |
| Kill before transaction commit | No visible object, journal, idempotency result or success acknowledgement |
| Kill after durable commit before reply | Complete committed state survives; identical authorized retry resolves the outcome without repeating the mutation |
| Concurrent rename/collision or revoked actor | No duplicate matching key; stable GUID/SID; serialized authorization and explicit rejection rather than partial changes |
| Process/host kill at journal checkpoints | Old or new complete state; no acknowledged mutation lost and no missed committed change below a published watermark |
| Disk full, database unavailable, lock/deadline exhaustion | Bounded failure, no success acknowledgement, no fallback in-memory success or disabled durability setting |
| Snapshot/restore, schema upgrade interruption | Version/epoch checks and coherent state/journal recovery; stale replica remains quarantined until the qualified restore procedure succeeds |
| Full synthetic workload | Existing 10k-identity/three-site targets remain intact; record hardware, indexes, cold/warm latency and write-lock contention without claiming an unrun benchmark |

The first storage experiment uses synthetic non-credential objects only. It must
qualify the PostgreSQL major/driver, lock/error mapping, packaging and crash tests
in the same implementation PR. No valuable credentials persist until encryption,
key custody, rotation, backup and recovery rules are selected and tested.

## Remaining decisions and exit

D-04’s engine choice is resolved. Its version/driver, durability measurements,
backup/upgrade and credential key-custody qualification remain open. D-05 still
requires worked AD-compatible conflict, naming-context, RID/FSMO, invocation and
restore-epoch rules against selected MS-ADTS/MS-DRSR profiles and real references.
A local SQL transaction does not resolve that decision.

D-06 still requires a GPO/SYSVOL state machine: staged content and ACL/version
metadata, publication, interrupted transition recovery and qualified inter-DC
transport. Directory and filesystem writes cannot be called one atomic SQL
transaction. Windows clients must never receive an unqualified claim of coherent
policy after a partial publication.

The [synthetic local-state experiment](0004-synthetic-postgresql-state-experiment.md)
now exercises a bounded subset using official psql in an isolated container. It is
not a Rust production adapter and does not close the remaining qualifications.

Further implementation proceeds once its dependency
and schema proposal meet these contracts. Account/password mutations, Windows
join and writable multi-controller operation remain behind their separate gates.
See [decision register](../decisions.md), [Phase 1](../phases/phase-01.md),
[replication qualification](../phases/phase-03.md) and
[validation](../validation-plan.md). No phase requirement is accepted by this ADR.
