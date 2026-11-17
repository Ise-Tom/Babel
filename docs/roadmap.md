# Roadmap and exit gates

Estimates require a staffed team and the Phase 0 spike; no delivery dates or
production claims are implied. Work is sequenced by dependencies, with full AD
replacement in the first production release. Security and ergonomics are
continuous workstreams, not final-stage add-ons.

Babel will own a native AD-compatible core. Samba AD DC is not a required runtime
or migration stepping stone. The [native-core plan](native-core-plan.md)
subdivides Phases 0–1 into N-00–N-06 with explicit protocol/model/test dependencies;
reviewed libraries remain permitted and cryptography will not be reinvented.

All Babel production services must be hosted on Linux. Windows environments
provide clients and AD interoperability references, not a required production
host. PLAT-01–PLAT-03 in the [requirements](requirements.md) are release gates.

| Phase | Deliverables | Exit gate / evidence |
| --- | --- | --- |
| 0 — Contract and feasibility | Inventory AD-01–AD-10 and integration expectations; qualify the Linux baseline; select license, maintainers and disclosure channel; establish native identity/storage/replication design and conformance harness; define Windows test licenses and infrastructure budget | Approved operation/client compatibility matrix, native-core/toolchain/storage ADRs, legal review, disposable Windows reference lab and test-runner isolation; N-00/N-01 gates |
| 1 — Reproducible vertical slice | Native core milestones N-02–N-06: durable identity/ACL model, read-only discovery/LDAP subset, authentication and authorized writes, Windows membership, initial GPO/SYSVOL and delegated UI/API; Linux packaging and observability | All N-02–N-06 dependency gates; locked build, negative ACL/parser/fuzz tests, clean Linux install/reboot, real Windows join/login/password/policy tests, SBOM and vulnerability scans; previews explicitly limited |
| 2 — Full protocol scope | Forest/domain semantics, LDAP/GC, Kerberos, DNS, SMB/RPC/Netlogon, GPO/SYSVOL, schema and functional levels, trust/migration | AD-01–AD-10 conformance matrix with real Windows clients and an isolated AD reference; documented failures block production |
| 3 — Multi-site and operations | Six DCs/three sites, partition/conflict handling, safe upgrades, restore, key/certificate rotation, external audit | Fault injection, 24-hour partition/rejoin, isolated domain restore, one-node/site loss, upgrade/rollback evidence and no lost acknowledged data within stated model |
| 4 — Security, capacity and usability qualification | Full threat review, independent assessment, 10k dataset load/soak, delegated admin journeys and accessibility | All SEC/OPS/UX gates; 24-hour mixed-load soak, SLO report, five-admin usability study, no unresolved critical/high security findings without explicit security-owner disposition |
| 5 — Production candidate and release | Signed/verifiable versioned packages/images, compatibility guide, support policy, migration rehearsal and operator runbooks | All prior gates approved, rollback/restore rehearsal, two-maintainer release review, license compliance and immutable artifacts promoted by digest |
| 6 — Sustainable operations | Supported update channels, upstream CVE intake, quarterly restore drills, regression matrix and documented deprecation | Published response/support policy, continuous conformance and capacity regression evidence |
| 7 — Strong identity and privileged operations | Passwordless admin access, hardened recovery, expiring privileged grants, managed credentials and GPO governance | Selected wave 7 items in the extended security catalog have compatibility, abuse, recovery and authorization evidence |
| 8 — Posture and detection | Entitlement review, endpoint posture, certificate/federation integrations and SIEM detection | Qualified client/integration matrix, measured detection quality, privacy review and capacity impact |
| 9 — Containment and resilience | Supported branch-controller isolation, hardware key custody, controlled incident response and compromise recovery | Backend feasibility, key/provider outage tests, partition and clean-room recovery drills |
| 10 — Continuous security assurance | Reproducible delivery, extended protocol verification, independent assessments and security usability | Reviewed evidence for selected assurance features, recurring regression and response exercises |
| 11 — Endpoint inventory and patch feasibility | Linux-hosted patch control plane, secure Windows/Linux agents, software/update inventory and trusted applicability catalog | Qualified OS/product support matrix, native updater proof, secure enrollment and isolated lab evidence |
| 12 — Controlled endpoint patch deployment | Approved campaigns, canary rings, maintenance/reboot windows, site caching, verified install and supported recovery | PATCH-01–PATCH-15 functional/security coverage, offline resume, bad-patch pause and denied-operation tests |
| 13 — Fleet-scale patch management | 10,000 managed devices across three sites, risk-based remediation, compliance reporting and resilient orchestration | Measured fleet/resource/bandwidth results, no directory SLO regression, independent security review and compromise/recovery drill |
| 14 — Remote device access | Windows/Linux remote desktop and terminal support through a Linux-hosted broker; attended consent and separately approved unattended access | REMOTE-01–REMOTE-06 OS/session, MFA, authorization, consent and revocation tests |
| 15 — General server-to-device file delivery | Authorized uploads, bulk targeting, protected destinations, resumable transfers and verified receipts | FILE-01–FILE-05 integrity, permission/path safety, interruption and no-automatic-execution tests |
| 16 — Native endpoint detection and response | Dedicated endpoint agent/module, OS telemetry, behavioral detection, investigation and authorized process/file/device containment | EDR-01–EDR-08 sensor qualification, labeled detection quality, privacy and safe-response evidence |
| 17 — Fleet endpoint operations qualification | Remote support, file delivery and EDR alongside patch management at 10,000 devices/three sites | Joint resource/bandwidth/retention benchmarks, independent assessment, compromised-agent/controller recovery and no directory SLO regression |

## Extended security capability backlog

The [extended security roadmap](security-roadmap.md) details 69 proposed
capabilities, including implementation prerequisites and acceptance constraints.
Waves 7–10 are sequencing proposals, not a reason to defer first-release security
or a feature already selected in the AD compatibility contract. Core password
and identity management (IAM-01), GPO and domain services remain first-production
requirements. No new application/security tests exist until implemented; add
feature-specific security, interoperability, recovery and capacity checks with
each capability.

## Later endpoint patch management

Phases 11–13 add [Tanium-like endpoint patch management](patch-management-roadmap.md)
as a Linux-hosted module for Windows and Linux devices. This includes real
patch deployment and verified remediation, not just inventory or GPO update
settings. The detailed plan defines 15 acceptance requirements, agent trust
boundaries, operational recovery, capacity targets and the additional CI/CD
tests required with implementation. It is a later product expansion; secure
maintenance and updates of Babel itself remain first-release requirements.

## Final endpoint operations and EDR expansion

Phases 14–17 add [remote access, general file uploads and native EDR](endpoint-operations-roadmap.md)
after patch management. Management services remain Linux-hosted, with installed
Windows/Linux endpoint agents or isolated modules. The plan specifies attended
and unattended remote support, separate transfer/execution permissions, native
endpoint sensors, behavioral detection and controlled containment. It defines
19 acceptance requirements and OS-specific validation, privacy, agent-security
and fleet-capacity gates. These capabilities extend the product after the core
directory release; no implementation or operating capacity is claimed yet.

## Pipeline expansion alongside implementation

The present CI does not pretend to run unimplemented application tests. Expand
it at each phase using these mandatory gates:

- Every pull request: locked build, formatter/linter/type checks, unit and
  authorization tests, license/dependency/SAST scans, parser fuzz smoke runs,
  workflow lint and secret scan. Security findings need triage, not blanket ignores.
- Main integration: reproducible packages, SBOM, vulnerability scan, ephemeral
  service tests on the qualified Linux baseline, including install/reboot and
  data permissions; approved changes run Windows domain join, policy and
  trust tests against disposable reference domains. Publish exact test counts.
- Nightly: broader supported-client matrix, longer fuzzing, multi-site faults,
  replication/restore and dependency security rechecks. Scheduled jobs must
  actually be provisioned before claiming this coverage.
- Release candidate: all full-scope protocol, security, capacity and usability
  reports measured on Linux server hosts; artifact signing/provenance, fresh install, upgrade, rollback and
  restore checks. A single green unit suite is insufficient.
- Deployment: promote the exact scanned/attested image digest to an isolated
  staging domain, run join/login/policy/replication checks, then require a
  protected production environment and a tested migration plan. Domain schema
  and key changes may require restore/forward fix; do not assume image rollback
  restores directory state. Use a planned DC rollout with abort criteria.

## Work to open first

1. Approve compatibility/integration inventory and license (owner/security lead).
2. Specify the native identity/storage/replication model and implement the
   N-00/N-01 conformance/toolchain foundation (protocol/storage maintainers).
3. Provision licensed Windows reference images and isolated trusted CI runners
   (infrastructure maintainer); do not expose these runners to fork PR code.
4. Choose implementation toolchain and add real build/test/dependency gates
   (application maintainers).
5. Define schemas for role delegation, audit events and health status, then
   prototype the domain setup and helpdesk journeys (security + UX maintainers).

The roadmap is committed documentation, not remotely created GitHub issues.
