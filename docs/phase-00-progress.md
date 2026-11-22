# Phase 0 — Contract and laboratory progress

The initial compatibility scope is owner-selected: **2016 domain and forest
functional levels**, Linux-hosted native servers, Windows clients **and Linux/macOS
clients**. This is a scope decision, not compatibility acceptance. The 2025
functional level is not advertised by this initial profile; Server 2025 clients
are still proposed test targets at the selected level.

## Owner decisions

On 22 November 2026 the project owner approved the nine packets below in one
decision in the Babel management chat. The accepted scope and limits are those
in the pinned packets.

| Requirement | Exact reviewed scope and limits | Delivery | CI on the final PR revision |
| --- | --- | --- | --- |
| P00-02 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-02.md) | [PR #30](https://github.com/Ise-Tom/Babel/pull/30) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44507652333) |
| P00-03 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-03.md) | [PR #30](https://github.com/Ise-Tom/Babel/pull/30) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44507652333) |
| P00-04 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/validation/p00-04.md) | [PR #29](https://github.com/Ise-Tom/Babel/pull/29) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44376168435) |
| P00-06 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/validation/p00-06.md) | [PR #29](https://github.com/Ise-Tom/Babel/pull/29) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44376168435) |
| P00-07 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-07.md) | [PR #30](https://github.com/Ise-Tom/Babel/pull/30) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44507652333) |
| P00-10 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/validation/p00-10.md) | [PR #28](https://github.com/Ise-Tom/Babel/pull/28) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44351294880) |
| P00-11 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/validation/p00-11.md) | [PR #28](https://github.com/Ise-Tom/Babel/pull/28) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44351294880) |
| P00-13 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/292291ec4d79a03f7355e8d3646c9e850b6c0489/docs/validation/p00-13.md) | [PR #31](https://github.com/Ise-Tom/Babel/pull/31) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44543165955) |
| P00-14 | [Reviewed packet](https://github.com/Ise-Tom/Babel/blob/cf6681c22bc42707de6efc5b5c8db59eb70504ea/docs/validation/p00-14.md) | [PR #33](https://github.com/Ise-Tom/Babel/pull/33) | [Passed](https://github.com/Ise-Tom/Babel/actions/runs/44952652411) |

Phase 0 now has **12 of 17 requirements accepted**. P00-01, P00-16 and P00-17
remain in progress, and P00-05 and P00-12 remain blocked. Whole-phase acceptance,
production qualification and the 60 unrun client-conformance scenarios remain open.

## Requirement history and remaining evidence

| Requirement | Concrete result | Remaining exit evidence |
| --- | --- | --- |
| P00-01 | [Versioned matrix](../lab/compatibility.json): 30 operation families, positive/negative scenarios, requirements, protocol references, target/client combinations and accountable owner | Exact patched images/packages, complete wire-operation/control/error decomposition, approved profile and real-client runs |
| P00-02 | [Full identity/authorization packet](validation/p00-02.md): nine local cases cover stable GUID/domain SID, schema/matching, ordered ACLs, asynchronous inheritance, groups, revocation and durable receipts against pinned ADTS/DRSR/DTYP | Native identity/ACL implementation remains separate |
| P00-03 | [Full replication/restore design packet](validation/p00-03.md): eleven cases specify attribute wrap/GUID rules, link lifetimes, naming conflicts, deletion, progress, restore and RID quarantine against actual source sections | Native DRS/reference/fault qualification remains separate |
| P00-04 | [Full toolchain/parser packet](validation/p00-04.md): declared Linux profiles, exact compiler/ELF facts, release overflow checks, locked debug/release/client/fuzz/security gates and maintenance review | Changes to qualified targets or parser dependencies require requalification |
| P00-05 | Existing [isolated Windows lab definition](windows-reference-lab.md) retained | Licensed host/images, exact builds and two clean provisioning/discovery/cleanup runs; no host exists yet |
| P00-06 | [Full license/contribution packet](validation/p00-06.md): existing Apache-2.0/DCO choice, complete obligations, strict notice archives and standalone dashboard license retention | Specification/image/fixture rights remain P00-16 |
| P00-07 | [Full boundary/threat packet](validation/p00-07.md): eleven owned boundaries cover all twenty threats with assets, misuse, denial/fault behavior, residual risk and implementation gates | Live intake/backup coverage remains P00-17 and independent production assessment remains required |
| P00-08 | [Executable validator](../scripts/check_conformance.py) and [evidence inventory](../lab/conformance-evidence.json), included in CI | Real artifacts, exact platforms/specs and reviewer disposition; no structural check is product evidence |
| P00-09 | [Approved workload method](phase-00-workload.md), seeded fixture tooling and [executed RootDSE workload evidence](validation/p00-09.md) | Native mixed operations, real hosts and clients, cold and sustained profiles, WAN and outage runs, resource/cost measurements and owner SLO ratification remain |
| P00-10 | [Complete criterion packet](validation/p00-10.md): six reviewed-design transition examples, source/digest-bound CI checker and exception/invalidation controls | Runtime transitions retain their implementation gates |
| P00-11 | [Complete functional-level profile](functional-level-profile.md): 2016/2016 Linux-hosted creation contract, level/OS distinction, incompatibilities and transition refusal | Exact builds, native behavior and client runs remain separate |
| P00-12 | Windows/Linux/macOS profile templates remain explicit and unqualified | Exact owned/licensed host/image/build/package/architecture identifiers and rights are missing; no image has been acquired |
| P00-13 | [Full TLS/provider/channel review packet](validation/p00-13.md): exact stack, custody decision/limits, CRL rejection, in-process certificate replacement, independent exporter comparison and entropy/clock/key/signer faults | Native LDAP/EPA, general revocation freshness and production key/service/client/capacity gates remain separate |
| P00-14 | [Full dependency-review packet](validation/p00-14.md): signed MIT krb5 1.22.3 candidate, exact Linux AES profile, synthetic signed-PAC and service/time/replay negatives, maintained alternatives, license and FFI boundary | Product Rust adapter, AD PAC/delegation/PKINIT and real-client conformance remain separate unrun gates |
| P00-15 | [Entire original driver gate](validation/p00-15.md) explicitly accepted by owner | Native AD adapter/domain/key/backup behavior remains later implementation work |
| P00-16 | [Thirteen byte-pinned references and actual use-notice review](reference-use-review.md); external image use/distribution denied without explicit rights | Resolve concrete patent/program and reference-fixture/image rights; no blanket clearance or legal certification |
| P00-17 | [Solo intake/custody/absence process and explicit timing proposal](security-response-readiness.md); reporting configuration observed enabled | Original actual receipt/escalation drill and available backup remain unmet; timing change awaits owner agreement, no report sent |

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
accepted the entire original Phase 0 gate and selected profile. Phase 0 then had
**3 accepted, 8 in progress, 1 blocked and 5 planned requirements**. The four
earlier acceptance proofs remain unchanged. Later native directory/key/backup/
capacity gates remain under their actual Phase 1/3/4 requirements; neither
Phase 0 as a whole nor production AD compatibility is accepted.


## Completed functional-profile and governance exit packets

The Phase 0 design packets for P00-10 and P00-11 cover
[upgrade/recovery/scope governance](validation/p00-10.md) and
[domain/forest functional profile](validation/p00-11.md). The original requirements
are unchanged. Six worked interrupted transitions cover schema, keys, domain
restore, functional levels, storage and GPO; CI now rejects missing recovery and
invalidation material, expired exceptions, baseline waivers and false outcomes.
The Linux-hosted 2016/2016 creation profile preserves Windows/Linux/macOS clients
and explicitly refuses unqualified advertisements or level transitions. Immutable
reference review distinguishes 2025 DC operating systems from the 2025 level and
records a stale-source conflict. The owner accepted both scopes on 22 November
2026. Actual upgrades, domain recovery and all 60 client conformance cases remain unrun.


## Completed toolchain/parser and project-license gates

The owner accepted the P00-04 and P00-06 packets on 22 November 2026.
Actual native evidence binds the Linux/compiler/ELF/lockfile/binary;
debug and release arithmetic checks expose overflow, and required probes/fuzz/
audits retain their separate results. Contribution/redistribution terms are
recorded against real package notices. Notice extraction rejects omissions,
unlisted files and rewritten manifests; the standalone dashboard safely retains
full terms and blocks new unreviewed bundled runtime inputs. These close the
original Phase 0 foundation gates. Native AD conformance remains separate.


## Completed state, replication and threat-design gates

P00-02, P00-03 and P00-07 now each have a full original-criterion validation
packet. Twenty original worked design cases bind exact readable publisher
editions and 58 section headings. Corrections include cross-domain SID changes,
ordered ACL evaluation, asynchronous inheritance, group/token freshness and
distinct attribute/link/name conflict algorithms. Eleven accountable boundaries
cover all twenty threats and preserve explicit residual risks. The required CI
checker rejects missing cases/owners, source drift, false runtime/independent
assessment and unjustified external-asset use. It checks design integrity, not
AD semantics or proof of rights. All product cases remain unrun.

The owner accepted these design scopes on 22 November 2026. Detailed
operation mapping, exact licensed lab profiles, reference-use clearance and
the current P00-17 operational gate remain open.
The solo-response scheduling proposal records the genuine constraint without
pretending there is another responder or a successful intake drill.


## Completed TLS library/provider/channel qualification review

P00-13 now has a [full original-criterion packet](validation/p00-13.md) for the
selected Linux/Rustls/ring engineering profile. Ten Rust tests and 27 independent
methods exercise actual cryptographic controls, not only documentation. The
selected CRL expiry option is now explicitly enforced, certificate replacement
is observed in one process, independent OpenSSL exporter values are checked
against their exact session and provider faults fail authentication. The review
records WebPKI's unchecked CRL thisUpdate, lab-only software-key custody and
unimplemented LDAP/SASL/EPA as explicit constraints; it does not claim production
revocation or AD compatibility. Required CI retains source/input/binary evidence
and repeats coverage, sanitizer fuzz and packaged-binary probes.

The owner accepted the selected TLS review scope on 22 November 2026. Production
TLS qualification remains open.

## Kerberos/PAC dependency review candidate

P00-14 now has a [criterion-by-criterion packet](validation/p00-14.md) and
reproducible signed-source MIT krb5 1.22.3 lab. The fresh synthetic run passed
AES-256/AES-128 AP requests, signed minimal PAC verification, and negative
wrong-service, replay, expired, missing-PAC, tampered-PAC and wrong-client cases.
The library accepts a valid AP request without a PAC; Babel must reject
PAC-dependent authority separately. Delegation, PKINIT, production FFI and AD
client conformance remain explicitly unrun. The owner accepted the bounded
P00-14 dependency review on 22 November 2026.
