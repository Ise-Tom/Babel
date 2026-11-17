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
| P08-01 | Qualify certificate/smart-card authentication and enrollment profiles. | Real supported clients pass valid mapping/rotation and reject invalid templates, SAN escalation, expired/revoked certificates and weak mappings. |
| P08-02 | Provide secure federation/provisioning connectors with scoped authority. | Issuer/audience, nonce/state/PKCE where applicable, malicious attributes, duplicate events and cross-organization mix-ups are tested; unknown claims grant no privilege. |
| P08-03 | Integrate device posture and network-access policies with clear freshness. | Spoofed/stale/missing posture and provider outage behavior match approved policy; no raw posture flag grants Tier 0 membership. |
| P08-04 | Maintain certificate/key/trust inventory and renewal visibility. | Expiry forecasting, safe overlap, CA/CRL/OCSP failure and renewal tests produce accurate status without disabling verification. |
| P08-05 | Implement structured protected audit export and investigation timelines. | Schema/version/provenance, gap detection, redaction and denied-reader tests pass; root-controlled local files are not claimed tamper-proof. |
| P08-06 | Develop labeled directory/credential/trust/GPO detection scenarios. | Versioned fixtures measure expected alerts and false positives; missing endpoint signals/forged ticket limits are disclosed. |
| P08-07 | Provide safe canary identities and replayable detection-rule tests. | Decoys have no real privilege, trigger approved handling and cannot be accidentally promoted into normal production accounts. |
| P08-08 | Provide privacy-scoped search/export and retention controls. | LDAP/UI/API attribute denials, purpose-scoped exports, deletion/hold and residency policy tests pass without breaking required discovery. |
| P08-09 | Define organization isolation and external integration boundaries. | Independent deployment/forest boundaries are documented; shared writable DCs are never sold as hostile-tenant isolation based only on UI roles. |
| P08-10 | Qualify module cost, observability and accessible posture reporting. | Reports show freshness, unsupported/unknown state, rule quality, provider dependencies and mixed-load overhead; a module outage does not stop core domain auth. |

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
