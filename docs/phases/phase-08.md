# Phase 08 — Posture, certificate/federation services and detection

Status: specified; product acceptance not demonstrated.
Owner roles: integration/detection/privacy maintainers; named accountable owners must be assigned before execution.

## Scope and entry

Requires stable identities, scoped connectors and externally protected audit. Qualify optional CA/federation/posture modules separately; do not conflate modern SSO with AD protocol completion.

## Design and interfaces

Authenticated connectors ingest bounded, provenance-tagged posture/identity claims. Separate issuers handle OIDC/SAML, RADIUS/PKINIT and certificate enrollment with audience/template policy. Detection consumes correlated directory/endpoint signals and emits alerts/cases; it does not directly become an unlimited execution authority.

## Data and lifecycle

Version claim mappings, certificate templates, enrollment approvals, trust roots, rule definitions and observation timestamps. Inventory issuer/key/certificate ownership and expiry. Minimize released attributes and retain detection events with explicit access/retention boundaries.

## Security and failure handling

Treat malicious external claims, weak certificate mappings, template abuse and stale posture as untrusted. Validate nonce/audience/signatures/revocation as applicable. Certificate/federation availability is not permission to bypass authentication. Detection must show gaps and uncertainty rather than claiming proof of endpoint integrity.

## Capacity and operations

Run connector/issuer/rule workloads with the baseline directory load and measure query/audit/storage cost. Establish observation freshness, alert delay and false-positive/negative targets per connector/rule before enforcement. Provider outages and event loss must remain visible.

## Requirements and acceptance

All rows are normative design requirements, not passing test results. Thresholds
marked provisional require a reviewed ADR before their feature's production release.

| ID | Requirement | Verification / acceptance evidence |
| --- | --- | --- |
| P08-01 | Qualify certificate/smart-card authentication and mapping. | Supported clients validate mapping/rotation and reject expired/revoked credentials, weak mappings and unintended identities. |
| P08-02 | Provide scoped federation authentication connectors. | Issuer/audience, nonce/state/PKCE and organization-confusion cases preserve intended identity/audience. |
| P08-03 | Integrate device-posture observations with explicit freshness. | Spoofed/stale/missing inputs show known/unknown state; raw posture cannot grant Tier 0 membership. |
| P08-04 | Maintain certificate/key/trust inventory and renewal visibility. | Expiry forecasting and safe overlap report exact owned keys/providers and accurate next actions. |
| P08-05 | Implement structured protected audit export. | Versioned schema, redaction and reader authorization pass; collector loss and local root-trust limits remain explicit. |
| P08-06 | Develop labeled directory/credential/trust/GPO detection scenarios. | Versioned fixtures measure expected alerts and false positives; missing endpoint signals/forged ticket limits are disclosed. |
| P08-07 | Provide safe canary identities and replayable detection-rule tests. | Decoys have no real privilege, trigger approved handling and cannot be accidentally promoted into normal production accounts. |
| P08-08 | Provide purpose-scoped private search/export. | LDAP/UI/API attribute denials and scoped export prevent unauthorized collection while retaining required discovery. |
| P08-09 | Define organization isolation and external integration boundaries. | Independent deployment/forest boundaries are documented; shared writable DCs are never sold as hostile-tenant isolation based only on UI roles. |
| P08-10 | Qualify module resource cost and observability. | Mixed-load/provider measurements expose overhead and prevent module outages from stopping core authentication. |
| P08-11 | Qualify enrollment templates and issuance authorization. | Real providers/clients reject template/SAN escalation and unauthorized key/subject changes in enrollment and renewal. |
| P08-12 | Provide scoped provisioning and idempotent lifecycle mapping. | Malicious attributes, duplicate/reordered events and unavailable providers cannot grant privilege or corrupt identity lifecycle. |
| P08-13 | Qualify network-access decisions and provider-loss behavior. | Allowed/denied access follows scoped fresh inputs and tested failure policy without silently admitting devices on dependency failure. |
| P08-14 | Handle CA/CRL/OCSP outage and expiry conservatively. | Revocation-provider loss and stale responses have declared per-operation behavior without disabling trust verification. |
| P08-15 | Build investigation timelines with provenance and gap detection. | Clock/reorder/duplicate/source gaps remain visible; absent observations cannot produce an apparently complete timeline. |
| P08-16 | Enforce retention, deletion/hold and residency policy. | Expiry, holds, deletion and region boundaries preserve authorized evidence without indefinite unnecessary identity-data storage. |
| P08-17 | Provide accessible posture and detection-quality reporting. | Reports expose freshness, unknown/unsupported state and rule quality through accessible operator workflows rather than healthy-by-default gaps. |

## Requirement refinement

Composite requirements were split by independent acceptance evidence. Original IDs
retain the primary responsibility named in their row; additional IDs carry the
other obligations from the earlier combined row. Scope is preserved and previously
accepted IDs/scopes are unchanged. Refinement does not start or accept work.

- `P08-01`: separately verify `P08-11`.
- `P08-02`: separately verify `P08-12`.
- `P08-03`: separately verify `P08-13`.
- `P08-04`: separately verify `P08-14`.
- `P08-05`: separately verify `P08-15`.
- `P08-08`: separately verify `P08-16`.
- `P08-10`: separately verify `P08-17`.

## Evidence and exit

For every P08 requirement retain commit/build/platform identifiers, scenario,
expected/actual result, duration, artifacts, owner and review disposition. Record
passed, failed, skipped, unsupported and unrun separately. Unit, negative/security,
integration and fault cases are mandatory where the row specifies them; no empty
or simulated-only run proves real-client behavior. Product evidence jobs are
added alongside implementation in the [validation plan](../validation-plan.md).
A release gate cannot pass with unexplained failed/skipped/unrun acceptance.
Only Phase 00 design evidence can be accepted without product executable tests.

## Dependencies and traceability

Phase 07 supplies the preceding delivery gate; only independent design/lab work may overlap. All relevant first-production baseline requirements continue to apply.

Traceability: A-02, C-06, D-05, D-06, E-04, E-05, G-01, G-02, G-03, G-04, G-05, G-06, J-01, J-02, J-03, J-04, J-05, L-01

Associations above link to the [global requirements](../requirements.md),
[security catalog](../security-roadmap.md), [patch contract](../patch-management-roadmap.md)
and [endpoint contract](../endpoint-operations-roadmap.md). Association means scope
coverage, not that any implementation has passed. The [index](README.md) defines
baseline precedence, phase sequencing and how changes are reviewed.
