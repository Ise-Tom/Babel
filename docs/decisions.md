# Design decisions and release blockers

The native-core and Linux-hosting directions are accepted. Rust 1.100.0 is
selected for the initial bounded lab slice in [ADR 0001](adr/0001-native-ldap-lab.md);
this does not resolve broader crypto/storage/client decisions. The following choices
need accountable named owners and evidence; proposals are not implemented facts.
Independent design/testing may continue while an external decision is pending.
Do not silently select license terms, buy infrastructure or weaken acceptance.

| ID | Decision / alternatives and evidence | Owner role | Deadline / blocked capability |
| --- | --- | --- | --- |
| D-01 | Owner selected Apache-2.0 + DCO 1.1 on 17 November 2026; LICENSE/DCO/metadata are applied in this PR. Third-party linking/distribution, specification and reference-fixture rights still require review | Project owner with legal review | Phase 0; public distribution/external contributions and all product/source releases |
| D-02 | Ratify client builds/editions, functional levels, trust/migration and integration scope; Windows 11 and Server 2022/2025 plus Linux are proposed, macOS later | Product/protocol lead | Before operation conformance acceptance; first production blocked by an incomplete matrix |
| D-03 | Qualify Rust/toolchain and async/parser/TLS/Kerberos dependencies, TypeScript UI plan and optional Go agents; compare security maintenance, portability, packaging and team capacity | Core/security maintainers | Rust 1.100.0 lab subset accepted in ADR 0001; broader runtime/crypto choices require review before corresponding source and CI scope extension |
| D-04 | PostgreSQL backend family accepted by the owner on 17 November 2026 in ADR 0003. PostgreSQL 18.7/official psql synthetic transaction/process-crash experiment passes in ADR 0004. Production Rust driver, full identity/schema, host/disk/backup/upgrade and key custody remain unqualified before credential writes | Storage/security maintainers | Before persistent valuable credentials or stable disk formats; engine selection does not prove durability or AD replication |
| D-05 | Specify AD-compatible conflict/RID/FSMO/DRS metadata, naming contexts, snapshot epochs and required functional levels | Protocol/replication maintainers | Before multi-controller writes or fixed recovery formats; worked partition/concurrency/rollback cases required |
| D-06 | Qualify GPO/SYSVOL consistency and inter-DC transport, including any Windows-DC coexistence/DFS-R profile; ordinary file copying is not compatible replication evidence | Protocol/policy maintainers | Before complete GPO/mixed-domain claims in Phases 2–3 |
| D-07 | Choose PKINIT/CA/federation/HSM/KMS supported key classes and provider trust/outage/recovery behavior | Identity/key security owners | Before Phases 8–9 optional-module enforcement; earlier if selected for first production |
| D-08 | Ratify endpoint OS/kernel/application/desktop matrices, native update engines and signing/driver/relay distribution requirements | Endpoint maintainers | Before Phase 11/14/16 feature qualification; unsupported devices cannot appear compliant/protected |
| D-09 | Approve sensor/recording/evidence fields, retention, legal/consent policy, response automation and measured alert-quality thresholds | Privacy/security/operations owners | Before collecting real endpoint/user data or enabling prevention; Phase 16/17 capacity includes full retention cost |
| D-10 | Assign maintainers/security contacts, licensed isolated Windows infrastructure and supported GitHub protection/attestation options with explicit budget | Project/infrastructure owner | Before trusted interoperability labs and enforced production releases; no automatic paid-plan/visibility changes |

See [PostgreSQL state contract](adr/0003-postgresql-directory-state.md) and the
[unprovisioned Windows lab](windows-reference-lab.md) for the concrete next gates.

Hardware budgets, exact supported versions and performance thresholds must be
ratified through measured ADRs. Changes preserve stable requirement IDs or add
explicit supersession records with scope/security impact and updated tests.
No requirement is marked delivered because its document exists or CI parses it.
