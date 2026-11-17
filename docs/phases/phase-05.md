# Phase 05 — First production release and controlled deployment

Status: specified; product acceptance not demonstrated.
Owner roles: release and operations maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires Phase 4 readiness evidence, selected license and recovery qualification. This is the first production AD-like release; limited protocol previews cannot bypass its scope.

## Design and interfaces

Build versioned Linux packages/images once in trusted CI, generate SBOM/provenance and sign through narrowly scoped release identities. Promote exact digests to isolated staging, then perform a planned DC rollout in a protected production environment. Directory/schema/key transitions are separate reviewed migrations, not consequences of an image tag.

## Data and lifecycle

Artifacts carry immutable version, source commit, supported matrix, migration epoch and verification instructions. Link release decisions to evidence and backup/restore readiness. Keep signing trust/recovery outside the domain and retain support/security notices by version.

## Security and failure handling

Require independent release review, restricted refs/runners and verified installer/update paths. Production deploy must pause on health/convergence or authentication regressions. Rollback can be forward-fix or restore when keys/schema/state are irreversible; never blindly downgrade binary state.

## Capacity and operations

Fresh-install/upgrade tests run on the full baseline dataset and multi-site topology. A release must preserve authentication SLOs during serialized rollout and remain recoverable within RPO/RTO. Source-only drafting remains distinct from qualified product distribution.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P05-01 | Release only artifacts built from the reviewed tested commit. | Package digest, SBOM and provenance resolve to the same source/build identity; rebuilding during production promotion is prohibited. |
| P05-02 | Enforce release licensing, dependency notices and support metadata. | Approved license/obligations and supported-version matrix ship with artifacts; missing notices or unclear redistribution rights block publication. |
| P05-03 | Sign and verify artifacts/installer metadata through scoped identities. | Consumer verification rejects modified bytes, wrong signer, expired/untrusted metadata and replayed unsupported releases. |
| P05-04 | Gate publication on the complete readiness/evidence bundle. | Every Phase 0–4 baseline gate has current passing evidence; skipped client/capacity/security acceptance does not count as a pass. |
| P05-05 | Rehearse clean install and supported upgrade/migration paths. | Fresh Linux hosts and prior supported versions preserve identities, permissions, keys and policy state; incompatible downgrade is rejected. |
| P05-06 | Promote exact artifacts through isolated staging with functional checks. | Domain join/login/password/GPO/replication/restore smoke tests pass before production approval, with synthetic credentials and scoped access. |
| P05-07 | Serialize production rollout by fault domain with explicit abort criteria. | Canary/DC rollout preserves remaining authentication/DNS service; induced health/convergence failure pauses expansion and alerts the operator. |
| P05-08 | Provide tested rollback, forward-fix or restore per migration class. | Runbooks identify irreversible transitions and expected RPO/RTO; exercises recover safely without replaying incompatible schema/key state. |
| P05-09 | Require independent sensitive-release approval and audit the decision. | No self-approved high-risk publication or privileged fork runner; platform limitations are disclosed, never treated as enforced protection. |
| P05-10 | Publish operator/security/support guides and known limitations. | A new operator verifies/install/updates/restores using shipped docs; unsupported levels/clients and disclosure contacts are explicit. |

## Evidence and exit

For every P05 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 04 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: PLAT-01, PLAT-02, PLAT-03, AD-01, AD-02, AD-03, AD-04, AD-05, AD-06, AD-07, AD-08, AD-09, AD-10, IAM-01, OPS-01, UX-01, SEC-01, SEC-02, SEC-03, SEC-04, SEC-05, SEC-06, SEC-07, SEC-08, SEC-09, SEC-10, SEC-11

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
