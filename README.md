<!-- Generated report. Edit canonical phase documents and dashboard/progress.json. -->
# Babel project dashboard

Read this page in your browser using the repository's existing GitHub access. Bookmark this URL; no download or additional account is needed.

> Main code and open-PR proposals are reported separately. CI failures remain visible; public deployment still requires successful main CI.

Report source: [d1aabf4](<https://github.com/Ise-Tom/Babel/tree/d1aabf492bca13a7820d16e716488a62297c93f3>). Recorded implementation evidence: 2026-11-19, [525ac74](<https://github.com/Ise-Tom/Babel/tree/525ac7490b3208dff26073e01b72b086b49f8d8d>). These are separate revisions. Rebuilding does not accept requirements or refresh evidence.

**18 phases · 274 requirements · 130 features · 0 phases accepted · 56 recorded increments · 6 open problems**

Shared preparation links do not start a phase. Status follows explicit requirement activity and acceptance. Implemented increments can be narrower than their parent requirement. Acceptance is recorded after an explicit owner review of the stated scope, evidence and limits. Requirement and increment counts can differ between phases and are not effort percentages. Design records and passing CI do not establish AD compatibility or production readiness.

**Current focus:** Phase 00 — Three more Phase 0 design gates are ready: identity/ACL, replication/restore and threat ownership. Seven now await owner validation; three are accepted. Lab profiles, crypto qualification, use rights and response evidence remain open.

[Phase board](#phase-board) · [Implementation journal](#implementation-journal) · [Problems encountered](#problems-encountered) · [Feature catalog](#feature-catalog)

Use your browser's Find command to search. Expand a phase's requirements to read its details. The standalone HTML adds interactive search/filtering and JSON export; this GitHub view is the persistent report.

## Phase board

| Phase | Status | Accepted requirements | Ready for validation | In progress | Blocked | Planned | Related work records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [00 · Contract, native-core design and laboratory](#phase-00) | In progress | 3/17 | 7 | 4 | 2 | 1 | 47 |
| [01 · Native core and end-to-end development slice](#phase-01) | In progress | 2/16 | 0 | 3 | 2 | 9 | 28 |
| [02 · Complete directory and AD interoperability contract](#phase-02) | Planned | 0/24 | 0 | 0 | 0 | 24 | 1 |
| [03 · Multi-site replication, durability and recovery](#phase-03) | Planned | 0/16 | 0 | 0 | 0 | 16 | 1 |
| [04 · Security, capacity and administrator qualification](#phase-04) | Planned | 0/13 | 0 | 0 | 0 | 13 | 1 |
| [05 · First production release and controlled deployment](#phase-05) | Planned | 0/12 | 0 | 0 | 0 | 12 | 5 |
| [06 · Sustained operations and maintenance](#phase-06) | Planned | 0/13 | 0 | 0 | 0 | 13 | 1 |
| [07 · Strong identity and privileged administration](#phase-07) | Planned | 0/15 | 0 | 0 | 0 | 15 | 1 |
| [08 · Posture, certificate/federation services and detection](#phase-08) | Planned | 0/17 | 0 | 0 | 0 | 17 | 1 |
| [09 · Containment, key custody and compromise resilience](#phase-09) | Planned | 0/14 | 0 | 0 | 0 | 14 | 1 |
| [10 · Continuous security assurance and trusted delivery](#phase-10) | Planned | 0/14 | 0 | 0 | 0 | 14 | 4 |
| [11 · Endpoint inventory and patch-control foundation](#phase-11) | Planned | 0/15 | 0 | 0 | 0 | 15 | 1 |
| [12 · Controlled patch campaigns and verified installation](#phase-12) | Planned | 0/16 | 0 | 0 | 0 | 16 | 1 |
| [13 · Production patch fleet, compliance and resilience](#phase-13) | Planned | 0/13 | 0 | 0 | 0 | 13 | 1 |
| [14 · Remote desktop and terminal access](#phase-14) | Planned | 0/15 | 0 | 0 | 0 | 15 | 1 |
| [15 · General server-to-device file delivery](#phase-15) | Planned | 0/13 | 0 | 0 | 0 | 13 | 1 |
| [16 · Native endpoint detection and response](#phase-16) | Planned | 0/17 | 0 | 0 | 0 | 17 | 1 |
| [17 · Joint fleet qualification and endpoint service release](#phase-17) | Planned | 0/14 | 0 | 0 | 0 | 14 | 1 |

## Open pull requests

Main-branch totals above exclude these proposals. CI success does not merge a PR or accept a requirement. Validation below is author-recorded until reviewed.

GitHub metadata checked: 2026-11-19T14:24:59\+01:00.

**Current main CI: success.** A failed build is shown here; it does not qualify a public deployment or product release.

No open pull requests against main were observed.


## Phase 00

**Contract, native-core design and laboratory — In progress**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-00.md>)

**Requirement status:** 7 ready for validation · 4 in progress · 2 blocked · 1 planned · 3 accepted

**Recent recorded work:**

- W56 · Define solo vulnerability-response process and make timing proposal reviewable — [source evidence](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/security-response-readiness.md>)
- W55 · Pin actual public protocol editions and separate reference use from image/patent clearance — [source evidence](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/reference-use-review.md>)
- W54 · Complete accountable Tier 0 and later-module threat-boundary design — [source evidence](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-07.md>)

<details>
<summary>17 requirements, associated features and evidence</summary>

### P00-01

**Define the protocol-operation matrix and operation ownership. — In progress**

The protocol-operation inventory is drafted. Functional-level profile and exact platform pins now have separate P00-11/P00-12 acceptance; detailed positive/negative wire/control/error coverage remains unqualified.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Every AD operation maps to expected positive/negative behavior and an owner; unknown operations remain visible.

**Implementation explanations:** W32: Inventory the initial 2016 AD profile and Windows/Linux/macOS clients; W33: Enforce versioned conformance evidence integrity in CI; W39: Refine phase requirements by independent acceptance obligations; W55: Pin actual public protocol editions and separate reference use from image/patent clearance. See the [implementation journal](#implementation-journal).

### P00-02

**Define stable identities, authorization order, schema rules and local commit semantics. — Ready for validation**

Nine worked local cases cover GUID/domain SID rules, schema/matching and collisions, ordered ACLs and asynchronous inheritance, nested groups/token freshness, locally serialized revocation and durable receipts. Actual readable ADTS/DRSR/DTYP sections are bound by edition/raw digest/heading. The full original Phase 0 design gate is prepared; explicit owner validation is pending. Native directory/ACL implementation is not claimed.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Design review covers rename, DN collision, ACL inheritance, nested groups, concurrent updates and durable acknowledgment boundaries.

**Validation packet:** Full original P00-02 Phase 0 Identity/schema/authorization/local commit design gate; no native AD behavior, independent production assessment or whole-phase acceptance. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-02.md>)

**Implementation explanations:** W12: Threat model and open decision register; W27: Record PostgreSQL selection and a reviewable native state contract; W28: Run real PostgreSQL synthetic transaction and process-crash experiments; W34: Specify stable state and worked replication/recovery invariants; W52: Complete identity, schema, authorization and local commit design. See the [implementation journal](#implementation-journal).

### P00-03

**Define attribute replication/versioning and restore epochs before fixing a disk format. — Ready for validation**

Eleven worked cases specify independent updates, version wrap/half-range, little-endian GUIDs, separate link lifetimes and naming conflicts, lifecycle repair, progress commits, invocation epochs, retention and RID authority. Exact ADTS/DRSR sections are pinned; no disk format is frozen. The full original Phase 0 design gate is prepared; explicit owner validation is pending. Native replication/reference/fault evidence remains unrun.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Worked partition/delete/conflict/rollback examples specify observable outcomes and map to MS-ADTS/MS-DRSR.

**Validation packet:** Full original P00-03 Phase 0 Replication/versioning/conflict/restore epoch design gate; no native AD behavior, independent production assessment or whole-phase acceptance. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-03.md>)

**Implementation explanations:** W12: Threat model and open decision register; W34: Specify stable state and worked replication/recovery invariants; W53: Complete source-pinned replication, conflicts and restore epoch design. See the [implementation journal](#implementation-journal).

### P00-04

**Qualify the memory-safe toolchain and parser baseline. — Ready for validation**

The full original Phase 0 toolchain/parser gate is complete: Linux x86\_64 GNU on Ubuntu 24.04 CI/Debian 13 locally, exact pinned Rust/compiler/LLVM/ELF/binary/lock evidence, dependency-free unsafe-forbidden parser roots, reviewed alternatives and advisory/license maintenance. Debug/release overflow tests, real independent probes, coverage, locked audits and bounded sanitizer fuzz are required. Owner validation is pending. TLS/Kerberos/storage and all native AD/client behavior remain their separate gates.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Record supported platforms, alternatives, license/advisory maintenance and locked build/fuzz/security jobs.

**Validation packet:** Full original P00-04 memory-safe toolchain/parser-baseline gate for linux-x86\_64-gnu-bounded-parser-v1; no native AD or whole-server qualification. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/validation/p00-04.md>)

**Implementation explanations:** W01: Native Rust workspace and reproducible builds; W27: Record PostgreSQL selection and a reviewable native state contract; W35: Map security ownership and dependency/rights qualification gaps; W39: Refine phase requirements by independent acceptance obligations; W42: Qualify a bounded Rustls/ring TLS candidate with independent enforcement tests; W50: Complete the qualified Linux/Rust toolchain and bounded parser baseline. See the [implementation journal](#implementation-journal).

### P00-05

**Provide a disposable Windows reference and Linux host lab with reproducible DNS/time. — Blocked**

The isolated Windows lab definition exists; licensed Windows/Mac hosts and exact images are missing. Linux/macOS client qualification and two clean deployments have not run.

**Associated features:** [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect; declared Linux/macOS identity lookup, enrollment where supported, login/password and Kerberos SSO](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Two fresh deployments run discovery probes, isolate egress, clean up resources and publish exact image/build identifiers.

**Implementation explanations:** W26: Prepare an isolated Windows reference lab definition without provisioning; W32: Inventory the initial 2016 AD profile and Windows/Linux/macOS clients. See the [implementation journal](#implementation-journal).

### P00-06

**Establish the project license and contributor terms. — Ready for validation**

The full original Phase 0 license/contribution gate is complete: existing owner-selected Apache-2.0/DCO, actual contribution terms, selected third-party obligations and source/native/driver/dashboard distribution handling. Strict complete notice/package accounting and trusted pre-archive manifest integrity are enforced; standalone HTML retains full terms and rejects unreviewed bundled runtime inputs. Owner validation is pending; specification/image/fixture rights stay P00-16 and no certification is invented.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Record owner license/DCO decisions, contribution terms and third-party notice/redistribution obligations before distribution; do not invent certification.

**Validation packet:** Full original P00-06 project-license/contributor/third-party-obligation-recording gate; preserves the existing license decision, with specification/image/fixture and future product release rights separate. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/validation/p00-06.md>)

**Implementation explanations:** W25: Apply owner-selected Apache-2.0 license and DCO contribution terms; W32: Inventory the initial 2016 AD profile and Windows/Linux/macOS clients; W35: Map security ownership and dependency/rights qualification gaps; W39: Refine phase requirements by independent acceptance obligations; W43: Retain and verify actual license notices in experimental native archives; W44: Qualify an async PostgreSQL driver and prevent false transaction acknowledgments; W51: Complete project contribution and redistribution obligations with omission-safe artifacts. See the [implementation journal](#implementation-journal).

### P00-07

**Establish Tier 0 boundaries, review ownership and threats. — Ready for validation**

Eleven separately owned trust boundaries map all twenty threats to assets, misuse, denial/fault behavior, residual risk and canonical implementation gates. CI rejects missing owners or false runtime/independent-assessment claims. The full original Phase 0 design gate is prepared; explicit owner validation is pending. No second reviewer, operational backup or successful private drill is invented; P00-17 remains separate.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-09: Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Every boundary has misuse cases and accountable review; solo development review is not independent production assessment.

**Validation packet:** Full original P00-07 Phase 0 Tier 0 boundary/threat/ownership design gate; no native AD behavior, independent production assessment or whole-phase acceptance. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-07.md>)

**Implementation explanations:** W12: Threat model and open decision register; W35: Map security ownership and dependency/rights qualification gaps; W39: Refine phase requirements by independent acceptance obligations; W54: Complete accountable Tier 0 and later-module threat-boundary design. See the [implementation journal](#implementation-journal).

### P00-08

**Version the compatibility/evidence schema and requirement traceability. — Accepted**

Current version-1 compatibility/evidence schema and traceability tooling accepted by the owner. All 60 product conformance scenarios remain unrun; no AD compatibility, future schema expansion or whole-phase acceptance is implied.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Evidence records commit, test/client/spec revision, requirement, outcome and redacted artifacts; skipped/unrun are never passing.

**Acceptance review:** Project owner \(explicit approval in this conversation\), 2026-11-18. The project owner explicitly answered “Accept this schema/tooling scope” in this conversation on 18 November 2026. Scope: current version-1 schema and traceability implementation in PR \#22, not client compatibility or phase acceptance. Implementation/tests pinned to b98dac7d33b20bef1ab6ccfb4a295f40d2330500: https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/scripts/check\_conformance.py ; https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/tests/test\_conformance.py . 118 local repository tests passed; all 60 conformance scenarios are explicitly unrun.

**Implementation explanations:** W10: Required native and repository CI gates; W11: Complete phase specifications and traceability; W14: Phase dashboard and portable engineering report; W15: Permanent private GitHub dashboard publication; W18: Open-PR-aware private progress reporting; W33: Enforce versioned conformance evidence integrity in CI; W37: Make Phase 0 recovery, scope and acceptance governance concrete; W38: Separate actual phase execution from related preparation; W41: Track all global capabilities with explicit implementation scope and evidence; W45: Make phase activity and recent work visible separately from acceptance. See the [implementation journal](#implementation-journal).

### P00-09

**Approve the target workload, fault profiles and performance measurement method. — Accepted**

The owner-approved engineering method now has a deterministic generator and independent fixture auditor. Full-size data was generated/audited twice with byte-identical artifacts. The approval remains the workload/method scope; no token encoder, native load/capacity or production SLO is qualified.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Reviewed load model includes mixed successful/denied requests, cold cache, WAN loss/latency, partial outages and hardware costs.

**Acceptance review:** Project owner \(explicit approval in this conversation\), 2026-11-18. The project owner explicitly answered “Approve the workload/method scope” in this conversation on 18 November 2026. This accepts the Phase 0 engineering method only, not measured capacity or production SLO ratification. Reviewed proposal pinned to https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-workload.md ; tracked in https://github.com/Ise-Tom/Babel/pull/22 . No benchmark or infrastructure procurement was performed.

**Implementation explanations:** W12: Threat model and open decision register; W36: Define a reproducible target-scale mixed workload and fault method; W40: Generate and independently audit reproducible target-scale synthetic data. See the [implementation journal](#implementation-journal).

### P00-10

**Specify upgrade, recovery and scope-change governance. — Ready for validation**

The full Phase 0 upgrade/recovery/scope-governance design gate is complete. Six worked transitions define forward checkpoints, interruption, kind-specific recovery and invalidation. Required CI checks owner/review material, UTC expiry, baseline/phase-gate waiver rejection and unchanged unrun observations; its report binds the source and input digests. Explicit owner validation remains pending. Runtime recovery remains its actual implementation gates.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Irreversible schema/key/storage decisions require review and recovery examples; scope exceptions have owner, expiry and production impact.

**Validation packet:** Full original P00-10 Phase 0 governance design gate, including review/recovery examples and owner/expiry/production-impact exception policy; not runtime recovery. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/validation/p00-10.md>)

**Implementation explanations:** W13: Tested source and lab archive packaging; W14: Phase dashboard and portable engineering report; W15: Permanent private GitHub dashboard publication; W16: Compact interactive interface and verified static-hosting workflow; W18: Open-PR-aware private progress reporting; W19: Remove unpatched vulnerable tooling dependency path; W20: Scope-based phase sizes and explicit owner acceptance reviews; W21: Support public repository dashboard publication and prepare visibility transition; W22: Keep the tested compiler API instead of silently weakening security lint; W23: Verify Pages archives and minimize privileged deployment operations; W24: Verify correct Pages settings without administration writes; W29: Verify owner-applied repository protections and security settings; W30: Validate existing source-release protections before draft source prereleases; W31: Adapt development governance to the sole maintainer without bypassing CI; W33: Enforce versioned conformance evidence integrity in CI; W34: Specify stable state and worked replication/recovery invariants; W37: Make Phase 0 recovery, scope and acceptance governance concrete; W38: Separate actual phase execution from related preparation; W41: Track all global capabilities with explicit implementation scope and evidence; W45: Make phase activity and recent work visible separately from acceptance; W48: Complete recovery/scope governance with enforced design-contract checks. See the [implementation journal](#implementation-journal).

### P00-11

**Define the domain/forest functional-level profile. — Ready for validation**

The full Phase 0 functional-level design gate is complete: Linux-hosted 2016 domain/2016 forest creation profile, reference DC OS versus client OS distinction, inherited/optional/2025 incompatibilities and explicit refusal of unimplemented transitions. Immutable source review resolves a stale 2025-level statement. CI binds the matrix, preserves non-Windows clients and rejects false level advertisements. Owner validation is pending; no native level/client conformance is claimed.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Review supported levels, transitions and incompatible behavior; do not advertise unqualified levels.

**Validation packet:** Full original P00-11 Phase 0 level/transition/incompatibility design gate; no native functional-level or client-conformance acceptance. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/validation/p00-11.md>)

**Implementation explanations:** W49: Complete the Linux-hosted 2016 domain/forest functional-level contract. See the [implementation journal](#implementation-journal).

### P00-12

**Pin exact Windows, Linux and macOS platform profiles. — Blocked**

Exact Windows/Linux/macOS profiles cannot qualify without the selected licensed hosts/images and actual patched OS/build/package/architecture identifiers. Profile templates are not pinned acquisitions; no image was purchased, downloaded or provisioned. This is an external lab prerequisite, not passing client evidence.

**Associated features:** [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect; declared Linux/macOS identity lookup, enrollment where supported, login/password and Kerberos SSO](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Edition, architecture, OS/build, package and image identifiers are explicit; missing profiles cannot qualify compatibility.

No implemented increment is recorded for this requirement.

### P00-13

**Qualify the TLS library/provider and channel boundary. — In progress**

ADR 0006 and a bounded Rustls 0.23.46/ring 0.17.14 mutual-TLS lab now have certificate/identity/protocol/property/OpenSSL/fuzz and separate coverage evidence. This qualifies a candidate experiment only; production selection, LDAP/SASL channel binding, client compatibility, revocation/rotation/key custody, provider faults and load remain open.

**Associated features:** [SEC-04: TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Review exact versions/features, key custody, certificate, downgrade, channel-binding and provider-loss cases; no custom cryptography.

**Implementation explanations:** W42: Qualify a bounded Rustls/ring TLS candidate with independent enforcement tests. See the [implementation journal](#implementation-journal).

### P00-14

**Qualify Kerberos/PAC dependencies and cryptographic maintenance. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Review AES/PAC/replay/delegation support, licenses, FFI/unsafe boundaries and upstream maintenance; generic Kerberos is not AD conformance.

No implemented increment is recorded for this requirement.

### P00-15

**Qualify the storage driver and transactional interface. — Accepted**

The project owner explicitly validated the entire original Phase 0 driver/transaction gate on 18 November 2026: version review, parameterization, cancellation, commit/error mapping and recovery. The selected tokio-postgres 0.7.18/Tokio 1.54.1 local Unix/SCRAM/no-pool profile passes all 29 qualification cases, including actual lost durable replies and two process restarts. Native AD schema/ACL/service/key and domain recovery/capacity retain their separate Phase 1/3/4 gates.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Review versions, parameterization, cancellation, commit/error mapping and recovery before credentials or stable formats persist.

**Acceptance review:** Project owner \(explicit validation in this conversation\), 2026-11-18. The project owner explicitly answered “Validate P00-15” in this conversation on 18 November 2026. This validates the entire original Phase 0 gate: driver/version review, parameterization, cancellation, commit/error handling and recovery, for profile pg18-local-unix-scram-no-pool-v1. Reviewed implementation and full criterion packet: https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/validation/p00-15.md . All 29 cases pass, with actual lost commit replies, two database process restarts and 97.81% driver-library line coverage; all 14 CI jobs pass: https://github.com/Ise-Tom/Babel/actions/runs/44327591957 . Recorded decision: https://github.com/Ise-Tom/Babel/blob/49abca719c43082e4e9af30c5bc960d2b714f1b0/docs/validation/p00-15.md . Native AD storage, credential/key custody, domain recovery/capacity, the 60 unrun client scenarios and whole-phase acceptance remain separate gates.

**Validation packet:** Full P00-15 Phase 0 driver/transaction qualification gate and selected pg18-local-unix-scram-no-pool-v1 profile, accepted by the project owner on 18 November 2026. [Review exit criteria and evidence](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/validation/p00-15.md>)

**Implementation explanations:** W44: Qualify an async PostgreSQL driver and prevent false transaction acknowledgments; W46: Complete the P00-15 storage driver and transaction qualification gate; W47: Record owner validation of the full P00-15 Phase 0 gate. See the [implementation journal](#implementation-journal).

### P00-16

**Review specification and reference-fixture use rights. — In progress**

Thirteen actual public document editions now have publisher URLs, byte hashes, notice identity and reference-only dispositions; 58 state-design headings were verified against readable editions. Corrected the invalid DFS-R reference to MS-FRS2 and added MS-DTYP. External image/fixture uses remain denied without explicit rights. Concrete patent/program/image clearance remains unresolved; this is not blanket legal approval.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Pin document revisions and use/redistribution obligations separately from project licensing; unclear image/fixture rights block distribution.

**Implementation explanations:** W55: Pin actual public protocol editions and separate reference use from image/patent clearance. See the [implementation journal](#implementation-journal).

### P00-17

**Exercise private vulnerability intake and backup response coverage. — In progress**

Documented solo intake, private custody, triage/disclosure, owner absence and an explicit scheduling proposal. A read-only 19 November check reports private reporting enabled; receipt/notification/escalation are untested. The current live-drill and actual-backup gate is unchanged and unmet. Proposed pre-production scheduling awaits owner agreement; no private report was authorized or sent.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-09: Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** A synthetic private intake drill and real backup contact demonstrate receipt/escalation; no contact, SLA or exercise is invented.

**Implementation explanations:** W56: Define solo vulnerability-response process and make timing proposal reviewable. See the [implementation journal](#implementation-journal).

</details>


## Phase 01

**Native core and end-to-end development slice — In progress**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-01.md>)

**Requirement status:** 0 ready for validation · 3 in progress · 2 blocked · 9 planned · 2 accepted

**Recent recorded work:**

- W39 · Refine phase requirements by independent acceptance obligations — [source evidence](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/docs/phases/README.md>)
- W31 · Adapt development governance to the sole maintainer without bypassing CI — [source evidence](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/docs/github-main-ruleset.json>)
- W29 · Verify owner-applied repository protections and security settings — [source evidence](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/docs/github-security-settings.md>)

<details>
<summary>16 requirements, associated features and evidence</summary>

### P01-01

**Add actual native source only with locked build, lint, types, unit/property tests and fuzz smoke. — Accepted**

Current native LDAP component development safeguards accepted by the project owner. Future components and full product qualification remain separate obligations.

**Associated features:** [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** The scope guard is extended in the same reviewed PR; clean Linux build plus malformed-input regression corpus passes.

**Acceptance review:** Project owner \(explicit approval in this conversation\), 2026-11-17. Project owner explicitly answered “Accept this scope” in this conversation on 2026-11-17. Scope: development safeguards for the current native LDAP component, not the full server or future components. PR \#16 and its 12-job successful CI run: https://github.com/Ise-Tom/Babel/pull/16 ; https://github.com/Ise-Tom/Babel/actions/runs/44152161324 . Merged main cd6ad149870a05db4ab2a4f7fbca3e4d461af848 also passed all 12 jobs in run 44153995669.

**Implementation explanations:** W01: Native Rust workspace and reproducible builds; W02: Bounded BER / LDAP decoder; W06: Independent client and packaged-binary checks; W07: Property tests and core coverage gate; W08: Sanitizer fuzz smoke; W09: Native dependency, license and SBOM checks; W10: Required native and repository CI gates; W13: Tested source and lab archive packaging; W17: Bounded LDAP RootDSE filter discovery; W19: Remove unpatched vulnerable tooling dependency path; W20: Scope-based phase sizes and explicit owner acceptance reviews; W21: Support public repository dashboard publication and prepare visibility transition; W22: Keep the tested compiler API instead of silently weakening security lint; W23: Verify Pages archives and minimize privileged deployment operations; W24: Verify correct Pages settings without administration writes; W29: Verify owner-applied repository protections and security settings; W31: Adapt development governance to the sole maintainer without bypassing CI. See the [implementation journal](#implementation-journal).

### P01-02

**Implement stable identity and schema primitives before mutations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Preserve GUID/SID on rename and reject DN collisions, invalid classes and matching-rule violations.

**Implementation explanations:** W27: Record PostgreSQL selection and a reviewable native state contract; W28: Run real PostgreSQL synthetic transaction and process-crash experiments; W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P01-03

**Implement a transactionally durable local store. — In progress**

The P00-15 driver/transaction profile is now technically complete and ready for validation, including typed writes, bounds, abandoned futures, durable reply loss and actual before/after-commit Rust-driver recovery. Native AD identity/schema/ACL integration and the production directory store remain Phase 1 implementation work; this does not accept that store.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Commit-boundary kills recover old or new complete state; never acknowledge an undurable mutation.

**Implementation explanations:** W27: Record PostgreSQL selection and a reviewable native state contract; W28: Run real PostgreSQL synthetic transaction and process-crash experiments; W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P01-04

**Implement the declared bounded LDAP discovery/read subset. — In progress**

Loopback bounded RootDSE discovery/filter reads are implemented and tested; directory reads, controls and real-client qualification remain open. DNS discovery is separately tracked in P01-13.

**Associated features:** [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-05: AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Real probes and negative paging/filter/referral tests pass; RootDSE is not domain join.

**Implementation explanations:** W02: Bounded BER / LDAP decoder; W03: Read-only RootDSE queries; W05: TCP framing and session budgets; W06: Independent client and packaged-binary checks; W17: Bounded LDAP RootDSE filter discovery; W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P01-05

**Integrate reviewed authentication and initial bind/AS/TGS flows. — Blocked**

Credential rejection is implemented; real Kerberos/password/key behavior awaits design and conformance prerequisites.

**Associated features:** [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Positive/denied authentication, replay, expiry and downgrade tests pass without credential disclosure.

**Implementation explanations:** W04: Credential rejection and safe diagnostics; W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P01-06

**Implement computer-account membership and secure-channel rollover. — Blocked**

Windows lab, DNS/authentication and membership implementation are missing.

**Associated features:** [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect; declared Linux/macOS identity lookup, enrollment where supported, login/password and Kerberos SSO](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-08: Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** A supported Windows client joins, logs in and rotates its machine password; unsigned/unauthorized membership requests fail.

**Implementation explanations:** W26: Prepare an isolated Windows reference lab definition without provisioning. See the [implementation journal](#implementation-journal).

### P01-07

**Implement an initial GPO/SYSVOL delivery path with ACL/version consistency. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-06: Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** A Windows client applies and reverts a declared policy; interrupted writes recover without silently serving contradictory versions.

No implemented increment is recorded for this requirement.

### P01-08

**Provide delegated account/group/password administration through API/CLI. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Create/disable/reset/group actions require correct rights with consistent denied-action audit.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P01-09

**Package constrained Linux services and lifecycle health checks. — In progress**

Lab packaging/limits/diagnostics are tested; production Linux service lifecycle and privilege boundaries are unqualified. Certificate/TLS configuration is separately tracked in P01-16.

**Associated features:** [PLAT-02: Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-04: TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Clean install/reboot, DNS/time prerequisites and least-privilege file/port tests yield safe actionable errors.

**Implementation explanations:** W04: Credential rejection and safe diagnostics; W05: TCP framing and session budgets; W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P01-10

**Label and inventory development limitations. — Accepted**

Project owner accepted the current prototype’s scope inventory and limitation reporting. Authentication, storage, domain join and GPO remain unimplemented and Phase 1 remains in progress.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Each public operation has a tested/unsupported status; lab credentials and incomplete protocol behavior cannot be promoted as a production release.

**Acceptance review:** Project owner \(explicit approval in this conversation\), 2026-11-17. Project owner explicitly answered “Accept this scope” in this conversation on 2026-11-17. Scope: documentation, tests and CLI label the current prototype as a loopback-only LDAP discovery lab and disclose missing production/domain functionality. Evidence pinned to merged main: https://github.com/Ise-Tom/Babel/blob/cd6ad149870a05db4ab2a4f7fbca3e4d461af848/docs/phase-01-progress.md ; https://github.com/Ise-Tom/Babel/blob/cd6ad149870a05db4ab2a4f7fbca3e4d461af848/native/babel-ldap/src/main.rs . This accepts scope reporting, not those missing features or production readiness.

**Implementation explanations:** W14: Phase dashboard and portable engineering report; W15: Permanent private GitHub dashboard publication; W16: Compact interactive interface and verified static-hosting workflow; W17: Bounded LDAP RootDSE filter discovery; W18: Open-PR-aware private progress reporting; W20: Scope-based phase sizes and explicit owner acceptance reviews; W21: Support public repository dashboard publication and prepare visibility transition; W23: Verify Pages archives and minimize privileged deployment operations; W24: Verify correct Pages settings without administration writes. See the [implementation journal](#implementation-journal).

### P01-11

**Implement ordered ACL, inheritance and nested-group authorization. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Allowed/denied tests cover ACE order, object/parent rights, inheritance, group cycles and bounded expansion before writes.

No implemented increment is recorded for this requirement.

### P01-12

**Implement versioned journal recovery and durable retry receipts. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** State/journal/audit/idempotency commit together; lost replies and replay cannot skip committed changes or repeat mutations.

No implemented increment is recorded for this requirement.

### P01-13

**Implement DNS discovery and eligible DC locator records. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-05: AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Clients discover only eligible DCs; stale/invalid records and unsupported updates fail explicitly.

No implemented increment is recorded for this requirement.

### P01-14

**Implement password changes and principal-key lifecycle. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Authorized/denied password operations enforce policy; key custody, rotation and redaction precede valuable credential storage.

No implemented increment is recorded for this requirement.

### P01-15

**Provide the minimal delegated administration UI. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Accessible UI journeys use the same authorized core operations; allowed/denied results agree with API/CLI.

No implemented increment is recorded for this requirement.

### P01-16

**Implement certificate configuration and TLS failure handling. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-02: Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-04: TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Missing/expired/untrusted certificates and unsafe channel settings stop affected operations without disabling verification.

No implemented increment is recorded for this requirement.

</details>


## Phase 02

**Complete directory and AD interoperability contract — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-02.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 24 planned · 0 accepted

<details>
<summary>24 requirements, associated features and evidence</summary>

### P02-01

**Complete domain/forest lifecycle and naming contexts. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Reference creation/removal and queries preserve forest/domain boundaries and reject incompatible transitions.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-02

**Complete account lifecycle through supported protocol/API paths. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-07: Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Create/disable/delete/restore and membership changes preserve identity, rights and audit across supported clients.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-03

**Complete Kerberos AS/TGS, SPNs and service authentication. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-03: Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Real flows enforce declared encryption/time policy and reject replay, expiry, wrong keys and downgrade.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-04

**Complete LDAP controls, paging and referrals. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** RSAT/LDAP clients agree with reference continuation/referral/control semantics; unsupported controls fail explicitly.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-05

**Complete authenticated secure DNS updates. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-05: AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Signed authorized updates work; unsigned/replayed/wrong-owner changes and stale-record substitution fail.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-06

**Complete protected Netlogon membership and secure-channel paths. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-08: Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-02: Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Join/rejoin, machine-secret rollover and reset verify signing/sealing, identity and least privilege.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-07

**Complete GPO objects, linking, inheritance and filtering. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-06: Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Actual Windows resultant policy/script selection matches reference behavior and denies unauthorized edits.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-08

**Implement qualified functional levels and schema transitions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Unsupported levels and interrupted incompatible changes cannot leave false capability advertisements.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-09

**Complete forest/domain trusts and cross-domain authorization. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-09: Forest/domain trusts, cross-domain authorization, migration and coexistence with existing AD](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Two reference forests verify creation/removal, SID filtering, selective authentication and denied access.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P02-10

**Publish an operation-level compatibility report without unsupported universal-OS claims. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect; declared Linux/macOS identity lookup, enrollment where supported, login/password and Kerberos SSO](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Every AD contract row has real-client evidence with exact builds/spec revisions and no unexplained failure, skip or unrun acceptance case.

No implemented increment is recorded for this requirement.

### P02-11

**Complete schema/class/attribute matching semantics. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Reference import/export and mutations compare encodings, matching rules and invalid-class/value rejection.

No implemented increment is recorded for this requirement.

### P02-12

**Complete stable identity and object security-descriptor semantics. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Reference ACL/object tests preserve GUID/SID through rename/restore and verify inherited/object-specific allowed and denied access.

No implemented increment is recorded for this requirement.

### P02-13

**Complete password history, expiry, lockout and fine-grained policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-07: Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** User/admin changes enforce effective policy; weak passwords and inconsistent protocol enforcement are rejected.

No implemented increment is recorded for this requirement.

### P02-14

**Complete delegated password recovery authorization. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-07: Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Authorized recovery works; impersonation, enumeration and unauthorized reset/group escalation fail with redacted audit.

No implemented increment is recorded for this requirement.

### P02-15

**Complete PAC construction and validation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-03: Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Real service/reference cases verify signatures and required authorization data; forged/malformed/mismatched PACs fail.

No implemented increment is recorded for this requirement.

### P02-16

**Complete supported constrained-delegation behavior. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-03: Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Permitted delegation succeeds; unintended audiences, unapproved targets and escalation variants fail on actual services.

No implemented increment is recorded for this requirement.

### P02-17

**Complete global catalog and partial attribute sets. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Cross-domain searches return authorized partial attributes with correct naming-context and freshness behavior.

No implemented increment is recorded for this requirement.

### P02-18

**Complete attribute-level LDAP authorization and error filtering. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Protected attributes/existence do not leak through results, errors, paging or referrals.

No implemented increment is recorded for this requirement.

### P02-19

**Complete site/subnet placement, DC locator and discovery failover. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-05: AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Real clients select eligible sites/DCs and recover from stale DNS, wrong-site answers and server loss within declared bounds.

No implemented increment is recorded for this requirement.

### P02-20

**Complete SAMR/LSA and required administrative RPC operations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-08: Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-02: Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Supported RSAT/service-account calls agree with reference; unauthorized enumeration, escalation and unsupported opnums fail.

No implemented increment is recorded for this requirement.

### P02-21

**Complete required SMB transport and share protection. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-08: Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-02: Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Supported negotiation/signing/sealing and share access pass; downgrade, wrong recipient and unauthorized reads/writes fail.

No implemented increment is recorded for this requirement.

### P02-22

**Complete SYSVOL ACL/version consistency and qualified delivery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-06: Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Directory/filesystem permissions and versions reconcile after failure; actual policy files arrive through declared delivery/replication.

No implemented increment is recorded for this requirement.

### P02-23

**Implement FSMO/RID ownership, transfer and seizure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Handoff, failed-holder recovery and RID range tests prevent duplicate authority/allocation and preserve recoverable state.

No implemented increment is recorded for this requirement.

### P02-24

**Complete migration and coexistence with rehearsed recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-09: Forest/domain trusts, cross-domain authorization, migration and coexistence with existing AD](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Identity/permission/key mappings preserve cutover behavior; interrupted migration recovers without duplicate principals or credential exposure.

No implemented increment is recorded for this requirement.

</details>


## Phase 03

**Multi-site replication, durability and recovery — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-03.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 16 planned · 0 accepted

<details>
<summary>16 requirements, associated features and evidence</summary>

### P03-01

**Authenticate and authorize replication membership and secret access. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Unknown, revoked and insufficiently privileged replicas cannot read credential changes or alter membership; every enrollment is audited.

No implemented increment is recorded for this requirement.

### P03-02

**Apply change data and replication cursors atomically and idempotently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Duplicate/reordered/interrupted exchanges do not lose acknowledged local transactions or skip unapplied remote changes.

No implemented increment is recorded for this requirement.

### P03-03

**Resolve concurrent scalar attribute and object naming changes. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Modify/modify and move/rename converge under qualified metadata rules despite reordered delivery.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P03-04

**Handle replication topology and naming contexts under loss. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Discovery and replication respect eligible sites/context boundaries during node/site loss and rejoin.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P03-05

**Expose replication freshness and revocation uncertainty. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-09: Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** A partition causes visible stale/unknown warnings with measured convergence; UI/API never claims instant global disable during disconnection.

No implemented increment is recorded for this requirement.

### P03-06

**Protect against unsupported rollback and stale replica reintroduction. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Restore old snapshots with conflicting invocation/progress metadata; reject/quarantine unsafe joins and follow a tested recovery path.

No implemented increment is recorded for this requirement.

### P03-07

**Create coherent encrypted directory/SYSVOL/key-metadata backups. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Manifests bind directory, policy, keys and replica epochs and reject partial/inconsistent snapshots.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P03-08

**Meet the online DC/client failover objective. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Fault drills measure DNS/DC failover &lt;=60 seconds; offline cached login is not online service recovery.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P03-09

**Rotate TLS certificates and issuer trust safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Expiry, issuer loss and interrupted overlap reject unsafe trust without verification bypass.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P03-10

**Recover from local storage, process and queue exhaustion. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Disk-full, queue pressure and kills have bounded retries/memory and complete journal/audit outcomes.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P03-11

**Resolve linked membership, deletion/recycle and lingering-object conflicts. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Add/remove/delete/modify and tombstone-expiry cases converge without privilege resurrection or orphaned link authority.

No implemented increment is recorded for this requirement.

### P03-12

**Recover role/RID authority under transfer and seizure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** No duplicate holder/allocator survives recovery; a stale former owner cannot silently resume authoritative writes.

No implemented increment is recorded for this requirement.

### P03-13

**Restore full backups in a clean room with independent custody. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Recovery at target size works without the original domain or a sole directory-held key and verifies identity/ACL/policy/replica state.

No implemented increment is recorded for this requirement.

### P03-14

**Meet whole-domain disaster-recovery RPO/RTO. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Full-domain drills at target size prove RPO &lt;=1 hour and RTO &lt;=4 hours; breaches block qualification.

No implemented increment is recorded for this requirement.

### P03-15

**Rotate Kerberos, service, machine and trust credentials. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Actual clients verify intended overlap/rotation; compromised old keys do not remain valid indefinitely and recovery is explicit.

No implemented increment is recorded for this requirement.

### P03-16

**Recover from prolonged partitions, clock faults and degraded WAN. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** A 24-hour partition/rejoin, asymmetric loss and skew retain bounded queues and publish stale-state/convergence/data-loss outcomes.

No implemented increment is recorded for this requirement.

</details>


## Phase 04

**Security, capacity and administrator qualification — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-04.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 13 planned · 0 accepted

<details>
<summary>13 requirements, associated features and evidence</summary>

### P04-01

**Run independent integrated assessment and threat review. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Scoped reproducible findings cover protocol, keys, UI/API, replication, supply chain and restore.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P04-02

**Enforce secure protocol defaults and scoped legacy exceptions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-02: Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-03: Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-04: TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Invalid TLS, anonymous sensitive reads, unsigned channels and weak crypto fail; exceptions carry scope/expiry/audit and cannot silently become defaults.

No implemented increment is recorded for this requirement.

### P04-03

**Measure the full mixed-load contract with real clients and reference requests. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Publish dataset, hardware, caches, concurrency, rates, percentiles and unexpected errors; each baseline target is met or release-blocking.

No implemented increment is recorded for this requirement.

### P04-04

**Qualify sustained operation through the full soak. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** A 24-hour mixed-load soak shows bounded queues/storage and no unexplained credential/data corruption.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P04-05

**Demonstrate complete and privacy-preserving security audit. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-09: Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** For each privileged/auth/policy/key operation, expected events and denied cases are present, correlated and redacted; export loss is visible.

No implemented increment is recorded for this requirement.

### P04-06

**Qualify administrator journeys with representative users. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** At least five admins achieve &gt;=90% unassisted completion per declared journey, including delegation, policy, diagnosis and restore; publish time-on-task.

No implemented increment is recorded for this requirement.

### P04-07

**Qualify keyboard/screen-reader accessibility. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** WCAG 2.2 AA audit and manual assistive-technology journeys pass across supported administration surfaces.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P04-08

**Test denial and recovery through UI, API and CLI consistently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-05: Web/API admin MFA through phishing-resistant authentication, step-up for privileged actions, scoped sessions/tokens, CSRF protection and reauthentication](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-07: Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Role/session expiry, CSRF, unauthorized export/reset, recovery bypass and stale privilege tests preserve authorization and provide safe actionable errors.

No implemented increment is recorded for this requirement.

### P04-09

**Ratify production sizing and operating limits from results. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** ADR records DC/backup/audit capacity, retention, bandwidth and expansion triggers; suggested 4-vCPU/16-GiB sizing is not treated as measured beforehand.

No implemented increment is recorded for this requirement.

### P04-10

**Produce a signed-off first-production readiness bundle. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Every baseline requirement maps to current passing evidence; outstanding exceptions, unsupported clients and residual risks are explicit and approved before Phase 5.

No implemented increment is recorded for this requirement.

### P04-11

**Remediate and independently retest assessment findings. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Each finding has an owner/severity/fix/retest/disposition; an assessment report alone cannot close qualification.

No implemented increment is recorded for this requirement.

### P04-12

**Qualify DC/site failure headroom under load. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Losing a DC/site at sustained traffic preserves declared SLO/resource bounds and publishes degraded-mode limits and failures.

No implemented increment is recorded for this requirement.

### P04-13

**Qualify dangerous-action previews and unsupported-setting handling. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Bulk/irreversible changes preview exact scope/consequences; unsupported settings and partial failures are never silently discarded.

No implemented increment is recorded for this requirement.

</details>


## Phase 05

**First production release and controlled deployment — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-05.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 12 planned · 0 accepted

<details>
<summary>12 requirements, associated features and evidence</summary>

### P05-01

**Release only artifacts built from the reviewed tested commit. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Package digest, SBOM and provenance resolve to the same source/build identity; rebuilding during production promotion is prohibited.

No implemented increment is recorded for this requirement.

### P05-02

**Enforce release licensing, dependency notices and support metadata. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Approved license/obligations and supported-version matrix ship with artifacts; missing notices or unclear redistribution rights block publication.

**Implementation explanations:** W25: Apply owner-selected Apache-2.0 license and DCO contribution terms. See the [implementation journal](#implementation-journal).

### P05-03

**Sign artifact and installer metadata through scoped identities. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Signer/trust custody and artifacts resolve to reviewed tested source without broad release credentials.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P05-04

**Gate publication on the complete readiness/evidence bundle. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect; declared Linux/macOS identity lookup, enrollment where supported, login/password and Kerberos SSO](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Every Phase 0–4 baseline gate has current passing evidence; skipped client/capacity/security acceptance does not count as a pass.

No implemented increment is recorded for this requirement.

### P05-05

**Rehearse clean install and supported upgrade/migration paths. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [PLAT-02: Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Fresh Linux hosts and prior supported versions preserve identities, permissions, keys and policy state; incompatible downgrade is rejected.

No implemented increment is recorded for this requirement.

### P05-06

**Promote exact artifacts through isolated staging with functional checks. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect; declared Linux/macOS identity lookup, enrollment where supported, login/password and Kerberos SSO](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-06: Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Domain join/login/password/GPO/replication/restore smoke tests pass before production approval, with synthetic credentials and scoped access.

No implemented increment is recorded for this requirement.

### P05-07

**Serialize production rollout by fault domain with explicit abort criteria. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Canary/DC rollout preserves remaining authentication/DNS service; induced health/convergence failure pauses expansion and alerts the operator.

No implemented increment is recorded for this requirement.

### P05-08

**Rehearse compatible package rollback per migration class. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Runbooks identify reversible changes; rollback restores service without replaying incompatible data or key state.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P05-09

**Require independent sensitive-release approval and audit the decision. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** No self-approved high-risk publication or privileged fork runner; platform limitations are disclosed, never treated as enforced protection.

**Implementation explanations:** W29: Verify owner-applied repository protections and security settings; W30: Validate existing source-release protections before draft source prereleases; W31: Adapt development governance to the sole maintainer without bypassing CI. See the [implementation journal](#implementation-journal).

### P05-10

**Publish operator/security/support guides and known limitations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** A new operator verifies/install/updates/restores using shipped docs; unsupported levels/clients and disclosure contacts are explicit.

No implemented increment is recorded for this requirement.

### P05-11

**Qualify consumer verification and signed-metadata replay rejection. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Consumers reject changed bytes, wrong signers, expired/untrusted metadata and replayed unsupported releases.

No implemented increment is recorded for this requirement.

### P05-12

**Rehearse forward-fix or restore for irreversible transitions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Schema/key/state changes with no safe downgrade recover through tested forward-fix/coherent restore with explicit RPO/RTO.

No implemented increment is recorded for this requirement.

</details>


## Phase 06

**Sustained operations and maintenance — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-06.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 13 planned · 0 accepted

<details>
<summary>13 requirements, associated features and evidence</summary>

### P06-01

**Maintain explicit supported versions and security-update commitments. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Published matrix identifies release support/EOL and upgrade paths; advisory intake reaches accountable maintainers.

No implemented increment is recorded for this requirement.

### P06-02

**Monitor real online authentication, DNS and time. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Online fault probes alert accurately; cached offline login or missing telemetry cannot count as service success.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P06-03

**Operate vulnerability triage and coordinated disclosure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Exercises prove private report receipt, severity/impact assessment, patch/mitigation tracking and secure publication without premature sensitive details.

No implemented increment is recorded for this requirement.

### P06-04

**Run regular independent backup verification and restore drills. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Quarterly full-dataset isolated restores meet &lt;=1 h RPO/&lt;=4 h RTO and include credentials, SYSVOL and recovery-key access.

No implemented increment is recorded for this requirement.

### P06-05

**Manage expiry and security exception debt. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Certificate/key/legacy-protocol exceptions have owners and expiry; expired/unowned exceptions cannot silently continue.

No implemented increment is recorded for this requirement.

### P06-06

**Provide privacy-safe support diagnostics. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Export is explicitly scoped/redacted and access-audited; credential material, arbitrary user data and complete environments are excluded.

No implemented increment is recorded for this requirement.

### P06-07

**Keep capacity and reliability reports with meaningful error budgets. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Monthly site-level availability and growth trends include exclusions/outages and remediation; breaches generate owned corrective work.

No implemented increment is recorded for this requirement.

### P06-08

**Maintain recurring dependency/tool advisory scans and remediation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Scheduled scans actually run; stale results alert and urgent advisories receive owned out-of-cycle remediation.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P06-09

**Rehearse contact/maintainer and provider service-loss response. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** An absent administrator or unavailable provider has an owned tested escalation and service-recovery path.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P06-10

**Decommission data and versions through controlled retention policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Removal preserves required evidence/backup holds while preventing indefinite unnecessary identity data retention; migrations are auditable.

No implemented increment is recorded for this requirement.

### P06-11

**Monitor replica freshness, certificate expiry and capacity. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Injected replica/certificate/resource faults produce owned actionable alerts with explicit stale/unknown and observation gaps.

No implemented increment is recorded for this requirement.

### P06-12

**Maintain signing trust and reproducible update verification. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Signing/key/tool changes preserve consumer verification and rebuild checks; replay or expiry is not bypassed to ship.

No implemented increment is recorded for this requirement.

### P06-13

**Rehearse independent signing and backup-custody recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>)

**Acceptance evidence required:** Recovered authority works without a failed domain/provider or sole unavailable maintainer and remains auditable.

No implemented increment is recorded for this requirement.

</details>


## Phase 07

**Strong identity and privileged administration — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-07.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 15 planned · 0 accepted

<details>
<summary>15 requirements, associated features and evidence</summary>

### P07-01

**Secure privileged passkey/hardware-key enrollment. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-01: WebAuthn/FIDO2 passkeys and hardware security keys for administrator login; multiple authenticators and secure enrollment](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [A-03: Recovery hardened against helpdesk impersonation, SIM swapping and MFA fatigue](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Origin/replay/unauthorized enrollment fails; factors bind to intended identities with audited registration.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P07-02

**Implement time-bounded just-in-time/just-enough privileges. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-01: Just-in-time and just-enough privilege with expiring grants](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Grant expiry remains enforced after worker restart; tests cover nested groups, stale sessions/tickets and delayed replication with declared limits.

No implemented increment is recorded for this requirement.

### P07-03

**Separate requester/approver/executor for high-risk actions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-02: Dual approval and separation of duties for Tier 0 membership, trusts, replication rights, backup export and key operations](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** UI/API/bulk operations reject self-approval and scope substitution; signed-off target/content changes require reapproval.

No implemented increment is recorded for this requirement.

### P07-04

**Provide scoped managed service credential lifecycles. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [C-01: Windows LAPS-compatible local administrator password rotation and retrieval](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [C-02: Managed service accounts, including gMSA compatibility where selected](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [C-03: Linux service identities, keytab lifecycle and supported workload identity integrations](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Qualified gMSA/keytab retrieval, rotation and offline/reconnect behavior work on Windows/Linux services; unauthorized readers and secret logging fail.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P07-05

**Implement hardened password/self-service and lifecycle workflows. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-04: Password protection beyond basic policy: locally checked breached/common passwords, contextual exclusions, password history and supported fine-grained policies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [A-05: Adaptive throttling and credential-stuffing/password-spray detection across replicas](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [C-04: Joiner/mover/leaver workflows, ownership and deprovisioning reconciliation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [C-05: Delegated self-service password change/reset, account recovery and group requests](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Spray, enumeration, recovery impersonation and unauthorized reset/group request tests fail; breach checks do not export raw passwords.

No implemented increment is recorded for this requirement.

### P07-06

**Provide effective-permission and privilege-path views. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-05: Effective-permission explorer and privilege-path analysis](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [B-06: Periodic access certification, ownership and orphaned-privilege cleanup](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Displayed paths match ACL/trust/group decisions without exposing protected relationships to unauthorized viewers.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P07-07

**Govern GPO changes through diffs, preview and approval. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [D-01: GPO version history, diffs, independent approval and staged OU rollout](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-02: Effective policy preview, precedence and resultant-policy troubleshooting](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-03: Tested hardening templates for Windows and Linux](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-04: Policy integrity/drift detection, safe script distribution and privileged policy ownership](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Approved content/scope matches committed policy; out-of-band edits and directory/SYSVOL conflicts are detected.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P07-08

**Provide monitored break-glass and privileged-workstation guidance. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-03: Privileged access workstations and tiered administration guidance](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [B-04: Emergency break-glass access with separate custody and monitored use](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** A rehearsed IdP/provider outage preserves audited emergency access with separate custody and post-use rotation, without permanent hidden bypass.

No implemented increment is recorded for this requirement.

### P07-09

**Enforce exception ownership and expiration. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-02: Policy simulation and explainable access decisions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-03: Safe bulk operations with scope preview, dry run, idempotency and compensating actions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-04: Accessible secure enrollment/recovery and understandable authentication errors](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-05: Security exception register and policy-as-code change review](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Expired/unowned grants and exceptions fail closed with visible review and renewal decisions.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P07-10

**Qualify advanced privilege features without weakening baseline defaults. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-06: Authentication strength policies, session inventory and bounded revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-06: Operator training, trustworthy runbooks and versioned security baselines](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Negative/auth-strength/latency/recovery evidence covers selected feature IDs and mixed load; new security service failures cannot silently bypass MFA.

No implemented increment is recorded for this requirement.

### P07-11

**Secure factor replacement and privileged recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-01: WebAuthn/FIDO2 passkeys and hardware security keys for administrator login; multiple authenticators and secure enrollment](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [A-03: Recovery hardened against helpdesk impersonation, SIM swapping and MFA fatigue](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Lost-factor/replacement and impersonation cases pass without SMS-only Tier 0 or hidden permanent bypass.

No implemented increment is recorded for this requirement.

### P07-12

**Provide scoped local-administrator credential retrieval and rotation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [C-01: Windows LAPS-compatible local administrator password rotation and retrieval](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [C-02: Managed service accounts, including gMSA compatibility where selected](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [C-03: Linux service identities, keytab lifecycle and supported workload identity integrations](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** LAPS/platform-equivalent retrieval, rotation and offline recovery respect device/reader boundaries and redact secret material.

No implemented increment is recorded for this requirement.

### P07-13

**Implement access-review decisions and effective revocation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-05: Effective-permission explorer and privilege-path analysis](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [B-06: Periodic access certification, ownership and orphaned-privilege cleanup](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Owned reviews produce auditable retain/remove decisions and verify grant removal including stale sessions and replication limits.

No implemented increment is recorded for this requirement.

### P07-14

**Stage GPO rollout by OU and verify actual client revert. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [D-01: GPO version history, diffs, independent approval and staged OU rollout](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-02: Effective policy preview, precedence and resultant-policy troubleshooting](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-03: Tested hardening templates for Windows and Linux](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-04: Policy integrity/drift detection, safe script distribution and privileged policy ownership](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Pilot/target resultant policy is measured; failures pause expansion and revert restores real client behavior.

No implemented increment is recorded for this requirement.

### P07-15

**Qualify accessible privileged policy workflows and bulk simulation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-02: Policy simulation and explainable access decisions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-03: Safe bulk operations with scope preview, dry run, idempotency and compensating actions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-04: Accessible secure enrollment/recovery and understandable authentication errors](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-05: Security exception register and policy-as-code change review](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Keyboard/screen-reader users can preview, approve and diagnose exact-scope changes without hidden omission or unsafe defaults.

No implemented increment is recorded for this requirement.

</details>


## Phase 08

**Posture, certificate/federation services and detection — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-08.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 17 planned · 0 accepted

<details>
<summary>17 requirements, associated features and evidence</summary>

### P08-01

**Qualify certificate/smart-card authentication and mapping. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-02: Smart-card/certificate-based domain logon through PKINIT and compatible hardware-backed keys](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [E-04: Certificate enrollment and PKI integration, with any AD CS-compatible role separately qualified](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Supported clients validate mapping/rotation and reject expired/revoked credentials, weak mappings and unintended identities.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P08-02

**Provide scoped federation authentication connectors. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [C-06: Signed, versioned provisioning integrations such as SCIM and an external secrets manager](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [J-01: OIDC/OAuth2 and SAML federation through separately qualified modules](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Issuer/audience, nonce/state/PKCE and organization-confusion cases preserve intended identity/audience.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P08-03

**Integrate device-posture observations with explicit freshness. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [D-05: Device posture and conditional-access integrations](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-06: Support for endpoint credential protections and application-control baselines](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [J-02: Network access integrations such as RADIUS/EAP-TLS](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Spoofed/stale/missing inputs show known/unknown state; raw posture cannot grant Tier 0 membership.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P08-04

**Maintain certificate/key/trust inventory and renewal visibility. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [E-05: Certificate/key inventory, expiry forecasting and automated rotation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Expiry forecasting and safe overlap report exact owned keys/providers and accurate next actions.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P08-05

**Implement structured protected audit export. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [G-01: Structured, correlated audit export to SIEM/syslog with externally protected storage](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [G-05: Investigation views: identity timeline, effective permissions and configuration history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Versioned schema, redaction and reader authorization pass; collector loss and local root-trust limits remain explicit.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P08-06

**Develop labeled directory/credential/trust/GPO detection scenarios. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [G-02: Detection for replication abuse, suspicious DC registration, ACL escalation and privileged group changes](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [G-03: Detection for ticket abuse, password sprays, abnormal service-ticket requests and trust/GPO persistence](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Versioned fixtures measure expected alerts and false positives; missing endpoint signals/forged ticket limits are disclosed.

No implemented increment is recorded for this requirement.

### P08-07

**Provide safe canary identities and replayable detection-rule tests. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [G-04: Deception identities and monitored canary credentials](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [G-06: Detection engineering with replayable synthetic event fixtures](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Decoys have no real privilege, trigger approved handling and cannot be accidentally promoted into normal production accounts.

No implemented increment is recorded for this requirement.

### P08-08

**Provide purpose-scoped private search/export. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [J-03: Attribute-level privacy, scoped directory search and data-export controls](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [J-04: Retention, deletion and legal-hold policy for identity and audit data](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** LDAP/UI/API attribute denials and scoped export prevent unauthorized collection while retaining required discovery.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P08-09

**Define organization isolation and external integration boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [J-05: Explicit multi-organization/tenant security boundaries](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Independent deployment/forest boundaries are documented; shared writable DCs are never sold as hostile-tenant isolation based only on UI roles.

No implemented increment is recorded for this requirement.

### P08-10

**Qualify module resource cost and observability. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-01: Security posture dashboard with actionable, evidence-backed findings](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Mixed-load/provider measurements expose overhead and prevent module outages from stopping core authentication.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P08-11

**Qualify enrollment templates and issuance authorization. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-02: Smart-card/certificate-based domain logon through PKINIT and compatible hardware-backed keys](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [E-04: Certificate enrollment and PKI integration, with any AD CS-compatible role separately qualified](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Real providers/clients reject template/SAN escalation and unauthorized key/subject changes in enrollment and renewal.

No implemented increment is recorded for this requirement.

### P08-12

**Provide scoped provisioning and idempotent lifecycle mapping. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [C-06: Signed, versioned provisioning integrations such as SCIM and an external secrets manager](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [J-01: OIDC/OAuth2 and SAML federation through separately qualified modules](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Malicious attributes, duplicate/reordered events and unavailable providers cannot grant privilege or corrupt identity lifecycle.

No implemented increment is recorded for this requirement.

### P08-13

**Qualify network-access decisions and provider-loss behavior. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [D-05: Device posture and conditional-access integrations](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [D-06: Support for endpoint credential protections and application-control baselines](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [J-02: Network access integrations such as RADIUS/EAP-TLS](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Allowed/denied access follows scoped fresh inputs and tested failure policy without silently admitting devices on dependency failure.

No implemented increment is recorded for this requirement.

### P08-14

**Handle CA/CRL/OCSP outage and expiry conservatively. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [E-05: Certificate/key inventory, expiry forecasting and automated rotation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Revocation-provider loss and stale responses have declared per-operation behavior without disabling trust verification.

No implemented increment is recorded for this requirement.

### P08-15

**Build investigation timelines with provenance and gap detection. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [G-01: Structured, correlated audit export to SIEM/syslog with externally protected storage](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [G-05: Investigation views: identity timeline, effective permissions and configuration history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Clock/reorder/duplicate/source gaps remain visible; absent observations cannot produce an apparently complete timeline.

No implemented increment is recorded for this requirement.

### P08-16

**Enforce retention, deletion/hold and residency policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [J-03: Attribute-level privacy, scoped directory search and data-export controls](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [J-04: Retention, deletion and legal-hold policy for identity and audit data](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Expiry, holds, deletion and region boundaries preserve authorized evidence without indefinite unnecessary identity-data storage.

No implemented increment is recorded for this requirement.

### P08-17

**Provide accessible posture and detection-quality reporting. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-01: Security posture dashboard with actionable, evidence-backed findings](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Reports expose freshness, unknown/unsupported state and rule quality through accessible operator workflows rather than healthy-by-default gaps.

No implemented increment is recorded for this requirement.

</details>


## Phase 09

**Containment, key custody and compromise resilience — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-09.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 14 planned · 0 accepted

<details>
<summary>14 requirements, associated features and evidence</summary>

### P09-01

**Implement typed response workflows with scoped approvals and idempotency. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-01: Audited response workflows for account/device disable, trust suspension and service-key rotation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Disable/quarantine/trust/key actions reject wrong scope, replay, expired approval and unauthorized API calls; execution and cancellation are audited.

No implemented increment is recorded for this requirement.

### P09-02

**Rehearse domain ticket-signing credential recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-02: Domain-compromise recovery plan covering ticket-signing, machine, service, trust and administrator credentials](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Double rotation and downstream ticket validity are sequenced and verified in an isolated compromise-recovery drill.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P09-03

**Quarantine and safely reintroduce suspect replicas. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-03: Replica quarantine and controlled reintroduction after suspected compromise](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** A compromised/stale replica cannot contaminate clean state; evidence preservation, trust revocation, role recovery and controlled reenrollment are exercised.

No implemented increment is recorded for this requirement.

### P09-04

**Qualify read-only branch and password-cache exposure profiles. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [I-01: Read-only/limited-secret branch controller profiles when explicitly implemented by the native core](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Exact RODC/password-replication semantics, permitted caches, theft blast radius and credential reset behavior pass; writable state is never labeled read-only.

No implemented increment is recorded for this requirement.

### P09-05

**Qualify HSM/TPM/KMS operations per key class. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [F-03: Hardware-backed key custody through HSM/TPM or a supported external KMS](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Exact supported operations, provider latency limits and unsupported verifier/key types are documented and tested.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P09-06

**Apply least-privilege host/service and network exposure profiles. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [F-01: Reviewed systemd sandboxing, capability reduction and AppArmor/SELinux profiles](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [F-02: Host security posture: supported Secure Boot, measured boot and disk encryption](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [F-05: Hardened Linux storage, syscall and network profiles for optional container packages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [F-06: Linux host baseline drift and agent/update integrity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [E-06: Protocol exposure control and network segmentation templates](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Capabilities, systemd sandboxing, LSM policies, RPC ranges and update paths pass functional/denied tests without a privileged-container default.

No implemented increment is recorded for this requirement.

### P09-07

**Maintain coherent clean-room/offline recovery artifacts. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [I-02: Immutable/offline encrypted backups with split custody and recovery-key escrow](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [I-05: Recovery environment integrity and safe backup validation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [H-04: Recovery-safe security state restoration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Backups bind directory/SYSVOL/key/replica metadata and reconcile revoked identities and security epochs.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P09-08

**Provide safe degraded modes for security-service outages. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [I-03: Site isolation, failover and revocation-risk visibility](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [I-04: Security operation budgets and safe degraded modes](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** MFA/audit/KMS/CA failures have explicit per-operation behavior; no silent auth bypass, unbounded audit flood or hidden evidence loss occurs.

No implemented increment is recorded for this requirement.

### P09-09

**Exercise ransomware and insider response. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-05: Tested response playbooks and tabletop exercises](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Tabletop/technical containment and restore drills retain response time, operator mistakes, evidence and retested follow-ups.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P09-10

**Validate compartmentalization under malicious and resource-exhaustion scenarios. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [F-04: Resource isolation and DoS controls per service/peer](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [E-01: Compatibility-aware legacy authentication retirement](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [E-02: Kerberos delegation, ticket and principal hardening](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [E-03: Trust quarantine and cross-forest entitlement inspection](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Noisy response/relay/query workloads cannot exceed approved blast radius or violate authentication SLOs without an explicit failed qualification.

No implemented increment is recorded for this requirement.

### P09-11

**Rehearse service/machine/trust/admin credential recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-02: Domain-compromise recovery plan covering ticket-signing, machine, service, trust and administrator credentials](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Class-specific rotations reconcile exposed/revoked state and downstream clients without retaining compromised authority.

No implemented increment is recorded for this requirement.

### P09-12

**Qualify key-provider outage, backup and custody recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [F-03: Hardware-backed key custody through HSM/TPM or a supported external KMS](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Provider loss/restoration preserve required key custody and availability without plaintext fallback or unreviewed replacement authority.

No implemented increment is recorded for this requirement.

### P09-13

**Prove split-custody recovery independent of the failed domain. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [I-02: Immutable/offline encrypted backups with split custody and recovery-key escrow](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [I-05: Recovery environment integrity and safe backup validation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [H-04: Recovery-safe security state restoration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Required shares/contacts/keys work through an approved procedure after domain/provider loss without a single unrestricted custodian.

No implemented increment is recorded for this requirement.

### P09-14

**Exercise maintainer and external-provider compromise response. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-05: Tested response playbooks and tabletop exercises](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Signer/maintainer/provider compromise has tested revocation, independent recovery and owned disclosure/remediation.

No implemented increment is recorded for this requirement.

</details>


## Phase 10

**Continuous security assurance and trusted delivery — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-10.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 14 planned · 0 accepted

<details>
<summary>14 requirements, associated features and evidence</summary>

### P10-01

**Produce independently verifiable reproducible artifacts. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-01: Reproducible packages/images, signed provenance/SBOM and dependency license/CVE inventory](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Independent rebuilds compare bytes or explicitly reviewed nondeterminism for identical source/toolchain inputs.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P10-02

**Protect update channels from wrong signer, rollback and freeze. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-02: Secure update metadata with rollback/freeze protection and key recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Expired/version-replayed metadata and malicious mirrors fail verification; signing-key compromise and offline update recovery are rehearsed.

No implemented increment is recorded for this requirement.

### P10-03

**Maintain bounded multi-protocol fuzz campaigns. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-03: Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** LDAP/RPC/Kerberos/DNS/policy parsers and state machines have maintained sanitizer/property campaigns and resource budgets.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P10-04

**Differentially test protocol semantics against a licensed reference. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-03: Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Versioned selected operations compare real outputs/state effects; divergence is triaged, not accepted solely because a second implementation matches.

No implemented increment is recorded for this requirement.

### P10-05

**Apply focused formal/property analysis to high-risk invariants. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-04: Property-based checks or formal analysis for bounded high-risk logic](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Models for authorization, grant expiry, replication conflict and key transitions state assumptions and find/reject known counterexamples.

No implemented increment is recorded for this requirement.

### P10-06

**Run recurring independent assessment and remediation retests. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-05: Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Scoped assessments produce owned findings and independently verified fixes without exposing active secrets.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P10-07

**Require independent sensitive update/release decisions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-06: Hardened release governance and maintainer continuity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** One compromised signer/reviewer cannot silently publish trusted high-risk updates; exact-scope approval and audit are enforced.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P10-08

**Keep accessible posture, policy-as-code and operator education current. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-01: Security posture dashboard with actionable, evidence-backed findings](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-02: Policy simulation and explainable access decisions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-03: Safe bulk operations with scope preview, dry run, idempotency and compensating actions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-04: Accessible secure enrollment/recovery and understandable authentication errors](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-05: Security exception register and policy-as-code change review](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [L-06: Operator training, trustworthy runbooks and versioned security baselines](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Freshness/uncertainty, safe previews and exception expiry are tested; new operators complete privileged and emergency runbooks without hidden knowledge.

No implemented increment is recorded for this requirement.

### P10-09

**Monitor governance and platform enforcement limitations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-06: Hardened release governance and maintainer continuity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Actual required-check/review/ref/environment protections are verified where supported; unavailable private-repo features remain explicit release risks.

**Implementation explanations:** W29: Verify owner-applied repository protections and security settings; W30: Validate existing source-release protections before draft source prereleases; W31: Adapt development governance to the sole maintainer without bypassing CI. See the [implementation journal](#implementation-journal).

### P10-10

**Publish recurring security assurance evidence without certification overclaims. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-05: Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>); [K-04: Property-based checks or formal analysis for bounded high-risk logic](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Reports include test/model scope, failures, skips, unsupported platforms and residual risks; a green scanner suite is never labeled proof of security.

No implemented increment is recorded for this requirement.

### P10-11

**Align SBOM, provenance, artifact identity and distribution obligations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-01: Reproducible packages/images, signed provenance/SBOM and dependency license/CVE inventory](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Inventories/build/source/artifact digests agree and required notices/consumer verification metadata remain complete.

No implemented increment is recorded for this requirement.

### P10-12

**Minimize fuzz failures and retain regression corpora. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-03: Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Qualifying failures yield tracked minimized reproducers and regression tests; suppressions cannot erase unresolved findings.

No implemented increment is recorded for this requirement.

### P10-13

**Operate coordinated research intake and safe-harbor disclosure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-05: Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Published authorized scope, private intake, disclosure coordination and funded remediation are exercised and maintained.

No implemented increment is recorded for this requirement.

### P10-14

**Rehearse maintainer continuity and emergency release recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-06: Hardened release governance and maintainer continuity](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>)

**Acceptance evidence required:** Loss of a signer/reviewer has a usable independently controlled recovery process without removing consumer trust protections.

No implemented increment is recorded for this requirement.

</details>


## Phase 11

**Endpoint inventory and patch-control foundation — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-11.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 15 planned · 0 accepted

<details>
<summary>15 requirements, associated features and evidence</summary>

### P11-01

**Define a supported endpoint/agent/application update matrix. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Exact Windows editions/builds, Linux releases/architectures and selected third-party products have native-engine feasibility and licensing evidence.

No implemented increment is recorded for this requirement.

### P11-02

**Enroll agents with unique authenticated device identity. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Wrong identities, cloned/replayed tokens and unauthorized enrollment fail without embedded domain-admin secrets.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P11-03

**Collect bounded native hardware/software inventory. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-01: Continuous hardware/OS/software inventory and update applicability assessment](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Inventory matches actual OS/package tools; malformed/oversized payloads cannot exhaust endpoint or controller resources.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P11-04

**Authenticate update applicability and native backport/version rules. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-02: Trusted patch/vulnerability catalog with dependencies, supersedence and known issues](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Vendor signatures and native version/backport fixtures yield correct applicability beyond string matching.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P11-05

**Maintain explicit dynamic-target attributes and provenance. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-04: Dynamic device groups, targeting previews and fixed campaign membership snapshots](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Approved device/OU/tag mappings resist spoofed inventory and unauthorized cross-group changes; hostname reuse does not inherit device authority.

No implemented increment is recorded for this requirement.

### P11-06

**Detect competing update authorities and unsupported endpoints. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** WSUS/Intune/native locks and EOL products surface actionable conflicts; the service does not race another manager into unsupported state.

No implemented increment is recorded for this requirement.

### P11-07

**Separate agent communication and privileged action boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** A malicious inventory payload cannot execute a command, read arbitrary files or gain package-install/EDR/support rights.

No implemented increment is recorded for this requirement.

### P11-08

**Design authenticated content staging. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Source/recipient/signature/digest and partial-content checks reject tamper before distribution.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P11-09

**Define inventory privacy, access and retention. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Fields, reader roles and expiry are documented and tested against unauthorized collection/export.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P11-10

**Deliver a recoverable Linux-hosted management foundation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Controller/agent restart, certificate expiry and provider outage preserve device identity and show stale state without affecting domain login.

No implemented increment is recorded for this requirement.

### P11-11

**Rotate, revoke and rescue device enrollment credentials. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Real certificate rotation/revocation/recovery preserve identity and audited custody without accepting stale authority.

No implemented increment is recorded for this requirement.

### P11-12

**Report inventory freshness, reboot and unsupported observations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-01: Continuous hardware/OS/software inventory and update applicability assessment](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Missing/stale/unknown/unsupported states stay distinct; reboot/pending transaction status agrees with native endpoint reality.

No implemented increment is recorded for this requirement.

### P11-13

**Resolve update supersedence, prerequisites and dependencies. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-02: Trusted patch/vulnerability catalog with dependencies, supersedence and known issues](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Conflicting/superseded/prerequisite/known-issue fixtures select supported remediation order and reject unsafe combinations.

No implemented increment is recorded for this requirement.

### P11-14

**Qualify site caching and relay authority separation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Poisoned metadata, eviction/retry and recipient tests retain verification; holding payload never authorizes installation.

No implemented increment is recorded for this requirement.

### P11-15

**Budget inventory/controller/agent capacity and freshness. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** 10k simulation plus representative real devices reports resource/storage overhead and truthful freshness denominators.

No implemented increment is recorded for this requirement.

</details>


## Phase 12

**Controlled patch campaigns and verified installation — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-12.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 16 planned · 0 accepted

<details>
<summary>16 requirements, associated features and evidence</summary>

### P12-01

**Approve exact targets, content and risk before scheduling. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-04: Dynamic device groups, targeting previews and fixed campaign membership snapshots](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Changing membership/digest/privileged scope requires reapproval; self-approval, cross-group API calls and stale authorization fail.

No implemented increment is recorded for this requirement.

### P12-02

**Implement gated canary/pilot/production rings. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-05: Canary/pilot/production rings with configurable dwell, health checks, rollout limits and automatic pause](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Bad patch/health/error-rate fixtures pause later rings; missing report coverage cannot count as promotion success.

No implemented increment is recorded for this requirement.

### P12-03

**Implement maintenance scheduling and user notice. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-06: Maintenance windows, deadlines, user notifications, reboot deferral and forced-reboot controls](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Time-zone/DST, sleep/offline and active-session cases follow approved schedules with visible grace/deferral notices.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P12-04

**Run disk/power and package-prerequisite preflight. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-07: Preflight disk/power/network checks, dependency handling and application/service-aware installation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Insufficient capacity/power or missing dependencies block the device with actionable state rather than unsafe installation.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P12-05

**Verify approved package/vendor/content authenticity. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Signatures and approved digests reject tamper, replay and incomplete payloads before privileged installation.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P12-06

**Revalidate typed job authority before privileged execution. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Expired/cancelled/wrong-scope jobs cannot run after reconnect; no arbitrary command authority is exposed.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P12-07

**Verify actual native installation state. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-10: Independent post-install verification of installed version, reboot completion and service health](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Native versions/receipts confirm remediation; exit zero, downloaded bytes or offline silence cannot qualify success.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P12-08

**Provide update-class-specific failure recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-11: Safe uninstall/rollback or tested recovery per update class](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Uninstall works where supported; irreversible kernel/application/state changes follow tested restore/reimage/forward-fix with recorded limitations.

No implemented increment is recorded for this requirement.

### P12-09

**Prioritize emergency remediation by explainable exposure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-12: Emergency remediation and risk-based prioritization](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Known-exploited/exposed assets receive transparent priority without changing approved target/content authority.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P12-10

**Protect identity-service availability during server patching. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-15: Availability-aware server and domain-controller maintenance](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** A controller rollout cannot reboot all site DCs together; induced auth/replication health failure pauses and recovers the campaign.

No implemented increment is recorded for this requirement.

### P12-11

**Enforce reboot, deadline and deferral policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-06: Maintenance windows, deadlines, user notifications, reboot deferral and forced-reboot controls](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Native reboot/deadline/forced-restart cases match explicit policy; unsupported reboot suppression is never silently asserted.

No implemented increment is recorded for this requirement.

### P12-12

**Check competing native transactions and application health. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-07: Preflight disk/power/network checks, dependency handling and application/service-aware installation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Native locks and unhealthy application conditions remain visible; no racing update authority or silent unsupported override.

No implemented increment is recorded for this requirement.

### P12-13

**Distribute bounded resumable/throttled packages through site caches. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Retries/proxies, connection loss, quotas and hit/miss paths preserve content integrity within declared bandwidth limits.

No implemented increment is recorded for this requirement.

### P12-14

**Make installation retries and lost replies idempotent. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Duplicate IDs, ambiguous responses and restarts reconcile durable native results without repeated unauthorized installation.

No implemented increment is recorded for this requirement.

### P12-15

**Verify post-reboot/application health before campaign success. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-10: Independent post-install verification of installed version, reboot completion and service health](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Required restart is observed and service checks pass; pending reboot or unhealthy applications remain unverified/failed.

No implemented increment is recorded for this requirement.

### P12-16

**Control emergency overrides through scope, expiry and approval. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-12: Emergency remediation and risk-based prioritization](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Independent approval and audit prevent emergency status from granting unlimited/permanent installation privilege.

No implemented increment is recorded for this requirement.

</details>


## Phase 13

**Production patch fleet, compliance and resilience — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-13.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 13 planned · 0 accepted

<details>
<summary>13 requirements, associated features and evidence</summary>

### P13-01

**Qualify real OS/application remediation plus large-fleet orchestration. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [PATCH-10: Independent post-install verification of installed version, reboot completion and service health](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Publish exact platform/device counts and real versus simulated roles; containers/simulators cannot replace native install/reboot evidence.

No implemented increment is recorded for this requirement.

### P13-02

**Meet inventory freshness with transparent denominators. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-01: Continuous hardware/OS/software inventory and update applicability assessment](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Connected/stale/offline/unsupported categories stay explicit; &gt;=99% targets cannot hide unexplained failures or missing agents.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P13-03

**Bound reconnect storms, work queues and retries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** 10k-agent recovery after controller/site outage preserves authorization/cancellation, avoids duplicate installs and publishes convergence and queue metrics.

No implemented increment is recorded for this requirement.

### P13-04

**Budget payload bandwidth and relay storage from real package sizes. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Transfer tests measure cache hits/misses/eviction/retries under configured site limits; control API rate is not reported as distribution throughput.

No implemented increment is recorded for this requirement.

### P13-05

**Produce truthful compliance/SLA and exception reports. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Missing/stale/offline/unverified/EOL devices cannot appear compliant; risk-based overdue time and exception expiry are reproducible from raw receipts.

No implemented increment is recorded for this requirement.

### P13-06

**Provide delegated patch UI/API/CLI workflows. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Role/target/approval/audit behavior agrees across clients and rejects unauthorized scopes.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P13-07

**Recover controller/relay state and interrupted upgrades safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [PATCH-11: Safe uninstall/rollback or tested recovery per update class](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Backups, expired certificates, full disks and process failures reconcile endpoint reality before resuming approved campaigns.

No implemented increment is recorded for this requirement.

### P13-08

**Rehearse compromised-controller containment and recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-12: Emergency remediation and risk-based prioritization](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Stop dispatch, revoke/rotate trust, inspect queue/catalog, recover signing/enrollment and reinstall trusted agents through a documented rescue process.

No implemented increment is recorded for this requirement.

### P13-09

**Qualify agent/controller version skew. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Declared old/new combinations preserve identity, typed jobs/cancellation and truthful unsupported state.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P13-10

**Release the patch service with owned operating limits. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-15: Availability-aware server and domain-controller maintenance](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Independent review, resource/storage/retention sizing, failure runbooks and mixed-load no-directory-SLO-regression evidence are approved before production.

No implemented increment is recorded for this requirement.

### P13-11

**Measure job acknowledgment separately from execution. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-01: Continuous hardware/OS/software inventory and update applicability assessment](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** p95 ack reports retain dropped/unexplained requests; controller acceptance is never verified endpoint remediation.

No implemented increment is recorded for this requirement.

### P13-12

**Integrate ticket systems without granting execution authority. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Outages, duplicate tickets and replayed external events cannot widen permissions or report false completion.

No implemented increment is recorded for this requirement.

### P13-13

**Roll out signed agent upgrades with pause and recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Staged upgrades reject bad signatures, pause bad versions and retain tested rollback/forward-recovery.

No implemented increment is recorded for this requirement.

</details>


## Phase 14

**Remote desktop and terminal access — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-14.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 15 planned · 0 accepted

<details>
<summary>15 requirements, associated features and evidence</summary>

### P14-01

**Qualify actual desktop sessions by supported endpoint platform. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real Windows/Linux desktops including X11/Wayland have exact build/engine and unsupported-behavior evidence.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P14-02

**Require unique authenticated devices and scoped operator MFA/step-up. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-03: Separately approved unattended administration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Wrong-device, replayed/expired tokens and stolen low-privilege accounts cannot open a session or reuse a privileged endpoint credential.

No implemented increment is recorded for this requirement.

### P14-03

**Provide visible attended consent and immediate disconnect. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-02: Attended support with visible user consent and an immediate disconnect action](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Denied/expired/misleading requests fail; local user sees operator identity and can terminate a session without a remote approval.

No implemented increment is recorded for this requirement.

### P14-04

**Gate unattended support separately with time/device boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-03: Separately approved unattended administration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** No implicit permission from domain membership or patch role; expired device/operator grants fail and administrative access is audited.

No implemented increment is recorded for this requirement.

### P14-05

**Separate terminal, clipboard, transfer and recording channels. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-06: Safe operation across OS privileges and session states](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Denied channels cannot be reenabled through protocol/API bypass or unrelated support grants.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P14-06

**Authenticate and encrypt broker/session transport. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Certificate, recipient and session-binding failures close connections while protecting device/operator credentials.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P14-07

**Enforce bounded revocation and outage session policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** A connected session loses authority within a configured, tested &lt;=60 s revocation target; offline/broker-failed cases follow explicit safe expiry rules.

No implemented increment is recorded for this requirement.

### P14-08

**Govern recording purpose, access and retention. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Recordings have explicit reader policy, expiry/deletion and protected evidence custody.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P14-09

**Handle reconnect, concurrent operators and privilege changes safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-06: Safe operation across OS privileges and session states](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Session identity and consent are revalidated; no unnoticed takeover, indefinitely cached grant or unintended concurrent control survives switching/restart.

No implemented increment is recorded for this requirement.

### P14-10

**Qualify relay concurrency, bitrate and latency. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real-session load publishes bounded resource/capacity limits without starving identity traffic.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P14-11

**Qualify terminal and headless access independently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real Windows/Linux terminal cases have declared engines and identity boundaries; desktop tests cannot qualify headless access.

No implemented increment is recorded for this requirement.

### P14-12

**Enforce elevation, lock-screen and OS security prompts. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-06: Safe operation across OS privileges and session states](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Switching users and elevating require scoped authority/consent; remote support cannot suppress native security boundaries.

No implemented increment is recorded for this requirement.

### P14-13

**Qualify relay trust, content visibility and NAT/proxy paths. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Compromised relay tests document content visibility and prevent impersonation or silent encryption weakening.

No implemented increment is recorded for this requirement.

### P14-14

**Enforce recording notice, consent and sensitive-input boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Users see accurate recording policy; covert capture and indiscriminate credential/key logging fail tests.

No implemented increment is recorded for this requirement.

### P14-15

**Recover from compromised operators or support brokers. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Revocation, termination and independent rescue regain control without depending on the compromised broker.

No implemented increment is recorded for this requirement.

</details>


## Phase 15

**General server-to-device file delivery — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-15.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 13 planned · 0 accepted

<details>
<summary>13 requirements, associated features and evidence</summary>

### P15-01

**Authorize exact file content, device scope, destination and expiry. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-01: Explicit server-originated uploads to one or many selected endpoints](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Target/digest/path changes require renewed approval; upload-only and cross-group operators cannot gain execution, patch or retrieval rights.

No implemented increment is recorded for this requirement.

### P15-02

**Protect staging and source/recipient authenticity. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-02: Secure staging, integrity and recipient verification](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Wrong sender/device, tampered metadata, unauthenticated hash substitution and untrusted TLS are rejected; staged confidential files are access-restricted.

No implemented increment is recorded for this requirement.

### P15-03

**Validate destination scope and lexical/canonical paths. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-03: Destination and privilege restrictions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Traversal, encoded paths and privileged startup/system destinations fail before accepting upload.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P15-04

**Apply explicit ownership, ACL and overwrite policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-03: Destination and privilege restrictions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Default deny for privileged locations; approved overwrite preserves declared permissions and cannot convert a data upload into executable persistence.

No implemented increment is recorded for this requirement.

### P15-05

**Provide resumable bounded authenticated transfers. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Corrupt/reordered/replayed chunks, offset overflow, connection loss and retries cannot finalize incorrect or unauthorized content.

No implemented increment is recorded for this requirement.

### P15-06

**Finalize atomically where supported and report verified receipt. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Partial files are never treated as delivered; unsupported atomic behavior is visible and staged fallback is tested with interrupted finalization.

No implemented increment is recorded for this requirement.

### P15-07

**Bound transfer disk, memory and bandwidth usage. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Quotas, full disk and excessive chunks/concurrency cannot exhaust endpoints/controllers or violate directory resource bounds.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P15-08

**Apply explicit file-content and malware policy without automatic execution. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Type/size/scanning failures block according to policy; detection limits are documented and uploads cannot silently launch installers/scripts.

No implemented increment is recorded for this requirement.

### P15-09

**Provide privacy-safe file-delivery audit. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Operator/device/path/digest/outcome is auditable without raw contents or unrelated user data.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P15-10

**Qualify transfer recovery and mixed-load resource isolation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Concurrent representative real filesystem transfers survive agent/controller restarts and malicious paths without directory SLO regression.

No implemented increment is recorded for this requirement.

### P15-11

**Defeat filesystem symlink/reparse/rename races. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-03: Destination and privilege restrictions](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real Windows/Linux open/finalization races cannot escape the approved directory or substitute privileged overwrite targets.

No implemented increment is recorded for this requirement.

### P15-12

**Enforce cancellation, expiry and abandoned staging cleanup. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Cancelled/expired jobs cannot resume after reconnect; stale partial content is removed within a stated deadline.

No implemented increment is recorded for this requirement.

### P15-13

**Authorize endpoint file retrieval independently from upload. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Upload-only operators cannot read user files; retrieval requires separate scope/privacy policy and denied-operation evidence.

No implemented increment is recorded for this requirement.

</details>


## Phase 16

**Native endpoint detection and response — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-16.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 17 planned · 0 accepted

<details>
<summary>17 requirements, associated features and evidence</summary>

### P16-01

**Enroll a dedicated sensor module with isolated authority. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Per-device identity/revocation and module boundaries prevent unrestricted patch/support credential reuse.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P16-02

**Implement supported native telemetry sources. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-02: OS-specific endpoint telemetry](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Process/network/file and selected persistence/security sources use the exact declared OS/kernel interfaces.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P16-03

**Preserve stable event/process provenance and loss visibility. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-02: OS-specific endpoint telemetry](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** PID reuse, clock changes, reconnect duplicates, reordered events and buffer overflow cannot silently corrupt identity or claim complete healthy telemetry.

No implemented increment is recorded for this requirement.

### P16-04

**Verify and execute bounded signed/versioned detection and indicator rules. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Untrusted/costly rules cannot bypass signing/version policy or exhaust endpoint CPU/memory.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P16-05

**Provide scoped investigation and collection actions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-04: Investigation and privacy-scoped evidence collection](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Case/timeline/collection permissions are audited and denied across unauthorized assets without blanket credential/memory extraction.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P16-06

**Contain the authorized process generation safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** PID reuse, protected targets and expired/replayed/wrong-scope actions fail with generation-aware receipts.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P16-07

**Implement recoverable network isolation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Narrow authenticated rescue survives isolation and release is rehearsed on actual endpoints.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P16-08

**Operate offline buffering and trusted cached rules safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Disk/memory quotas, encryption/access controls, sequence gaps and reconnect backpressure preserve visibility; outages do not stall domain login or fill disks indefinitely.

No implemented increment is recorded for this requirement.

### P16-09

**Detect sensor tamper and define realistic protection boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-06: Tamper resistance and trustworthy sensor health](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Stopped/stale sensors, changed policy and signer failure alert with provenance; root/kernel control is not claimed containable by local tamper protection.

No implemented increment is recorded for this requirement.

### P16-10

**Qualify prevention safety and endpoint overhead. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Supported enforcement, benign-safety and real performance cases meet declared limits before enabling prevention.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P16-11

**Sign, stage, recover and uninstall the sensor securely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Signed updates, authorized rescue/uninstall and staged rollback/forward-recovery work without stealth persistence.

No implemented increment is recorded for this requirement.

### P16-12

**Qualify telemetry ground truth and platform blind spots. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-02: OS-specific endpoint telemetry](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real fixtures compare events/lineage/hashes against truth; missing sources and unsupported builds remain visible.

No implemented increment is recorded for this requirement.

### P16-13

**Measure labeled detection quality and alert delay. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Versioned malicious/benign scenarios publish precision/recall, latency and false positives/negatives; missing signals are not clean results.

No implemented increment is recorded for this requirement.

### P16-14

**Preserve evidence provenance, integrity and retention. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-04: Investigation and privacy-scoped evidence collection](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Artifacts retain hashes/source/custody and authorized retention; tampered/incomplete evidence and unauthorized readers are rejected.

No implemented increment is recorded for this requirement.

### P16-15

**Quarantine and recover files under separate authority. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Quarantine/release preserves provenance/scope and documents prior-execution limits and protected-file recovery.

No implemented increment is recorded for this requirement.

### P16-16

**Bound automated and mass-response blast radius. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Independent high-impact approvals and false-positive tests prevent fleet/DC lockout or unrestricted authority from one detection.

No implemented increment is recorded for this requirement.

### P16-17

**Integrate SIEM/SOAR without replaying response authority. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Duplicate/forged/replayed connector actions and stale external grants cannot bypass typed native response controls.

No implemented increment is recorded for this requirement.

</details>


## Phase 17

**Joint fleet qualification and endpoint service release — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/phases/phase-17.md>)

**Requirement status:** 0 ready for validation · 0 in progress · 0 blocked · 14 planned · 0 accepted

<details>
<summary>14 requirements, associated features and evidence</summary>

### P17-01

**Run the combined supported-endpoint and directory workload. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-02: OS-specific endpoint telemetry](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Reports identify real versus simulated endpoints/sessions, platform counts, traffic mix and exact build/rule versions; all individual contracts remain satisfied.

No implemented increment is recorded for this requirement.

### P17-02

**Qualify aggregate session/transfer/telemetry concurrency and latency. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** 50 desktop/100 terminal/250 transfer plus EDR steady/burst profiles report achieved rates and failures under the combined mix.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P17-03

**Preserve authentication/replication SLOs under endpoint pressure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-15: Availability-aware server and domain-controller maintenance](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Telemetry floods, relay misses, large transfers and reconnect storms cannot starve core directory services within approved resource isolation limits.

No implemented increment is recorded for this requirement.

### P17-04

**Recover from site/provider/control-plane loss. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** A 24-hour partition and provider loss retain declared degraded operation and truthful unknown/offline state.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P17-05

**Reconcile pending/partial operations after backup/upgrade recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Actual endpoint patch/file/isolation/session states are verified before replay; duplicate, cancelled and expired jobs cannot gain fresh authority.

No implemented increment is recorded for this requirement.

### P17-06

**Exercise cross-module privilege and compromise boundaries independently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-03: Separately approved unattended administration](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [FILE-01: Explicit server-originated uploads to one or many selected endpoints](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Support/upload/patch/EDR roles cannot exchange execution authority; external review includes enrollment, brokers, privileged executors, signing and recovery.

No implemented increment is recorded for this requirement.

### P17-07

**Rehearse emergency stop and fleet trust recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Stop dispatch, revoke/rotate identities and rules, inspect queues and reenroll through an independent rescue path; offline stop limits and irreversible actions are explicit.

No implemented increment is recorded for this requirement.

### P17-08

**Qualify cross-module privacy and consent. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-02: Attended support with visible user consent and an immediate disconnect action](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-04: Investigation and privacy-scoped evidence collection](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Notice/recording/consent/evidence retention agree across services; missing data cannot appear healthy/compliant.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P17-09

**Build immutable signed service and agent releases. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Artifact digests, SBOM/provenance and supported Linux/Windows package identities resolve to tested reviewed source.

**Implementation explanations:** W39: Refine phase requirements by independent acceptance obligations. See the [implementation journal](#implementation-journal).

### P17-10

**Publish final endpoint service readiness and ownership. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [FILE-01: Explicit server-originated uploads to one or many selected endpoints](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** All PATCH/REMOTE/FILE/EDR and selected security gates have current evidence, operator/support owners and known limits; no unrun acceptance is labeled production ready.

No implemented increment is recorded for this requirement.

### P17-11

**Ratify joint capacity, retention, cost and endpoint overhead. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Measured CPU/RAM/disk/IOPS/network, retention and endpoint budgets include every module and exact hardware/provider/cost assumptions.

No implemented increment is recorded for this requirement.

### P17-12

**Recover from clock/DNS/disk/issuer faults and reconnect storms. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Skew, DNS loss, full disks, expired issuers and 10k reconnect preserve authorization and bounded queues without duplicate authority.

No implemented increment is recorded for this requirement.

### P17-13

**Qualify accessible operator triage/patch/support workflows. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-02: Attended support with visible user consent and an immediate disconnect action](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>); [EDR-04: Investigation and privacy-scoped evidence collection](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Representative users complete cross-module journeys with correct permissions, uncertainty and safe recovery actions.

No implemented increment is recorded for this requirement.

### P17-14

**Qualify staged upgrades, version skew and release recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>); [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Actual mixed-version endpoints preserve job/session/telemetry semantics, pause unsafe rollouts and recover by defined paths.

No implemented increment is recorded for this requirement.

</details>

## Implementation journal

### W01 · Native Rust workspace and reproducible builds

**Implemented increment**

**Requirements:** P01-01, P00-04

**How it was done:** Pinned Rust 1.100.0 and locked Cargo graphs. The native runtime uses only the standard library, and its library/binary forbid unsafe code. Development and fuzz dependencies are separate from runtime code.

**Recorded validation:** Linux debug/release builds and Clippy passed locally and in PR \#7.

**Limits and remaining work:** This qualifies the lab toolchain only; crypto, storage and other runtime libraries remain undecided.

**Problems:** None recorded

**Source evidence:** [Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/Cargo.toml>) · [rust-toolchain.toml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/rust-toolchain.toml>) · [native/babel-ldap/src/lib.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/src/lib.rs>)

### W02 · Bounded BER / LDAP decoder

**Implemented increment**

**Requirements:** P01-01, P01-04

**How it was done:** Implemented checked definite BER lengths and integer/tag validation without recursion. Frames are capped at 16 KiB, with attribute count/name and DN bounds applied before accepting requests.

**Recorded validation:** Negative tests cover truncation, malformed lengths/IDs/tags, unsupported controls and attribute limits; generated inputs exercise bounded behavior.

**Limits and remaining work:** Only the declared LDAP subset is decoded; this is not full LDAP or AD conformance.

**Problems:** None recorded

**Source evidence:** [native/babel-ldap/src/ber.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/src/ber.rs>) · [native/babel-ldap/src/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/src/protocol.rs>) · [native/babel-ldap/tests/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/protocol.rs>)

### W03 · Read-only RootDSE queries

**Implemented increment**

**Requirements:** P01-04

**How it was done:** Implemented empty-DN base searches for objectClass presence. Explicit attribute projection, \*, \+, 1.1 and typesOnly select static public metadata. No AD capability OIDs or naming contexts are advertised.

**Recorded validation:** The independent ldap3 client reads supportedLDAPVersion and vendor metadata from the running binary.

**Limits and remaining work:** There are no users, groups, schema, directory state or general searches.

**Problems:** None recorded

**Source evidence:** [native/babel-ldap/src/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/src/protocol.rs>) · [native/babel-ldap/tests/smoke\_ldap.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/smoke_ldap.py>)

### W04 · Credential rejection and safe diagnostics

**Implemented increment**

**Requirements:** P01-05, P01-09

**How it was done:** Only anonymous access to public lab metadata succeeds. Credential/SASL binds fail. Parsed request/debug state retains no bind DN or password, and service diagnostics use static messages.

**Recorded validation:** Tests verify credential rejection, no credential echo in debug/response/stdout/stderr, and unsupported search failures.

**Limits and remaining work:** This is a safeguard, not authentication or password management. There is no TLS; never send real credentials.

**Problems:** None recorded

**Source evidence:** [native/babel-ldap/src/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/src/protocol.rs>) · [native/babel-ldap/tests/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/protocol.rs>) · [native/babel-ldap/tests/smoke\_ldap.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/smoke_ldap.py>)

### W05 · TCP framing and session budgets

**Implemented increment**

**Requirements:** P01-04, P01-09

**How it was done:** Implemented fragmented/coalesced frame reads and a loopback-only, single-active-connection listener. Every read/write uses the remaining five-second total deadline; sessions stop after 32 requests.

**Recorded validation:** Socket tests cover idle deadlines, framing, public-interface refusal and request limits. A malformed peer does not kill the process.

**Limits and remaining work:** The sequential listener is a lab design, not a production availability or throughput claim.

**Problems:** None recorded

**Source evidence:** [native/babel-ldap/src/server.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/src/server.rs>) · [native/babel-ldap/tests/transport.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/transport.rs>)

### W06 · Independent client and packaged-binary checks

**Implemented increment**

**Requirements:** P01-01, P01-04

**How it was done:** A separate Python ldap3 client launches the Rust process on an ephemeral loopback port. CI tests the release binary, then extracts the internal archive and tests that executable again.

**Recorded validation:** Positive RootDSE, credential denial, scope denial, malformed-peer recovery and extracted-binary checks passed.

**Limits and remaining work:** This is Linux client evidence, not Windows domain join or a deployment qualification.

**Problems:** None recorded

**Source evidence:** [native/babel-ldap/tests/smoke\_ldap.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/smoke_ldap.py>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>)

### W07 · Property tests and core coverage gate

**Implemented increment**

**Requirements:** P01-01

**How it was done:** Added native negative/integration/property tests and instrumented coverage. The actual process is exercised in addition to direct parser tests; the core gate requires at least 90% lines.

**Recorded validation:** 21 Rust integration/property tests passed. Local measured core line coverage exceeded 90%; Python tooling had 34 passing tests and 98% combined coverage.

**Limits and remaining work:** Core line coverage excludes test/CLI dispatch files. Percentages do not measure coverage of future AD functionality.

**Problems:** None recorded

**Source evidence:** [native/babel-ldap/tests/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/protocol.rs>) · [native/babel-ldap/tests/transport.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/native/babel-ldap/tests/transport.rs>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>)

### W08 · Sanitizer fuzz smoke

**Implemented increment**

**Requirements:** P01-01

**How it was done:** Added a separate locked libFuzzer target for decode/respond and frame reading, seeded only with synthetic wire data. The PR budget caps iterations, time, input size and RSS.

**Recorded validation:** 20,000 local address-sanitizer fuzz runs completed without a crash and without changing the lockfiles. Hosted PR \#7 fuzz also passed.

**Limits and remaining work:** A bounded fuzz run is not proof that no vulnerability exists. Longer schedules apply after the workflow reaches main.

**Problems:** I07

**Source evidence:** [fuzz/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/fuzz/Cargo.toml>) · [fuzz/fuzz\_targets/ldap\_frame.rs](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/fuzz/fuzz_targets/ldap_frame.rs>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>)

### W09 · Native dependency, license and SBOM checks

**Implemented increment**

**Requirements:** P01-01

**How it was done:** Cargo deny checks advisories, licenses, sources and dependency bans for core and fuzz graphs, including development/build dependencies. Checksum-pinned Syft catalogs Cargo.lock into a CycloneDX inventory.

**Recorded validation:** Both dependency audits passed; the generated source inventory was checked for proptest and libfuzzer-sys.

**Limits and remaining work:** The SBOM includes test/fuzz dependencies; it is not a runtime-only or complete OS/stdlib inventory. The project license is still undecided.

**Problems:** I06, I07, I08

**Source evidence:** [deny.toml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/deny.toml>) · [scripts/install\_ci\_tools.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/scripts/install_ci_tools.py>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>)

### W10 · Required native and repository CI gates

**Implemented increment**

**Requirements:** P01-01, P00-08

**How it was done:** Added native build/coverage, supply-chain and sanitizer-fuzz jobs behind a reusable fail-closed aggregate. New source scopes must be explicitly registered with checks. Actions/tools/dependencies are pinned or hash-locked.

**Recorded validation:** All 11 checks in the main-branch CI run passed at merge commit 3a69a6b, following PR \#7.

**Limits and remaining work:** Checks run, but GitHub merge protection is not enforced on the current private-repository plan. Passing CI does not establish AD compatibility or production readiness.

**Problems:** None recorded

**Source evidence:** [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/ci.yml>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>) · [scripts/check\_ci\_scope.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/scripts/check_ci_scope.py>)

### W11 · Complete phase specifications and traceability

**Design recorded**

**Requirements:** P00-08

**How it was done:** Created 18 phase designs with 180 phase requirements referencing all 130 global capability IDs. CI checks missing phases, unknown/duplicate IDs, empty acceptance and unassigned capabilities.

**Recorded validation:** The baseline validator and its negative regression cases pass.

**Limits and remaining work:** A consistent document is not passing product evidence; no phase has been accepted.

**Problems:** I09

**Source evidence:** [docs/phases/README.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/phases/README.md>) · [scripts/check\_design.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/scripts/check_design.py>) · [tests/test\_design.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/tests/test_design.py>)

### W12 · Threat model and open decision register

**Design recorded**

**Requirements:** P00-02, P00-03, P00-07, P00-09

**How it was done:** Documented component authority, identity/state/replication invariants, attack paths and capacity assumptions. Unresolved choices have owner roles and explicit blocking points.

**Recorded validation:** Reviewed for internal consistency and linked into phase designs.

**Limits and remaining work:** Named accountable owners, independent assessment, Windows lab, final storage/key choices and measured capacity remain outstanding.

**Problems:** I03, I04, I05

**Source evidence:** [docs/architecture.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/architecture.md>) · [docs/threat-model.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/threat-model.md>) · [docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/decisions.md>)

### W13 · Tested source and lab archive packaging

**Implemented increment**

**Requirements:** P00-10, P01-01

**How it was done:** Source packaging archives the tested commit with deterministic compression and checksum verification. The lab archive is checked after extraction; source release remains license-gated and creates drafts only.

**Recorded validation:** Committed-source exclusion, unsafe-tag/Git-failure tests and internal archive smoke checks passed.

**Limits and remaining work:** No production installer, signed native product release, directory upgrade or recovery deployment exists.

**Problems:** I03

**Source evidence:** [scripts/package\_source.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/scripts/package_source.py>) · [tests/test\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/tests/test_delivery.py>) · [.github/workflows/release.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/release.yml>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>)

### W14 · Phase dashboard and portable engineering report

**Implemented increment**

**Requirements:** P00-08, P00-10, P01-10

**How it was done:** Built a typed standalone dashboard from canonical phase/feature documents and reviewed progress facts, with phase/substep navigation, source evidence, issues and export.

**Recorded validation:** PR \#11 implementation includes model/security tests and desktop/mobile browser validation.

**Limits and remaining work:** This is engineering reporting, not the product directory administration UI. It does not implement P01-08 or accept a phase.

**Problems:** None recorded

**Source evidence:** [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/20e2ea9affb745c4fb7b281475e647eb087c8a8a/dashboard/src/main.ts>) · [scripts/build\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/20e2ea9affb745c4fb7b281475e647eb087c8a8a/scripts/build_dashboard.py>)

### W15 · Permanent private GitHub dashboard publication

**Implemented increment**

**Requirements:** P00-08, P00-10, P01-10

**How it was done:** Rendered the validated model into a README-only automation branch using structured GitHub API requests, privacy checks, idempotence and fast-forward publication.

**Recorded validation:** The report branch was created and read back; idempotent refresh and stale-main handling were exercised.

**Limits and remaining work:** The original publication only followed main and omitted open-PR proposals; that limitation is addressed by the current development PR.

**Problems:** I12

**Source evidence:** [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/64580b9881c12d18d5a6df028110b8ed40324424/scripts/render_dashboard.py>) · [scripts/publish\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/64580b9881c12d18d5a6df028110b8ed40324424/scripts/publish_dashboard.py>) · [.github/workflows/dashboard-publish.yml](<https://github.com/Ise-Tom/Babel/blob/64580b9881c12d18d5a6df028110b8ed40324424/.github/workflows/dashboard-publish.yml>)

### W16 · Compact interactive interface and verified static-hosting workflow

**Implemented increment**

**Requirements:** P00-10, P01-10

**How it was done:** Replaced duplicate navigation with compact phase cards and a phase picker; made work/problems expandable. Added a separate Pages workflow consuming only an immutable successful-main HTML artifact.

**Recorded validation:** PR \#15 CI passed its 22 browser checks and hosting-source validation tests. The later merged main audit failure is recorded independently.

**Limits and remaining work:** A configured workflow is not a live site. Pages is not enabled and no in-chat preview route was established.

**Problems:** None recorded

**Source evidence:** [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/17228586920c9783ef3708f24ec782e542f48140/dashboard/src/main.ts>) · [.github/workflows/dashboard-pages.yml](<https://github.com/Ise-Tom/Babel/blob/17228586920c9783ef3708f24ec782e542f48140/.github/workflows/dashboard-pages.yml>) · [scripts/check\_pages\_source.py](<https://github.com/Ise-Tom/Babel/blob/17228586920c9783ef3708f24ec782e542f48140/scripts/check_pages_source.py>)

### W17 · Bounded LDAP RootDSE filter discovery

**Implemented increment**

**Requirements:** P01-01, P01-04, P01-10

**How it was done:** Evaluates presence, objectClass descriptor/OID equality and AND/OR/NOT against the fixed public RootDSE. Uses True/False/Undefined semantics, visits every branch, enforces depth 8 / 64 nodes / 256 assertion bytes and never retains assertion bytes.

**Recorded validation:** Local validation: 28 Rust tests, generated boolean/identifier properties, independent ldap3 positive/empty/unsupported checks, 94.49% core line coverage \(filter module 100%\) and 20,000 sanitizer-fuzz iterations without a crash.

**Limits and remaining work:** Lab-only synthetic/public data. Other matching rules, general directory/schema queries, DNS, credentials, TLS and Windows domain interoperability remain unimplemented.

**Problems:** I11

**Source evidence:** [native/babel-ldap/src/filter.rs](<https://github.com/Ise-Tom/Babel/blob/dca754d98dd339962c761b934b701e59c6544544/native/babel-ldap/src/filter.rs>) · [native/babel-ldap/src/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/dca754d98dd339962c761b934b701e59c6544544/native/babel-ldap/src/protocol.rs>) · [native/babel-ldap/tests/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/dca754d98dd339962c761b934b701e59c6544544/native/babel-ldap/tests/protocol.rs>) · [native/babel-ldap/tests/smoke\_ldap.py](<https://github.com/Ise-Tom/Babel/blob/dca754d98dd339962c761b934b701e59c6544544/native/babel-ldap/tests/smoke_ldap.py>) · [docs/adr/0002-bounded-rootdse-filters.md](<https://github.com/Ise-Tom/Babel/blob/dca754d98dd339962c761b934b701e59c6544544/docs/adr/0002-bounded-rootdse-filters.md>)

### W18 · Open-PR-aware private progress reporting

**Implemented increment**

**Requirements:** P00-08, P00-10, P01-10

**How it was done:** Reads open PR descriptions/files/CI state and bounded progress JSON as data. Shows new/changed work and problem records separately from main totals, links PR-head evidence to affected substeps and preserves per-record historical revisions.

**Recorded validation:** Local validation: 74 Python tests with 98% combined tooling coverage. GitHub Markdown rendering verified that a hostile PR description remained inert and preserved all phase disclosures.

**Limits and remaining work:** Automatic PR refresh activates after merge. Fork structured facts are omitted; metadata has explicit listing limits. Private overlays never enter public HTML artifacts.

**Problems:** I12

**Source evidence:** [scripts/collect\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/scripts/collect_pr_progress.py>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/scripts/render_dashboard.py>) · [scripts/build\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/scripts/build_dashboard.py>) · [.github/workflows/dashboard-publish.yml](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/.github/workflows/dashboard-publish.yml>) · [tests/test\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/tests/test_pr_progress.py>)

### W19 · Remove unpatched vulnerable tooling dependency path

**Implemented increment**

**Requirements:** P00-10, P01-01

**How it was done:** Removed TypeScript-ESLint and its picomatch path. Retained supported ESLint 10 / TypeScript 6, strict compiler checks and explicit-any AST checks; runs DOM/eval rules on compiler-erased JavaScript without bundling, minification or execution.

**Recorded validation:** Locked clean install; npm audit reports zero vulnerabilities. Six build/lint tests include typed HTML sinks, eval, explicit-any declarations/casts and safe text rendering; strict typecheck and lint pass.

**Limits and remaining work:** This replaces recommended TypeScript style rules with documented compiler/security policies; it does not claim rule-for-rule style equivalence. PR \#16 is merged; main run 44153995669 passed all 12 jobs.

**Problems:** I13

**Source evidence:** [dashboard/package.json](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/package.json>) · [dashboard/package-lock.json](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/package-lock.json>) · [dashboard/lint.mjs](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/lint.mjs>) · [dashboard/eslint.config.mjs](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/eslint.config.mjs>) · [dashboard/tests/lint.test.mjs](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/tests/lint.test.mjs>)

### W20 · Scope-based phase sizes and explicit owner acceptance reviews

**Implemented increment**

**Requirements:** P00-10, P01-01, P01-10

**How it was done:** Removed the enforced ten-item sequential quota, retaining unique phase-owned IDs, nonempty requirements/evidence and feature traceability. Renamed broad dashboard substeps to requirements. Documented concrete owner review questions and separate requirement/phase acceptance. Existing scope and stable IDs are preserved. The project owner explicitly approved P01-01 and P01-10 for their stated current-component scopes; reviewer/date/evidence records are stored on both requirements.

**Recorded validation:** 78 Python tests pass with 98% tooling coverage. Strict types, lint, documentation checks, six build/security-lint tests and 24 desktop/mobile browser tests pass. Synthetic 3/13-item phases exercise rendering, counts and expand-all; model/design fixtures allow unequal counts and noncontiguous IDs. Hosted run 44156039039 did not start: GitHub reported failed recent payments or an insufficient spending limit; this is not a hosted test result.

**Limits and remaining work:** Two scoped requirements \(P01-01 and P01-10\) are accepted by explicit owner answers on 2026-11-17. These approval records are proposed in PR \#18 until merge; the main baseline count updates after merge. The current baseline retains 180 requirements, and full AD functionality and Phase 1 acceptance remain outstanding. Future components must satisfy their own safeguards.

**Problems:** I14

**Source evidence:** [scripts/check\_design.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/scripts/check_design.py>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/scripts/render_dashboard.py>) · [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/dashboard/src/main.ts>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/dashboard/tests/dashboard.spec.ts>) · [tests/test\_design.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/tests/test_design.py>) · [tests/test\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/tests/test_dashboard.py>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/docs/project-dashboard.md>)

### W21 · Support public repository dashboard publication and prepare visibility transition

**Implemented increment**

**Requirements:** P00-10, P01-01, P01-10

**How it was done:** Publisher and PR collector accept either explicit Babel visibility and reject other repository identities or unknown visibility. Retained default-branch-only publication, current-main revision checks, bounded data-only PR imports, metadata-only fork reporting and fast-forward README-only updates. Renamed the publishing workflow and corrected private-only documentation.

**Recorded validation:** 80 Python tests pass with 98% tooling coverage; strict types, lint, documentation links, actionlint and Zizmor pass. Tests cover public/private publication, unknown visibility, unrelated destinations and public fork metadata isolation. Gitleaks scanned fetched branch history with redacted output and found no leaks.

**Limits and remaining work:** Owner explicitly authorized public visibility, but GitHub rejected the integration’s private=false request with HTTP 403. The repository remains private and hosted CI is still blocked by billing. This PR must merge before default-branch publication supports public visibility. No license was invented and no paid capacity was purchased.

**Problems:** None recorded

**Source evidence:** [scripts/publish\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/scripts/publish_dashboard.py>) · [scripts/collect\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/scripts/collect_pr_progress.py>) · [tests/test\_dashboard\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/tests/test_dashboard_delivery.py>) · [tests/test\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/tests/test_pr_progress.py>) · [.github/workflows/dashboard-publish.yml](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/.github/workflows/dashboard-publish.yml>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/docs/project-dashboard.md>)

### W22 · Keep the tested compiler API instead of silently weakening security lint

**Implemented increment**

**Requirements:** P00-10, P01-01

**How it was done:** Reproduced TypeScript 7.0.2 passing typecheck but crashing lint because ScriptTarget.Latest is absent. Restored TypeScript 6.0.3 and its locked tooling graph, retained AST/DOM/eval checks and deferred automatic major compiler proposals until the security-policy API is explicitly migrated. PR \#17 now carries this correction instead of an unsupported upgrade.

**Recorded validation:** Strict compiler checks, ESLint, six build/security-lint fixtures, 24 desktop/mobile browser tests and npm audit all pass locally; audit reports zero vulnerabilities. Hosted full CI is rerun for the corrected PR head.

**Limits and remaining work:** TypeScript 7 is deliberately not adopted. Migration to its different unstable APIs needs a separate qualified change; a passing compiler CLI alone does not establish equivalent security lint.

**Problems:** I17

**Source evidence:** [dashboard/package.json](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/dashboard/package.json>) · [.github/dependabot.yml](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/.github/dependabot.yml>) · [dashboard/lint.mjs](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/dashboard/lint.mjs>) · [dashboard/tests/lint.test.mjs](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/dashboard/tests/lint.test.mjs>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/docs/github-security-settings.md>)

### W23 · Verify Pages archives and minimize privileged deployment operations

**Implemented increment**

**Requirements:** P00-10, P01-01, P01-10

**How it was done:** Read-only preflight validates exact main CI, immutable artifact ID, size and SHA-256 digest. A bounded verifier rejects extra/traversing/symlink files and weak browser policy, then packages only HTML/.nojekyll. The separate Pages/OIDC job has no checkout or project-code execution, attempts Actions-only/HTTPS configuration and rechecks main before deployment. Added no-referrer policy, blocked images, CODEOWNERS, a main ruleset template and verified owner settings. Registered only the named ruleset JSON with object/syntax validation in the CI scope guard; unrelated JSON manifests remain rejected. Shortened the focus summary and compacted phase cards after hosted viewport checks caught overflow.

**Recorded validation:** 87 Python tests pass with 98% tooling coverage. Negative archive/CSP tests, actual standalone archive verification, strict types/lint, actionlint, Zizmor, six build/lint fixtures and 24 browser tests pass locally. Live current site returned HTTP 200; Pages API confirms HTTPS and environment main-only deployment policy.

**Limits and remaining work:** These stronger deployment changes await PR merge and a successful main workflow run. The integration cannot mutate admin settings \(HTTP 403\). The job-token Pages configuration step must succeed and read back correctly; no success is claimed in advance. Required review, private vulnerability reporting and other owner settings remain explicit actions. GitHub Pages does not support arbitrary security response headers.

**Problems:** I19

**Source evidence:** [.github/workflows/dashboard-pages.yml](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/.github/workflows/dashboard-pages.yml>) · [.github/workflows/dashboard.yml](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/.github/workflows/dashboard.yml>) · [scripts/check\_pages\_source.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/scripts/check_pages_source.py>) · [scripts/verify\_pages\_artifact.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/scripts/verify_pages_artifact.py>) · [tests/test\_pages\_artifact.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/tests/test_pages_artifact.py>) · [tests/test\_pages\_deployment.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/tests/test_pages_deployment.py>) · [dashboard/build.mjs](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/dashboard/build.mjs>) · [dashboard/src/index.html](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/dashboard/src/index.html>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/docs/github-security-settings.md>) · [docs/github-main-ruleset.json](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/docs/github-main-ruleset.json>) · [.github/CODEOWNERS](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/.github/CODEOWNERS>) · [scripts/check\_ci\_scope.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/scripts/check_ci_scope.py>) · [tests/test\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/tests/test_delivery.py>) · [dashboard/src/style.css](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/dashboard/src/style.css>)

### W24 · Verify correct Pages settings without administration writes

**Implemented increment**

**Requirements:** P00-10, P01-01, P01-10

**How it was done:** Removed the unconditional Pages PUT that failed with HTTP 403 even when Source/HTTPS were correct. The job now reads and requires Actions-only publishing and HTTPS, with an actionable failure if either is wrong. Digest, archive, current-main and privileged-job boundaries are unchanged.

**Recorded validation:** Observed failure run 44179766192: read-only artifact verification succeeded and the administration PUT failed. Live API confirms workflow publishing/HTTPS; corrected read-only predicate returns true locally. Workflow lint and Zizmor pass; actual new deployment still requires merge.

**Limits and remaining work:** The patch does not grant repository administration access or claim a deployment already succeeded. Missing/insecure settings and failed reads still block publication.

**Problems:** None recorded

**Source evidence:** [.github/workflows/dashboard-pages.yml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/.github/workflows/dashboard-pages.yml>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/github-security-settings.md>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/project-dashboard.md>)

### W25 · Apply owner-selected Apache-2.0 license and DCO contribution terms

**Implemented increment**

**Requirements:** P00-06, P05-02

**How it was done:** Copied the full Apache-2.0 and DCO 1.1 texts from their official publishers; added project notices, incoming contribution policy and consistent Cargo/npm SPDX metadata. Disabled the unpublished-package license-audit exemption. No contributor signature is fabricated.

**Recorded validation:** Core and fuzz Cargo dependency/license/source/advisory audits pass with private-package ignore=false; Cargo metadata resolves the project license. TypeScript lint/build/security fixtures and npm audit pass with zero vulnerabilities. The owner’s explicit choice is recorded in D-01.

**Limits and remaining work:** DCO sign-off review is a maintainer responsibility, not an invented automated check. Third-party/specification/reference-fixture rights and production qualification remain open; publish=false remains in Rust manifests.

**Problems:** I03

**Source evidence:** [LICENSE](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/LICENSE>) · [DCO](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/DCO>) · [NOTICE](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/NOTICE>) · [CONTRIBUTING.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/CONTRIBUTING.md>) · [Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/Cargo.toml>) · [native/babel-ldap/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/native/babel-ldap/Cargo.toml>) · [fuzz/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/fuzz/Cargo.toml>) · [dashboard/package.json](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/dashboard/package.json>) · [deny.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/deny.toml>) · [docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/decisions.md>)

### W26 · Prepare an isolated Windows reference lab definition without provisioning

**Implemented increment**

**Requirements:** P00-05, P01-06

**How it was done:** Defined two isolated .test networks and six scoped reference/Babel/client/probe machines with bounded resources, no bridge/routes/external DNS/downloads, fresh credentials and blank image metadata. Added a stdlib-only validator and same-PR configuration CI, with denied-safety/topology/resource/image tests and a provisioning/teardown/evidence contract.

**Recorded validation:** 93 Python tests pass with 98% tooling coverage; the lab validator has 100% measured line/branch coverage. The committed definition validates; require-images rejects the missing image placeholders. No KVM device or qualified Windows host exists in this worker.

**Limits and remaining work:** This is configuration preparation only. No images downloaded, terms accepted, VMs created, infrastructure purchased or Windows operations tested. I04 remains open; exact client builds and two clean real lab runs are required.

**Problems:** I04

**Source evidence:** [lab/windows-reference.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/lab/windows-reference.toml>) · [scripts/check\_lab\_definition.py](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/scripts/check_lab_definition.py>) · [tests/test\_lab\_definition.py](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/tests/test_lab_definition.py>) · [docs/windows-reference-lab.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/windows-reference-lab.md>) · [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/.github/workflows/ci.yml>) · [scripts/check\_ci\_scope.py](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/scripts/check_ci_scope.py>)

### W27 · Record PostgreSQL selection and a reviewable native state contract

**Design recorded**

**Requirements:** P00-02, P00-04, P01-02, P01-03

**How it was done:** Recorded the owner’s explicit PostgreSQL choice. ADR 0003 assigns identity/schema/ACL/replication semantics to Babel, independent local stores per DC, a proposed atomic journal/audit/idempotency transaction and ordered writer allocation. It explains why ordinary SQL sequence allocation can lose changes below a replicated watermark and specifies kill/retry/recovery qualification.

**Recorded validation:** Design is linked to D-04/D-05/D-06 and existing Phase 1/3 requirements. Documentation links and phase/model validation pass. Backend-family selection is approved; schema/driver/runtime and durability claims are not marked tested.

**Limits and remaining work:** No database is installed or implemented by this ADR. Key custody, crash/index/locking evidence, AD conflict/RID/FSMO and GPO/SYSVOL contracts remain separate gates. A future backend migration still needs data/recovery/conformance qualification.

**Problems:** I05

**Source evidence:** [docs/adr/0003-postgresql-directory-state.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/adr/0003-postgresql-directory-state.md>) · [docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/decisions.md>) · [docs/architecture.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/architecture.md>) · [docs/native-core-plan.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/native-core-plan.md>)

### W28 · Run real PostgreSQL synthetic transaction and process-crash experiments

**Implemented increment**

**Requirements:** P00-02, P01-02, P01-03

**How it was done:** Added a digest-pinned official PostgreSQL 18 dependency, a bounded synthetic SQL schema and a stdlib Docker/psql controller. State, local journal, audit intent and idempotency commit together under a transactional writer allocator; synthetic UUID/SID identity is immutable. Tests use actual concurrent sessions and SIGKILL/restart. Containers have no network, ports, host binds or privileged mode, with read-only rootfs and scoped cleanup. Added a required runtime CI/coverage job, strict types/lint/security checks and test-image inventory. Process launch/timeout failures are also converted to static diagnostics so command arguments and captured output are not exported.

**Recorded validation:** 22 component tests pass against PostgreSQL/psql 18.7; controller branch-inclusive coverage is 93%. Real cases cover collisions/injection/denial, rollback, ordered concurrent commit/rollback, kill before commit, committed-result recovery and idempotent retry after a discarded reply. Actual container isolation and cleanup are asserted. A CycloneDX test-image inventory was generated locally; 97 repository tests pass with 98% coverage.

**Limits and remaining work:** Proposed for review; hosted verification must pass on the PR head before merge. This is an isolated SQL experiment, not native directory storage, authentication/Windows ACL, real SID allocation, backup/upgrade, physical power-loss proof, credential protection, AD replication or capacity acceptance. The future Rust driver and production packaging remain unselected/unqualified.

**Problems:** I05, I21

**Source evidence:** [experiments/postgres\_store/Dockerfile](<https://github.com/Ise-Tom/Babel/blob/4d00412af3e1528758c605b16c1e5dd2c5281cfd/experiments/postgres_store/Dockerfile>) · [experiments/postgres\_store/experiment.py](<https://github.com/Ise-Tom/Babel/blob/4d00412af3e1528758c605b16c1e5dd2c5281cfd/experiments/postgres_store/experiment.py>) · [experiments/postgres\_store/schema.sql](<https://github.com/Ise-Tom/Babel/blob/4d00412af3e1528758c605b16c1e5dd2c5281cfd/experiments/postgres_store/schema.sql>) · [experiments/postgres\_store/test\_store.py](<https://github.com/Ise-Tom/Babel/blob/4d00412af3e1528758c605b16c1e5dd2c5281cfd/experiments/postgres_store/test_store.py>) · [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/4d00412af3e1528758c605b16c1e5dd2c5281cfd/.github/workflows/ci.yml>) · [docs/adr/0004-synthetic-postgresql-state-experiment.md](<https://github.com/Ise-Tom/Babel/blob/4d00412af3e1528758c605b16c1e5dd2c5281cfd/docs/adr/0004-synthetic-postgresql-state-experiment.md>)

### W29 · Verify owner-applied repository protections and security settings

**Design recorded**

**Requirements:** P00-10, P01-01, P05-09, P10-09

**How it was done:** Read the active main ruleset and effective branch rules, Pages mode/environment and private-reporting status. Recorded the owner’s explicit confirmation of the three Actions defaults separately from API-verifiable controls. No repository setting or remote branch was changed.

**Recorded validation:** The owner-adjusted solo ruleset and effective main rules are API-verified: zero approvals, code-owner/last-push/unattributed-change approval disabled, PR and up-to-date CI required, resolved conversations, no bypass and no force-push/deletion. Pages/private reporting observations remain valid. Actions defaults remain owner-confirmed because their API returns HTTP 403.

**Limits and remaining work:** Team approval is not sustainable for the sole maintainer and is being replaced for development, without claiming independent review. Source-release remains absent \(I22\). Main acceptance totals change after merge, not from PR proposals.

**Problems:** None recorded

**Source evidence:** [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/docs/github-security-settings.md>) · [docs/github-main-ruleset.json](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/docs/github-main-ruleset.json>) · [.github/CODEOWNERS](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/.github/CODEOWNERS>)

### W30 · Validate existing source-release protections before draft source prereleases

**Implemented increment**

**Requirements:** P00-10, P05-09, P10-09

**How it was done:** Read-only preflight precedes the contents/OIDC job. Explicit solo mode requires no reviewer gate, disabled admin bypass and only v\* tag deployments. Optional team mode additionally requires eligible independent reviewers and self-review prevention. Missing/inaccessible settings fail before automatic environment creation.

**Recorded validation:** Seven release-policy regression tests pass, including solo/team profiles, protected tag scope, denied access and preservation of mandatory PR/CI boundaries in the ruleset template. The 100-test repository suite passes at 98% coverage; this helper has 100% coverage. Workflow syntax/security checks pass. No hosted release was run.

**Limits and remaining work:** The source-release environment is still absent. The workflow change is proposed for review and has not been executed as hosted release code. It assumes the reviewed release workflow and does not replace owner-controlled release-tag creation or platform protection.

**Problems:** None recorded

**Source evidence:** [scripts/check\_release\_environment.py](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/scripts/check_release_environment.py>) · [tests/test\_release\_environment.py](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/tests/test_release_environment.py>) · [.github/workflows/release.yml](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/.github/workflows/release.yml>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/docs/github-security-settings.md>)

### W31 · Adapt development governance to the sole maintainer without bypassing CI

**Implemented increment**

**Requirements:** P00-10, P01-01, P05-09, P10-09

**How it was done:** Changed the main ruleset template to zero approvals with code-owner, last-push and unattributed-change approval disabled. Kept PRs, up-to-date GitHub Actions CI gate, resolved conversations and no force-push/deletion/bypass. Aligned source-only prerelease preflight, owner guidance and contribution policy; CODEOWNERS still records ownership.

**Recorded validation:** 100 repository tests pass with 98% coverage, including solo/team release modes and main ruleset safeguards. Ruff, strict mypy, actionlint, Zizmor and local Markdown links pass. After the integration write was denied HTTP 403, owner UI changes were verified through the full ruleset and effective main rules: all solo settings match and PR/CI/no-bypass protections remain.

**Limits and remaining work:** Implementation is proposed in PR \#21. Live owner-applied solo rules are verified and I24 is resolved. This is owner review plus CI, not independent review; future production security qualification remains required. Source-release is still absent; no release/tag/merge/deployment was triggered.

**Problems:** None recorded

**Source evidence:** [docs/github-main-ruleset.json](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/docs/github-main-ruleset.json>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/docs/github-security-settings.md>) · [scripts/check\_release\_environment.py](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/scripts/check_release_environment.py>) · [tests/test\_release\_environment.py](<https://github.com/Ise-Tom/Babel/blob/911ef20b425782e9cbd5d7797ecfa41fbac6578a/tests/test_release_environment.py>)

### W32 · Inventory the initial 2016 AD profile and Windows/Linux/macOS clients

**Design recorded**

**Requirements:** P00-01, P00-05, P00-06

**How it was done:** Added a versioned matrix of 30 operation families, positive/negative expectations, requirement/protocol references, profile/comparison targets and owner. Preserved Linux hosting and made Ubuntu/Debian/macOS identity clients explicit; Windows GPO and later cross-platform agents remain separate.

**Recorded validation:** Matrix/evidence structure validation passes for 60 explicitly unrun scenarios. Scope regression tests retain the owner-selected 2016 level and Windows/Linux/macOS profiles; canonical AD-01–AD-10, PLAT-01–PLAT-03, IAM/OPS/UX references are covered.

**Limits and remaining work:** Exact patched builds, wire-operation/control/error decomposition, specification revisions and rights remain pending. No real-client compatibility or full requirement acceptance is claimed.

**Problems:** I04, I25, I28

**Source evidence:** [lab/compatibility.json](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/lab/compatibility.json>) · [docs/phase-00-progress.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-progress.md>) · [docs/windows-reference-lab.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/windows-reference-lab.md>)

### W33 · Enforce versioned conformance evidence integrity in CI

**Implemented increment**

**Requirements:** P00-01, P00-08, P00-10

**How it was done:** Implemented a stdlib validator with exact matrix digest binding, unique complete positive/negative cases, known references and distinct passed/failed/skipped/unsupported/unrun outcomes. Executed passes need exact profiles/builds/source/tool/time metadata, retained file hashes and every declared comparison. A separate readiness mode blocks unqualified or unaccepted evidence.

**Recorded validation:** 118 repository tests pass at 99% combined tooling coverage; all statements/branches in the new validator are covered. Tests reject stale digests, fabricated/partial passes, scope loss, wrong results, changed assertions, unsafe artifact paths/symlinks, missing review and skipped/unrun qualification. Current readiness fails as expected; no Windows job was fabricated. The owner explicitly accepted the current schema/tooling scope on 18 November 2026; this does not accept the unrun product scenarios.

**Limits and remaining work:** Schema validation cannot authenticate evidence, prove redaction, validate assertion semantics or replace trusted execution/human review. All current 60 product scenarios remain unrun; temporary synthetic unit fixtures are not product evidence.

**Problems:** I04, I25, I28

**Source evidence:** [scripts/check\_conformance.py](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/scripts/check_conformance.py>) · [tests/test\_conformance.py](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/tests/test_conformance.py>) · [lab/conformance-evidence.json](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/lab/conformance-evidence.json>) · [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/.github/workflows/ci.yml>)

### W34 · Specify stable state and worked replication/recovery invariants

**Design recorded**

**Requirements:** P00-02, P00-03, P00-10

**How it was done:** ADR 0005 defines immutable identities, schema matching boundaries, ordered access checks, local authorization/write serialization and durable acknowledgement. Worked cases cover rename/collision/revocation/groups/idempotency, GPO partial publication, attribute/link conflicts, cursor crashes, stale restore, tombstones and RID authority.

**Recorded validation:** Canonical traceability/document links validate. The ADR identifies unresolved exact MS-ADTS/MS-DRSR comparison/encoding/restore rules rather than presenting a custom replication algorithm as qualified.

**Limits and remaining work:** No native identity/ACL/replication implementation or Windows reference model evidence is introduced. The existing local SQL experiment does not establish AD metadata, replication or credential durability.

**Problems:** I05, I28

**Source evidence:** [docs/adr/0005-directory-and-replication-invariants.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/adr/0005-directory-and-replication-invariants.md>) · [docs/adr/0003-postgresql-directory-state.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/adr/0003-postgresql-directory-state.md>)

### W35 · Map security ownership and dependency/rights qualification gaps

**Design recorded**

**Requirements:** P00-04, P00-06, P00-07

**How it was done:** Named Ise-Tom as the current accountable development owner for Tier 0 and future module boundaries, mapped threats to required misuse evidence, and documented a private synthetic intake/incident exercise procedure. Separated qualified lab inputs from unqualified production TLS/Kerberos/storage/transports and versioned specification-rights reviews.

**Recorded validation:** Threat links and canonical documentation checks pass. Existing project license/DCO and scoped dependency jobs remain intact; no invented contact, private report submission, legal clearance or production library selection is recorded.

**Limits and remaining work:** Backup response coverage, intake/incident exercises and independent production assessment remain open. Solo diff/CI review does not provide independent security review or separation of duty.

**Problems:** I03, I26, I27, I28

**Source evidence:** [docs/phase-00-security-and-dependencies.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-security-and-dependencies.md>) · [docs/threat-model.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/threat-model.md>) · [docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/decisions.md>)

### W36 · Define a reproducible target-scale mixed workload and fault method

**Design recorded**

**Requirements:** P00-09

**How it was done:** Specified seeded synthetic 10k-user/10k-computer/2k-group distributions, six-DC/three-site topology, mixed successful/denied authentication/read/write traffic, open-loop overload accounting, cold/warm/burst/soak phases, WAN/DC/site/clock/storage/key/audit faults, per-site histograms and hardware/cost manifests.

**Recorded validation:** Cross-checked rates, topology, network/failure and provisional SLO values against requirements.md; documentation integrity passes. No benchmark output or infrastructure cost was invented. The owner explicitly approved the workload/measurement method on 18 November 2026, without accepting capacity or SLO results.

**Limits and remaining work:** The generator/load runner and actual hosts are not implemented or allocated. The engineering method is owner-approved; measured SLO ratification remains outstanding. SQL microbenchmarks or simulated login cannot replace native protocol/client load.

**Problems:** I04

**Source evidence:** [docs/phase-00-workload.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-workload.md>) · [docs/requirements.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/requirements.md>)

### W37 · Make Phase 0 recovery, scope and acceptance governance concrete

**Design recorded**

**Requirements:** P00-08, P00-10

**How it was done:** Documented owner-reviewed scope changes, evidence invalidation, expiring exact-scope exceptions and worked interrupted schema/key/restore/functional-level/storage/GPO transitions. Kept sole-maintainer PR/CI workflow while retaining independent production qualification and explicit acceptance.

**Recorded validation:** Design, documentation and dashboard validation pass. No scope exception can remove the first-production AD/IAM/OPS/UX or baseline security contract. The problem list now excludes ten GitHub setup records while retaining stable development problem IDs and source history.

**Limits and remaining work:** These are reviewable transition contracts; no runtime migration, clean-domain restore or whole Phase 0 acceptance is demonstrated. GitHub setup history remains in operational documentation/Git history rather than the problem list.

**Problems:** I05, I25

**Source evidence:** [docs/phase-00-governance.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-governance.md>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/project-dashboard.md>) · [docs/phase-00-progress.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-progress.md>)

### W38 · Separate actual phase execution from related preparation

**Implemented increment**

**Requirements:** P00-08, P00-10

**How it was done:** Removed work-link promotion of planned phases. Explicit requirement activity/acceptance determines phase status; phase cards/report label related records and planned rows explain preparatory links. Shared work remains traceable without implying execution.

**Recorded validation:** 119 repository tests pass at 99% tooling coverage. All 26 desktop/mobile browser tests and six build/security-lint tests pass, including real-model Phases 5/10 planned, exactly two active phases, and explicit activity fixtures. Strict types/lint, Bandit, actionlint/Zizmor and design/doc/evidence checks pass.

**Limits and remaining work:** No product functionality, phase acceptance or later-phase execution is introduced. Four owner-accepted requirement scopes remain exactly unchanged. Public dashboards reflect this code after merge and trusted deployment.

**Problems:** I29

**Source evidence:** [scripts/build\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/scripts/build_dashboard.py>) · [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/dashboard/src/main.ts>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/scripts/render_dashboard.py>) · [tests/test\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/tests/test_dashboard.py>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/dashboard/tests/dashboard.spec.ts>)

### W39 · Refine phase requirements by independent acceptance obligations

**Design recorded**

**Requirements:** P00-01, P00-04, P00-06, P00-07, P01-02, P01-03, P01-04, P01-05, P01-08, P01-09, P02-01, P02-02, P02-03, P02-04, P02-05, P02-06, P02-07, P02-08, P02-09, P03-03, P03-04, P03-07, P03-08, P03-09, P03-10, P04-01, P04-04, P04-07, P05-03, P05-08, P06-02, P06-08, P06-09, P07-01, P07-04, P07-06, P07-07, P07-09, P08-01, P08-02, P08-03, P08-04, P08-05, P08-08, P08-10, P09-02, P09-05, P09-07, P09-09, P10-01, P10-03, P10-06, P10-07, P11-02, P11-03, P11-04, P11-08, P11-09, P12-03, P12-04, P12-05, P12-06, P12-07, P12-09, P13-02, P13-06, P13-09, P14-01, P14-05, P14-06, P14-08, P14-10, P15-03, P15-07, P15-09, P16-01, P16-02, P16-04, P16-05, P16-06, P16-07, P16-10, P17-02, P17-04, P17-08, P17-09

**How it was done:** Reviewed composite requirements across all 18 phases. Original IDs retain their primary responsibility; 94 additional stable IDs carry separately verifiable obligations, with parent-to-split trace lists in each canonical document. Preserved original capability coverage and all accepted scopes. Updated feature associations, roadmap references and quota-based tests.

**Recorded validation:** Design/model validation covers 274 current requirements and all 130 existing global capabilities. Actual phase sizes range from 12 to 24; examples are 17 Phase 0, 16 Phase 1, 24 AD interoperability and 12 first production release. Unequal-size/export/browser regressions pass.

**Limits and remaining work:** This is requirement design/refinement, not new product work or 94 new features. Counts are not effort estimates. New split rows remain planned until explicitly assigned activity/evidence; legacy work links are retained for historical traceability. No later phase is started and no new acceptance is inferred.

**Problems:** I14

**Source evidence:** [docs/phases/README.md](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/docs/phases/README.md>) · [docs/phases/phase-00.md](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/docs/phases/phase-00.md>) · [docs/phases/phase-02.md](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/docs/phases/phase-02.md>) · [docs/phases/phase-05.md](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/docs/phases/phase-05.md>) · [dashboard/associations.json](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/dashboard/associations.json>)

### W40 · Generate and independently audit reproducible target-scale synthetic data

**Implemented increment**

**Requirements:** P00-09

**How it was done:** Added stdlib Python tooling with fixed namespace/hash-based sampling, exact site/payload/direct-membership distributions, synthetic GUID/SID/DN and ACL/GPO labels, disjoint depth-1/3/8 group chains and separate cycle/over-budget inputs. An independent bounded auditor checks artifact hashes, relationships/counts, reference consistency, duplicate identities/edges, graph shape and explicit unmeasured fields. Required CI generates/audits the full profile and retains only manifest/summary.

**Recorded validation:** 136 local repository tests pass at 99% tooling coverage; both new modules have 100% statement/branch coverage. Full profile generated and audited twice at source 521dfe82f6d32db979185084b2a6e0a8dac2e02a; all four files are byte-identical. Both audits report 22,150 objects, 254,000 direct plus 12 nested edges and max effective group count 111. Local manifest SHA-256: 9409b80dd69a5d762d52c8c01c324802990c3314a7e8bc3a60ae8bef556a901f. Objects/memberships are 35,440,934/32,005,476 bytes. Strict types/lint, Bandit, workflow and canonical checks pass.

**Limits and remaining work:** Synthetic logical fixture schema only: no credentials, domain/schema import, real ACL/GPO/SYSVOL behavior, AD RID allocator, endpoint provisioning, client denial tests or native load. Token bytes, index/storage expansion, throughput and latency remain null/unmeasured. Negative graph shape is verified, not actual server rejection. Existing method acceptance is not expanded; all 60 conformance scenarios remain unrun.

**Problems:** I30

**Source evidence:** [scripts/generate\_workload.py](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/scripts/generate_workload.py>) · [scripts/check\_workload.py](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/scripts/check_workload.py>) · [tests/test\_workload.py](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/tests/test_workload.py>) · [docs/synthetic-workload.md](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/docs/synthetic-workload.md>) · [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/.github/workflows/ci.yml>)

### W41 · Track all global capabilities with explicit implementation scope and evidence

**Implemented increment**

**Requirements:** P00-08, P00-10

**How it was done:** Added a sparse versioned claim register over all 130 canonical capabilities, planned defaults, strict references, explicit stage/status, implemented and missing behavior and separate full-capability acceptance. The interactive tab supports search/status filters, lazy details, direct links, mobile navigation, work/source/blocker links and related preparation. The GitHub report renders the same claims. Documentation requires same-PR updates without inferring delivery from related work or accepted requirement subsets. Implemented claims cannot retain declared gaps; implementation and acceptance have separate labels. The focus summary stays compact so all 18 phase cards remain visible in the tested desktop viewport.

**Recorded validation:** 150 repository tests pass at 99% combined statement/branch coverage; the tracker validator has 100%. All 30 desktop/mobile browser tests and six build/security tests pass, including capability navigation, missing scope, immutable evidence, filters/deep links, no horizontal overflow and WCAG 2.2 AA-tagged automated checks. Strict TypeScript/lint and canonical/docs validation pass.

**Limits and remaining work:** This is project development tooling, not domain administration UI/API or product conformance. Claims still require human review and maintenance. No full capability acceptance, additional requirement acceptance or later phase activity is inferred. Pages receives the change only after merge and successful trusted deployment; open-PR increments appear separately in the GitHub report.

**Problems:** I31

**Source evidence:** [dashboard/capabilities.json](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/dashboard/capabilities.json>) · [scripts/capability\_tracker.py](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/scripts/capability_tracker.py>) · [tests/test\_capabilities.py](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/tests/test_capabilities.py>) · [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/dashboard/src/main.ts>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/dashboard/tests/dashboard.spec.ts>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/scripts/render_dashboard.py>) · [docs/capability-tracker.md](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/docs/capability-tracker.md>)

### W42 · Qualify a bounded Rustls/ring TLS candidate with independent enforcement tests

**Implemented increment**

**Requirements:** P00-04, P00-13

**How it was done:** Implemented a standalone loopback, one-session Rustls 0.23.46/ring 0.17.14 experiment with explicit client CA, mandatory client certificates, server verification by an independent OpenSSL client, TLS 1.2/1.3 AES-GCM/ECDHE suites, no early data/tickets/cache, bounded DER/wire/application buffers and monotonic deadlines. Added certificate/identity/time/purpose failures, tampering, scoped exporter prerequisites, property tests, a TLS-record sanitizer fuzzer and separate library coverage gate. ADR 0006 compares provider alternatives, actual license terms and unqualified production obligations.

**Recorded validation:** Seven Rust TLS tests pass, including 64-case generated-record checks; the existing 28 LDAP tests pass. Nineteen OpenSSL methods pass against release, instrumented and extracted binaries using OpenSSL 3.5.7. TLS library line coverage is 93.23%; combined native coverage is 94.21%. TLS and LDAP sanitizer targets each complete 20,000 local iterations with no crash. Formatting/Clippy, both locked graph advisory/license/source audits, Bandit and workflow analysis pass.

**Limits and remaining work:** Qualification experiment only: no LDAP/StartTLS/SASL/EPA integration, AD authentication, production key custody/revocation/rotation/HSM/provider-loss or load qualification. Generic exporter agreement is not Windows channel-binding conformance. No Windows/macOS host was used; all 60 conformance cases remain unrun. Ring uses native C/assembly; this is not all-memory-safe or FIPS validation. No owner acceptance is inferred.

**Problems:** I26

**Source evidence:** [docs/adr/0006-tls-qualification-lab.md](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/docs/adr/0006-tls-qualification-lab.md>) · [native/babel-tls-lab/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/native/babel-tls-lab/Cargo.toml>) · [native/babel-tls-lab/src/lib.rs](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/native/babel-tls-lab/src/lib.rs>) · [native/babel-tls-lab/tests/handshake.rs](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/native/babel-tls-lab/tests/handshake.rs>) · [native/babel-tls-lab/tests/interop\_tls.py](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/native/babel-tls-lab/tests/interop_tls.py>) · [fuzz/fuzz\_targets/tls\_record.rs](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/fuzz/fuzz_targets/tls_record.rs>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/.github/workflows/native.yml>)

### W43 · Retain and verify actual license notices in experimental native archives

**Implemented increment**

**Requirements:** P00-06

**How it was done:** Added a fail-closed collector for actual nested LICENSE/COPYING/COPYRIGHT/NOTICE and declared license files in the selected normal/runtime Cargo dependency closure, plus project LICENSE/NOTICE/DCO and Rust library copyright/referenced terms. Preserved versions/SPDX and per-file SHA-256/size in a manifest. Native CI packages both binaries with notices, extracts/verifies the archive and reruns independent LDAP and TLS probes; full development/fuzz graph license and advisory checks remain mandatory.

**Recorded validation:** Eight notice tests pass, covering nested and explicit terms, normal-vs-dev closure, graph cycles/unknown roots, missing/linked/empty terms, traversal and same-size digest tampering. Actual local archive contains notices for 11 selected runtime crates and 40 retained files totaling 1,738,841 bytes; post-extraction notice verification and both protocol probes pass. Root tooling coverage remains 99%.

**Limits and remaining work:** Experimental Linux x86\_64 lab archive only. Rust reference notices may list components not linked; this is not complete binary-link analysis, legal clearance, protocol/fixture rights or product-distribution acceptance. Notice verification checks retained bytes, not legal interpretation or provenance by itself.

**Problems:** I32

**Source evidence:** [scripts/collect\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/scripts/collect_native_notices.py>) · [tests/test\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/tests/test_native_notices.py>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/.github/workflows/native.yml>) · [deny.toml](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/deny.toml>) · [docs/adr/0006-tls-qualification-lab.md](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/docs/adr/0006-tls-qualification-lab.md>)

### W44 · Qualify an async PostgreSQL driver and prevent false transaction acknowledgments

**Implemented increment**

**Requirements:** P00-15, P00-06

**How it was done:** Added an isolated tokio-postgres 0.7.18/Tokio 1.54.1 candidate helper and explicit real-database qualification target. The existing owned container can share exactly one socket-only child below a private 0700 directory while TCP stays disabled. The harness observes isolation, requires SCRAM activation and every declared case, redacts synthetic credentials and verifies cleanup. Helpers bind parameters, classify failures, verify durability settings, enforce deadlines/discard, track failed transactions and conservatively report unknown commits without retry. Required CI adds an independent driver library coverage gate and actual selected dependency notices; reviewed Unicode-3.0 terms stay enforced.

**Recorded validation:** 16 real Rust/PostgreSQL 18.7 cases pass with none ignored, including the raw-driver aborted-COMMIT comparison, coupled commit/explicit/drop rollback, deferred errors, SCRAM/privilege denial, typed text/null/binary parameters, serialization/lock contention, server/client/transaction deadlines, explicit cancellation and connection loss. Local driver line coverage is 92.12% \(152/165\). All 156 repository tests pass at 99% tooling coverage; 25 SQL/controller tests pass at 94% controller coverage. All-feature Clippy, strict types/lint, Bandit, workflow checks and both locked graph audits pass. The actual driver notice bundle verifies 62 selected normal-closure packages and 144 files \(2,254,392 bytes\).

**Limits and remaining work:** Qualification helper only, separate from LDAP and a native storage adapter. No directory identities/schema/ACLs, production auth-policy/pooling/key custody, row/byte bounds, measured capacity or real-client conformance. Upstream still supports trust/cleartext/MD5 authentication; only owned-lab SCRAM is qualified. Exact after-durable-commit wire response loss, durable retry identities, caller-dropped-future safety and host/disk/backup/upgrade need further work. Four accepted scopes remain unchanged and all 60 conformance scenarios remain unrun. Hosted checks must pass on the PR head before merge.

**Problems:** I05, I26, I33

**Source evidence:** [native/babel-store-driver-lab/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/native/babel-store-driver-lab/Cargo.toml>) · [native/babel-store-driver-lab/src/lib.rs](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/native/babel-store-driver-lab/src/lib.rs>) · [native/babel-store-driver-lab/tests/database.rs](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/native/babel-store-driver-lab/tests/database.rs>) · [native/babel-store-driver-lab/tests/fixture.sql](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/native/babel-store-driver-lab/tests/fixture.sql>) · [scripts/qualify\_store\_driver.py](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/scripts/qualify_store_driver.py>) · [tests/test\_store\_driver\_harness.py](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/tests/test_store_driver_harness.py>) · [experiments/postgres\_store/experiment.py](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/experiments/postgres_store/experiment.py>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/.github/workflows/native.yml>) · [docs/adr/0007-postgresql-driver-qualification.md](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/docs/adr/0007-postgresql-driver-qualification.md>) · [deny.toml](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/deny.toml>)

### W45 · Make phase activity and recent work visible separately from acceptance

**Implemented increment**

**Requirements:** P00-08, P00-10

**How it was done:** Reproduced the live main dashboard after PR \#26: current build f42815d included W44 and 35 Phase 0 records, but its bar showed only 2/17 accepted and its header showed the older baseline. Replaced the acceptance-only bar with labeled explicit-status segments; cards show active/planned counts and related records. Active phase pages show status totals and the newest three source-backed work records above collapsed requirements. The header now uses the artifact build revision and the footer labels the separate recorded CI baseline. The GitHub report shows the same counts and recent records outside disclosures.

**Recorded validation:** All 32 desktop/mobile browser checks and six build/security tests pass. New regressions verify activity and acceptance remain separate, current build labeling, actual recent work/source evidence, and no promotion of future planned phases. All 18 phase cards still fit the tested desktop viewport; mobile overflow and automated WCAG 2.2 AA-tagged checks pass. All 157 repository tests pass at 99% branch-inclusive tooling coverage; the GitHub report has a regression for visible status/recent evidence without phase acceptance. Strict types/lint, Bandit and workflow analysis pass.

**Limits and remaining work:** This is dashboard visibility and traceability work, not new native AD behavior or acceptance. Requirement counts and status segments are not effort/completion percentages. Work linked to a planned phase remains preparation. Pages receives the UI change after merge and successful trusted deployment; proposed work is visible separately in the GitHub report. Four accepted scopes remain unchanged and all 60 conformance scenarios stay unrun.

**Problems:** I34

**Source evidence:** [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/dashboard/src/main.ts>) · [dashboard/src/style.css](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/dashboard/src/style.css>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/dashboard/tests/dashboard.spec.ts>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/scripts/render_dashboard.py>) · [tests/test\_dashboard\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/tests/test_dashboard_delivery.py>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/docs/project-dashboard.md>)

### W46 · Complete the P00-15 storage driver and transaction qualification gate

**Implemented increment**

**Requirements:** P00-15

**How it was done:** Closed the candidate increment&\#x27;s technical gaps in the existing component. Added a typed default create/rename path over atomic state/journal/audit/actor-request-payload receipts; generic SQL/transaction entry is qualification-only. Streaming results and statement/parameter inputs have explicit budgets. Armed RAII guards poison and close sessions on caller-dropped futures for query/BEGIN/mutation/rollback/COMMIT. A bounded private relay withholds the actual PostgreSQL commit reply; an independent connection verifies committed effects before recovery. The controller now SIGKILLs/restarts its owned database at two mandatory Rust checkpoints and rejects missing checkpoint accounting. Added a complete criterion-by-criterion P00-15 exit packet and a validation-ready state requiring pinned evidence, separate from owner acceptance.

**Recorded validation:** All 29 qualification cases pass with none ignored; driver library line coverage is 97.81% \(312/319\). Tests prove actual committed state exists after restart before any retry, staged state is absent after a pre-commit kill, lost durable replies and dropped commit futures recover exactly one effect, concurrent duplicate requests commit once, changed payload/revoked actors are denied, and over-budget or abandoned operations cannot reuse their connection. Both real process-crash checkpoints completed. All 160 repository tests pass at 99% tooling coverage; 34 desktop/mobile browser checks and six build/security tests pass. Strict types, all-feature Clippy, Bandit, workflow checks and root/fuzz locked graph audits pass.

**Limits and remaining work:** This completes the entire stated Phase 0 P00-15 library/transaction review, submitted for owner validation. It does not accept later native AD storage or a production release. Native GUID/SID/schema/ACL integration, service provisioning, credential/key custody and domain/host/disk/backup/upgrade/capacity qualification retain their actual Phase 1/3/4 gates. The fixed fixture identities and actor switch are not AD semantics/authentication. All 60 client conformance scenarios remain unrun; existing accepted proofs are unchanged.

**Problems:** I05, I26, I35

**Source evidence:** [docs/validation/p00-15.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/validation/p00-15.md>) · [docs/adr/0007-postgresql-driver-qualification.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/adr/0007-postgresql-driver-qualification.md>) · [native/babel-store-driver-lab/src/lib.rs](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/src/lib.rs>) · [native/babel-store-driver-lab/src/mutation.rs](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/src/mutation.rs>) · [native/babel-store-driver-lab/tests/database.rs](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/tests/database.rs>) · [native/babel-store-driver-lab/tests/support/mod.rs](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/tests/support/mod.rs>) · [native/babel-store-driver-lab/tests/fixture.sql](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/tests/fixture.sql>) · [scripts/qualify\_store\_driver.py](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/scripts/qualify_store_driver.py>) · [tests/test\_store\_driver\_harness.py](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/tests/test_store_driver_harness.py>)

### W47 · Record owner validation of the full P00-15 Phase 0 gate

**Design recorded**

**Requirements:** P00-15

**How it was done:** The project owner explicitly answered “Validate P00-15” after reviewing the complete criterion packet and passing CI. Recorded the dated decision in the source-pinned packet and acceptance ledger, changed P00-15 from ready for validation to accepted, and preserved all four earlier acceptance proofs. Phase 0 now has 3 accepted, 8 in progress, 1 blocked and 5 planned requirements.

**Recorded validation:** The reviewed implementation passed all 29 driver qualification cases with none ignored, both actual database restart checkpoints, 97.81% driver-library coverage and all 14 CI jobs in run 44327591957. The full original criterion and exact qualified profile are recorded with the owner decision; acceptance is explicit, not inferred from CI.

**Limits and remaining work:** This accepts the full Phase 0 driver/transaction gate, not the whole phase or a production directory server. Native AD identity/schema/ACL integration, service/key custody and domain recovery/capacity retain their separate Phase 1/3/4 gates. All 60 product/client conformance scenarios remain unrun.

**Problems:** I05, I26, I35

**Source evidence:** [docs/validation/p00-15.md](<https://github.com/Ise-Tom/Babel/blob/49abca719c43082e4e9af30c5bc960d2b714f1b0/docs/validation/p00-15.md>)

### W48 · Complete recovery/scope governance with enforced design-contract checks

**Implemented increment**

**Requirements:** P00-10

**How it was done:** Added a versioned contract and strict planning checker with six complete worked schema/key/domain-restore/functional-level/storage/GPO records. Each contains owner/scope/requirements, all five impact classes, interruption and recovery controls, evidence invalidation/reruns and proposed review. Exceptions require named operation/client/site, owner/control/review, UTC activation/expiry and production impact; baseline/unknown/phase-gate waivers and rewriting observed outcomes fail. Required CI validates the contract and retains source/contract/matrix digest/time evidence. Prepared the complete original P00-10 criterion packet.

**Recorded validation:** All 172 repository tests pass at 99% combined statement/branch coverage. The new checker has 100% statement/branch coverage. Negative tests reject omitted controls, false runtime passes, partial invalidation, unreviewed exceptions, expiry at its exact boundary, unknown IDs, protected baseline/phase-gate waivers and mutable/duplicate references. Strict mypy/Ruff and Bandit/workflow lint/security checks pass.

**Limits and remaining work:** This implements planning consistency checks and completes the Phase 0 design gate; it neither authenticates prose/reviewer claims nor performs/authorizes a live migration or recovery. No current exception is active. Actual native migration, key/domain recovery and independent production review remain their own gates. Owner validation is pending; all five existing acceptance proofs are preserved.

**Problems:** I37

**Source evidence:** [docs/validation/p00-10.md](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/validation/p00-10.md>) · [docs/phase-00-governance.md](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/phase-00-governance.md>) · [lab/phase0-contract.json](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/lab/phase0-contract.json>) · [scripts/check\_phase0\_contract.py](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/scripts/check_phase0_contract.py>) · [tests/test\_phase0\_contract.py](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/tests/test_phase0_contract.py>) · [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/.github/workflows/ci.yml>)

### W49 · Complete the Linux-hosted 2016 domain/forest functional-level contract

**Design recorded**

**Requirements:** P00-11

**How it was done:** Fixed the initial 2016-domain/2016-forest profile with fresh-forest creation design and explicit transition/refusal/failure review. Distinguished functional levels from reference DC OS and Windows/Linux/macOS member clients. Reviewed inherited/optional security features, 2025-level additions, FRS/DFSR, coexistence and conditional rollback. Pinned two immutable MicrosoftDocs revisions and resolved their contradictory no-levels-since-2016 sentence using the current level table. Required CI rejects matrix/profile/client drift and unqualified advertised levels. Submitted the complete original P00-11 criterion packet.

**Recorded validation:** The same 172-test run and 100%-covered planning checker exercise fresh 2016/2016 design, unsupported create/raise/lower/coexist combinations, forest/domain mismatch, exact matrix cross-binding, removed non-Windows clients, false advertisements and reference pins. Public upstream source revisions were read on 18 November 2026. The compatibility inventory still accounts for exactly 60 unrun product scenarios.

**Limits and remaining work:** The checker returns design\_only or unsupported, never an executable deployment approval. Native RootDSE level advertising, actual creation/transitions, inherited feature semantics, Windows coexistence and client behavior are unimplemented/unqualified. Exact builds and licensed hosts remain P00-12/P00-05, operation decomposition P00-01. No full product capability or later phase is started or accepted.

**Problems:** I36

**Source evidence:** [docs/validation/p00-11.md](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/validation/p00-11.md>) · [docs/functional-level-profile.md](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/functional-level-profile.md>) · [lab/phase0-contract.json](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/lab/phase0-contract.json>) · [scripts/check\_phase0\_contract.py](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/scripts/check_phase0_contract.py>) · [tests/test\_phase0\_contract.py](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/tests/test_phase0_contract.py>) · [lab/compatibility.json](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/lab/compatibility.json>)

### W50 · Complete the qualified Linux/Rust toolchain and bounded parser baseline

**Implemented increment**

**Requirements:** P00-04

**How it was done:** Declared and qualified a Linux x86\_64 GNU parser profile, with Ubuntu 24.04 CI and Debian 13 observations. Added source/lock/policy/compiler/LLVM/readelf/host/binary facts and runtime Cargo-closure checks; new parser normal/build/FFI expansion or missing PIE/full RELRO/non-executable-stack protections fails. Enabled optimized overflow checks and added a real debug/release overflow test. Required CI now retains actual parser-baseline evidence alongside existing probes, coverage, audit and sanitizer-fuzz results. Recorded alternatives and upstream maintenance responsibilities in the full original P00-04 packet.

**Recorded validation:** 185 repository tests pass at 99% combined statement/branch coverage; the new qualification collector has 100% coverage. Local all-feature Clippy, workspace tests and real release LDAP/OpenSSL probes pass, including all 19 TLS methods. Release arithmetic visibly fails rather than wrapping. The actual Debian 13.6 binary shows PIE, full RELRO and a non-executable stack, exact Rust 1.100.0/LLVM 23.1.5 and a dependency-free parser normal/runtime crate closure. Required CI separately repeats the real tests, &gt;=90% native coverage, locked graph audits and bounded sanitizer fuzz.

**Limits and remaining work:** This completes the entire stated Phase 0 compiler/parser baseline; owner validation is pending. Std/libc internals remain upstream trust, and ring native code is a separate TLS boundary. Other targets/new parser dependencies require requalification. Linux server baseline qualification does not qualify Windows/Linux/macOS client behavior or native AD semantics, capacity, credential handling or full-server operation. All 60 conformance scenarios remain unrun.

**Problems:** I38

**Source evidence:** [docs/validation/p00-04.md](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/validation/p00-04.md>) · [docs/native-parser-baseline.md](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/native-parser-baseline.md>) · [scripts/qualify\_parser\_baseline.py](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/scripts/qualify_parser_baseline.py>) · [tests/test\_parser\_baseline.py](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/tests/test_parser_baseline.py>) · [Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/Cargo.toml>) · [native/babel-ldap/tests/toolchain.rs](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/native/babel-ldap/tests/toolchain.rs>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/.github/workflows/native.yml>)

### W51 · Complete project contribution and redistribution obligations with omission-safe artifacts

**Implemented increment**

**Requirements:** P00-06

**How it was done:** Preserved the owner-selected Apache-2.0/DCO and documented the complete contribution/selected-third-party obligation register. Hardened notice verification against missing required terms, omitted/unlisted files, symlinks and missing/duplicate/unaccounted package inventories; extraction compares a manifest SHA-256 captured before archiving. Standalone dashboard HTML now retains full project and actual esbuild terms inertly; esbuild input accounting refuses new unreviewed bundled runtime sources. One-pass template substitution also preserves authored placeholder text. Prepared the full original P00-06 criterion packet. Native bundles also retain actual glibc/libgcc package copyright and LGPL/GPL texts; system libraries remain dynamically replaceable and are not bundled.

**Recorded validation:** 185 repository tests pass at 99% combined coverage, including 13 notice-verifier methods with omission, changed-manifest, package-binding, digest and symlink denials. A real protocol notice bundle \(11 packages/46 files\) was archived, extracted and verified against its original manifest digest; the real driver bundle \(62 packages/150 files\) also passes strict verification. Nine dashboard build/security tests pass, checking full retained license text, inert escaping, literal placeholder preservation and rejected runtime inputs. No dependency or Cargo license allowance was added; actual GNU runtime terms are retained separately, with no fabricated DCO sign-off.

**Limits and remaining work:** This completes the original Phase 0 project-license/contributor/obligation-recording gate, pending owner validation. Inventories and trusted CI digests are not independent legal certification, complete binary-link analysis or public release signatures. Actual system shared-library names are recorded separately from Cargo; broader installers/containers must assess their contents. Exact protocol/reference-image/fixture rights stay P00-16, and future product/agent distribution retains its own review. Existing five accepted proofs and pending P00-10/P00-11 decisions are unchanged.

**Problems:** I39, I40

**Source evidence:** [docs/validation/p00-06.md](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/validation/p00-06.md>) · [docs/licensing-and-redistribution.md](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/licensing-and-redistribution.md>) · [CONTRIBUTING.md](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/CONTRIBUTING.md>) · [scripts/collect\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/scripts/collect_native_notices.py>) · [tests/test\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/tests/test_native_notices.py>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/.github/workflows/native.yml>) · [dashboard/build.mjs](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/dashboard/build.mjs>) · [dashboard/tests/build.test.mjs](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/dashboard/tests/build.test.mjs>) · [dashboard/src/index.html](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/dashboard/src/index.html>)

### W52 · Complete identity, schema, authorization and local commit design

**Design recorded**

**Requirements:** P00-02

**How it was done:** Replaced ambiguous draft invariants with nine original worked cases against actual pinned ADTS/DRSR/DTYP editions. Distinguished GUID from domain-move SID changes, local uniqueness from replica name repair, ordered object/attribute/control checks, move-parent rights, hidden filter attributes, asynchronous inheritance, group/GC/token freshness and durable reauthorized receipts.

**Recorded validation:** 196 repository tests pass at 99% combined statement/branch coverage. The new checker has 99% coverage and exercises missing-case/owner/source/rights/runtime denials. Actual public bytes for 13 document editions and all 58 referenced section headings were checked locally; required CI validates committed source bindings offline.

**Limits and remaining work:** Full original P00-02 design gate prepared for owner validation; this does not implement or qualify native GUID/SID/schema/matching/ACL/token behavior. Inheritance, existing PAC and cross-site freshness are not instantaneous revocation promises. All 60 client cases remain unrun.

**Problems:** I41

**Source evidence:** [docs/validation/p00-02.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-02.md>) · [docs/adr/0005-directory-and-replication-invariants.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/adr/0005-directory-and-replication-invariants.md>) · [lab/state-security-contract.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/state-security-contract.json>) · [scripts/check\_state\_security.py](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/scripts/check_state_security.py>) · [tests/test\_state\_security.py](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/tests/test_state_security.py>)

### W53 · Complete source-pinned replication, conflicts and restore epoch design

**Design recorded**

**Requirements:** P00-03

**How it was done:** Specified eleven worked cases for per-attribute origin/local progress, modular version comparison, little-endian GUID ordering, distinct link lifetimes, timestamp/object-GUID naming conflicts, deletion repair, safe response/cycle progress, invocation epochs, stale-retention quarantine and RID authority. The disk format remains unfrozen.

**Recorded validation:** The selected ADTS/DRSR/DTYP PDF bytes and exact section headings were inspected and checked. Required consistency checks reject lost cases, stale heading hashes and invented passing outcomes; 196 repository tests pass. Attribute, link and naming rules are expressly distinct rather than an unqualified generic comparator.

**Limits and remaining work:** Full original P00-03 design gate prepared for owner validation. No native DRS comparator, convergent multi-DC service, Windows observation, VM-generation detection, clean-domain recovery or RID seizure is implemented or accepted.

**Problems:** I42

**Source evidence:** [docs/validation/p00-03.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-03.md>) · [docs/adr/0005-directory-and-replication-invariants.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/adr/0005-directory-and-replication-invariants.md>) · [lab/state-security-contract.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/state-security-contract.json>) · [lab/specification-pins.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/specification-pins.json>) · [scripts/check\_state\_security.py](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/scripts/check_state_security.py>)

### W54 · Complete accountable Tier 0 and later-module threat-boundary design

**Design recorded**

**Requirements:** P00-07

**How it was done:** Bound eleven named trust boundaries to all twenty canonical threats, with current owner Ise-Tom, assets, misuse cases, required denial/fault behavior, residual risk and actual implementation gates. Covered core/store/keys/replicas/web/restore/supply chain/external/fleet/support-files/EDR authority without starting later phases.

**Recorded validation:** CI consistency checks require all original boundaries, every threat, nonempty owners and known implementation gates; regression tests reject absent coverage, unknown threats, lost residual risks and false independent/runtime qualification. All 196 repository tests pass.

**Limits and remaining work:** Full original P00-07 design gate prepared for owner validation. Solo ownership is not independent assessment, operational backup coverage or implemented service security. Actual response exercises remain P00-17 and later production safeguards.

**Problems:** I27

**Source evidence:** [docs/validation/p00-07.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-07.md>) · [docs/threat-model.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/threat-model.md>) · [docs/phase-00-security-and-dependencies.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/phase-00-security-and-dependencies.md>) · [lab/state-security-contract.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/state-security-contract.json>) · [tests/test\_state\_security.py](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/tests/test_state_security.py>)

### W55 · Pin actual public protocol editions and separate reference use from image/patent clearance

**Implemented increment**

**Requirements:** P00-01, P00-16

**How it was done:** Added 13 raw-byte-pinned public document records with actual notice identity, edition, reviewer/date and restrictive rights dispositions. Corrected nonexistent MS-DFSR to MS-FRS2, added descriptor rules from MS-DTYP and rebound all 60 still-unrun conformance records to the changed matrix. Added optional actual-byte/PDF-heading reproduction and synthetic-asset hash/purpose checks with explicit external-image denial.

**Recorded validation:** Checked all 13 actual document byte hashes and 58 section headings locally; default CI validates committed metadata offline. Negative tests cover changed/duplicate/missing/protected documents, extractor timeout, stale headings, path traversal/symlinks, unknown purposes and unprovided image rights. Apache/DCO acceptance and all existing five acceptance proofs are unchanged.

**Limits and remaining work:** P00-16 remains in progress: Microsoft patent/program coverage and concrete image/fixture clearance are not established. No upstream PDFs, protected-document decryption, vendor images or captures are imported. MS-DNSP is management, not the full DNS wire protocol; detailed P00-01 mapping remains open.

**Problems:** I28

**Source evidence:** [docs/reference-use-review.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/reference-use-review.md>) · [lab/specification-pins.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/specification-pins.json>) · [lab/compatibility.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/compatibility.json>) · [lab/conformance-evidence.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/conformance-evidence.json>) · [scripts/check\_state\_security.py](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/scripts/check_state_security.py>) · [tests/test\_state\_security.py](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/tests/test_state_security.py>)

### W56 · Define solo vulnerability-response process and make timing proposal reviewable

**Design recorded**

**Requirements:** P00-17

**How it was done:** Documented private intake, hostile-attachment custody, severity/reproduction, disclosure and sole-owner absence, with a concrete unrun drill record. Proposed Phase 0 process review plus mandatory actual drill/backup before supported production. Kept the existing P00-17 and pre-preview security policy unchanged pending owner agreement.

**Recorded validation:** A read-only GitHub API observation on 19 November reports private vulnerability reporting enabled. Local documentation/traceability checks pass; no private report, recipient, receipt, escalation or backup availability is fabricated.

**Limits and remaining work:** Configuration is not delivery/response evidence. The current live-drill/real-backup gate is not complete, and this proposal is not an approved scheduling change, a support promise, or authorization to send a report.

**Problems:** I27

**Source evidence:** [docs/security-response-readiness.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/security-response-readiness.md>) · [docs/phase-00-security-and-dependencies.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/phase-00-security-and-dependencies.md>) · [SECURITY.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/SECURITY.md>) · [docs/phases/phase-00.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/phases/phase-00.md>)

## Problems encountered

### I03 · Project license and contributor policy not selected

**Resolved** · Phases 00, 01, 05

No project LICENSE is selected. Native crates remain unpublished and source-prerelease creation is blocked by the license gate.

**Resolution:** The project owner explicitly selected Apache-2.0 plus DCO in this conversation on 2026-11-17. The full license/DCO texts, contribution policy, notices and package SPDX metadata are applied; unpublished Rust packages are now included in the license audit. This resolves selection, not all third-party or specification rights reviews.

**Next action:** Merge the reviewed terms and retain upstream notices; maintainers verify external contribution sign-offs and complete the remaining D-01 rights review before corresponding distribution.

**Provenance:** Current repository decision register; third-party development license policy does not choose the project license.

[LICENSE](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/LICENSE>) · [DCO](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/DCO>) · [NOTICE](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/NOTICE>) · [CONTRIBUTING.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/CONTRIBUTING.md>) · [Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/Cargo.toml>) · [native/babel-ldap/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/native/babel-ldap/Cargo.toml>) · [fuzz/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/fuzz/Cargo.toml>) · [dashboard/package.json](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/dashboard/package.json>) · [deny.toml](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/deny.toml>) · [docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/b58df33f10f80688bfeaf55e44d08d52156e7608/docs/decisions.md>)

### I04 · Licensed Windows/Mac lab hosts and real cross-platform client evidence are missing

**Open** · Phases 00, 01, 02

The existing six-VM isolated Windows reference definition is prepared but no host/images have been provisioned. The initial scope now also includes Linux SSSD/MIT Kerberos and macOS Apple Silicon/Intel; Mac hardware/image rights and exact client/package builds are not allocated or qualified.

**Resolution:** Still open

**Next action:** Select licensed isolated test infrastructure and exact image/package manifests; extend provisioning for Linux/macOS clients, then perform two clean deployment/discovery/cleanup runs with actual login/password/SSO evidence. No purchase or automatic VM/image download is authorized.

**Provenance:** Explicitly outstanding; no Windows test is marked passed.

[lab/windows-reference.toml](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/lab/windows-reference.toml>) · [scripts/check\_lab\_definition.py](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/scripts/check_lab_definition.py>) · [tests/test\_lab\_definition.py](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/tests/test_lab_definition.py>) · [docs/windows-reference-lab.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/windows-reference-lab.md>) · [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/.github/workflows/ci.yml>) · [scripts/check\_ci\_scope.py](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/scripts/check_ci_scope.py>) · [docs/phase-00-progress.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-progress.md>)

### I05 · Qualified driver profile available; native AD directory storage still needs implementation

**Open** · Phases 00, 01, 02, 03

P00-15 driver/transaction qualification is complete and explicitly owner-accepted, including typed bounds, dropped futures, real durable-reply loss and Rust-client process recovery. The native AD identity/schema/ACL/store and domain formats remain separate implementation obligations; the fixture is not a directory server.

**Resolution:** Still open

**Next action:** Integrate the owner-accepted driver profile into P01-02/P01-03/P01-11/P01-12 with native identity/schema/ACL and durable journal semantics. Service/key custody, domain replication/backup/upgrade and production capacity retain their separate gates.

**Provenance:** Design blocker, not an implemented storage defect.

[docs/validation/p00-15.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/validation/p00-15.md>) · [native/babel-store-driver-lab/src/lib.rs](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/src/lib.rs>) · [docs/phases/phase-01.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/phases/phase-01.md>)

### I06 · Proposed SBOM generator had a yanked locked dependency

**Resolved** · Phases 01

The proposed cargo-cyclonedx installation reported a yanked transitive XML dependency. That generator was not used for accepted SBOM output.

**Resolution:** Removed the unused tool and used checksum-pinned Syft 1.57.2 for Cargo.lock source inventory. Native project/fuzz dependency graphs are audited separately.

**Next action:** Review SBOM tool pins and upstream advisories regularly.

**Provenance:** Recorded development-session tool-selection correction; no checksum or advisory bypass was introduced.

[scripts/install\_ci\_tools.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/scripts/install_ci_tools.py>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>)

### I07 · Fuzzer license and path dependency failed the initial audit

**Resolved** · Phases 01

libfuzzer-sys requires NCSA alongside its MIT/Apache choice; the initial allowlist lacked it. The local path dependency also lacked an exact version constraint.

**Resolution:** Recorded the development-harness license obligation, enabled development/build license checks and pinned the local path version. Both graphs now pass.

**Next action:** Retain upstream notices; do not confuse this development policy with project-license approval.

**Provenance:** Initial cargo-deny findings and subsequent passing audits.

[deny.toml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/deny.toml>) · [fuzz/Cargo.toml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/fuzz/Cargo.toml>)

### I08 · SBOM cataloger selection used the wrong CLI operation

**Resolved** · Phases 01

The initial Syft selector treated a cataloger name as a tag and produced no valid report.

**Resolution:** Switched to the explicit default-cataloger override and checked that CycloneDX output contains both core-development and fuzz packages.

**Next action:** Validate report contents as well as command success when changing catalog/tool versions.

**Provenance:** Recorded local validation failure and correction; the failed output was not counted as evidence.

[.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/.github/workflows/native.yml>)

### I09 · Design checker needed precise empty-acceptance handling

**Resolved** · Phases 00

A regression test found that an empty acceptance cell was reported as a missing row instead of a specific empty-cell error.

**Resolution:** Adjusted the row parser and added explicit empty-cell validation. The negative test and complete baseline now pass.

**Next action:** Keep negative cases when modifying the document schema.

**Provenance:** Recorded implementation-test failure; no product conformance was affected.

[scripts/check\_design.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/scripts/check_design.py>) · [tests/test\_design.py](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/tests/test_design.py>)

### I11 · Preserve Undefined while adding boolean LDAP filters

**Resolved** · Phases 00, 01

A binary match/nonmatch model would incorrectly turn an unrecognized attribute into a match when negated. Unsupported matching also must not be hidden by a true OR branch.

**Resolution:** Implemented explicit Undefined/Unsupported outcomes, full branch validation and exact resource limits with negative/property/client tests.

**Next action:** Review matching rules before any general directory/schema implementation.

**Provenance:** Recorded development-session evidence and repository/CI observations; no separate public issue was created.

[native/babel-ldap/src/filter.rs](<https://github.com/Ise-Tom/Babel/blob/dca754d98dd339962c761b934b701e59c6544544/native/babel-ldap/src/filter.rs>) · [native/babel-ldap/tests/protocol.rs](<https://github.com/Ise-Tom/Babel/blob/dca754d98dd339962c761b934b701e59c6544544/native/babel-ldap/tests/protocol.rs>)

### I12 · Progress facts and the GitHub report omitted recent PR contents

**Resolved** · Phases 00, 01

Main progress still referenced the initial native snapshot after dashboard PRs merged; pending implementation and its explanations were absent until manual updates.

**Resolution:** Backfilled merged dashboard work and added bounded private PR overlays with per-record revisions, pending labels and current main CI health.

**Next action:** Update progress facts in every development PR; automatic PR import activates after this change is merged.

**Provenance:** Recorded development-session evidence and repository/CI observations; no separate public issue was created.

[scripts/collect\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/scripts/collect_pr_progress.py>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/scripts/render_dashboard.py>) · [CONTRIBUTING.md](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/CONTRIBUTING.md>)

### I13 · Main CI rejected newly vulnerable picomatch tooling graph

**Resolved** · Phases 00, 01

Main run 44142657828 failed npm audit for GHSA-fc5q-39xc-vjpf. The advisory affects picomatch through 4.0.7 and no patched version was published when checked.

**Resolution:** PR \#16 removed the vulnerable dependency path while retaining supported compiler/ESLint versions and tested DOM/eval/explicit-any checks. Merged main run 44153995669 passed all 12 jobs, including dependency audit.

**Next action:** Keep all-severity audit enforcement and regression coverage on future tooling updates.

**Provenance:** Recorded development-session evidence and repository/CI observations; no separate public issue was created.

[dashboard/package-lock.json](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/package-lock.json>) · [dashboard/lint.mjs](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/lint.mjs>) · [dashboard/tests/lint.test.mjs](<https://github.com/Ise-Tom/Babel/blob/647a7ba026622bd08f2870c22397a070b4982ef2/dashboard/tests/lint.test.mjs>)

### I14 · Fixed requirement quotas and ambiguous substep acceptance labels

**Resolved** · Phases 00, 01

The earlier repair removed validator quotas but left every authored phase at ten broad rows and some tests at a fixed total. Independently testable obligations remained bundled, so actual roadmap granularity still looked uniform.

**Resolution:** Refined composite obligations in all 18 canonical phase documents, retaining primary original IDs and tracing split obligations to new stable IDs. Counts now follow the actual rows \(12–24 per phase\); acceptance scopes are unchanged. Dashboard/export tests derive totals and exercise unequal phase sizes.

**Next action:** Keep counts tied to independent acceptance obligations, never a quota or effort percentage; update canonical traceability and explicit acceptance when scope changes.

**Provenance:** Project owner requested acceptance questions and said substep counts need not be linear; no separate GitHub issue was created.

[docs/phases/README.md](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/docs/phases/README.md>) · [scripts/check\_design.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/scripts/check_design.py>) · [scripts/build\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/scripts/build_dashboard.py>) · [tests/test\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/tests/test_dashboard.py>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/dashboard/tests/dashboard.spec.ts>)

### I17 · TypeScript 7 removed the compiler API used by security lint

**Resolved** · Phases 00, 01

PR \#17 run 44154241268 passed typecheck but failed dashboard lint with TypeError reading ScriptTarget.Latest. Local reproduction confirmed the major version no longer exposes the JavaScript compiler API; alternate APIs are unstable and require migration.

**Resolution:** The corrected PR retains TypeScript 6.0.3 and the existing AST/DOM/eval protections, with compatible updates still enabled and automatic compiler majors deferred. Local build, lint, browser and audit checks pass.

**Next action:** Verify corrected PR CI. Migrate the policy explicitly before upgrading the compiler major; retain malformed-input and security regressions.

**Provenance:** Observed failed hosted job 134361914270 and local reproduction of the same failure; no check was skipped.

[dashboard/package.json](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/dashboard/package.json>) · [.github/dependabot.yml](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/.github/dependabot.yml>) · [dashboard/lint.mjs](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/dashboard/lint.mjs>) · [dashboard/tests/lint.test.mjs](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/dashboard/tests/lint.test.mjs>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/9700ddc9a28f62a9204bafc49e0f67390ed0036e/docs/github-security-settings.md>)

### I19 · Hosted hardening run caught unregistered ruleset data and viewport overflow

**Resolved** · Phases 00, 01

Run 44177850164 rejected the new docs/github-main-ruleset.json under the default-deny component scope policy. The desktop browser check also measured the last phase row at 1015px in a 1000px viewport after the progress summary grew. Local browser validation had preceded that progress-data update.

**Resolution:** Registered that exact non-executable JSON file with readable-object validation and negative tests; other JSON manifests remain rejected. Shortened the focus summary and reduced phase-card spacing. Rebuilt using the final progress data before rerunning browser checks; no CI assertion or source guard was removed.

**Next action:** Require the corrected full hosted run to pass and keep rebuilding dashboard data before visual checks when progress facts change.

**Provenance:** Observed hosted repository/browser failures and inspected the actual 1440×1000 CI screenshot; not inferred from a local-only result.

[scripts/check\_ci\_scope.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/scripts/check_ci_scope.py>) · [tests/test\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/tests/test_delivery.py>) · [dashboard/src/style.css](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/dashboard/src/style.css>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/b2cad80fed4acb38f132f5e15e34339b9e7748af/dashboard/tests/dashboard.spec.ts>)

### I21 · PostgreSQL temporary initialization server looked ready before final startup

**Resolved** · Phases 00, 01

The first real container experiment saw pg\_isready succeed against the official image’s temporary initialization server before the final database process was available, so the first query failed.

**Resolution:** Readiness now requires the container’s final postgres PID 1 before the socket probe; startup is bounded and failed initialization removes only the owned container/volumes. The final process/crash suite passes.

**Next action:** Keep the startup barrier while using this pinned image and requalify it on reviewed image changes.

**Provenance:** Observed local real-container failure and subsequent successful 21-test integration run; not a Windows or production failure claim.

[experiments/postgres\_store/Dockerfile](<https://github.com/Ise-Tom/Babel/blob/7cb02d8bec6b9eae84f8550c90a2670b1fb17710/experiments/postgres_store/Dockerfile>) · [experiments/postgres\_store/experiment.py](<https://github.com/Ise-Tom/Babel/blob/7cb02d8bec6b9eae84f8550c90a2670b1fb17710/experiments/postgres_store/experiment.py>) · [experiments/postgres\_store/schema.sql](<https://github.com/Ise-Tom/Babel/blob/7cb02d8bec6b9eae84f8550c90a2670b1fb17710/experiments/postgres_store/schema.sql>) · [experiments/postgres\_store/test\_store.py](<https://github.com/Ise-Tom/Babel/blob/7cb02d8bec6b9eae84f8550c90a2670b1fb17710/experiments/postgres_store/test_store.py>) · [.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/7cb02d8bec6b9eae84f8550c90a2670b1fb17710/.github/workflows/ci.yml>) · [docs/adr/0004-synthetic-postgresql-state-experiment.md](<https://github.com/Ise-Tom/Babel/blob/7cb02d8bec6b9eae84f8550c90a2670b1fb17710/docs/adr/0004-synthetic-postgresql-state-experiment.md>)

### I25 · Exact compatibility builds and detailed wire cases remain unqualified

**Open** · Phases 00

The initial profile and 30 operation families are explicit, but exact Windows/Linux/macOS image/package builds and detailed control/opnum/error fixtures are not approved. Every one of the 60 initial product conformance scenarios is unrun.

**Resolution:** Still open

**Next action:** Pin exact licensed images/packages, decompose operation families into executable reference/negative cases and retain reviewed evidence per client/target; keep unknown or unsupported behavior visible.

**Provenance:** Current repository implementation/design inventory; this is a development gap, not a GitHub account or hosting setting.

[lab/compatibility.json](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/lab/compatibility.json>) · [lab/conformance-evidence.json](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/lab/conformance-evidence.json>) · [docs/phase-00-progress.md](<https://github.com/Ise-Tom/Babel/blob/b98dac7d33b20bef1ab6ccfb4a295f40d2330500/docs/phase-00-progress.md>)

### I26 · Production TLS/Kerberos/storage/transport libraries need qualification

**Open** · Phases 00

The owner explicitly validated the full P00-15 driver/transaction gate on 18 November 2026. TLS/channel/key integration, Kerberos/PAC and DNS/SMB/RPC decisions remain open at their own gates; native store implementation is tracked by I05.

**Resolution:** Still open

**Next action:** Continue P00-13/P00-14 and transport qualification. Preserve the accepted driver profile and its qualification cases while implementing the native store under Phase 1; changes to transport/pool/stack/profile require requalification.

**Provenance:** Current repository implementation/design inventory; this is a development gap, not a GitHub account or hosting setting.

[docs/validation/p00-15.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/validation/p00-15.md>) · [docs/phase-00-security-and-dependencies.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/phase-00-security-and-dependencies.md>) · [docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/decisions.md>)

### I27 · Actual private receipt/escalation, backup response and production incident exercises remain unqualified

**Open** · Phases 00

P00-07 now has complete boundary/threat/ownership design for review. Reporting is configured but notification/receipt/escalation and a genuine backup are unverified; sole-owner process design is not operational coverage.

**Resolution:** Still open

**Next action:** Review the explicit solo scheduling proposal; retain the original gate until agreed. No synthetic private report may be sent without explicit authorization and an available recipient.

**Provenance:** Current repository implementation/design inventory; this is a development gap, not a GitHub account or hosting setting.

[docs/security-response-readiness.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/security-response-readiness.md>) · [docs/phase-00-security-and-dependencies.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/phase-00-security-and-dependencies.md>)

### I28 · Exact references pinned; concrete program/patent/image use rights and detailed operation mapping remain open

**Open** · Phases 00

Thirteen actual reference editions and notices are now pinned, including corrected MS-FRS2 and added MS-DTYP. Concrete Microsoft patent/program coverage and licensed Windows/macOS image/fixture rights remain unresolved; citations do not grant them.

**Resolution:** Still open

**Next action:** Complete actual use-rights review before acquiring/distributing affected fixtures, and decompose detailed protocol operations including DNS wire RFCs. Keep unprovided images denied and all product conformance unrun.

**Provenance:** Current repository implementation/design inventory; this is a development gap, not a GitHub account or hosting setting.

[docs/reference-use-review.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/reference-use-review.md>) · [lab/specification-pins.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/specification-pins.json>) · [scripts/check\_state\_security.py](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/scripts/check_state_security.py>)

### I29 · Shared preparation incorrectly started later phases

**Resolved** · Phases 00, 01, 05, 10

The dashboard promoted a planned phase to in\_progress when any work record linked to it, including shared licensing, CI and source-prerelease preparation. This incorrectly started Phases 5 and 10 without active requirements.

**Resolution:** Removed promotion based on work links. Explicit active/accepted requirement state drives phase activity, with separate whole-phase acceptance. UI/report call these related records and planned requirements explain preparation. Python/browser regressions verify shared design/implementation records do not start future phases.

**Next action:** Keep preparatory traceability separate from execution. Start a later phase only by explicitly recording actual requirement activity and evidence; do not infer it from a shared work item.

**Provenance:** Reproduced against merged main: Phases 5 and 10 were in\_progress while all their requirements were planned; the corrected model has only Phases 0 and 1 active.

[scripts/build\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/scripts/build_dashboard.py>) · [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/dashboard/src/main.ts>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/scripts/render_dashboard.py>) · [tests/test\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/tests/test_dashboard.py>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/794345f04c36a8be4811a56183a0462a985780e8/dashboard/tests/dashboard.spec.ts>)

### I30 · Approved workload lacked reproducible target-scale fixtures and independent integrity checks

**Resolved** · Phases 00

The owner-approved workload specified counts/distributions and faults but had no executable seeded dataset. Future storage/load tests could therefore use inconsistent memberships/payloads or mistake self-reported hashes/counts for structural correctness.

**Resolution:** Implemented a bounded streaming generator and independent relational/artifact auditor, including semantic tamper tests after rehashing. Two full generations/audits produced byte-identical artifacts with exact approved distributions. Tests cover failed writes, no overwrite/symlinks, duplicate/missing references, false runtime claims and acyclic graphs with wrong nesting profiles. Required CI runs full generation/audit and keeps small evidence artifacts.

**Next action:** Use the versioned dataset in future qualified storage/protocol/load runners and retain source/seed/input manifests. Add actual encoder/storage/resource/client measurements before claiming runtime capacity; do not relabel fixture graph validation as AD conformance.

**Provenance:** Actual local generator/auditor executions and negative integrity tests at the pinned source; no service, Windows/Mac host or real directory was contacted.

[docs/synthetic-workload.md](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/docs/synthetic-workload.md>) · [scripts/generate\_workload.py](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/scripts/generate_workload.py>) · [scripts/check\_workload.py](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/scripts/check_workload.py>) · [tests/test\_workload.py](<https://github.com/Ise-Tom/Babel/blob/521dfe82f6d32db979185084b2a6e0a8dac2e02a/tests/test_workload.py>)

### I31 · Capability associations lacked an explicit implementation tracker

**Resolved** · Phases 00

Phase work and broad feature associations could not show which subset of a global capability actually existed or distinguish supporting tools from product functionality.

**Resolution:** Added an explicit 130-capability tracker with scoped claims, implemented/missing behavior, work/evidence/blocker links and separate full-capability acceptance. Planned defaults and validation prevent shared design/tooling or accepted requirement subsets from automatically claiming delivery.

**Next action:** Maintain claims with every functional-scope change and review actual behavior; do not infer product acceptance from a green dashboard check.

**Provenance:** Development implementation/tooling gap observed in the repository and verified with executable tests; not a GitHub setup incident.

[docs/capability-tracker.md](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/docs/capability-tracker.md>) · [scripts/capability\_tracker.py](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/scripts/capability_tracker.py>) · [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/dashboard/src/main.ts>) · [tests/test\_capabilities.py](<https://github.com/Ise-Tom/Babel/blob/a3c58b409f362dd6ccb0e5999572620f17652b15/tests/test_capabilities.py>)

### I32 · Internal native binary archive did not carry actual third-party notice texts

**Resolved** · Phases 00

The previous LDAP lab had no external runtime crate dependencies. The added TLS stack introduces copyright/permission/disclaimer obligations that an SPDX SBOM alone does not retain in the binary archive.

**Resolution:** Reviewed ISC/BSD-3-Clause terms alongside Apache/MIT and bundled actual nested runtime-source license files, project terms and Rust-library notices. Added a per-file digest manifest, extraction verification and both packaged executable probes; no audit findings are ignored.

**Next action:** Re-review actual notices on dependency/provider/toolchain changes and expand platform/product distribution analysis before publishing product packages; specification/fixture rights remain open.

**Provenance:** Development implementation/tooling gap observed in the repository and verified with executable tests; not a GitHub setup incident.

[scripts/collect\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/scripts/collect_native_notices.py>) · [tests/test\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/tests/test_native_notices.py>) · [deny.toml](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/deny.toml>) · [.github/workflows/native.yml](<https://github.com/Ise-Tom/Babel/blob/37df14a3507b8468f7e7246b17f7490265e3b0fd/.github/workflows/native.yml>)

### I33 · Caught SQL errors can make raw COMMIT completion look like a committed mutation

**Resolved** · Phases 00

A real tokio-postgres 0.7.18/PostgreSQL 18.7 comparison shows that after a caught statement error, Transaction.commit\(\) can return Ok while PostgreSQL rolls back the transaction and no inserted record exists. Raw SQL command completion alone is therefore not a durable mutation acknowledgment.

**Resolution:** The qualification helper tracks statement failures, rolls back and returns Aborted instead of successful commit. Deferred commit failures and lost connections never return success; unconfirmed commit outcomes conservatively discard the session and return UnknownCommit without automatic retry. Actual tests verify committed/absent database state.

**Next action:** Carry this invariant into a typed authorized native adapter and constrain unmanaged transaction SQL. Qualify durable idempotency, caller-dropped-future safety and exact after-commit response loss; this helper does not close the wider I05/I26 production gaps.

**Provenance:** Observed with the real pinned database and Rust driver, then protected by executable helper regressions. This is a development correctness finding, not a GitHub setup incident or an upstream vulnerability claim.

[native/babel-store-driver-lab/src/lib.rs](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/native/babel-store-driver-lab/src/lib.rs>) · [native/babel-store-driver-lab/tests/database.rs](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/native/babel-store-driver-lab/tests/database.rs>) · [docs/adr/0007-postgresql-driver-qualification.md](<https://github.com/Ise-Tom/Babel/blob/32c80310d3a19a9b4ed522a2e9f8974c8ef5ed7f/docs/adr/0007-postgresql-driver-qualification.md>)

### I34 · Acceptance-only meter hid Phase 0 activity and recent implementations

**Resolved** · Phases 00

The live site was correctly deployed after PR \#26 and contained the Rust-driver increment. Phase 0 nevertheless looked unchanged because its bar represented only accepted requirements \(2/17\); 9 active requirements and recent work were buried in collapsed details. The header also displayed an older evidence baseline instead of the artifact build revision.

**Resolution:** Added explicit status counts/segments alongside acceptance, visible recent work and source-backed explanations on active phase pages, corresponding GitHub report summaries, and actual build identification. Browser/report regressions preserve acceptance totals and ensure shared preparation does not start future phases.

**Next action:** Maintain explicit requirement states and work evidence in each development PR. Keep activity, acceptance, related preparation and recorded CI baseline distinct; do not turn counts into effort percentages or infer acceptance from CI.

**Provenance:** Observed in the actual published f42815d dashboard data and reproduced against main. This is a development usability defect; CI and Pages publication had succeeded.

[dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/dashboard/src/main.ts>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/dashboard/tests/dashboard.spec.ts>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/scripts/render_dashboard.py>) · [tests/test\_dashboard\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/5463fb55119f1f89841c5ea645bd9ebcefd8a8f6/tests/test_dashboard_delivery.py>)

### I35 · Abandoned futures, durable reply loss and native-client recovery left P00-15 unfinished

**Resolved** · Phases 00

The first candidate only handled its own timers and lost connections before commit. Dropping the caller&\#x27;s commit future could leave an uncertain session reusable; no real post-commit response was withheld, typed bounded operations were absent, and process recovery had only been tested through psql. Later product gates also obscured the original Phase 0 exit criteria.

**Resolution:** Implemented armed operation guards and a typed default interface with bounded results. Real COMMIT-response withholding plus independent state observation proves durable receipt recovery without duplicate effects. Added mandatory owned SIGKILL/restart checkpoints before commit and after acknowledged commit, with state checked before retry. A full criterion packet completes P00-15; the owner explicitly validated the entire Phase 0 gate on 18 November 2026; later AD integration/keys/domain recovery remain their actual separate requirements.

**Next action:** Preserve the owner-accepted invariants while implementing the native directory store. Any new transport/pool/stack/profile needs requalification. Acceptance of this Phase 0 gate does not accept later product features or client conformance.

**Provenance:** Concrete missing driver semantics were closed with actual database, reply-loss and process-crash tests. This is development correctness and completion of a requirement, not a GitHub setup incident.

[docs/validation/p00-15.md](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/docs/validation/p00-15.md>) · [native/babel-store-driver-lab/src/lib.rs](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/src/lib.rs>) · [native/babel-store-driver-lab/tests/database.rs](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/native/babel-store-driver-lab/tests/database.rs>) · [scripts/qualify\_store\_driver.py](<https://github.com/Ise-Tom/Babel/blob/8d21b7b83a76bd45f9564f7a44f7e144c50c9142/scripts/qualify_store_driver.py>)

### I36 · Functional-level scope lacked a complete transition contract and current reference precedence

**Resolved** · Phases 00

The owner-selected 2016 baseline did not yet distinguish current Windows DC OS support from functional levels or enumerate unsupported transition/optional-feature behavior. The pinned upgrade article also says no levels were added since 2016, contradicting the current functional-level table’s 2025 profile.

**Resolution:** Completed the 2016/2016 Linux-hosted design, preserved Windows/Linux/macOS clients, reviewed inherited/optional/2025/FRS/coexistence/rollback boundaries, and documented current-table precedence. CI checks exact matrix/profile consistency, immutable distinct references and the empty advertised-level set. The full design packet is ready for owner validation.

**Next action:** Owner review of the complete P00-11 design gate; qualify actual native levels/features/clients and exact platforms under their separate requirements before advertisement.

**Provenance:** Concrete design/reference conflict found by reading the current upstream source revisions; not a GitHub setup issue.

[docs/functional-level-profile.md](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/functional-level-profile.md>) · [docs/validation/p00-11.md](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/validation/p00-11.md>)

### I37 · Recovery governance lacked enforced complete review and exception records

**Resolved** · Phases 00

The earlier prose outlined transitions but had no versioned complete records or CI guard against omitted recovery controls, expired exceptions, unknown/baseline waivers and observations being relabeled passed. Future design changes could drift without a source-bound consistency report.

**Resolution:** Implemented all six worked transition records, the strict source/digest-bound checker and required CI artifact. Added negative tests for recovery, evidence invalidation, review material, exact UTC expiry, unknown/phase-gate/baseline waivers and false outcomes. Completed the original Phase 0 governance criterion packet.

**Next action:** Owner review of P00-10; preserve the review contract and implement/test real runtime state machines at their native phase gates. Passing record structure does not authenticate review identity or prove recovery.

**Provenance:** Development design-integrity gap resolved with concrete CI/tooling and full criterion evidence; not an account/hosting incident.

[docs/phase-00-governance.md](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/docs/phase-00-governance.md>) · [scripts/check\_phase0\_contract.py](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/scripts/check_phase0_contract.py>) · [tests/test\_phase0\_contract.py](<https://github.com/Ise-Tom/Babel/blob/380d564183b9217acbde16476658fe003cf72338/tests/test_phase0_contract.py>)

### I38 · Optimized arithmetic and observed native build protections lacked an explicit qualification gate

**Resolved** · Phases 00

The release profile inherited disabled overflow checks, while current host/compiler/ELF facts were not bound to the exact tested parser artifact. The original Phase 0 parser/toolchain gate also lacked a complete platforms/alternatives/maintenance exit packet.

**Resolution:** Enabled release overflow checks with a real debug/release failure test. Added compiler/host/lock/binary-bound evidence, parser dependency/FFI guards and actual PIE/full-RELRO/NX-stack checks to required CI, plus the full original criterion packet.

**Next action:** Owner review of P00-04; keep the profile bounded and requalify toolchain/target/dependency changes. Native AD and client behavior retain their separate requirements.

**Provenance:** Concrete development/build/distribution gap verified against existing code and closed with negative regression tests; not a GitHub setup issue.

[docs/native-parser-baseline.md](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/native-parser-baseline.md>) · [scripts/qualify\_parser\_baseline.py](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/scripts/qualify_parser_baseline.py>) · [native/babel-ldap/tests/toolchain.rs](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/native/babel-ldap/tests/toolchain.rs>)

### I39 · Notice verification could miss omitted inventory entries and standalone HTML lacked retained full terms

**Resolved** · Phases 00

The verifier checked only listed files. Dropping a file/package entry could therefore escape self-manifest checks, and the standalone dashboard did not retain the full project license and applicable build-tool notice text.

**Resolution:** Require complete file/package accounting, mandatory project/Rust terms, no symlink roots/trees/manifests, and the original pre-archive manifest digest at extraction. Retain full project/esbuild terms inside inert dashboard HTML and block newly bundled runtime inputs until their notice policy is reviewed. Retain actual GNU runtime copyright/LGPL/GPL terms as well as Cargo/Rust terms, without broadening the Cargo license policy.

**Next action:** Owner review of P00-06; re-evaluate actual contents before broader distributions. Keep specification/image/fixture rights under P00-16.

**Provenance:** Concrete development/build/distribution gap verified against existing code and closed with negative regression tests; not a GitHub setup issue.

[docs/licensing-and-redistribution.md](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/docs/licensing-and-redistribution.md>) · [scripts/collect\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/scripts/collect_native_notices.py>) · [tests/test\_native\_notices.py](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/tests/test_native_notices.py>) · [dashboard/build.mjs](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/dashboard/build.mjs>)

### I40 · Authored template-placeholder text could consume a later dashboard build replacement

**Resolved** · Phases 00

Sequential template replacement scanned already inserted authored data. Literal placeholder text in a title could consume a later replacement and break the generated dashboard data/script. This was a build correctness defect in repository-controlled document content.

**Resolution:** Use one-pass replacement over the original HTML template, with escaped inert notice text. A regression preserves all authored placeholder tokens and the complete embedded JSON while inserting the actual script.

**Next action:** Preserve the one-pass substitution and escaping when adding new template slots. This repair does not change requirement or capability acceptance.

**Provenance:** Concrete development/build/distribution gap verified against existing code and closed with negative regression tests; not a GitHub setup issue.

[dashboard/build.mjs](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/dashboard/build.mjs>) · [dashboard/tests/build.test.mjs](<https://github.com/Ise-Tom/Babel/blob/900a24e7cd38957905d00f628e0b5445511ae52d/dashboard/tests/build.test.mjs>)

### I41 · Earlier state draft conflated immutable SIDs, ordered ACLs, propagation and token freshness

**Resolved** · Phases 00

The draft could suggest an unchanging SID across domain moves, global deny-first evaluation, immediate inheritance/revocation and invalidity of every group cycle. Those assumptions would lead to incorrect native authorization behavior.

**Resolution:** Replaced draft assumptions with pinned GUID/SID move exceptions, ordered access checks, hidden-filter semantics, asynchronous inheritance and separate GC/token freshness, with nine worked design cases. Native implementation remains its own gate.

**Next action:** Owner validation of the full Phase 0 design packet; qualify actual native/client/fault behavior under its implementation gates.

**Provenance:** Concrete design/reference interpretation gap found by inspecting actual readable publisher editions; resolved at the design layer only, not a GitHub setup incident.

[docs/validation/p00-02.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-02.md>) · [docs/adr/0005-directory-and-replication-invariants.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/adr/0005-directory-and-replication-invariants.md>) · [lab/state-security-contract.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/state-security-contract.json>)

### I42 · Draft replication conflict rules needed distinct attribute, link and name procedures

**Resolved** · Phases 00

A generic version/time/origin comparator misses attribute wrap/half-range rules, linked lifetimes, little-endian GUID comparison and the name timestamp/object-GUID conflict rule. Unqualified cursor/restore assumptions could advertise unseen data.

**Resolution:** Pinned actual DRSR/ADTS rules and eleven worked cases, distinguishing scalar/link/name algorithms, safe progress, deletion repair, invocation epochs and RID/retention quarantine. No unimplemented runtime comparator is labeled passing.

**Next action:** Owner validation of the full Phase 0 design packet; qualify actual native/client/fault behavior under its implementation gates.

**Provenance:** Concrete design/reference interpretation gap found by inspecting actual readable publisher editions; resolved at the design layer only, not a GitHub setup incident.

[docs/validation/p00-03.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/validation/p00-03.md>) · [docs/adr/0005-directory-and-replication-invariants.md](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/docs/adr/0005-directory-and-replication-invariants.md>) · [lab/state-security-contract.json](<https://github.com/Ise-Tom/Babel/blob/2989ed476e57297f729d0e3dffd89a703e4175ac/lab/state-security-contract.json>)

## Feature catalog

Implementation states are explicit scoped claims. Related requirements, design and CI do not imply completion. Full capability acceptance is separate from scoped requirement acceptance.

| Feature | Capability | Implementation | Scope | Acceptance evidence |
| --- | --- | --- | --- | --- |
| [PLAT-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency | planned | The existing parser lab has a completed Linux x86\_64 GNU compiler/binary qualification packet \(P00-04\), pending owner review. Full domain-server installation and operation remain unimplemented. | Clean Linux host provisions a domain; Windows client joins, authenticates and applies GPO; admin API/UI operate with no Windows server present |
| [PLAT-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Fresh-host install, reboot and interrupted-upgrade tests; documented service ordering, DNS/time/firewall prerequisites and explicit data-deletion procedure |
| [PLAT-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Linux host hardening and persistent data integrity | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Verified service identities, minimum required privileges, secret/data file permissions, applicable AppArmor/SELinux policy, filesystem ACL/xattr preservation and backup/restore tests |
| [AD-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore | planned | Full P00-02 identity/schema/ACL/local commit design and P00-11 functional-profile design are prepared for owner validation. Native domain/object/account/password behavior is unimplemented. | Import/export and object/ACL comparison against an isolated Windows AD reference domain; denied-operation cases |
| [AD-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect; declared Linux/macOS identity lookup, enrollment where supported, login/password and Kerberos SSO | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Disposable Windows 11 and Windows Server 2022/2025 clients plus declared Linux/macOS clients; exact editions/builds/packages and platform-specific behaviors pinned in the Phase 0 compatibility matrix |
| [AD-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Positive/negative Windows and Linux client tests, ticket expiry/replay and delegation abuse cases |
| [AD-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog | prototype | Read-only loopback LDAP RootDSE discovery lab; not an AD directory service. | Windows RSAT and standard LDAP clients; paging/filter conformance, unauthorized attributes excluded |
| [AD-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Discovery, stale records, DNS failover, and unsigned-update rejection |
| [AD-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Real Windows client resultant policy, policy version conflict, script distribution and failover tests; document supported replication mechanism |
| [AD-07](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery | planned | Full P00-03 replication/conflict/restore epoch design is prepared for owner validation; no native replica transport, convergence or recovery service is implemented. | Partition/rejoin, concurrent writes, lingering objects, rollback protection and disaster recovery |
| [AD-08](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Supported Microsoft protocol test cases plus real-client workflows; signed/sealed secure channels |
| [AD-09](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Forest/domain trusts, cross-domain authorization, migration and coexistence with existing AD | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Two disposable forests, trust creation/removal, SID filtering, selective authentication and migration rollback |
| [AD-10](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Domain/forest functional levels and FSMO role ownership, transfer and failure recovery | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Explicit supported level matrix, role transfer/seizure, schema and functional-level upgrade tests |
| [IAM-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | UI/API and supported client tests for allowed and denied operations, policy enforcement, account enumeration resistance, password redaction and post-reset authentication |
| [OPS-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Backup/restore, upgrades, rotation, audit export, health and capacity visibility | planned | The P00-15 driver/transaction foundation is owner-accepted; the complete six-transition P00-10 governance contract now has enforced CI consistency and awaits review. Native directory backup/restore/upgrade operations remain unimplemented. | Repeated restore drills, interrupted upgrade, disk-full and certificate-expiry tests |
| [UX-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Accessible web administration and documented automation API/CLI | planned | The project dashboard is development tooling; the domain administration UI/API/CLI are not implemented. | Tested admin journeys, WCAG 2.2 AA audit and API authorization matrix |
| [SEC-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account | planned | Full P00-07 boundary/threat/ownership design and P00-02 ordered authorization design are prepared for review. Production privilege enforcement and separation remain unimplemented. | Threat model, privilege matrix, denied-operation integration tests |
| [SEC-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1 | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Protocol downgrade and anonymous access tests with pinned clients |
| [SEC-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Kerberos encryption negotiation, NTLM relay/downgrade tests and documented compatibility impact |
| [SEC-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly | prototype | Standalone Rustls/ring mutual-TLS qualification lab; no LDAP/SASL integration or production TLS selection. | Invalid/expired certificate rejection and live rotation tests; no verification bypass |
| [SEC-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Web/API admin MFA through phishing-resistant authentication, step-up for privileged actions, scoped sessions/tokens, CSRF protection and reauthentication | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Browser/API tests for session expiry/revocation, cross-site attacks, role escalation |
| [SEC-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Crypto design review, secret/log scan, rotation and backup recovery drills |
| [SEC-07](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Spray, brute-force, denial-of-service and recovery abuse tests |
| [SEC-08](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion | prototype | Input and session limits for the current loopback LDAP component only. | Parser fuzzing, adversarial query tests and memory/CPU ceilings |
| [SEC-09](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Audit completeness, redaction and external collector outage tests |
| [SEC-10](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore | partial | Development supply-chain and CI safeguards; production services/update/recovery are unqualified. | Packaging review, dependency/secret scans, artifact verification and restore exercise |
| [SEC-11](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/requirements.md>) | Minimize identity data, encrypt backups, document retention/deletion and data residency | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Privacy review, retention/restore tests and synthetic-only CI fixtures |
| [A-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | WebAuthn/FIDO2 passkeys and hardware security keys for administrator login; multiple authenticators and secure enrollment | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Reject origin/RP mismatch and replay; audited enrollment, replacement and revocation; keep usable accessible recovery |
| [A-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Smart-card/certificate-based domain logon through PKINIT and compatible hardware-backed keys | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Real supported Windows/Linux client logon, certificate mapping, revocation, expiry and downgrade tests; a web passkey is not automatically a Kerberos credential |
| [A-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Recovery hardened against helpdesk impersonation, SIM swapping and MFA fatigue | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | No security questions or SMS-only privileged recovery; dual review for Tier 0, notifications and synthetic social-engineering exercises |
| [A-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Password protection beyond basic policy: locally checked breached/common passwords, contextual exclusions, password history and supported fine-grained policies | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | No raw passwords or unsalted password hashes sent externally; test supported protocol reset/change paths and directory ACLs; avoid routine forced expiry absent a requirement or compromise |
| [A-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Adaptive throttling and credential-stuffing/password-spray detection across replicas | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Bound attacker-induced lockout and distributed attempts; test NAT/shared networks, emergency access and behavior during collector/WAN failure |
| [A-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Authentication strength policies, session inventory and bounded revocation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Distinguish phishing-resistant, certificate and password-only authentication; test web logout, API revocation and ticket lifetimes separately; document where legacy protocols cannot enforce MFA |
| [B-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Just-in-time and just-enough privilege with expiring grants | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Enforce expiration even when workflow workers fail; test nested membership, tickets with cached privileges, replication delays and denied access after expiry |
| [B-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Dual approval and separation of duties for Tier 0 membership, trusts, replication rights, backup export and key operations | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Approver cannot approve their own change or bypass through API/bulk import; audit request, approval, execution and cancellation |
| [B-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Privileged access workstations and tiered administration guidance | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Publish tested workstation/server management baselines and safe delegation; directory administrators do not use privileged credentials on lower-trust endpoints |
| [B-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Emergency break-glass access with separate custody and monitored use | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Rehearse access without the normal IdP/MFA provider, alert every use, rotate afterward and protect against emergency-account lockout or silent persistence |
| [B-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Effective-permission explorer and privilege-path analysis | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Explain ACL inheritance, nested groups, delegation, SID history and trust boundaries; validate against actual access decisions and redact data from unauthorized viewers |
| [B-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Periodic access certification, ownership and orphaned-privilege cleanup | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Review privileged/service/stale accounts with accountable owners; preview removals and preserve recovery paths; do not automatically delete based on last-login alone |
| [C-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Windows LAPS-compatible local administrator password rotation and retrieval | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Qualify the exact client/schema/encryption profile; tightly restrict password reads, audit retrieval, rotate after use and test offline endpoints |
| [C-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Managed service accounts, including gMSA compatibility where selected | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Validate supported KDS/key derivation and authorized password retrieval, rollover and real Windows services; never emulate compatibility by exposing shared plaintext secrets |
| [C-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Linux service identities, keytab lifecycle and supported workload identity integrations | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Scoped principals, minimal keytab readers, short lifetimes where supported, automated rotation and revocation; no long-lived administrator credentials in workloads |
| [C-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Joiner/mover/leaver workflows, ownership and deprovisioning reconciliation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Preview group/ACL changes, require approval for sensitive roles, disable access through each integrated system and report failures; measure ticket/session revocation limits |
| [C-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Delegated self-service password change/reset, account recovery and group requests | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Validate identity proof, factor replacement and approval boundaries; no account enumeration, unaudited helpdesk impersonation or permanent recovery bypass |
| [C-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Signed, versioned provisioning integrations such as SCIM and an external secrets manager | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Treat external sources as scoped authorities; test replay, duplicate events, malicious attributes, tenant mix-ups and outages; do not store arbitrary application secrets in directory attributes |
| [D-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | GPO version history, diffs, independent approval and staged OU rollout | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test both directory and SYSVOL versions/ACLs, conflict resolution and a rollback that actually restores client behavior; audit all management paths |
| [D-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Effective policy preview, precedence and resultant-policy troubleshooting | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Model security filtering, inheritance, enforced/block settings and WMI filters; compare predictions with real Windows resultant policy and expose unsupported settings |
| [D-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Tested hardening templates for Windows and Linux | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Cover supported firewall, audit, authentication and host protections; Linux policy delivery needs an explicit supported agent/configuration integration rather than assuming Windows GPO applies |
| [D-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Policy integrity/drift detection, safe script distribution and privileged policy ownership | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Detect out-of-band SYSVOL edits and dangerous scripts; verify applicable signatures and permissions without inventing incompatible GPO wire formats |
| [D-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Device posture and conditional-access integrations | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Qualified endpoint attestation, encryption/patch posture and device identity; define freshness, spoof resistance and fail behavior; posture claims alone must not grant Tier 0 access |
| [D-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Support for endpoint credential protections and application-control baselines | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test compatible Credential Guard, protected-user, LSA protection and application-control profiles; endpoint edition/features determine availability, and enforcement is not performed by the DC alone |
| [E-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Compatibility-aware legacy authentication retirement | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Discover NTLM/RC4/unsigned dependencies, offer a migration report and enforce expiring scoped exceptions; first-release secure defaults stay in force |
| [E-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Kerberos delegation, ticket and principal hardening | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Detect unsafe unconstrained/resource-based delegation, SPN conflicts, weak service secrets and excessive ticket lifetimes; test constrained delegation and protected accounts on real clients |
| [E-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Trust quarantine and cross-forest entitlement inspection | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Validate SID filtering, selective authentication, name suffix routing and SID-history migration boundaries; require approval and audit trust changes |
| [E-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Certificate enrollment and PKI integration, with any AD CS-compatible role separately qualified | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test template/enrollment ACLs, identity mapping, SAN constraints, approval, issuance/revocation and renewal; protect CA keys separately and reject escalation-prone configurations |
| [E-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Certificate/key inventory, expiry forecasting and automated rotation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Exercise TLS, PKINIT, service and trust material separately; support safe overlap, CRL/OCSP outages and core/provider-specific lifecycle constraints |
| [E-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Protocol exposure control and network segmentation templates | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Enumerate actual DNS/LDAP/Kerberos/SMB/RPC and replication flows, narrow dynamic RPC ranges where supported, test firewall changes and preserve diagnostic access |
| [F-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Reviewed systemd sandboxing, capability reduction and AppArmor/SELinux profiles | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test per-role requirements, upgrades and restore; document any privileged native-core/OS operations instead of promising all services run unprivileged |
| [F-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Host security posture: supported Secure Boot, measured boot and disk encryption | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Document provisioning and recovery-key custody; boot attestation must be verified externally; disk encryption does not protect a running compromised DC |
| [F-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Hardware-backed key custody through HSM/TPM or a supported external KMS | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Qualify each key type and key-provider API; do not claim AD password verifiers or every Kerberos key can be moved into an HSM; test latency, outage and recovery |
| [F-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Resource isolation and DoS controls per service/peer | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Exercise expensive LDAP searches, nested groups, parser inputs, connection exhaustion, audit floods and replication queues under limits without starving legitimate login |
| [F-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Hardened Linux storage, syscall and network profiles for optional container packages | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Validate ACL/xattrs, persistent state, time/DNS, service discovery and restore; no unreviewed privileged-container default; VM/bare-metal hosting stays supported |
| [F-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Linux host baseline drift and agent/update integrity | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Detect changed service units, executable/config permissions and obsolete kernels/packages; verify updates and rehearse service continuity during host maintenance |
| [G-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Structured, correlated audit export to SIEM/syslog with externally protected storage | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Version schemas, synchronize time, track gaps, redact credentials and enforce export RBAC; an append-only local file is not tamper-proof against root |
| [G-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Detection for replication abuse, suspicious DC registration, ACL escalation and privileged group changes | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Labeled authorized lab scenarios, expected alerts and false-positive measurements; some credential theft leaves no definitive directory-only signal |
| [G-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Detection for ticket abuse, password sprays, abnormal service-ticket requests and trust/GPO persistence | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Correlate KDC, directory and endpoint signals; do not promise reliable golden/silver-ticket detection solely from server logs |
| [G-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Deception identities and monitored canary credentials | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Isolate synthetic decoys with no real privileges, prohibit use in normal workflows and test safe high-confidence alert handling |
| [G-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Investigation views: identity timeline, effective permissions and configuration history | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Preserve provenance and access controls; reproducible evidence export, chain of custody and bounded retention; do not expose password hashes/tickets in UI |
| [G-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Detection engineering with replayable synthetic event fixtures | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Version rules, test sensitivity/precision, alert latency and collector failure; publish thresholds and capacity overhead at the 10k-identity target |
| [H-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Audited response workflows for account/device disable, trust suspension and service-key rotation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Scope, preview, approval, idempotency and a rescue path; automated detections cannot globally lock out a domain without a separate safety decision |
| [H-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Domain-compromise recovery plan covering ticket-signing, machine, service, trust and administrator credentials | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Sequence native-core/provider-specific rotations, including safe double rotation of Kerberos signing keys; prove clean restores and ticket invalidation within documented limits |
| [H-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Replica quarantine and controlled reintroduction after suspected compromise | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Protect evidence, revoke replication trust safely, avoid contaminating clean replicas and test topology/role recovery; partitioning alone does not remove stolen credentials |
| [H-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Recovery-safe security state restoration | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Reconcile revoked identities, changed privileges, deleted objects and key epochs after restoring older backups; prevent silently reactivating known-compromised access |
| [H-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Tested response playbooks and tabletop exercises | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Include lost MFA provider, stolen backup, compromised maintainer, ransomware and malicious insider; track response time, operator mistakes and retained evidence |
| [I-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Read-only/limited-secret branch controller profiles when explicitly implemented by the native core | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Qualify exact RODC/password replication policy semantics, cached-secret restrictions, theft impact and credential reset procedure; never market a writable replica as read-only |
| [I-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Immutable/offline encrypted backups with split custody and recovery-key escrow | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Separate backup administration, restoration quorum where appropriate, retention verification and regular clean-room restores without depending on the failed domain |
| [I-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Site isolation, failover and revocation-risk visibility | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Surface stale replication, stale policy and uncertain revocation; test WAN partitions and clock/DNS faults without claiming global immediate consistency |
| [I-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Security operation budgets and safe degraded modes | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Define authentication, MFA, KMS, CA and audit failure behavior separately; backpressure noisy services, alert on queue loss and never silently bypass admin MFA |
| [I-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Recovery environment integrity and safe backup validation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Scan and validate restore media, signed tooling and host images; rehearse total loss and schema incompatibility; ordinary VM snapshot rollback is not assumed safe for a DC |
| [J-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | OIDC/OAuth2 and SAML federation through separately qualified modules | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Validate issuer/audience, redirect URI, nonce/state/PKCE, signing keys, claim minimization, logout and key rollover; modern SSO does not replace AD protocols |
| [J-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Network access integrations such as RADIUS/EAP-TLS | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Qualify identity/certificate mapping, mutual authentication and revocation behavior; avoid insecure password fallback and document external network-device dependencies |
| [J-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Attribute-level privacy, scoped directory search and data-export controls | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Denied attribute/search tests across LDAP and UI/API, purpose-scoped access and export audit; avoid breaking required AD discovery semantics |
| [J-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Retention, deletion and legal-hold policy for identity and audit data | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Reconcile tombstones/backups/security investigations and residency obligations; no claim of GDPR or other regulatory certification from feature availability |
| [J-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Explicit multi-organization/tenant security boundaries | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Prefer independent domains/forests or deployments for hostile tenants; a shared writable DC and UI RBAC do not create hard tenant isolation; independently assess any shared architecture |
| [K-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Reproducible packages/images, signed provenance/SBOM and dependency license/CVE inventory | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Independently rebuild, compare artifacts and verify expected signer/workflow identities; document unreproducible parts and dependency exception expiry |
| [K-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Secure update metadata with rollback/freeze protection and key recovery | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Verify signatures, version/expiry and release channel; rehearse signing-key compromise, offline updates and supported emergency rollback without bypassing checks |
| [K-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Synthetic isolated workloads for LDAP/RPC/Kerberos/DNS and policy handling; compare observable semantics with a licensed AD lab and retain minimized regression cases |
| [K-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Property-based checks or formal analysis for bounded high-risk logic | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Prioritize authorization, grant expiry, replication conflict handling and key transitions; publish model assumptions rather than claiming a formally secure whole server |
| [K-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Public scope/safe-harbor terms, private intake and supported-version response; remediate findings with regression tests and publish appropriate summaries |
| [K-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Hardened release governance and maintainer continuity | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Two-person sensitive release review, scoped OIDC, protected builders/refs, signer rotation and tested maintainer-loss recovery; use no privileged fork runners |
| [L-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Security posture dashboard with actionable, evidence-backed findings | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Show observation time, affected identities/hosts, severity rationale and safe remediation; never present missing telemetry as healthy |
| [L-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Policy simulation and explainable access decisions | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Preview bulk ACL/GPO/role changes against representative identities and devices; show stale/unknown data and compare predictions with actual enforcement |
| [L-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Safe bulk operations with scope preview, dry run, idempotency and compensating actions | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Independent approval for mass privileged changes; test partial failure and rollback limits; no plaintext credential exports |
| [L-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Accessible secure enrollment/recovery and understandable authentication errors | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Keyboard/screen-reader tests and usability studies include recovery and approvals; messages help legitimate users without revealing account existence or secrets |
| [L-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Security exception register and policy-as-code change review | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Every exception has owner, justification, scope, expiry and audit; reject stale exceptions, detect out-of-band drift and protect policy signing/approval keys |
| [L-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/security-roadmap.md>) | Operator training, trustworthy runbooks and versioned security baselines | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Rehearse common and emergency tasks with new administrators; publish prerequisite/compatibility warnings and measure unassisted completion and recovery success |
| [PATCH-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Continuous hardware/OS/software inventory and update applicability assessment | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Compare installed versions, missing updates, reboot state, device identity and observation timestamps with native tools; distinguish fresh, stale, unknown and unsupported devices |
| [PATCH-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Trusted patch/vulnerability catalog with dependencies, supersedence and known issues | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Reproduce applicable/not-applicable decisions, including vendor backports; correlate vendor severity, CVEs and known-exploited data without treating version-string matches as proof of vulnerability |
| [PATCH-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Windows OS, Linux package/kernel and explicitly selected third-party application patching | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Use supported Windows Update APIs and supported distribution package managers such as APT/DNF; test vendor prerequisites, licenses, conflicts and package signatures; GPO update settings alone are insufficient |
| [PATCH-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Dynamic device groups, targeting previews and fixed campaign membership snapshots | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Scope by approved inventory/domain/OU/tag criteria; show sample devices, exclusions and counts; audit later membership changes and prevent silent expansion of an approved rollout |
| [PATCH-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Canary/pilot/production rings with configurable dwell, health checks, rollout limits and automatic pause | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Inject a bad update or failed health check; later rings halt at the approved threshold; low report coverage cannot count as successful promotion |
| [PATCH-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Maintenance windows, deadlines, user notifications, reboot deferral and forced-reboot controls | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test time zones/DST, sleeping devices, user sessions, grace periods, blackout windows and missed windows; unsupported reboot suppression must be surfaced rather than silently overridden |
| [PATCH-07](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Preflight disk/power/network checks, dependency handling and application/service-aware installation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test low disk, pending reboot, conflicting package transaction, required services, application health and interrupted install; mark blocked devices separately from failed ones |
| [PATCH-08](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Bandwidth-aware content distribution with authenticated site relays and approved offline import | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Verify vendor signatures plus approved content digests, resume interrupted transfers, deduplicate/cache payloads and apply per-site/concurrency limits; a relay may serve content but cannot authorize deployment |
| [PATCH-09](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Durable campaign orchestration and disconnected endpoint recovery | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Idempotent job identifiers, bounded retries/backoff, resume after agent/controller restart, cancel/expiry checks before execution and reconciliation after lost acknowledgments; no unbounded queued command execution |
| [PATCH-10](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Independent post-install verification of installed version, reboot completion and service health | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Separate downloaded, installed, reboot-pending, verified, failed, paused and unknown states; a zero exit code or missing device report is not proof of remediation |
| [PATCH-11](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Safe uninstall/rollback or tested recovery per update class | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Advertise rollback only where the vendor supports it; demonstrate restore/reimage/forward-fix for irreversible changes; preserve operator instructions and abort criteria before rollout |
| [PATCH-12](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Emergency remediation and risk-based prioritization | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Prioritize exploited/exposed assets with transparent evidence; exceptional maintenance/approval overrides need explicit scope, independent approval, expiry and immutable audit export |
| [PATCH-13](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Compliance dashboards, remediation SLAs, exception register and report export | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Show coverage denominator, overdue/stale/offline devices, unsupported/EOL products and expiring exceptions; track time-to-remediate by risk; do not report unknown endpoints as compliant |
| [PATCH-14](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Separate catalog approval, targeting, execution, exception and reporting rights; test unauthorized cross-group actions, approver self-approval, API bypass and scoped automation credentials |
| [PATCH-15](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/patch-management-roadmap.md>) | Availability-aware server and domain-controller maintenance | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Serialize DC maintenance by site/failure domain, preserve DNS/KDC/replication quorum where applicable, respect service topology and recovery checks; a workstation policy must never reboot every DC together |
| [REMOTE-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Authenticated desktop and terminal sessions to enrolled, authorized devices | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Real Windows/Linux session tests including headless Linux, NAT/proxy/relay paths and explicit unsupported configurations; choose maintained protocols/components rather than inventing a remote-control protocol |
| [REMOTE-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Attended support with visible user consent and an immediate disconnect action | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Reject denied/expired consent and misleading session requests; show operator identity and active session; no covert access mode |
| [REMOTE-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Separately approved unattended administration | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Explicit device policy, scoped operator rights, time-bounded grants, admin MFA/step-up and maintenance restrictions; no unattended access inferred from domain membership |
| [REMOTE-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Session control, audit and sensitive-channel separation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Record actor/device, approvals, start/end and actions available to the operator; independently authorize elevation, clipboard, transfer and recording; test clipboard/drive redirection restrictions |
| [REMOTE-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Secure brokering and prompt revocation | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Per-session authorization, authenticated encrypted transport and device verification; no domain-admin credentials in the agent; bounded disconnect after revocation and defined behavior during broker/identity-provider failure |
| [REMOTE-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Safe operation across OS privileges and session states | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test lock screen, user switching, terminal privilege escalation, reconnect and concurrent operators; honor OS security boundaries and document elevation requirements; no bypass of OS credential protection |
| [FILE-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Explicit server-originated uploads to one or many selected endpoints | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Preview exact recipients, content digest, size, expiry and destination; approve bulk/sensitive delivery and prevent recipient expansion after approval |
| [FILE-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Secure staging, integrity and recipient verification | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Authenticate uploader/source/device, encrypt in transit and protect staged content at rest; verify hashes against authenticated metadata, not an attacker-supplied hash alone |
| [FILE-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Destination and privilege restrictions | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Per-role/device allowed paths, canonicalization, symlink/race and traversal defenses, disk quota, ownership/mode preservation rules and explicit overwrite policy; prohibit silent writes into privileged startup/system locations |
| [FILE-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Resumable, bandwidth-limited transfer with accurate receipts | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Test interruptions, duplicate requests, stale jobs, full disks and agent restarts; stage then atomically finalize where supported; report partial/expired/failed/verified states and clean up abandoned content |
| [FILE-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Content policy, separate execution and audit | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Apply approved type/size/malware policies without promising scanners detect every threat; uploaded files are not automatically executed; record who sent what to which device and destination, without exposing confidential file contents in logs |
| [EDR-01](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Dedicated installed sensor/agent module with secure enrollment and update lifecycle | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Signed/verifiable packages and policy, mutual authentication, per-device identity/revocation, staged updates and rescue/uninstall flow; module isolation from remote support and patch execution |
| [EDR-02](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | OS-specific endpoint telemetry | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Qualified process lineage, executable hashes/signatures, network connections, file and relevant persistence/security events using supported APIs; document blind spots, event loss and OS/privilege prerequisites |
| [EDR-03](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Behavioral detection, indicator matching and versioned rules | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Labeled synthetic scenarios, expected detections, measured false positives/negatives and tuning/exclusion audit; verify rules and bound their CPU/memory cost; no claim of universal malware detection |
| [EDR-04](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Investigation and privacy-scoped evidence collection | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Process/device timeline, alert correlation and case workflow; approved minimal evidence capture with provenance, hashes, access controls and retention; no indiscriminate memory, credential or user-file collection |
| [EDR-05](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Authorized response: stop/quarantine malicious processes/files and isolate a device | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Separate response RBAC, approvals and bounded automation; preserve narrow authenticated management/recovery paths, define reboot persistence and test release from isolation; protect DC/service topology from fleet-wide lockout |
| [EDR-06](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Tamper resistance and trustworthy sensor health | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Detect stopped/stale sensors, policy/signature changes and telemetry gaps; audit exceptions and uninstall; qualify protections per OS and acknowledge a compromised kernel/root can defeat local evidence |
| [EDR-07](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | SIEM/SOAR integration and safe automated response | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Authenticated scoped connectors, deduplicated alerts, expiring/idempotent actions and auditable decisions; false detections must not autonomously disable the whole domain or isolate the whole fleet |
| [EDR-08](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/endpoint-operations-roadmap.md>) | Offline operation and resilience under telemetry/provider outages | planned | No functional implementation is claimed. Related design/tooling does not qualify this capability. | Bounded encrypted event buffering, trusted cached rules, freshness/loss indicators and controlled reconnect; avoid login disruption, disk exhaustion and treating missing events as a healthy device |

### PLAT-01 implementation scope

The existing parser lab has a completed Linux x86\_64 GNU compiler/binary qualification packet \(P00-04\), pending owner review. Full domain-server installation and operation remain unimplemented.

**State:** planned · runtime\_lab

**Implemented subset:** No product behavior claimed

**Missing/unqualified:** Qualified installation/service lifecycle of all native Linux server roles; Actual domain creation, authentication, GPO and administration without a Windows server; Production packaging and supported-platform evidence

**Evidence:** W50 (implementation journal)

Full capability acceptance: not recorded

### AD-01 implementation scope

Full P00-02 identity/schema/ACL/local commit design and P00-11 functional-profile design are prepared for owner validation. Native domain/object/account/password behavior is unimplemented.

**State:** planned · product

**Implemented subset:** No product behavior claimed

**Missing/unqualified:** Native domain/forest creation and qualified functional-level behavior; Stable GUID/SID/schema/ACL and account/group/password semantics; Client/reference denied-operation and recycle/restore qualification

**Evidence:** W49 (implementation journal); W52 (implementation journal)

Full capability acceptance: not recorded

### AD-04 implementation scope

Read-only loopback LDAP RootDSE discovery lab; not an AD directory service.

**State:** prototype · runtime\_lab

**Implemented subset:** Bounded BER/LDAP request decoding and TCP framing; Read-only RootDSE and bounded presence/objectClass equality/boolean filters; Credential rejection, connection/session budgets and safe errors

**Missing/unqualified:** Stored directory entries and attribute-level access checks; Authentication and password operations; TLS/LDAPS integration; AD controls, paging/referrals and global catalog; Windows/Linux/macOS directory conformance

**Evidence:** W02 (implementation journal); W03 (implementation journal); W04 (implementation journal); W05 (implementation journal); W06 (implementation journal); W07 (implementation journal); W08 (implementation journal); W17 (implementation journal)

Full capability acceptance: not recorded

### AD-07 implementation scope

Full P00-03 replication/conflict/restore epoch design is prepared for owner validation; no native replica transport, convergence or recovery service is implemented.

**State:** planned · product

**Implemented subset:** No product behavior claimed

**Missing/unqualified:** Authenticated DRS peer/NC authority and actual wire replication; Native attribute/link/name conflict, deletion and safe-cursor handling; Multi-site partition/rejoin, restore/VM/RID/retention fault qualification

**Evidence:** W53 (implementation journal)

Full capability acceptance: not recorded

### OPS-01 implementation scope

The P00-15 driver/transaction foundation is owner-accepted; the complete six-transition P00-10 governance contract now has enforced CI consistency and awaits review. Native directory backup/restore/upgrade operations remain unimplemented.

**State:** planned · experiment

**Implemented subset:** No product behavior claimed

**Missing/unqualified:** Native directory backup/restore and upgrade; Domain credential/key rotation; Product health, audit export and measured capacity

**Evidence:** W27 (implementation journal); W28 (implementation journal); W40 (implementation journal); W44 (implementation journal); W46 (implementation journal); W48 (implementation journal)

Full capability acceptance: not recorded

### UX-01 implementation scope

The project dashboard is development tooling; the domain administration UI/API/CLI are not implemented.

**State:** planned · engineering

**Implemented subset:** No product behavior claimed

**Missing/unqualified:** Delegated domain administration API and CLI; Identity/password/GPO operator UI; Product accessibility and administrator journey qualification

**Evidence:** W14 (implementation journal); W16 (implementation journal); W18 (implementation journal); W38 (implementation journal); W41 (implementation journal); W45 (implementation journal)

Full capability acceptance: not recorded

### SEC-01 implementation scope

Full P00-07 boundary/threat/ownership design and P00-02 ordered authorization design are prepared for review. Production privilege enforcement and separation remain unimplemented.

**State:** planned · product

**Implemented subset:** No product behavior claimed

**Missing/unqualified:** Native operation/attribute/control authorization and privilege separation; Protected credential/key/replica/recovery authority; Denied-operation and independent production assessment evidence

**Evidence:** W52 (implementation journal); W54 (implementation journal)

Full capability acceptance: not recorded

### SEC-04 implementation scope

Standalone Rustls/ring mutual-TLS qualification lab; no LDAP/SASL integration or production TLS selection.

**State:** prototype · experiment

**Implemented subset:** Explicit trust root and mandatory certificate validation in a bounded TLS 1.2/1.3 lab; Certificate identity/trust/time/purpose, obsolete-protocol and unapproved-cipher rejection tests; Independent OpenSSL probes, exporter prerequisites, malformed-record fuzzing and separate coverage gate

**Missing/unqualified:** LDAP/StartTLS and SASL/EPA channel-binding integration; Live certificate rotation/revocation and protected key/provider custody; Real Windows/Linux/macOS client and production fault/load qualification

**Evidence:** W42 (implementation journal)

Full capability acceptance: not recorded

### SEC-08 implementation scope

Input and session limits for the current loopback LDAP component only.

**State:** prototype · runtime\_lab

**Implemented subset:** Bounded LDAP filter depth, node/value and frame/session budgets; Malformed-input, negative/property tests and sanitizer fuzz smoke

**Missing/unqualified:** Stored-query/index cost controls; Kerberos, DNS, RPC and replication limits; Distributed resource exhaustion qualification

**Evidence:** W02 (implementation journal); W05 (implementation journal); W07 (implementation journal); W08 (implementation journal); W17 (implementation journal)

Full capability acceptance: not recorded

### SEC-10 implementation scope

Development supply-chain and CI safeguards; production services/update/recovery are unqualified.

**State:** partial · engineering

**Implemented subset:** Scoped CI permissions, required quality/security gates and source inventory; Pinned dependencies, secret/advisory/license scans and SBOM; Verified source/dashboard artifacts and prerelease preflight; Actual project/runtime-crate/Rust-library notice packaging and extraction verification; Source-bound Phase 0 change/recovery review and expiry/baseline consistency checks; Source-bound native compiler/ELF qualification, optimized overflow checks and complete notice/distribution guards; Source-pinned state/security design integrity and restrictive reference/asset accounting

**Missing/unqualified:** Production Linux service hardening; Signed product update and installer qualification; Exercised security response and domain restore

**Evidence:** W01 (implementation journal); W09 (implementation journal); W10 (implementation journal); W13 (implementation journal); W23 (implementation journal); W30 (implementation journal); W43 (implementation journal); W44 (implementation journal); W48 (implementation journal); W50 (implementation journal); W51 (implementation journal); W54 (implementation journal); W55 (implementation journal); W56 (implementation journal)

Full capability acceptance: not recorded

## Recorded CI observation

[Evidence snapshot CI](<https://github.com/Ise-Tom/Babel/actions/runs/44408618949>): passed, 14 passing checks when checked. Verified main baseline: PR \#29 merged and 525ac74 passed all 14 CI jobs. This PR prepares full original P00-02/P00-03/P00-07 design gates for owner review, pins public references and records remaining use-rights/lab/crypto/response gaps. No new owner acceptance, native AD conformance or independent assessment is inferred.

[Dashboard maintenance and interactive build guide](<https://github.com/Ise-Tom/Babel/blob/d1aabf492bca13a7820d16e716488a62297c93f3/docs/project-dashboard.md>)

Generated from reviewed repository facts. This report does not query live CI in the browser. Edit the source facts through a PR; the dashboard-live branch is owned by automation.
