# Phase design and requirements index

Design baseline: native AD-compatible core, Linux-hosted services and Windows/Linux
client/agent qualification. These specifications replace the previous summary-only
phase descriptions. Product implementation and acceptance remain outstanding.
Existing CI validates tooling and document integrity; it does not validate AD.

Each of the 18 phases has ten uniquely identified requirements, technical design,
state/interfaces, security/failure behavior, capacity, dependencies and evidence.
The 180 phase requirements refine and trace all 130 existing global/catalog IDs.
A trace link is not a claim of delivery. Existing security/patch/endpoint catalogs
remain normative capability contracts; phase specifications define their design
and delivery gates. No requirement may be silently dropped to pass a milestone.

| Phase | Detailed design and requirements | Accountable roles |
| --- | --- | --- |
| 00 | [Contract, native-core design and laboratory](phase-00.md) | product/security/protocol leads |
| 01 | [Native core and end-to-end development slice](phase-01.md) | protocol/storage and management maintainers |
| 02 | [Complete directory and AD interoperability contract](phase-02.md) | protocol/conformance maintainers |
| 03 | [Multi-site replication, durability and recovery](phase-03.md) | replication/recovery maintainers |
| 04 | [Security, capacity and administrator qualification](phase-04.md) | security/performance/accessibility reviewers |
| 05 | [First production release and controlled deployment](phase-05.md) | release and operations maintainers |
| 06 | [Sustained operations and maintenance](phase-06.md) | support/security operations owners |
| 07 | [Strong identity and privileged administration](phase-07.md) | identity/security and UX maintainers |
| 08 | [Posture, certificate/federation services and detection](phase-08.md) | integration/detection/privacy maintainers |
| 09 | [Containment, key custody and compromise resilience](phase-09.md) | security/platform/recovery maintainers |
| 10 | [Continuous security assurance and trusted delivery](phase-10.md) | assurance/release maintainers |
| 11 | [Endpoint inventory and patch-control foundation](phase-11.md) | endpoint/inventory maintainers |
| 12 | [Controlled patch campaigns and verified installation](phase-12.md) | patch/agent and operations maintainers |
| 13 | [Production patch fleet, compliance and resilience](phase-13.md) | fleet/patch operations maintainers |
| 14 | [Remote desktop and terminal access](phase-14.md) | remote-support/security maintainers |
| 15 | [General server-to-device file delivery](phase-15.md) | file-delivery/agent maintainers |
| 16 | [Native endpoint detection and response](phase-16.md) | endpoint detection/security maintainers |
| 17 | [Joint fleet qualification and endpoint service release](phase-17.md) | fleet/security/performance reviewers |

## Baseline and change rules

Phases 0–5 deliver the first production identity server with full AD-01–AD-10,
IAM-01, PLAT/SEC/OPS/UX acceptance. Phases 6–10 sustain/extend security. Phases
11–17 add patch, remote access, transfer and EDR services with their own release
gates. A feature selected in the first-production compatibility profile is gated
before Phase 5 even if it also appears as an advanced later phase. Working lab
subsets are allowed; they do not redefine production scope.

The initial sizing/SLOs and later fleet profiles are proposed acceptance targets,
not benchmark claims. Changing one requires an ADR with rationale, security/client
impact, updated tests and owner approval before release qualification; failed
benchmarks must never be hidden by silently weakening the target.

Design/lab work may overlap when independent. Execution starts only after each
component's entry dependencies are met. Named owners, final library/database
choices, licensing, supported platform versions and paid infrastructure are not
invented here; [open decisions](../decisions.md) identify exactly what they block.
The documents remain reviewable even when those decisions require experiments.

Use [architecture](../architecture.md) for shared boundaries, [requirements](../requirements.md)
for normative baselines, [threat model](../threat-model.md) for attackers/trust,
and [validation plan](../validation-plan.md) for required executable evidence.
