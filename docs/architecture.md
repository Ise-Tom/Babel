# Architecture decisions

## ADR-0001: Product boundary and protocol core (proposed)

Goal: full AD replacement, with Windows compatibility included in the first
production acceptance contract. Target: 10,000 identities / three sites.
All production server roles must run on Linux, with no Windows Server runtime
required for a standalone Babel domain. Windows is a client/interoperability
target; existing Windows AD servers may participate in migration or coexistence.

Recommendation to validate: use a maintained AD-compatible protocol core such
as Samba AD DC, and concentrate Babel's differentiation in safe administration,
installation, observability, recovery and automation. Reusing a backend does
not establish conformance: verify the pinned version against AD-01–AD-10,
especially functional levels, trusts, multi-site behavior, SYSVOL and GPO tools.
A backend gap is a scope/delivery decision, not permission to omit a requirement.

Compare this with a new protocol core through a time-boxed interoperability
spike hosted on Linux. Building a new LDAP/Kerberos stack alone does not provide Windows AD
semantics; replication, PAC, Netlogon, DNS, SMB/RPC and policy delivery must all
work. Evaluate memory safety, fuzzability, security history, upgrade support,
licensing, dependency activity, packaging and test infrastructure. Do not commit
to a new server implementation before this evidence exists.

Proposed boundaries:

1. Protocol/data plane: domain authentication, directory, DNS, replication and
   policy delivery; remains available if Babel's admin control plane is down.
2. Administration plane: accessible web UI, versioned API, delegated operations,
   auditable jobs and explicit high-risk action confirmation. No browser-to-DC
   privileged credential exposure; backend service identity is least privilege.
3. Operations plane: health, upgrades, encrypted backup, restore and audit export.
   Do not store recovery keys solely in the directory they recover.

No language, database, container strategy, or frontend framework is chosen yet.
Choose after the spike; add their locked build/test/security pipelines with the
first implementation. Do not infer a required Kubernetes cluster from this plan.
The proposed first hosting baseline is Ubuntu Server 24.04 LTS x86-64 with
systemd-managed services on VMs or physical servers, subject to Phase 0
qualification. Containers are a separate packaging decision. Backend selection
must satisfy PLAT-01–PLAT-03 as well as the Windows protocol contract.

## ADR-0002: Licensing and project governance (open, release-blocking)

The owner must choose a project license and contributor policy. If Samba or
other copyleft software is incorporated or distributed, evaluate actual linking,
derivation and packaging obligations before choosing compatible terms. SPDX
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

Recommend evaluating Samba AD DC on the Linux server baseline before considering
a new AD core. Cross-platform **client** compatibility follows protocols and
validated OS behavior, not the programming language used by the server. The
Windows/Linux contract is mandatory; qualify macOS and other clients separately.
No stack can promise compatibility with every OS or every protocol version.

A portable administration API/UI and versioned backend adapter can isolate
Babel's management features from Samba-specific integration. Directory writes
must still use supported backend mechanisms and preserve its authorization,
schema and replication semantics; an adapter is not a license to bypass them.
A second protocol core is justified only by demonstrated requirements the
qualified backend cannot meet and a separately funded conformance/security plan.

Evaluate Go for management services and portable agents, TypeScript for the web
interface, and Rust for new low-level agent/sensor components when needed.
Python remains suitable for tooling and potentially administration/orchestration;
10,000 identities alone does not make it unsuitable. Choose by component needs,
team expertise, security review and measurements, keeping the language count
small. This CI's Python tooling is not a decision to build the server in Python.

Running all server roles on Windows/macOS as well as Linux would be a new host
portability scope, not a consequence of cross-compiling an API. The current
contract remains Linux-hosted; endpoint agents/sensors require separate OS APIs,
packaging, signing and real-client tests even with Go/Rust shared code.
