# Verification and evidence plan

Current implementation: repository tooling and the first bounded Rust LDAP
RootDSE lab slice described in [progress](phase-01-progress.md). Phase documents, threat models
and acceptance criteria are executable-evidence specifications, not implemented
AD/endpoint tests. The new design integrity check validates coverage/structure;
it cannot prove protocol correctness, security or feasibility.

## Evidence contract

Each acceptance record contains requirement ID, scenario/test version, source
commit, artifact/tool/client/spec versions, dataset/host topology, expected/actual
result, outcome, time, retained redacted artifacts, accountable reviewer and
exception/expiry if applicable. Distinguish passed, failed, skipped, unsupported
and unrun. A zero-case/disabled-only run is not acceptance. A changed implementation
invalidates affected old evidence until rerun; archived results remain traceable.

Unit/property tests exercise invariants and denied operations. Integration tests
cross actual process/storage/protocol boundaries. Real-client tests use licensed
isolated Windows and declared Linux hosts/agents. Simulators support scale but
cannot qualify OS install/reboot, desktop behavior or endpoint sensor truth.
Security testing is authorized and isolated with synthetic identities; CI must
not control production endpoints or dump customer directory data.

## Per-phase executable gates to add with implementation

| Phase | Required evidence jobs / representative failures | Required retained result |
| --- | --- | --- |
| 00 | Spec/matrix trace, clean lab provisioning and cleanup, DNS/time/identity isolation, library/license/threat review | Reviewed operation matrix, ADRs and synthetic reference-lab run |
| 01 | Native locked build/lint/types/unit/property/parser fuzz, local durability faults, LDAP/DNS subset, real join/password/GPO slice | Exact supported operations, parser regressions, denied access and crash-consistency reports |
| 02 | Protocol/functional-level matrix, PAC/delegation/trust/GC/RSAT/GPO, password lifecycle and negative controls | Per-operation real-client/reference conformance with no unexplained acceptance gaps |
| 03 | Six-DC/three-site concurrency/partition, role loss, tombstones, stale restore, key rotation and full restore | Convergence/durability outcomes and <=1 h RPO/<=4 h RTO evidence |
| 04 | SAST/dependency/SBOM/fuzz, independent assessment, 24-hour mixed-load soak, UI/API misuse and accessibility/user study | Findings/retests, baseline SLO distributions and five-admin >=90% journey results |
| 05 | Reproducible trusted build, signatures/provenance/license, clean install/upgrade, staging, serialized rollout and abort/restore | Same immutable artifact digest through promotion and approved first-production readiness bundle |
| 06 | Actual scheduled scans, synthetic online auth probes, expiry alerts, support redaction and quarterly restore | Support/EOL/advisory history, monthly availability/error budget and drill outcomes |
| 07 | Enrollment/recovery, grant expiry, approval bypass, managed credentials, GPO revert and access reviews | Negative authorization/abuse, real-client credential rotation and privileged UX evidence |
| 08 | CA/template/federation claim attacks, stale posture/provider loss, detection fixtures and privacy export | Connector/support matrix, rule precision/recall/latency and privacy/failure reports |
| 09 | HSM/KMS/CA loss, branch credential exposure, compromised-replica quarantine and domain key recovery | Native feature feasibility, clean-room restore, scoped response and rescue evidence |
| 10 | Independent rebuild, signed update replay/freeze, long fuzz/differential/model tests and red-team exercises | Reproducibility, model assumptions, minimized regressions and independent retest outcomes |
| 11 | Agent enrollment/revocation, malicious inventory, actual package applicability/backports and updater conflicts | Device/catalog provenance, platform matrix, freshness and endpoint overhead |
| 12 | Bad canary, DST/offline schedule, reboot/native updater, signature/approval replay and irreversible recovery | Real Windows/Linux install/post-reboot verification, ring pause and cancellation evidence |
| 13 | 10k reconnect/mixed campaigns, degraded WAN/cache, controller compromise, agent skew and compliance truth | Freshness/ack/payload costs and no-directory-SLO-regression release bundle |
| 14 | Real headless/desktop sessions, consent/elevation, stolen session/relay, revocation and broker failure | Supported OS/session matrix, <=60 s connected revocation target and privacy/recording tests |
| 15 | Real filesystem traversal/reparse/race, quota/cancel, transfer resumption and no implicit execution | Authenticated digests/receipts, privileged-path denials and cleanup/recovery outcomes |
| 16 | Real OS sensor ground truth, PID reuse/event gaps, labeled benign/attack detections and safe containment | Precision/recall/latency, blind spots, tamper/rescue and prevention safety reports |
| 17 | Combined 10k agent/remote/transfer/EDR traffic, site/provider outages and cross-module compromise | Capacity/storage/cost, endpoint overhead, isolation/privacy and final service readiness bundle |

## Pipeline enforcement and trusted infrastructure

For any new component, the same PR adds its locked build, quality/type checks,
unit/property/functional tests, applicable SAST/dependency/license/SBOM scans,
parser fuzzing, packaging and scope-policy update. Never add always-green empty
jobs to claim a future gate exists. Each language/agent/OS matrix needs explicit
coverage; the present Python tools' 90% combined coverage threshold is not a
universal substitute for product-specific negative and conformance tests.

Untrusted PR code runs on ephemeral unprivileged hosted runners without domain,
cloud or signing secrets. Approved-main trusted lab jobs use disposable isolated
Windows/Linux VMs and per-run synthetic credentials with deterministic cleanup.
Nightly fuzz/multi-site/scale runs and release assessments require real allocated
resources; record provisioning failures as failures, not skips. Restrict release
OIDC/ref/environment identities and verify actual required-check/review controls
where supported. The owner explicitly authorized public repository visibility; required-check and
review enforcement must still be verified. Paid capacity and infrastructure remain
D-10 owner decisions, not automatically authorized by a visibility change.

Before a phase/module production gate, every phase requirement and linked global
requirement must have current passing evidence or an explicitly reviewed scope
exception that does not contradict the first-production contract. Documentation
integrity is necessary traceability, never proof that a security control works.
