# ADR 0005 — Directory invariants and replication qualification cases

Status: proposed Phase 0 design. PostgreSQL is selected in [ADR 0003](0003-postgresql-directory-state.md);
its synthetic experiment does not implement the directory/replication model below.
The initial functional-level scope is owner-selected, but the required MS-ADTS /
MS-DRSR revision/section mapping remains unqualified. No disk or AD wire format is
frozen by this ADR. Do not implement a new conflict algorithm as a substitute for
qualifying Microsoft's required semantics.

## Identity, schema and authority

The core owns immutable object GUID, immutable applicable SID, parent GUID,
structured RDN, class/schema identity, per-attribute matching rules, descriptor
version, object/security epoch and lifecycle. A DN is a locator, not identity.
Escaping, Unicode, multi-valued RDNs, deleted-object naming and case matching
follow the pinned schema/protocol rules; generic Unicode case folding or SQL
collation is not sufficient. Store original display values separately from
schema-versioned comparison keys. Never reissue a deleted principal's SID/GUID.

Authorization order is a single core boundary:

1. Bound and decode the request; validate channel/authentication/replay policy.
2. Resolve immutable actor, target and naming context under a bounded snapshot.
3. Expand groups with cycle/work limits and interpret descriptors in the required
   Windows access-check order. A blanket "all deny ACEs first" rewrite is not
   equivalent to ordered ACE/object/inheritance semantics.
4. Check operation-specific control access, attribute rights, lifecycle/schema and
   parent rights. Move/rename includes old and new parents; membership and password
   reset are distinct rights. Management and wire paths use the same evaluator.
5. Acquire writer/security-epoch locks, revalidate authority/state and commit state,
   journal, idempotency result and audit intent together. Only durable commit is
   local success. Exported audit delivery can lag; losing the local audit intent
   cannot become silent success.

Principal/policy revocation serializes with local writes. Cross-site freshness is
explicit; an isolated DC may not yet observe remote revocation. Secret attributes
have a separate internal custody interface and cannot leak through ordinary LDAP,
management, diagnostics, backup browsing or PostgreSQL error text.

## Worked local cases

| Case / starting state | Required observable outcome | Qualification still needed |
| --- | --- | --- |
| Rename GUID G/SID S from OU A to B while a group references G | G/S remain unchanged; backlinks resolve the same identity; old/new parent rights checked; old DN no longer resolves after commit | Reference DN/matching and move access checks |
| Two writers create schema-equivalent RDNs under one parent | At most one local live matching key; loser gets declared collision result, with no partial object/journal/audit/receipt | Matching-rule fixtures and concurrent native adapter test |
| Actor authorized, then its delegation revoked before write | Lock/epoch order yields either earlier authorized commit or reauthorization/denial; never stale privilege after the locally serialized revoke | Security-descriptor evaluator and concurrent denial test |
| Groups A→B→A or a very deep nesting chain | Bounded traversal with explicit budget/error; no privilege from incomplete expansion and no unbounded allocation | Reference handling, matching/inheritance, depth/work budgets |
| Lost response after durable create | Retry of the same actor/request/digest resolves recorded result after reauthorization; changed digest is denied | Native idempotency retention and cross-DC retry behavior |
| GPO directory metadata commits but SYSVOL staging fails | Do not claim coherent publication; retain recoverable staged state and reconcile/revert through a defined state machine | Separate GPO/SYSVOL publication/transport ADR and real Windows application |

## Replication metadata and recovery

Origin change metadata and a receiver's local journal position are separate.
Track naming context, originating invocation ID/USN and the protocol-required
attribute/link version, originating time and DSA identity. Up-to-dateness vectors,
per-source high-watermarks and local USNs have distinct meanings. Receiver
application, conflict outcome and acknowledged cursor commit atomically.
PostgreSQL streaming replication, wall-clock last-write-wins and one global SQL
sequence cannot provide these semantics.

| Case | Required invariant / expected observation | Outstanding specification/reference work |
| --- | --- | --- |
| A and B edit different attributes while partitioned | Preserve independently winning attribute values; object-level overwrite cannot discard unrelated changes | Pin MS-ADTS metadata rules and observe both delivery orders |
| A and B edit the same attribute | Follow required version/time/origin tie-breaking and representation rules; reordered/duplicate delivery converges | Exact comparison order, GUID byte ordering and equal-metadata behavior; no invented ordering |
| Concurrent rename/move or same-name create across DCs | Preserve stable identities and use required naming-conflict handling; never merge two principals by DN alone | Conflict names, parent resolution and reference visible errors |
| Group link add/remove concurrent with object deletion | Preserve required linked-value/delete metadata and tombstone retention; no resurrection or privilege from an orphaned backlink | Link-value replication, recycle state and garbage-collection rules |
| Apply received batch then crash before cursor commit | State and cursor are both committed or both rolled back; replay is idempotent | Native batch transaction and process/host fault tests |
| Restore A from an old snapshot after B has advanced | Quarantine A; validate coherent snapshot/keys/schema, establish the qualified new invocation/restore epoch and reconcile before serving | VM-generation/restore semantics, retained tombstones and replication reference drills |
| Isolated RID master or a role seizure | Existing authorized RID pools may be consumed only within their valid allocation; never reuse ranges or accept two uncontrolled allocators | Exact pool/role ownership and emergency seizure/rejoin procedure |
| Tombstone lifetime exceeded or untrusted replica reappears | Refuse unsafe incremental rejoin; rebuild from a clean qualified source instead of silently importing lingering objects | Operational retention limits and full rebuild evidence |

These are required test outcomes and unresolved interpretation points, not passing
replication model tests. Add exact protocol sections/versions and minimized
reference traces to the matrix before implementing each wire operation. Clock
precision and skew are explicit inputs; timestamps alone never grant authority.

## Format and implementation gate

Keep internal records versioned, but do not freeze credential, ACL, RID, replication
or backup formats until their encoding, migration, key custody and failure/recovery
cases have review evidence. The next storage adapter may use synthetic local
objects only until those gates are met. Changes update the compatibility/evidence
binding and invalidate affected observations. No credential writes, production
multi-controller operation or Windows coexistence is accepted by this design.
