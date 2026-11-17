# Endpoint patch management capability contract

Status: planned later product capability; no patch service/agent is implemented.
[Phase 11](phases/phase-11.md), [Phase 12](phases/phase-12.md) and
[Phase 13](phases/phase-13.md) are the complete per-phase design and acceptance
specifications, refined by joint [Phase 17](phases/phase-17.md). The 15 stable
PATCH IDs below remain normative and fully traced.

The module follows the native AD-like server and advanced security milestones. The goal is Tanium-like endpoint patch-management
functionality: discover, assess, target, approve, distribute, install, verify and
report remediation across a fleet. This does not claim Tanium feature parity,
protocol compatibility or equivalent measured performance.

The management server, scheduler, repositories/relays and reporting services
must run on Linux. Windows and Linux endpoints use supported agents and native
update engines. This is a separately operated module; authentication, DNS and
directory replication must remain available if patch management is stopped or
overloaded. Core identity-server patching and secure updates remain mandatory
before this module; they are not deferred to these later phases.

## Latest roadmap phases

| Phase | Deliverables | Exit gate |
| --- | --- | --- |
| 11 — Endpoint inventory and feasibility | Secure agent enrollment, hardware/software/update inventory, platform support matrix, vulnerability/applicability catalog, native updater integration and Linux-hosted control-plane prototype | Signed agent installation and upgrade, trustworthy device identity, real Windows/Linux inventory tests, metadata/license review, coexistence and isolation threat review |
| 12 — Controlled patch deployment | Approved campaigns, deployment rings, prerequisites, maintenance/reboot policy, caching/relays, installation verification, failure handling and administrator UI/API | Real OS and selected third-party update tests, approval/RBAC denial tests, offline resume, tamper rejection, supported recovery and canary-abort exercises |
| 13 — Fleet qualification and production patch service | Three-site fleet operation, emergency remediation, disconnected-site workflows, compliance/SLA reporting, resilient orchestration and operational runbooks | 10,000-device qualification, degraded WAN/control-plane tests, compromise/recovery assessment, resource/bandwidth reports and usable operator workflows |

These phases have separate release gates from the first production directory
release. Scope the initial supported Windows editions/builds, Linux releases,
architectures and third-party products in Phase 11, publishing explicit limits.
Start with the qualified Linux host baseline and supported Windows client/server
matrix; add RPM-based distributions, additional architectures and applications
only after qualification. macOS, firmware/BIOS and mobile devices remain
separate extensions. General remote access, file uploads and native EDR are
explicitly planned after this module in the
[final endpoint operations phases](endpoint-operations-roadmap.md), with separate
permissions and acceptance gates; they are not patch-executor privileges.

## Functional acceptance contract

| ID | Required capability | Acceptance evidence |
| --- | --- | --- |
| PATCH-01 | Continuous hardware/OS/software inventory and update applicability assessment | Compare installed versions, missing updates, reboot state, device identity and observation timestamps with native tools; distinguish fresh, stale, unknown and unsupported devices |
| PATCH-02 | Trusted patch/vulnerability catalog with dependencies, supersedence and known issues | Reproduce applicable/not-applicable decisions, including vendor backports; correlate vendor severity, CVEs and known-exploited data without treating version-string matches as proof of vulnerability |
| PATCH-03 | Windows OS, Linux package/kernel and explicitly selected third-party application patching | Use supported Windows Update APIs and supported distribution package managers such as APT/DNF; test vendor prerequisites, licenses, conflicts and package signatures; GPO update settings alone are insufficient |
| PATCH-04 | Dynamic device groups, targeting previews and fixed campaign membership snapshots | Scope by approved inventory/domain/OU/tag criteria; show sample devices, exclusions and counts; audit later membership changes and prevent silent expansion of an approved rollout |
| PATCH-05 | Canary/pilot/production rings with configurable dwell, health checks, rollout limits and automatic pause | Inject a bad update or failed health check; later rings halt at the approved threshold; low report coverage cannot count as successful promotion |
| PATCH-06 | Maintenance windows, deadlines, user notifications, reboot deferral and forced-reboot controls | Test time zones/DST, sleeping devices, user sessions, grace periods, blackout windows and missed windows; unsupported reboot suppression must be surfaced rather than silently overridden |
| PATCH-07 | Preflight disk/power/network checks, dependency handling and application/service-aware installation | Test low disk, pending reboot, conflicting package transaction, required services, application health and interrupted install; mark blocked devices separately from failed ones |
| PATCH-08 | Bandwidth-aware content distribution with authenticated site relays and approved offline import | Verify vendor signatures plus approved content digests, resume interrupted transfers, deduplicate/cache payloads and apply per-site/concurrency limits; a relay may serve content but cannot authorize deployment |
| PATCH-09 | Durable campaign orchestration and disconnected endpoint recovery | Idempotent job identifiers, bounded retries/backoff, resume after agent/controller restart, cancel/expiry checks before execution and reconciliation after lost acknowledgments; no unbounded queued command execution |
| PATCH-10 | Independent post-install verification of installed version, reboot completion and service health | Separate downloaded, installed, reboot-pending, verified, failed, paused and unknown states; a zero exit code or missing device report is not proof of remediation |
| PATCH-11 | Safe uninstall/rollback or tested recovery per update class | Advertise rollback only where the vendor supports it; demonstrate restore/reimage/forward-fix for irreversible changes; preserve operator instructions and abort criteria before rollout |
| PATCH-12 | Emergency remediation and risk-based prioritization | Prioritize exploited/exposed assets with transparent evidence; exceptional maintenance/approval overrides need explicit scope, independent approval, expiry and immutable audit export |
| PATCH-13 | Compliance dashboards, remediation SLAs, exception register and report export | Show coverage denominator, overdue/stale/offline devices, unsupported/EOL products and expiring exceptions; track time-to-remediate by risk; do not report unknown endpoints as compliant |
| PATCH-14 | Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history | Separate catalog approval, targeting, execution, exception and reporting rights; test unauthorized cross-group actions, approver self-approval, API bypass and scoped automation credentials |
| PATCH-15 | Availability-aware server and domain-controller maintenance | Serialize DC maintenance by site/failure domain, preserve DNS/KDC/replication quorum where applicable, respect service topology and recovery checks; a workstation policy must never reboot every DC together |

## Agent and control-plane security

Patch orchestration can execute highly privileged changes across the fleet.
Treat compromise of its approval/signing authority as a potential fleet-wide
compromise, independent of the directory's own privileged roles.

- Bootstrap agents through an authenticated administrator-approved enrollment
  path with short-lived, scoped enrollment credentials. Bind unique device
  identities to mutual TLS, rotate certificates and revoke lost/cloned agents.
  Do not embed domain-admin credentials or share one secret across devices.
- Separate the low-privilege communication process from a minimal privileged
  update executor. Authorize typed, allowlisted operations and exact package
  versions/digests; do not provide arbitrary remote shell execution through the
  patch API. Run native installers with only the privilege they require.
- Bind authorized jobs to device/group scope, approved content, expiry, replay
  protection and campaign identity. Revalidate cancellation/authorization before
  execution, including after offline periods. Document command-signing trust,
  verifier rotation and offline revocation limits.
- Preserve vendor package and repository signature verification. Authenticate
  catalog/relay metadata; defend against malicious mirrors, downgrade/freeze
  attacks, path traversal, poisoned caches and replayed jobs. Hash checking alone
  cannot establish that an untrusted vendor or catalog is legitimate.
- Use approval separation and bounded concurrency/blast radius for sensitive
  campaigns. Protect agent updates with reviewed signatures/provenance and a
  recoverable rollout; uninstall/tamper protection must have an audited rescue
  path and cannot promise resistance to a fully compromised local kernel/root.
- Separate patch control-plane identities, storage and signing credentials from
  DC administration and directory secrets. Use scoped directory read access for
  targeting, not directory replication/password-read rights. Keep an approved
  recovery channel if the directory or normal identity provider is unavailable.
- Audit enrollment, inventory changes, catalog edits, approvals, commands,
  package provenance, installation results, exceptions and key changes to an
  external protected collector. Never capture real passwords, tickets, full
  process environments or unrelated user files in diagnostics.
- Define inventory data minimization, administrative access and retention.
  Address device naming and application inventory privacy; remote inventory
  must not silently become unrestricted endpoint surveillance.

Publish the Windows/Linux support matrix, required outbound endpoints, proxy
behavior and coexistence policy with WSUS/Intune/other managers. Detect competing
updaters/package locks and designate one deployment authority per workload.
No dependency on a Windows-hosted management server is allowed; optional vendor
services must be explicit and have tested outage behavior. An actual Windows
endpoint lab is still required for validation.

## Capacity and reliability qualification

Provisional target: **10,000 managed computer endpoints across three sites**,
matching the directory's initial computer-account dataset. This is separate
from the 10,000 human identities and is not a measured capability. Cover both
Windows and Linux endpoints and publish the actual workload mix.

Before implementation, ratify control-plane/relay sizing and SLOs in an ADR.
Initial engineering targets for Phase 13 qualification:

- Under the declared healthy network profile, at least 99% of continuously
  connected enrolled endpoints provide an inventory update within 15 minutes;
  p95 delivery/acknowledgment of an authorized job is within 60 seconds. Measure
  scheduled waiting, download/install and reboot durations separately.
- Test 10,000-agent reconnection after site/controller outage with randomized
  retry/backoff, rate limiting and durable queues. Recover campaign state without
  duplicate installs or silently losing approved jobs; report convergence time,
  queue depth and stale/unknown devices explicitly.
- Exercise simultaneous inventory, reporting, patch downloads and installs under
  configurable concurrency. Publish CPU/RAM/disk/IOPS, idle and active endpoint
  agent overhead, telemetry/storage retention and per-site bandwidth consumed.
  Patch traffic must not violate the core directory authentication SLOs.
- Reuse the [directory network fault profiles](requirements.md), including WAN
  latency/loss and a 24-hour site partition. Installation is maintenance-window
  and payload dependent; do not promise a fixed whole-fleet patch completion
  time without a measured bandwidth/availability model.
- Include real payload sizes in the distribution budget: a 2 GiB package sent
  independently to 10,000 endpoints is roughly 20,000 GiB before retries. Measure
  site-cache savings, disk eviction and cache miss storms; control-plane request
  throughput is not evidence of payload delivery capacity.
- Test controller/relay failure, filled caches/disks, expired certificates,
  agent compromise, bad catalog entries, provider outages and interrupted
  controller upgrades. Preserve authorization and campaign audit/state across
  backup/restore; unknown install outcomes require reconciliation.

## CI/CD and release evidence to add with implementation

Extend the pipeline when actual agent/control-plane source exists. Required
checks include Linux server builds plus the supported agent build matrix,
signed package/agent artifact verification, SBOM/dependency scans, message/parser
fuzzing, authorization tests and malicious job/catalog rejection. Use disposable
Windows/Linux VM snapshots for real OS/kernel/reboot cycles; containers alone
cannot qualify these flows. Add agent version-skew and staged agent-update tests.

Integration and release suites must exercise every PATCH ID, native package
applicability, supersedence, partial failures, offline resume, deployment rings,
canary pause, DST scheduling, verified install, supported rollback and clean-room
control-plane recovery. Use approved test patches and synthetic organizations.
Isolate trusted integration runners from untrusted PRs; never test deployments
against developer or production devices. Nightly fleet simulation supports, but
does not replace, measured real-endpoint qualification. Publish device counts,
target platforms, failures/skips and freshness/coverage with each result.

Before public release, independently assess the enrollment/executor/signing
boundaries and rehearse a compromised-controller response: stop dispatch, revoke
issuers/agents as appropriate, restore trusted metadata, inspect queued jobs,
rotate keys and safely re-establish managed endpoints. Document exactly what
cannot be undone once a privileged patch has run.
