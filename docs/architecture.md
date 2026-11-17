# Architecture decisions

## ADR-0001: Native AD-compatible protocol core (accepted direction)

Owner decision: build Babel's own directory/domain core rather than wrapping
Samba AD DC. The [native-core implementation plan](native-core-plan.md) defines
the reuse boundary, dependency-ordered milestones, storage/replication decisions
and executable acceptance gates. Samba is not a required production runtime,
bundled domain controller, administrative tool or persistent-data dependency.

Goal: full AD replacement with the first production release, at 10,000 identities
across three sites. All server roles run on Linux with no Windows Server runtime
required for a standalone domain. Windows remains a client/reference target;
existing AD may participate in qualified trust/migration/coexistence scenarios.

Own the identity/authorization, protocol integration, storage and replication
semantics. Reuse reviewed cryptographic/TLS, storage and protocol libraries where
appropriate; a native core is not an instruction to invent cryptography. Match
published specifications and real-client behavior. The project now owns the
complete conformance and security-maintenance burden for its native integration.

Service boundaries:

1. Native protocol/data plane: directory/authentication, DNS, replication and
   GPO delivery, with sole authority over security-state mutations.
2. Administration plane: web UI and versioned delegated API/CLI, using authorized
   core operations rather than raw-store or replication-secret access.
3. Operations plane: health, upgrade, audit and encrypted backup/recovery; recovery
   keys must not exist solely inside the directory they recover.
4. Later endpoint plane: patch, support, file-transfer and EDR services with
   separate authorization and credentials; outages do not stop authentication.

No production language, database or container strategy is selected yet. The
first toolchain ADR must add matching CI before source is accepted. The proposed
host baseline remains Ubuntu Server 24.04 LTS x86-64 with systemd on VMs/physical
servers; qualify exact versions. PLAT-01–PLAT-03 and the full AD contract remain
release gates. Kubernetes is not required. N-00–N-06 are development milestones,
not promises that full domain compatibility can be implemented in one step.

## ADR-0002: Licensing and project governance (open, release-blocking)

The owner must choose a project license and contributor policy. Review the
actual linking, derivation and packaging obligations of all reused dependencies
and the terms of protocol specifications/reference material before distribution. SPDX
identifiers, dependency licenses, source offers where required, notices and
redistribution rights must be checked before distribution. No license is
invented for the owner by the CI bootstrap. At least two maintainers/security
contacts and review ownership must be assigned before public previews.

## ADR-0003: Delivery boundary (accepted for this foundation)

Current CI checks the repository and delivery machinery only. Tag-driven
releases can create **draft source prereleases** after the license and approved
ref gates pass. No service deployment exists until an application, environment,
health/migration checks and rollback procedure exist. Production deployment is
blocked by the roadmap's full compatibility and security gates.

## ADR-0004: Portability and implementation languages (proposed)

Cross-platform client behavior follows protocols and validated OS behavior, not
just the server language. The Windows/Linux contract is mandatory; qualify
macOS/other clients separately. Running server roles on Windows/macOS too would
be a separate host-portability scope. The accepted host contract remains Linux.

Evaluate Rust for the memory-safe native protocol/storage integration core, Go
for management services and portable agents, and TypeScript for a future web UI.
Prefer a small initial language set and require a language/toolchain ADR before
source is added. Python remains suitable for tooling/test orchestration and
possibly management functions; this repository's Python CI helpers do not select
the product language. Reviewed libraries still need integration, fuzz and abuse
tests regardless of language. OS-specific agent/sensor components require native
API, packaging/signing and real-device validation even with shared Go/Rust code.
