# Phase 0 — Contract and laboratory progress

The initial compatibility scope is owner-selected: **2016 domain and forest
functional levels**, Linux-hosted native servers, Windows clients **and Linux/macOS
clients**. This is a scope decision, not compatibility acceptance. The 2025
functional level is not advertised by this initial profile; Server 2025 clients
are still proposed test targets at the selected level.

## Work delivered in this change

| Requirement | Concrete result | Remaining exit evidence |
| --- | --- | --- |
| P00-01 | [Versioned matrix](../lab/compatibility.json): 30 operation families, positive/negative scenarios, requirements, protocol references, target/client combinations and accountable owner | Exact patched images/packages, complete wire-operation/control/error decomposition, approved profile and real-client runs |
| P00-02 | [State and authorization contract](adr/0005-directory-and-replication-invariants.md): stable identity, authorization order and worked rename/collision/revocation/group examples | Review against pinned specifications and native implementations |
| P00-03 | Same ADR: separate origin/local metadata, conflict/delete/restore examples and replica quarantine | Exact MS-ADTS/MS-DRSR algorithms, reference observations, multi-DC implementation and fault tests |
| P00-04 | [Dependency qualification register](phase-00-security-and-dependencies.md): qualified lab subset versus unselected production TLS/Kerberos/storage libraries | Production dependency ADRs, licenses/advisories and executable qualification |
| P00-05 | Existing [isolated Windows lab definition](windows-reference-lab.md) retained | Licensed host/images, exact builds and two clean provisioning/discovery/cleanup runs; no host exists yet |
| P00-06 | Apache-2.0/DCO owner decision retained; protocol/specification rights review explicitly versioned | Pin specification revisions and finish distribution/reference-fixture obligations |
| P00-07 | Named current owner, Tier 0 boundaries, boundary-to-threat/evidence ownership and intake exercise procedure | Actual private intake exercise, backup security contact and incident drill; no fictitious contact or test |
| P00-08 | [Executable validator](../scripts/check_conformance.py) and [evidence inventory](../lab/conformance-evidence.json), included in CI | Real artifacts, exact platforms/specs and reviewer disposition; no structural check is product evidence |
| P00-09 | [Mixed workload/fault method](phase-00-workload.md), hardware and measurement/cost accounting | Owner review, implementation, measured runs and SLO ratification; no invented benchmark |
| P00-10 | [Recovery/scope governance](phase-00-governance.md), irreversible transition examples and exception rules | Exercise transitions once implemented; independent production assessment remains separate from solo PR review |

## Client coverage

Windows 11 Pro/Enterprise and Server 2022/2025 are initial Windows targets.
Non-Windows targets are Ubuntu 24.04 LTS and Debian 13 with SSSD/MIT Kerberos,
and macOS on Apple Silicon and Intel using its directory/Kerberos integration.
Exact OS releases, cumulative updates, kernels, packages and architecture availability
must be pinned and supported by the upstream vendor before qualification; these
names do not promise support for every future build or hardware platform.

Linux/macOS cases include account/group lookup, permitted enrollment, online login,
password change/expiry/revocation and service-ticket SSO. They compare against
both a Babel host and an isolated Windows reference. Local login/PAM/keychain,
cached credentials and reconnect behavior need OS-specific observations. Windows
GPO is a Windows client capability. Linux/macOS policy enforcement requires
separately designed platform integrations/agents; later patch, remote access, file
transfer and EDR remain explicit roadmap features with their own OS matrices.

Mobile devices and network appliances remain explicit integration targets, not
claimed Windows domain-join/GPO clients. Federation, certificate enrollment and
RADIUS need their corresponding protocol/module qualification before support is
advertised. Linux compatibility does not mean hosting the server on every OS.

## Evidence format and execution

The JSON inventory uses schema version 1 and a SHA-256 binding to the exact
compatibility file bytes. Updating the matrix invalidates the old binding; inspect
which observations must be rerun before intentionally rebinding evidence. CI rejects
missing/duplicate cases, unknown requirement/profile/spec references, lost positive
or negative expectations and stale contract digests. All **60 scenarios are unrun**.
Existing native lab CI is separate, limited evidence; it has not been relabeled as
Windows or full LDAP conformance.

Each executed observation records source commit, client build/image, profile,
Babel/reference target, run/operator, environment/dataset, expected/actual result,
time/duration, tool versions and retained artifact paths/digests. Passed scenarios
must include all declared profile/target combinations with passing results. Failed
observations can be retained. Unrun/skipped/unsupported cases require a reason and
cannot contain executions or qualify a release. Review metadata is separate from
outcome. An operator cannot replace a failed comparison by dropping that client.

Artifacts must be existing bounded regular files under `lab/evidence-artifacts`,
without path traversal or symlink parents, and match their recorded SHA-256. Only
synthetic redacted evidence belongs in public Git; keep private security material
in restricted custody. The checker does not prove redaction, authenticity, correct
assertions or specification interpretation. Human review and trusted execution
remain necessary. No artifact is downloaded or test host contacted by validation.

Run:

```sh
python scripts/check_conformance.py
python scripts/check_conformance.py --require-ready
```

The first command checks structure and prints outcome counts. The second is an
explicit conformance-readiness check: approved contract, implemented operation families, exact qualified profiles,
pinned/reviewed specifications and accepted passing scenarios are mandatory. It
**must fail on the current inventory**. It is not the complete product release gate:
capacity, security assessment, recovery, packaging and all other phase exits still
apply. The validator's synthetic test fixtures are not checked-in product evidence.

Phase 0 remains in progress. No whole requirement or phase acceptance is inferred
from documents, tests of the validator or a green CI run. The dashboard keeps
user-accepted P01 scopes unchanged and records granular Phase 0 work separately.

## Explicit owner scope acceptance — 18 November 2026

The owner accepted **P00-08 for the current version-1 schema/traceability tooling**
and **P00-09 for the proposed workload/measurement method** after reviewing their
linked scopes in this conversation. These are design/tooling acceptances: all 60
conformance cases remain unrun and capacity/SLOs unmeasured. Other Phase 0
requirements and whole-phase acceptance remain outstanding. The dashboard records
reviewer/date, pinned implementation/proposal evidence and these limits.
