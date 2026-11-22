# ADR 0005 — Directory state, authority and replication contract

Status: **full P00-02/P00-03 Phase 0 design specified for owner review**.
PostgreSQL remains the selected engine. The
[synthetic directory core](../validation/p01-02.md) exercises native identity and
schema primitives in memory. ACL, replication and durable storage integration
remain open. Credential, ACL, RID, replication and backup formats remain unfrozen.
[Twenty worked cases](../../lab/state-security-contract.json) bind the design to
[exact source editions and hashes](../../lab/specification-pins.json). The check
validates review coverage and source bindings; it does not execute AD semantics.

## Reference editions and interpretation

The state/replication review uses **MS-ADTS v20260824**, **MS-DRSR v20251121** and
**MS-DTYP v20231212**. The registry retains the exact publisher PDF URLs, byte
counts, SHA-256 and reviewed section headings. Broader document/image/patent use
rights remain separately tracked; a public reference is not blanket clearance.

Important corrections to the earlier draft:

- A SID is stable within its applicable domain lifecycle, but **cross-domain moves
  are an explicit exception**. GUID identity and SID/SID-history transitions must
  follow the specified move protocol; never let callers assign arbitrary SIDs.
- Attribute and link-value comparison are different algorithms. Attribute versions
  include wrap/half-range rules; linked values also distinguish their lifetimes.
- GUID comparisons use little-endian octets. Native SQL UUID or text ordering is
  not an assumed equivalent.
- Cross-object naming conflict resolution uses the **name timestamp and object
  GUID** rule, not a generic attribute-version/origin-invocation comparison.
- Inheritance propagation is a background task. A parent-ACL commit is not an
  acknowledgment that every descendant descriptor has already changed.
- A cyclic group graph is not universally an invalid AD graph. Termination,
  group-scope constraints and authorization completeness are separate concerns.

These are normative design/reference decisions, not passing Windows observations.
The operation-specific client/build/wire matrix and actual native implementation
retain their later qualification gates.

## Stable identity, schema and lifecycle

The core owns object GUID, current domain-scoped SID where applicable, parent
identity, structured RDN, schema/class identity, per-attribute matching metadata,
security descriptor and object/security/lifecycle versions. A DN is a locator,
not identity. Preserve original display values separately from comparison keys.
Never reissue a deleted principal's identity to another principal. Cross-domain
SID allocation/history is an authorized migration, not arbitrary SID mutation.

MS-ADTS 3.1.1.1.3 specifies GUID/SID behavior; 3.1.1.1.6 covers object references
and referential integrity; 3.1.1.2 and 3.1.1.5.1.1–3 govern schema, naming and
uniqueness. Schema version and attribute rules determine encodings, equality,
case/Unicode behavior and links. Generic Unicode casefolding or SQL collation is
insufficient. Escaping/multi-valued RDNs, classes, system-only fields, required
attributes, deletion/recycle and originating versus replicated constraints are
explicit inputs. The fixed SID/GUID helper in the driver fixture is not this model.

## One authorization and commit boundary

1. Bound/decode the request; verify its declared channel/authentication/replay
   profile. The management API is not a generic SQL writer or secret reader.
2. Resolve the authenticated actor context, stable target and naming context.
   A verified PAC/token context is distinct from live directory group membership.
3. Evaluate ordered descriptors/object-specific rights using the required
   Windows rules. Include operation/attribute/control rights and current resource
   policy. Do not globally reorder all deny ACEs before all allow ACEs.
4. For an intradomain move, check write-property on the name, create-child on the
   destination and delete on the object **or** delete-child on the source parent,
   with the additional NC/class/private-object restrictions in MS-ADTS
   3.1.1.5.4.1.1. Do not reduce this to one target-object permission.
5. Acquire bounded writer/security-version authority and revalidate mutable
   resource/schema/lifecycle constraints. Commit state, journal, audit intent and
   actor/request/payload receipt together. Only confirmed durability acknowledges
   that local transition. Replays reauthorize before returning a receipt.

An originating user request cannot supply an unauthenticated "replication" flag.
Replicated updates use a separate verified-peer/NC/secret-scope authority; the
absence of originating-user ACL checks in the replication algorithm is not an
exception for untrusted traffic. Authenticate and constrain the peer first.

MS-ADTS 3.1.1.4.3 requires inaccessible attributes to act **absent** in both return
values and filter evaluation. Respect descriptor owner/privilege/object rules and
NULL versus empty DACL distinctions (MS-DTYP 2.5.3.2). An object-level allow does
not expose every attribute or authorize password reset/group membership changes.

## Worked local review cases

| Case | Required observable result / refusal | Primary source |
| --- | --- | --- |
| `S-RENAME` | Same-domain move preserves GUID/current SID and stable link targets; denied moves have no partial effects | ADTS 3.1.1.1.3, 3.1.1.1.6, 3.1.1.5.4.1.1 |
| `S-CROSS-DOMAIN-SID` | Domain move has explicit destination SID/history/authority rules; it is not an ordinary rename | ADTS 3.1.1.1.3, 3.1.1.5.4.2; DTYP 2.4.2 |
| `S-COLLISION` | At most one local live schema-equivalent name commits; originating collision differs from replicated name repair | ADTS 3.1.1.5.1.2–3 |
| `S-SCHEMA` | Validate class/syntax/matching/system-field rules under one schema version; never guess an unqualified matcher | ADTS 3.1.1.2, 3.1.1.5.1.1, 3.1.1.5.3.2 |
| `S-ACL-ORDER` | An applicable explicit allow can satisfy a bit before a later inherited deny; hidden values act absent | DTYP 2.5.3.2; ADTS 5.1.3.3, 3.1.1.4.3, 6.1.3 |
| `S-INHERITANCE` | Recompute qualifying descendants eventually; protected DACL and AdminSDHolder rules remain distinct | ADTS 3.1.1.6.3, 3.1.1.6.1, 6.1.3; DTYP 2.5.3.4.1 |
| `S-NESTED-GROUPS` | Visited sets terminate cycles; apply group scope/GC/token rules and fail explicitly on incomplete authorization work | ADTS 3.1.1.3.4.4.3, 3.1.1.4.5.19; DRSR 4.1.8.3 |
| `S-REVOKE-RACE` | A write precedes the locally serialized target-ACL revoke or observes it; do not silently rewrite an issued PAC | ADTS 3.1.1.5.1.4, 5.1.3.3; DTYP 2.5.3.2 |
| `S-DURABLE-ACK` | State/journal/audit/receipt commit together; unknown commit is not success and retry cannot duplicate effects | ADTS 3.1.1.5.1.4, 3.1.1.1.16; Babel's accepted driver foundation |

For inheritance, MS-ADTS 3.1.1.6.3 expressly allows multiple transactions and a
period with old descendant ACEs. Propagator changes do not create replication
stamps. Show pending propagation instead of promising instant descendant-wide
revocation. Current target-descriptor checks, inherited-parent propagation,
issued ticket group SIDs and cross-site replication freshness are distinct clocks.
A stronger emergency-deny overlay would be a separately declared security policy.

Search requests/pages have separate transactions. The specification also has
post-response processing such as delayed links. Babel must durably record and
expose pending multi-resource/background work; a local SQL commit cannot falsely
claim coherent GPO/SYSVOL publication or completed domain-wide processing.

## Attribute, link and naming conflict rules

Keep originating invocation ID/USN separate from receiver-local USNs and cursors.
A receive operation preserves originating stamps; a local SQL sequence is not AD
replication metadata. Values absent from LDAP can still retain a stamp so a later
originating update increments the history rather than resetting it.

For scalar attributes, MS-DRSR 5.11/4.1.10.3.5 compares `CompareVersions`, then
`timeChanged`, then originating invocation GUID. `usnOriginating` is not an extra
conflict tie-breaker. Follow DWORD wrap/half-range behavior, not unsigned sorting
or one guessed signed subtraction. A version 9/time 90 change defeats version
8/time 100. In the specified wrap transition, 0 is newer than FFFFFFFF; the explicit
half-range case ranks 80000001 above 00000001. Keep compiler overflow checks on and
use modular arithmetic only where the qualified protocol explicitly requires it.

MS-DRSR 5.87 orders GUID **little-endian octets**. For example,
`00000001-0000-0000-0000-000000000000` compares greater than
`00000100-0000-0000-0000-000000000000`: first octets 01 and 00. Text/SQL ordering
would be an unjustified substitution.

For links, follow MS-DRSR 5.118/5.119 and 4.1.10.6.14: zero/nonzero-version handling,
lifetime `timeCreated`, signed 32-bit version difference, change time and origin.
Delete/recreate while a tombstone remains preserves the creation time and advances
version; a genuinely new post-GC lifetime differs. Wire presence carries deletion
state; do not invent a transmitted `timeDeleted` field where the format uses a flag.

For **different objects** wanting one name, MS-DRSR 4.1.10.6.12 compares name time
and **object GUID**, independently of the generic attribute comparator. Preserve
both identities. The losing RDN contains U+000A followed by `CNF:` and its dashed
GUID (4.1.10.6.13); the example documentation's display `#` is not the literal
separator. Normal DN serialization must escape the actual character correctly.

## Worked replication and restore review cases

| Case | Required outcome / boundary |
| --- | --- |
| `R-INDEPENDENT` | Partitioned changes to distinct attributes both survive either delivery order and duplicates |
| `R-SCALAR` | Per-attribute comparison uses the qualified version/time/origin rule; clock alone grants no authority |
| `R-GUID-ORDER` | The explicit little-endian example defeats text/SQL GUID ordering |
| `R-VERSION-WRAP` | Wrap/half-range cases use the specified attribute procedure, preserving overflow safeguards elsewhere |
| `R-LINK-LIFETIME` | Linked deletion/recreation uses its own lifetime/presence metadata, not a scalar comparator |
| `R-NAME-CONFLICT` | Name conflict preserves distinct objects and uses the timestamp/object-GUID rule and actual conflict separator |
| `R-DELETE-MODIFY` | UpdateObject/RemoveObj/RecycleObj retain required lifecycle invariants; delayed attributes/links do not grant resurrection |
| `R-CURSOR-COMMIT` | A committed bounded page and safe replay/progress checkpoint agree; UTD/PAS merges only after applied response/cycle completion |
| `R-RESTORE-EPOCH` | Isolate a coherent restored copy, establish the qualified invocation/USN epoch and reconcile before service |
| `R-RETENTION` | Missing deletion history prevents unsafe incremental rejoin; quarantine/rebuild through a qualified source |
| `R-RID-AUTHORITY` | No duplicate SID ranges or stale restored allocator may resume without qualified pool/role recovery |

Every case has exact section/headings in the machine-readable contract. Receive
processing follows MS-DRSR 4.1.10.6.1/10/14/15/16: object/link application and safe
progress first; broader UTD knowledge only after the completed cycle. Denied or
partial processing must not advertise unseen work as received. Replays cannot
skip changes or duplicate effects.

MS-ADTS 3.1.1.1.9 makes invocation ID an epoch for USNs and changes it after
restore; the host trigger is outside that abstract model. Do not invent an AD wire
`restoreEpoch` field. Version local recovery bookkeeping separately, quarantine a
stale snapshot and verify directory/SYSVOL/keys/schema/replica/RID state before
service. Actual host/VM-generation detection, clean-room restoration, retention
limits and role transfer/seizure remain native Phase 3 qualification work.

## Implementation and format gate

The design is reviewable now; its runtime cases remain **unrun**. Before admitting
valuable credentials or freezing durable formats, qualify their actual encodings,
access/token behavior, matching, key custody, migration and failure paths. The
accepted P00-15 driver proves only its selected transactional foundation. Required
CI rejects missing design cases/owners/source bindings or false runtime/independent
assessment claims. It does not execute a replacement AD conflict/access algorithm.

Review packets: [P00-02](../validation/p00-02.md), [P00-03](../validation/p00-03.md).
