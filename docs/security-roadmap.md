# Extended security roadmap

This is a proposed backlog for a Linux-hosted, fully capable AD-like server,
not a list of implemented protections. Core identity/password management,
Windows domain membership, GPO/SYSVOL, trusts, replication and recovery remain
in the first production contract. [SEC-01–SEC-11](requirements.md), Linux host
hardening and the [threat model](threat-model.md) are first-release gates;
placing enhancements here does not postpone those requirements.

This catalog broadens coverage across identity, endpoints, administration,
protocols, operations and software delivery. It is not an exhaustive guarantee
against future threats. Review it against backend capabilities, user needs,
incident lessons and current standards at every release-planning cycle.

## Sequencing and ownership

| Wave | Focus | Dependencies and exit evidence |
| --- | --- | --- |
| 7 — Strong identity and privileged operations | Passwordless administration, safe recovery, privileged access workflows, managed credentials and policy governance | Baseline MFA/RBAC/audit and full AD interoperability already working; credential lifecycle, abuse and negative-authorization suites pass |
| 8 — Posture and detection | Access reviews, entitlement graph, device posture integrations, certificate services, federation and detection engineering | Authoritative identity/device data, audited APIs and a licensed client matrix; real-client compatibility, detection quality and privacy reports |
| 9 — Containment and resilience | Isolated branch identities, stronger key custody, incident automation and recovery under compromise | Qualified backend/key provider and reliable backup/replication; partition, compromise simulation and recovery drills pass |
| 10 — Continuous assurance | Supply-chain maturity, extended verification, secure administration baselines and independent assessments | Maintained threat model, reproducible lab and release evidence; ongoing regression reports and vulnerability response exercises |

Wave numbers align with the [main roadmap](roadmap.md); independent items may
advance earlier. Reassess priorities after Phase 0. Any capability selected for
the first production compatibility profile becomes a Phase 5 gate, regardless
of its default wave here. Optional modules must remain disabled until configured
and qualified; installing a feature must not weaken domain security by default.

For each selected item, create a tracked issue with a named owner, threat and
asset, backend/version prerequisites, supported clients, secure defaults,
privacy impact, abuse tests, measured operating cost, migration/rollback limits,
and operator documentation. Proposed ownership: identity/protocol maintainers
for A/C/E; security and UX maintainers for B/D; platform maintainers for F/I;
detection maintainers for G; security architects for H/J; release maintainers
for K; security and UX maintainers jointly for L. These are responsibilities to
staff, not claims that such teams already exist.

## A. Authentication and password protection — wave 7

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| A-01 | WebAuthn/FIDO2 passkeys and hardware security keys for administrator login; multiple authenticators and secure enrollment | Reject origin/RP mismatch and replay; audited enrollment, replacement and revocation; keep usable accessible recovery |
| A-02 | Smart-card/certificate-based domain logon through PKINIT and compatible hardware-backed keys | Real supported Windows/Linux client logon, certificate mapping, revocation, expiry and downgrade tests; a web passkey is not automatically a Kerberos credential |
| A-03 | Recovery hardened against helpdesk impersonation, SIM swapping and MFA fatigue | No security questions or SMS-only privileged recovery; dual review for Tier 0, notifications and synthetic social-engineering exercises |
| A-04 | Password protection beyond basic policy: locally checked breached/common passwords, contextual exclusions, password history and supported fine-grained policies | No raw passwords or unsalted password hashes sent externally; test supported protocol reset/change paths and directory ACLs; avoid routine forced expiry absent a requirement or compromise |
| A-05 | Adaptive throttling and credential-stuffing/password-spray detection across replicas | Bound attacker-induced lockout and distributed attempts; test NAT/shared networks, emergency access and behavior during collector/WAN failure |
| A-06 | Authentication strength policies, session inventory and bounded revocation | Distinguish phishing-resistant, certificate and password-only authentication; test web logout, API revocation and ticket lifetimes separately; document where legacy protocols cannot enforce MFA |

## B. Privileged access and authorization — wave 7

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| B-01 | Just-in-time and just-enough privilege with expiring grants | Enforce expiration even when workflow workers fail; test nested membership, tickets with cached privileges, replication delays and denied access after expiry |
| B-02 | Dual approval and separation of duties for Tier 0 membership, trusts, replication rights, backup export and key operations | Approver cannot approve their own change or bypass through API/bulk import; audit request, approval, execution and cancellation |
| B-03 | Privileged access workstations and tiered administration guidance | Publish tested workstation/server management baselines and safe delegation; directory administrators do not use privileged credentials on lower-trust endpoints |
| B-04 | Emergency break-glass access with separate custody and monitored use | Rehearse access without the normal IdP/MFA provider, alert every use, rotate afterward and protect against emergency-account lockout or silent persistence |
| B-05 | Effective-permission explorer and privilege-path analysis | Explain ACL inheritance, nested groups, delegation, SID history and trust boundaries; validate against actual access decisions and redact data from unauthorized viewers |
| B-06 | Periodic access certification, ownership and orphaned-privilege cleanup | Review privileged/service/stale accounts with accountable owners; preview removals and preserve recovery paths; do not automatically delete based on last-login alone |

## C. Managed credentials and identity lifecycle — waves 7–8

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| C-01 | Windows LAPS-compatible local administrator password rotation and retrieval | Qualify the exact client/schema/encryption profile; tightly restrict password reads, audit retrieval, rotate after use and test offline endpoints |
| C-02 | Managed service accounts, including gMSA compatibility where selected | Validate supported KDS/key derivation and authorized password retrieval, rollover and real Windows services; never emulate compatibility by exposing shared plaintext secrets |
| C-03 | Linux service identities, keytab lifecycle and supported workload identity integrations | Scoped principals, minimal keytab readers, short lifetimes where supported, automated rotation and revocation; no long-lived administrator credentials in workloads |
| C-04 | Joiner/mover/leaver workflows, ownership and deprovisioning reconciliation | Preview group/ACL changes, require approval for sensitive roles, disable access through each integrated system and report failures; measure ticket/session revocation limits |
| C-05 | Delegated self-service password change/reset, account recovery and group requests | Validate identity proof, factor replacement and approval boundaries; no account enumeration, unaudited helpdesk impersonation or permanent recovery bypass |
| C-06 | Signed, versioned provisioning integrations such as SCIM and an external secrets manager | Treat external sources as scoped authorities; test replay, duplicate events, malicious attributes, tenant mix-ups and outages; do not store arbitrary application secrets in directory attributes |

## D. GPO and endpoint policy governance — waves 7–8

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| D-01 | GPO version history, diffs, independent approval and staged OU rollout | Test both directory and SYSVOL versions/ACLs, conflict resolution and a rollback that actually restores client behavior; audit all management paths |
| D-02 | Effective policy preview, precedence and resultant-policy troubleshooting | Model security filtering, inheritance, enforced/block settings and WMI filters; compare predictions with real Windows resultant policy and expose unsupported settings |
| D-03 | Tested hardening templates for Windows and Linux | Cover supported firewall, audit, authentication and host protections; Linux policy delivery needs an explicit supported agent/configuration integration rather than assuming Windows GPO applies |
| D-04 | Policy integrity/drift detection, safe script distribution and privileged policy ownership | Detect out-of-band SYSVOL edits and dangerous scripts; verify applicable signatures and permissions without inventing incompatible GPO wire formats |
| D-05 | Device posture and conditional-access integrations | Qualified endpoint attestation, encryption/patch posture and device identity; define freshness, spoof resistance and fail behavior; posture claims alone must not grant Tier 0 access |
| D-06 | Support for endpoint credential protections and application-control baselines | Test compatible Credential Guard, protected-user, LSA protection and application-control profiles; endpoint edition/features determine availability, and enforcement is not performed by the DC alone |

## E. Protocol, trust and certificate defenses — waves 7–9

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| E-01 | Compatibility-aware legacy authentication retirement | Discover NTLM/RC4/unsigned dependencies, offer a migration report and enforce expiring scoped exceptions; first-release secure defaults stay in force |
| E-02 | Kerberos delegation, ticket and principal hardening | Detect unsafe unconstrained/resource-based delegation, SPN conflicts, weak service secrets and excessive ticket lifetimes; test constrained delegation and protected accounts on real clients |
| E-03 | Trust quarantine and cross-forest entitlement inspection | Validate SID filtering, selective authentication, name suffix routing and SID-history migration boundaries; require approval and audit trust changes |
| E-04 | Certificate enrollment and PKI integration, with any AD CS-compatible role separately qualified | Test template/enrollment ACLs, identity mapping, SAN constraints, approval, issuance/revocation and renewal; protect CA keys separately and reject escalation-prone configurations |
| E-05 | Certificate/key inventory, expiry forecasting and automated rotation | Exercise TLS, PKINIT, service and trust material separately; support safe overlap, CRL/OCSP outages and backend-specific lifecycle constraints |
| E-06 | Protocol exposure control and network segmentation templates | Enumerate actual DNS/LDAP/Kerberos/SMB/RPC and replication flows, narrow dynamic RPC ranges where supported, test firewall changes and preserve diagnostic access |

## F. Linux platform and runtime protection — waves 7–9

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| F-01 | Reviewed systemd sandboxing, capability reduction and AppArmor/SELinux profiles | Test per-role requirements, upgrades and restore; document any privileged Samba/backend operations instead of promising all services run unprivileged |
| F-02 | Host security posture: supported Secure Boot, measured boot and disk encryption | Document provisioning and recovery-key custody; boot attestation must be verified externally; disk encryption does not protect a running compromised DC |
| F-03 | Hardware-backed key custody through HSM/TPM or a supported external KMS | Qualify each key type and backend API; do not claim AD password verifiers or every Kerberos key can be moved into an HSM; test latency, outage and recovery |
| F-04 | Resource isolation and DoS controls per service/peer | Exercise expensive LDAP searches, nested groups, parser inputs, connection exhaustion, audit floods and replication queues under limits without starving legitimate login |
| F-05 | Hardened Linux storage, syscall and network profiles for optional container packages | Validate ACL/xattrs, persistent state, time/DNS, service discovery and restore; no unreviewed privileged-container default; VM/bare-metal hosting stays supported |
| F-06 | Linux host baseline drift and agent/update integrity | Detect changed service units, executable/config permissions and obsolete kernels/packages; verify updates and rehearse service continuity during host maintenance |

## G. Detection, auditing and investigation — wave 8

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| G-01 | Structured, correlated audit export to SIEM/syslog with externally protected storage | Version schemas, synchronize time, track gaps, redact credentials and enforce export RBAC; an append-only local file is not tamper-proof against root |
| G-02 | Detection for replication abuse, suspicious DC registration, ACL escalation and privileged group changes | Labeled authorized lab scenarios, expected alerts and false-positive measurements; some credential theft leaves no definitive directory-only signal |
| G-03 | Detection for ticket abuse, password sprays, abnormal service-ticket requests and trust/GPO persistence | Correlate KDC, directory and endpoint signals; do not promise reliable golden/silver-ticket detection solely from server logs |
| G-04 | Deception identities and monitored canary credentials | Isolate synthetic decoys with no real privileges, prohibit use in normal workflows and test safe high-confidence alert handling |
| G-05 | Investigation views: identity timeline, effective permissions and configuration history | Preserve provenance and access controls; reproducible evidence export, chain of custody and bounded retention; do not expose password hashes/tickets in UI |
| G-06 | Detection engineering with replayable synthetic event fixtures | Version rules, test sensitivity/precision, alert latency and collector failure; publish thresholds and capacity overhead at the 10k-identity target |

## H. Containment and incident response — wave 9

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| H-01 | Audited response workflows for account/device disable, trust suspension and service-key rotation | Scope, preview, approval, idempotency and a rescue path; automated detections cannot globally lock out a domain without a separate safety decision |
| H-02 | Domain-compromise recovery plan covering ticket-signing, machine, service, trust and administrator credentials | Sequence backend-specific rotations, including safe double rotation of Kerberos signing keys; prove clean restores and ticket invalidation within documented limits |
| H-03 | Replica quarantine and controlled reintroduction after suspected compromise | Protect evidence, revoke replication trust safely, avoid contaminating clean replicas and test topology/role recovery; partitioning alone does not remove stolen credentials |
| H-04 | Recovery-safe security state restoration | Reconcile revoked identities, changed privileges, deleted objects and key epochs after restoring older backups; prevent silently reactivating known-compromised access |
| H-05 | Tested response playbooks and tabletop exercises | Include lost MFA provider, stolen backup, compromised maintainer, ransomware and malicious insider; track response time, operator mistakes and retained evidence |

## I. Availability, branch exposure and disaster resilience — wave 9

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| I-01 | Read-only/limited-secret branch controller profiles where the backend supports them | Qualify exact RODC/password replication policy semantics, cached-secret restrictions, theft impact and credential reset procedure; never market a writable replica as read-only |
| I-02 | Immutable/offline encrypted backups with split custody and recovery-key escrow | Separate backup administration, restoration quorum where appropriate, retention verification and regular clean-room restores without depending on the failed domain |
| I-03 | Site isolation, failover and revocation-risk visibility | Surface stale replication, stale policy and uncertain revocation; test WAN partitions and clock/DNS faults without claiming global immediate consistency |
| I-04 | Security operation budgets and safe degraded modes | Define authentication, MFA, KMS, CA and audit failure behavior separately; backpressure noisy services, alert on queue loss and never silently bypass admin MFA |
| I-05 | Recovery environment integrity and safe backup validation | Scan and validate restore media, signed tooling and host images; rehearse total loss and schema incompatibility; ordinary VM snapshot rollback is not assumed safe for a DC |

## J. Federation, privacy and policy boundaries — waves 8–9

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| J-01 | OIDC/OAuth2 and SAML federation through separately qualified modules | Validate issuer/audience, redirect URI, nonce/state/PKCE, signing keys, claim minimization, logout and key rollover; modern SSO does not replace AD protocols |
| J-02 | Network access integrations such as RADIUS/EAP-TLS | Qualify identity/certificate mapping, mutual authentication and revocation behavior; avoid insecure password fallback and document external network-device dependencies |
| J-03 | Attribute-level privacy, scoped directory search and data-export controls | Denied attribute/search tests across LDAP and UI/API, purpose-scoped access and export audit; avoid breaking required AD discovery semantics |
| J-04 | Retention, deletion and legal-hold policy for identity and audit data | Reconcile tombstones/backups/security investigations and residency obligations; no claim of GDPR or other regulatory certification from feature availability |
| J-05 | Explicit multi-organization/tenant security boundaries | Prefer independent domains/forests or deployments for hostile tenants; a shared writable DC and UI RBAC do not create hard tenant isolation; independently assess any shared architecture |

## K. Software supply chain and assurance — wave 10

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| K-01 | Reproducible packages/images, signed provenance/SBOM and dependency license/CVE inventory | Independently rebuild, compare artifacts and verify expected signer/workflow identities; document unreproducible parts and dependency exception expiry |
| K-02 | Secure update metadata with rollback/freeze protection and key recovery | Verify signatures, version/expiry and release channel; rehearse signing-key compromise, offline updates and supported emergency rollback without bypassing checks |
| K-03 | Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests | Synthetic isolated workloads for LDAP/RPC/Kerberos/DNS and policy handling; compare observable semantics with a licensed AD lab and retain minimized regression cases |
| K-04 | Property-based checks or formal analysis for bounded high-risk logic | Prioritize authorization, grant expiry, replication conflict handling and key transitions; publish model assumptions rather than claiming a formally secure whole server |
| K-05 | Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program | Public scope/safe-harbor terms, private intake and supported-version response; remediate findings with regression tests and publish appropriate summaries |
| K-06 | Hardened release governance and maintainer continuity | Two-person sensitive release review, scoped OIDC, protected builders/refs, signer rotation and tested maintainer-loss recovery; use no privileged fork runners |

## L. Security ergonomics and safe operation — waves 7–10

| ID | Capability | Acceptance / constraints |
| --- | --- | --- |
| L-01 | Security posture dashboard with actionable, evidence-backed findings | Show observation time, affected identities/hosts, severity rationale and safe remediation; never present missing telemetry as healthy |
| L-02 | Policy simulation and explainable access decisions | Preview bulk ACL/GPO/role changes against representative identities and devices; show stale/unknown data and compare predictions with actual enforcement |
| L-03 | Safe bulk operations with scope preview, dry run, idempotency and compensating actions | Independent approval for mass privileged changes; test partial failure and rollback limits; no plaintext credential exports |
| L-04 | Accessible secure enrollment/recovery and understandable authentication errors | Keyboard/screen-reader tests and usability studies include recovery and approvals; messages help legitimate users without revealing account existence or secrets |
| L-05 | Security exception register and policy-as-code change review | Every exception has owner, justification, scope, expiry and audit; reject stale exceptions, detect out-of-band drift and protect policy signing/approval keys |
| L-06 | Operator training, trustworthy runbooks and versioned security baselines | Rehearse common and emergency tasks with new administrators; publish prerequisite/compatibility warnings and measure unassisted completion and recovery success |

## Evidence required when delivering an item

Each feature needs positive and negative functional tests, denied-operation
coverage, abuse/failure scenarios, observable audit events, compatibility tests,
and an operator recovery procedure. Add these alongside implementation, not as
empty green jobs now. Execute production-like tests on Linux-hosted controllers
with the supported Windows/Linux client matrix where applicable. Maintain
per-feature support and known-limitations records.

Re-run mixed-load and fault tests after adding MFA, HSM/KMS, policy analysis,
SIEM exports or automated remediation: security features consume resources and
can introduce critical-path dependencies. Include CPU/RAM/storage, network and
retained-event volume, authentication latency/error budget and outage behavior
in each feature's capacity impact report. External providers must not undermine
the standalone Linux-hosting contract; declare optional versus required
integrations explicitly and test their failures.

Before release approval, security and product owners must review interacting
controls: emergency access versus lockout, audit retention versus privacy,
legacy compatibility versus signing/encryption, automation versus blast radius,
and availability versus revocation during partitions. No feature may claim to
contain a fully compromised writable DC merely because the administration UI
is hardened.
