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
