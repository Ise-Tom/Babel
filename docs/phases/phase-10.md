# Phase 10 — Continuous security assurance and trusted delivery

Status: specified; product acceptance not demonstrated.
Owner roles: assurance/release maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires supported releases, current threat model and maintained lab. Assurance features are continuous operating commitments, not a one-time scanner installation.

## Design and interfaces

Trusted ephemeral builders produce reproducible artifacts, SBOM and provenance from reviewed commits. Consumers verify signed update metadata, supported versions and trust identity. Independent tests, long-running fuzzing and focused formal/property models feed the same tracked vulnerability and release gate process.

## Data and lifecycle

Version rule/model assumptions, fuzz corpora, artifact digests, signing metadata, release channel state and evidence. Protect trust-root recovery independently of ordinary CI tokens. Reproducibility differences have owners and are never hidden by changing expected checksums.

## Security and failure handling

Exercise dependency, builder and signer compromise; reject freeze/downgrade and wrong-identity updates. No untrusted fork code runs with signing/cloud/domain authority. Use memory-safe code plus parser/authorization review; language choice alone does not establish correctness or certification.

## Capacity and operations

Define bounded per-PR fuzz smoke plus longer nightly campaigns and retain minimized regression cases. Measure CI durations, flake rates and security-tool freshness; do not silently skip expensive gates or convert tool failures into green status. Rebuild and compare representative packages on independent trusted builders.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P10-01 | Produce independently verifiable reproducible artifacts. | Independent rebuilds compare bytes or explicitly reviewed nondeterminism for identical source/toolchain inputs. |
| P10-02 | Protect update channels from wrong signer, rollback and freeze. | Expired/version-replayed metadata and malicious mirrors fail verification; signing-key compromise and offline update recovery are rehearsed. |
| P10-03 | Maintain bounded multi-protocol fuzz campaigns. | LDAP/RPC/Kerberos/DNS/policy parsers and state machines have maintained sanitizer/property campaigns and resource budgets. |
| P10-04 | Differentially test protocol semantics against a licensed reference. | Versioned selected operations compare real outputs/state effects; divergence is triaged, not accepted solely because a second implementation matches. |
| P10-05 | Apply focused formal/property analysis to high-risk invariants. | Models for authorization, grant expiry, replication conflict and key transitions state assumptions and find/reject known counterexamples. |
| P10-06 | Run recurring independent assessment and remediation retests. | Scoped assessments produce owned findings and independently verified fixes without exposing active secrets. |
| P10-07 | Require independent sensitive update/release decisions. | One compromised signer/reviewer cannot silently publish trusted high-risk updates; exact-scope approval and audit are enforced. |
| P10-08 | Keep accessible posture, policy-as-code and operator education current. | Freshness/uncertainty, safe previews and exception expiry are tested; new operators complete privileged and emergency runbooks without hidden knowledge. |
| P10-09 | Monitor governance and platform enforcement limitations. | Actual required-check/review/ref/environment protections are verified where supported; unavailable private-repo features remain explicit release risks. |
| P10-10 | Publish recurring security assurance evidence without certification overclaims. | Reports include test/model scope, failures, skips, unsupported platforms and residual risks; a green scanner suite is never labeled proof of security. |
| P10-11 | Align SBOM, provenance, artifact identity and distribution obligations. | Inventories/build/source/artifact digests agree and required notices/consumer verification metadata remain complete. |
| P10-12 | Minimize fuzz failures and retain regression corpora. | Qualifying failures yield tracked minimized reproducers and regression tests; suppressions cannot erase unresolved findings. |
| P10-13 | Operate coordinated research intake and safe-harbor disclosure. | Published authorized scope, private intake, disclosure coordination and funded remediation are exercised and maintained. |
| P10-14 | Rehearse maintainer continuity and emergency release recovery. | Loss of a signer/reviewer has a usable independently controlled recovery process without removing consumer trust protections. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P10-01`: separately verify `P10-11`.
- `P10-03`: separately verify `P10-12`.
- `P10-06`: separately verify `P10-13`.
- `P10-07`: separately verify `P10-14`.

## Evidence and exit

For every P10 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 09 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: K-01, K-02, K-03, K-04, K-05, K-06, L-01, L-02, L-03, L-04, L-05, L-06

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
