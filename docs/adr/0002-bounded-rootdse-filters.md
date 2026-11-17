# ADR 0002 — Bounded RootDSE filter evaluation

Status: proposed extension in the development PR; limited to the existing
non-credential-bearing Rust laboratory component. No state/schema/crypto
dependency decision or full Phase 1 acceptance is made here.

## Decision

Extend the public empty-DN base search with presence filters for the four fixed
lab attributes, objectClass equality, and AND/OR/NOT. objectClass equality uses
ASCII descriptor matching or the OID aliases `2.5.4.0` (attribute) and `2.5.6.0`
(top). Other attribute matching rules, substrings, ordering, approximate and
extensible matching remain unsupported and return unwillingToPerform (53),
including when nested under a boolean branch that otherwise determines a result.

Unrecognized attribute descriptions/options and invalid objectClass assertion
syntax evaluate Undefined. Boolean evaluation uses LDAP three-valued semantics;
NOT of Undefined remains Undefined. Only True emits the RootDSE entry. False and
Undefined yield successful SearchResultDone with zero entries, rather than an
unsupported-operation failure or a fabricated match. All branches are visited,
so a short circuit cannot conceal malformed or unsupported input.

Evaluation is against the four immutable synthetic/public attributes during
decoding; no filter AST, assertion value or credential is retained in Request or
Debug output. This is deliberately not a general directory query engine. It
must be revisited before filtering real objects, schema or authorization state.

## Limits and failure behavior

At most 8 levels (root included), 64 total nodes (including boolean operators),
and 256 assertion bytes are accepted. The existing 16-KiB frame, 64 attribute
projection and five-second/32-request session limits remain. The evaluator uses
bounded recursion with an explicit shared node counter and no heap allocation.
Empty AND/OR, wrong NOT arity, malformed BER, invalid names and exhausted budgets
fail decoding with static errors; the transport closes that session. Unsupported
matching bodies are opaque and bounded by the outer frame, never recursively
interpreted. No request value is included in diagnostics.

These are defensive lab limits, not production capacity measurements. No runtime
dependency, persistent state, account write, authentication or Windows-domain
compatibility claim is introduced.

## Validation

Protocol regressions cover match/no-match/undefined, OID/case forms, unsupported
operators under short circuits, structural and exact depth/node/assertion limits,
and assertion redaction. Generated tests cover boolean commutativity/double
negation and descriptor assertions. ldap3 exercises positive, empty-success and
unsupported results over the real loopback process. The existing sanitizer
target reaches the evaluator through decode/respond; a structured boolean seed
is registered with the CI scope policy. Core coverage remains gated at 90%.
