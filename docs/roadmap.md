# Native Babel delivery roadmap

Design baseline, not implementation status. Babel builds its own AD-compatible
core on Linux. The first production release includes identity/password management,
domain join, LDAP/GC, Kerberos/PAC, DNS, SMB/RPC/Netlogon, GPO/SYSVOL, trusts,
functional levels and recoverable multi-site replication. No Samba runtime is
required. Reviewed libraries remain allowed; no custom cryptography is planned.

Every phase now has a complete [design/requirements specification](phases/README.md).
The phase requirements refine and trace the 130 existing global capability
IDs. Existing CI now also checks the bounded Rust LDAP lab slice; full domain and
endpoint acceptance remains outstanding. See [progress](phase-01-progress.md). Dates, staffing, cost and
production readiness require the decisions and evidence listed below.

| Phase | Design, scope and requirements | Delivery boundary |
| --- | --- | --- |
| 00 | [Contract, native-core design and laboratory](phases/phase-00.md) | First production core contract |
| 01 | [Native core and end-to-end development slice](phases/phase-01.md) | First production core contract |
| 02 | [Complete directory and AD interoperability contract](phases/phase-02.md) | First production core contract |
| 03 | [Multi-site replication, durability and recovery](phases/phase-03.md) | First production core contract |
| 04 | [Security, capacity and administrator qualification](phases/phase-04.md) | First production core contract |
| 05 | [First production release and controlled deployment](phases/phase-05.md) | First production core contract |
| 06 | [Sustained operations and maintenance](phases/phase-06.md) | Ongoing operations / advanced security |
| 07 | [Strong identity and privileged administration](phases/phase-07.md) | Ongoing operations / advanced security |
| 08 | [Posture, certificate/federation services and detection](phases/phase-08.md) | Ongoing operations / advanced security |
| 09 | [Containment, key custody and compromise resilience](phases/phase-09.md) | Ongoing operations / advanced security |
| 10 | [Continuous security assurance and trusted delivery](phases/phase-10.md) | Ongoing operations / advanced security |
| 11 | [Endpoint inventory and patch-control foundation](phases/phase-11.md) | Later endpoint services with separate release gates |
| 12 | [Controlled patch campaigns and verified installation](phases/phase-12.md) | Later endpoint services with separate release gates |
| 13 | [Production patch fleet, compliance and resilience](phases/phase-13.md) | Later endpoint services with separate release gates |
| 14 | [Remote desktop and terminal access](phases/phase-14.md) | Later endpoint services with separate release gates |
| 15 | [General server-to-device file delivery](phases/phase-15.md) | Later endpoint services with separate release gates |
| 16 | [Native endpoint detection and response](phases/phase-16.md) | Later endpoint services with separate release gates |
| 17 | [Joint fleet qualification and endpoint service release](phases/phase-17.md) | Later endpoint services with separate release gates |

## Delivery and dependency rules

Phases 0–5 are mandatory before the first production identity release. A partial
native LDAP/Kerberos or single-controller preview is not a narrower production
product. Phases 6–10 maintain and expand assurance; continuous operating duties
remain active after their initial readiness gate and do not require waiting a
calendar quarter to start independent design work. Phases 11–17 expand endpoint
management/security after the core is qualified, without replacing identity scope.

Each detailed phase declares entry dependencies, interfaces/state, trust/failure
boundaries, provisional capacity targets and testable requirements. Independent
research/lab work may overlap. Never bypass a prerequisite for production writes,
credential storage, trusted execution or release approval. Advanced features
selected in the first-production compatibility profile move into the Phase 5
release gate; a later phase number does not excuse delaying baseline security.

## Capacity and acceptance

The core target remains 10k users, 10k computers, 2k groups and three sites/six
DCs. The later fleet target is 10k enrolled devices with separately qualified
remote-session, transfer and telemetry concurrency. Hardware figures and new
concurrency/event profiles are proposed engineering targets, not achieved claims.
Ratify them with evidence/ADRs before a feature release; do not silently lower a
target after tests fail. All supported OS/protocol/functional-level matrices must
be explicit. Every OS cannot be inferred from a portable server language.

Every phase exits with requirement-level evidence following the
[validation plan](validation-plan.md). Failures, unknown state, skipped/unrun
cases and simulator-only results stay visible. [Open decisions](decisions.md)
identify the owner and blocked capability for licensing, toolchain/storage,
replication/GPO, supported clients, privacy and infrastructure. Named owners and
paid resources are not invented by this plan.

## Capability contracts and shared design

- [Core/security/capacity requirements](requirements.md) remain the normative baseline.
- [System design](architecture.md) defines component authority, state and failure contracts.
- [Native-core milestones](native-core-plan.md) map the first implementation dependencies.
- [Threat model](threat-model.md) drives negative and abuse tests.
- [Advanced security catalog](security-roadmap.md) preserves all 69 capability IDs.
- [Patch contract](patch-management-roadmap.md) preserves PATCH-01–PATCH-15.
- [Remote/file/EDR contract](endpoint-operations-roadmap.md) preserves all 19 endpoint IDs.
- [CI/CD operation](ci-cd.md) distinguishes current executable checks from future product gates.

## First implementation work

Assign Phase 0 design/security ownership, choose the license/support profile and
fund a reproducible isolated reference lab. Review the native toolchain and
identity/storage/replication ADRs. Introduce only the first bounded native
parser/core slice with matching locked build/property/fuzz/security/packaging
jobs, then extend the scope guard in that same reviewed change. Grow read-only
discovery before persistent credentials, membership and policy behavior. No
placeholder server or always-green future job satisfies a phase requirement.
