# Phase 0 — Contract and laboratory progress

The initial compatibility scope is owner-selected: **2016 domain and forest
functional levels**, Linux-hosted native servers, Windows clients **and Linux/macOS
clients**. This is a scope decision, not compatibility acceptance. The 2025
functional level is not advertised by this initial profile; Server 2025 clients
are still proposed test targets at the selected level.

## Requirement history and remaining evidence

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
| P00-09 | [Mixed workload/fault method](phase-00-workload.md), hardware and measurement/cost accounting | Method approved and dataset tooling implemented; load runner, real hosts, measured runs and SLO ratification remain |
| P00-10 | [Complete criterion packet](validation/p00-10.md): six reviewed-design transition examples, source/digest-bound CI checker and exception/invalidation controls | Explicit owner validation of the full Phase 0 design gate; runtime transitions retain their implementation gates |
| P00-11 | [Complete functional-level profile](functional-level-profile.md): 2016/2016 Linux-hosted creation contract, level/OS distinction, incompatibilities and transition refusal | Explicit owner validation of the full Phase 0 design gate; exact builds, native behavior and client runs remain separate |

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

## Requirement refinement

The canonical phase now separates functional-level selection (P00-11), exact
platform profiles (P00-12), TLS/Kerberos/storage dependency review (P00-13–P00-15),
specification/fixture rights (P00-16) and intake/backup response exercise (P00-17).
These were bundled into P00-01/P00-04/P00-06/P00-07. Their separate acceptance
obligations remain unqualified; the two explicitly accepted scopes above are unchanged.

## Synthetic dataset implementation

The [generator/auditor](synthetic-workload.md) now implements the owner-approved
workload's seeded data inputs. Full-profile CI validates 22,150 logical objects,
254,000 direct and 12 nested membership edges, exact site/payload distributions
and separate negative graph inputs. This is development tooling under P00-09; the
owner's acceptance remains the engineering method scope, not measured capacity.
No native server, GPO/ACL semantics, token encoder or client conformance is accepted.

## TLS candidate and capability tracking

P00-13 now has an executable [Rustls/ring qualification experiment](adr/0006-tls-qualification-lab.md).
It implements bounded loopback mutual TLS, positive TLS 1.2/1.3 exchanges,
certificate/identity/time/purpose and obsolete-protocol rejection tests, exporter
prerequisite checks, a dedicated malformed-record sanitizer fuzzer and a separate
90% library coverage gate. Nineteen independent OpenSSL test methods run against
the real release process. These are transport qualification tests; LDAP/SASL
integration, Windows/Linux/macOS clients, revocation/key custody/provider-fault
and production load remain outstanding. All 60 conformance scenarios stay unrun.

P00-06 now includes actual notice retention for internal native lab archives,
including selected runtime dependencies and the Rust library bundle, with
post-extraction byte verification and both binaries retested. This does not finish
the separate P00-16 specification/reference-fixture rights obligation.

The [capability tracker](capability-tracker.md) exposes all 130 global capability
contracts with explicit implementation state, stage, implemented/missing behavior,
source-backed work and blockers. Shared design/tooling never automatically claims
functional implementation or starts a later phase. No new owner acceptance is
recorded; the four previously accepted requirement scopes remain unchanged.

## Earlier Rust PostgreSQL driver candidate

The earlier P00-15 increment introduced a [real async Rust driver qualification experiment](adr/0007-postgresql-driver-qualification.md)
against the owned PostgreSQL 18 lab. It tests binding, SCRAM rejection, limited
database privileges, commit/rollback, failed/deferred transactions, serialization,
lock/statement/client deadlines, explicit cancellation and connection loss.
A comparison demonstrates that raw driver command success after a caught SQL
failure does not establish a committed mutation; the helper tracks that failure
and refuses a successful acknowledgment. It conservatively reports unknown
commit outcomes and discards expired/lost connections without automatic retry.

The required CI adds a separate real-database driver job and 90% library coverage
gate, scenario-completeness checks and retained source/version/isolation/cleanup
evidence. Reviewed Unicode data terms and actual dependency notices are included.
That candidate increment did not close P00-15. The completed qualification and
subsequent owner decision are recorded below. I05/I26 retain their remaining
native integration and dependency obligations; all 60 client scenarios remain unrun.

## P00-15 full-gate acceptance — 18 November 2026

The [full driver/transaction validation packet](validation/p00-15.md) now addresses
every original P00-15 criterion. The selected stack has a typed default API,
streaming result bounds, cancellation-safe transaction ownership, durable receipt
replay with reauthorization, actual COMMIT reply-loss evidence and two coordinated
PostgreSQL process-crash recoveries. These close the gaps left by the candidate
increment. After reviewing the full packet and [passing 14-job CI](https://github.com/Ise-Tom/Babel/actions/runs/44327591957),
the owner explicitly answered **“Validate P00-15”** on 18 November 2026. This
accepts the entire original Phase 0 gate and selected profile. Phase 0 now has
**3 accepted, 8 in progress, 1 blocked and 5 planned requirements**. The four
earlier acceptance proofs remain unchanged. Later native directory/key/backup/
capacity gates remain under their actual Phase 1/3/4 requirements; neither
Phase 0 as a whole nor production AD compatibility is accepted.


## Completed functional-profile and governance exit packets

P00-10 and P00-11 now have complete Phase 0 design packets for owner validation:
[upgrade/recovery/scope governance](validation/p00-10.md) and
[domain/forest functional profile](validation/p00-11.md). The original requirements
are unchanged. Six worked interrupted transitions cover schema, keys, domain
restore, functional levels, storage and GPO; CI now rejects missing recovery and
invalidation material, expired exceptions, baseline waivers and false outcomes.
The Linux-hosted 2016/2016 creation profile preserves Windows/Linux/macOS clients
and explicitly refuses unqualified advertisements or level transitions. Immutable
reference review distinguishes 2025 DC operating systems from the 2025 level and
records a stale-source conflict. Both gates await explicit owner validation;
actual upgrades, domain recovery and all 60 client conformance cases remain unrun.
