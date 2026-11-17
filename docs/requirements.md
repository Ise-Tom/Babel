# Requirements and acceptance contract

Design baseline: native Babel, 2026-11-17. Owner scope is a **full AD-like
production identity server hosted on Linux**, targeting **10,000 human identities
and 10,000 computer accounts across three sites**. The first LDAP lab subset is documented in [progress](phase-01-progress.md);
no complete production capacity/protocol/security requirement below is claimed
accepted from that partial evidence.

The [18 phase specifications](phases/README.md) define the complete conception,
interfaces/state, security/failure behavior and 180 verifiable phase requirements.
They trace all 130 core/security/patch/endpoint capability IDs. This document is
the first-production baseline; later modules retain their own normative contracts.
No roadmap phase may silently remove a baseline function or replace executable
acceptance with a written promise. See [verification](validation-plan.md) for
per-phase evidence and [decisions](decisions.md) for unresolved owners/experiments.

## Requirement authority and phase allocation

| Contract | Detailed design / qualification | Production meaning |
| --- | --- | --- |
| PLAT, AD, IAM, OPS, UX, SEC | Phases 0–4 design/implement/qualify; Phase 5 promotes the reviewed bundle | Mandatory first-production gate; Phase 6 sustains it |
| Advanced identity, privilege, policy, detection and platform security | Phases 7–10, with earlier baseline overlap | All selected profiles must satisfy their catalog and phase requirements before module release |
| PATCH-01–PATCH-15 | Phases 11–13 | Real verified remediation on supported Windows/Linux endpoints; separate later service |
| REMOTE-01–REMOTE-06 | Phase 14 and joint Phase 17 | Attended/unattended session support with separately authorized channels |
| FILE-01–FILE-05 | Phase 15 and joint Phase 17 | General authenticated server-to-device upload, not implicit execution/retrieval |
| EDR-01–EDR-08 | Phase 16 and joint Phase 17 | Native supported-OS telemetry, measured detection and controlled response |

A capability selected for first-production compatibility cannot be deferred to
an advanced phase. Stable IDs survive this redesign; updated acceptance retains
prior intent. Requirement changes need an impact ADR, updated evidence and owner
review. Design associations do not mark any requirement delivered.

## Native implementation boundary

Babel owns its native AD-compatible directory/domain core; it must not require
Samba AD DC, its database or its administration tools in production. Reuse of
reviewed libraries is permitted. The [native-core plan](native-core-plan.md)
defines model/protocol/conformance milestones; only the bounded read-only
LDAP lab subset is currently implemented, with [progress](phase-01-progress.md)
recording the remaining gates. This direction does not relax any AD, security or capacity gate.

## Linux server hosting

Linux is the required production host platform for every Babel server component:
domain controllers, directory/DNS services, administration API/UI and operations
services. A standalone deployment must work without a Windows Server runtime.
Windows clients, RSAT tools and Windows AD reference domains remain necessary
for interoperability testing and migration/coexistence scenarios.

Proposed initial validation baseline: Ubuntu Server 24.04 LTS on x86-64, on a
VM or physical server, with systemd-managed services. Ratify the exact supported
distribution/kernel/native-core versions in Phase 0 (D-02/D-03). Other Linux distributions,
ARM64 and container deployment require their own qualification; they are not
implied by the Linux hosting requirement. Kubernetes is not a prerequisite.

| ID | Required production behavior | Acceptance evidence |
| --- | --- | --- |
| PLAT-01 | All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency | Clean Linux host provisions a domain; Windows client joins, authenticates and applies GPO; admin API/UI operate with no Windows server present |
| PLAT-02 | Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default | Fresh-host install, reboot and interrupted-upgrade tests; documented service ordering, DNS/time/firewall prerequisites and explicit data-deletion procedure |
| PLAT-03 | Linux host hardening and persistent data integrity | Verified service identities, minimum required privileges, secret/data file permissions, applicable AppArmor/SELinux policy, filesystem ACL/xattr preservation and backup/restore tests |

Document any native-core/OS requirement for root privileges and constrain it; the web
administration process must not gain root merely to manage a privileged backend.
Capacity, replication and recovery benchmarks below must run on the qualified
Linux hosts. Running repository checks on an Ubuntu CI runner alone does not
validate application hosting compatibility. PLAT-01–PLAT-03 are production gates.

## Compatibility and functionality

| ID | Required production behavior | Acceptance evidence |
| --- | --- | --- |
| AD-01 | AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore | Import/export and object/ACL comparison against an isolated Windows AD reference domain; denied-operation cases |
| AD-02 | Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect | Disposable Windows 11 and Windows Server 2022/2025 clients; exact editions/builds pinned in a compatibility matrix |
| AD-03 | Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication | Positive/negative Windows and Linux client tests, ticket expiry/replay and delegation abuse cases |
| AD-04 | LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog | Windows RSAT and standard LDAP clients; paging/filter conformance, unauthorized attributes excluded |
| AD-05 | AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator | Discovery, stale records, DNS failover, and unsigned-update rejection |
| AD-06 | Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions | Real Windows client resultant policy, policy version conflict, script distribution and failover tests; document supported replication mechanism |
| AD-07 | Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery | Partition/rejoin, concurrent writes, lingering objects, rollback protection and disaster recovery |
| AD-08 | Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration | Supported Microsoft protocol test cases plus real-client workflows; signed/sealed secure channels |
| AD-09 | Forest/domain trusts, cross-domain authorization, migration and coexistence with existing AD | Two disposable forests, trust creation/removal, SID filtering, selective authentication and migration rollback |
| AD-10 | Domain/forest functional levels and FSMO role ownership, transfer and failure recovery | Explicit supported level matrix, role transfer/seizure, schema and functional-level upgrade tests |
| IAM-01 | Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit | UI/API and supported client tests for allowed and denied operations, policy enforcement, account enumeration resistance, password redaction and post-reset authentication |
| OPS-01 | Backup/restore, upgrades, rotation, audit export, health and capacity visibility | Repeated restore drills, interrupted upgrade, disk-full and certificate-expiry tests |
| UX-01 | Accessible web administration and documented automation API/CLI | Tested admin journeys, WCAG 2.2 AA audit and API authorization matrix |

“Full replacement” must mean a published compatibility contract, not universal
compatibility with every Microsoft product. Phase 0 must enumerate protocol
versions, functional levels, client editions, management tools, trust types,
and known limitations. An unmet AD-01–AD-10 requirement blocks the first
production release; do not silently relabel it optional. Read-only controllers,
AD CS/PKI, ADFS, Exchange-specific extensions, Entra synchronization, RADIUS,
and OIDC/SAML federation are separate integration decisions: inventory demand
and state explicitly whether they are included before signing off the contract.
IAM-01, OPS-01 and UX-01 are also first-production release requirements.
The first production scope cannot be approved while these decisions are open.

## Security requirements

| ID | Requirement | Verification gate |
| --- | --- | --- |
| SEC-01 | Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account | Threat model, privilege matrix, denied-operation integration tests |
| SEC-02 | Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1 | Protocol downgrade and anonymous access tests with pinned clients |
| SEC-03 | Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited | Kerberos encryption negotiation, NTLM relay/downgrade tests and documented compatibility impact |
| SEC-04 | TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly | Invalid/expired certificate rejection and live rotation tests; no verification bypass |
| SEC-05 | Web/API admin MFA through phishing-resistant authentication, step-up for privileged actions, scoped sessions/tokens, CSRF protection and reauthentication | Browser/API tests for session expiry/revocation, cross-site attacks, role escalation |
| SEC-06 | Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning | Crypto design review, secret/log scan, rotation and backup recovery drills |
| SEC-07 | Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility | Spray, brute-force, denial-of-service and recovery abuse tests |
| SEC-08 | Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion | Parser fuzzing, adversarial query tests and memory/CPU ceilings |
| SEC-09 | Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets | Audit completeness, redaction and external collector outage tests |
| SEC-10 | Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore | Packaging review, dependency/secret scans, artifact verification and restore exercise |
| SEC-11 | Minimize identity data, encrypt backups, document retention/deletion and data residency | Privacy review, retention/restore tests and synthetic-only CI fixtures |

Domain credentials generally do not support universally enforced MFA for every
legacy protocol. Admin UI MFA does not make LDAP/NTLM/Kerberos MFA-safe; specify
smart-card/PKINIT support and protocol-level limitations in the compatibility
matrix. Hardware-backed admin credentials and Kerberos delegation need their own
tests. A compromised writable DC is a domain compromise; web RBAC cannot turn
multiple domains on a shared privileged backend into isolated tenants.

Advanced protections and optional integrations are cataloged in the
[extended security roadmap](security-roadmap.md). They extend this baseline;
any item chosen for the first-production compatibility profile must be gated
before that release, regardless of its proposed later wave.

## Capacity and reliability targets

These are provisional SLOs for the first production release. Benchmark results
must ratify or revise them in an ADR before a release candidate.

| Dimension | Target workload / acceptance threshold |
| --- | --- |
| Dataset | 10,000 enabled user identities, 10,000 computer accounts, 2,000 groups; report total objects, SID history, nesting, policy count and attribute sizes |
| Topology | Three sites, two writable DCs per site across independent failure domains; admin control plane must not be in the authentication critical path |
| Initial sizing hypothesis | Each DC: 4 vCPU, 16 GiB RAM, 100 GiB SSD; six DCs total, separate encrypted backup and audit storage. Measure CPU, working set, IOPS and replication traffic before procurement |
| Network profile | Site LAN RTT <=2 ms; inter-site RTT 50 ms, 1% loss and >=20 Mbit/s available. Benchmark degraded WAN at 150 ms and during a 24-hour partition |
| Auth load | 100 successful Kerberos authentications/s sustained for 60 minutes domain-wide; 500/s for five minutes; include service ticket issuance and failed-login mix |
| Directory load | 500 indexed LDAP reads/s plus 20 writes/s domain-wide; paged searches, nested membership and representative ACL evaluation; cap unindexed searches |
| Latency | LAN p95 <=100 ms, p99 <=300 ms for KDC exchanges and bounded indexed reads; p95 <=500 ms for accepted local writes; report network time separately |
| Error budget | <0.1% unexpected errors under the target mix; count expected access denials separately; no lost acknowledged writes under the documented durability model |
| Replication | p99 convergence <=5 s within a site, <=60 s between healthy sites; security changes need explicit urgent propagation behavior and partition semantics |
| Availability | 99.95% monthly authentication availability per healthy site, measured by synthetic domain login/ticket acquisition; test one DC down at the full sustained load |
| Recovery | Single DC loss: client failover <=60 s. Complete site loss: surviving sites continue serving; explicitly measure client DNS/DC locator behavior |
| Disaster recovery | Encrypted backups at least hourly, off-site immutable copies; whole-domain RPO <=1 hour and RTO <=4 hours, proven by an isolated restore at target dataset size |
| Headroom | At sustained load with one DC unavailable: CPU <=70%, RAM <=80%, no unbounded queue growth; document disk and audit retention limits |

Throughput is aggregate, latency percentiles are per operation class and site.
Run combined traffic, not isolated maxima; publish achieved rates, failed rates,
client concurrency, data distribution, warm/cold cache state and hardware. Test
site loss separately: offline cached Windows login is not successful online
authentication. During partitions, AD's multi-master consistency can delay
revocations; document stale reads, conflict resolution, and which writes are
acknowledged. Do not promise immediate global revocation or zero RPO under all
partitions. Quarterly restore drills and a 24-hour soak are release requirements.

## Ergonomics as an acceptance requirement

A new administrator must be able to provision a test domain, join a client,
create a delegated helpdesk role, apply a password policy, identify a failed
replica, and restore a deleted user using documented UI paths. Measure at least
five representative administrators: >=90% unassisted completion for each
journey, with setup prerequisites and time-on-task published. Target <=10 minutes
for user/group delegation tasks after domain setup. Include keyboard-only and
screen-reader testing, clear dangerous-action previews, effective-permission
inspection, audit correlation, localization-ready text and actionable errors
that do not reveal credentials. GPO editing must expose unsupported settings
instead of silently discarding them. CLI/API operations need equivalent RBAC.

## Standards and source material

Use these as normative inputs, checking the current revisions during Phase 0:

- [Microsoft Open Specifications](https://learn.microsoft.com/en-us/openspecs/): MS-ADTS, MS-DRSR, MS-KILE, MS-PAC, MS-NRPC, MS-GPOL, MS-SMB2 and MS-DNSP.
- [Samba AD DC documentation](https://www.samba.org/samba/docs/): optional secondary interoperability comparison; not the production backend or the sole conformance oracle.
- [Kerberos RFC 4120](https://www.rfc-editor.org/rfc/rfc4120) and [LDAP RFC 4511](https://www.rfc-editor.org/rfc/rfc4511).
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) for administration UI/API, plus a domain-specific protocol threat model.
- [NIST digital identity guidance](https://pages.nist.gov/800-63-4/) for authentication policy; do not claim certification from using this reference.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for the administration interface.
