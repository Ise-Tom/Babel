<!-- Generated report. Edit canonical phase documents and dashboard/progress.json. -->
# Babel project dashboard

Read this page in your browser using the repository's existing GitHub access. Bookmark this URL; no download or additional account is needed.

> Main code and open-PR proposals are reported separately. CI failures remain visible; public deployment still requires successful main CI.

Report source: [824d576](<https://github.com/Ise-Tom/Babel/tree/824d5760f4f95abb341f625b6ff37ab60dbd5d1f>). Recorded implementation evidence: 2026-11-17, [cd6ad14](<https://github.com/Ise-Tom/Babel/tree/cd6ad149870a05db4ab2a4f7fbca3e4d461af848>). These are separate revisions. Rebuilding does not accept requirements or refresh evidence.

**18 phases · 180 requirements · 130 features · 0 phases accepted · 21 recorded increments · 7 open problems**

Implemented increments can be narrower than their parent requirement. Acceptance is recorded after an explicit owner review of the stated scope, evidence and limits. Requirement and increment counts can differ between phases and are not effort percentages. Design records and passing CI do not establish AD compatibility or production readiness.

**Current focus:** Phase 01 — The read-only RootDSE lab is implemented. The development PR adds bounded LDAP boolean/objectClass filters and PR-aware progress reporting; durable identities, DNS, authentication and domain services remain future work.

[Phase board](#phase-board) · [Implementation journal](#implementation-journal) · [Problems encountered](#problems-encountered) · [Feature catalog](#feature-catalog)

Use your browser's Find command to search. Expand a phase's requirements to read its details. The standalone HTML adds interactive search/filtering and JSON export; this GitHub view is the persistent report.

## Phase board

| Phase | Status | Accepted requirements | Recorded increments |
| --- | --- | --- | --- |
| [00 · Contract, native-core design and laboratory](#phase-00) | In progress | 0/10 | 12 |
| [01 · Native core and end-to-end development slice](#phase-01) | In progress | 2/10 | 19 |
| [02 · Complete directory and AD interoperability contract](#phase-02) | Planned | 0/10 | 0 |
| [03 · Multi-site replication, durability and recovery](#phase-03) | Planned | 0/10 | 0 |
| [04 · Security, capacity and administrator qualification](#phase-04) | Planned | 0/10 | 0 |
| [05 · First production release and controlled deployment](#phase-05) | Planned | 0/10 | 0 |
| [06 · Sustained operations and maintenance](#phase-06) | Planned | 0/10 | 0 |
| [07 · Strong identity and privileged administration](#phase-07) | Planned | 0/10 | 0 |
| [08 · Posture, certificate/federation services and detection](#phase-08) | Planned | 0/10 | 0 |
| [09 · Containment, key custody and compromise resilience](#phase-09) | Planned | 0/10 | 0 |
| [10 · Continuous security assurance and trusted delivery](#phase-10) | Planned | 0/10 | 0 |
| [11 · Endpoint inventory and patch-control foundation](#phase-11) | Planned | 0/10 | 0 |
| [12 · Controlled patch campaigns and verified installation](#phase-12) | Planned | 0/10 | 0 |
| [13 · Production patch fleet, compliance and resilience](#phase-13) | Planned | 0/10 | 0 |
| [14 · Remote desktop and terminal access](#phase-14) | Planned | 0/10 | 0 |
| [15 · General server-to-device file delivery](#phase-15) | Planned | 0/10 | 0 |
| [16 · Native endpoint detection and response](#phase-16) | Planned | 0/10 | 0 |
| [17 · Joint fleet qualification and endpoint service release](#phase-17) | Planned | 0/10 | 0 |

## Open pull requests

Main-branch totals above exclude these proposals. CI success does not merge a PR or accept a requirement. Validation below is author-recorded until reviewed.

GitHub metadata checked: 2026-11-17T22:15:25\+01:00.

**Current main CI: success.** A failed build is shown here; it does not qualify a public deployment or product release.

### [\#17 · Bump typescript from 6.0.3 to 7.0.2 in /dashboard](<https://github.com/Ise-Tom/Babel/pull/17>)

**In review · Pending merge · CI: in\_progress** · Head 4ef5b4d

<details>
<summary>Description, changed files and proposed progress</summary>

**PR description (untrusted text):**

    Bumps [typescript](https://github.com/microsoft/TypeScript) from 6.0.3 to 7.0.2.
    <details>
    <summary>Release notes</summary>
    <p><em>Sourced from <a href="https://github.com/microsoft/TypeScript/releases">typescript's releases</a>.</em></p>
    <blockquote>
    <h2>TypeScript 7.0.2</h2>
    <p><a href="https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/">https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/</a></p>
    <p>This tag was originally released at: <a href="https://github.com/microsoft/typescript-go/releases/tag/typescript%2Fv7.0.2">https://github.com/microsoft/typescript-go/releases/tag/typescript%2Fv7.0.2</a></p>
    </blockquote>
    </details>
    <details>
    <summary>Commits</summary>
    <ul>
    <li><a href="https://github.com/microsoft/TypeScript/commit/1e4744d68260a7cb91b62b12edc3f6a2187faaf1"><code>1e4744d</code></a> Merge branch 'main' into ts7-release</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/a5a219c3b5da0db4fa0ecf6c0b1f588c9af9c669"><code>a5a219c</code></a><code>microsoft/typescript-go#4558</code></li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/ecfe30dce91368d52c9a49b6095bb0b673a238f8"><code>ecfe30d</code></a> Update status localization</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/5de25b5f8fec2ca35eadaed041f1f06d2e214895"><code>5de25b5</code></a> Hide executable name in TypeScript status</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/d7ce74a75da2b80e8201506a1599c06549432b93"><code>d7ce74a</code></a> Show bundled TypeScript version for packaged servers</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/29be66a607707f90d7a53103a4469bb3015a4d54"><code>29be66a</code></a> Correct TS 7 release version to 7.0.2</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/ed2bd1bfa4aac5211ce4bc58fcd1313c7eddc8ff"><code>ed2bd1b</code></a> Merge branch 'main' into ts7-release</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/887307575c58ea640dbeba3b4e8fdb6347cd3044"><code>8873075</code></a> Bump the github-actions group across 1 directory with 3 updates (microsoft/ty...</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/9427131ae2d4e230a90ee8a09daac4e75da3e311"><code>9427131</code></a> Set up stable / nightly extension split, other prep (microsoft/typescript-go#...</li>
    <li><a href="https://github.com/microsoft/TypeScript/commit/d4eaca5460a1f5f02a829e62706794b0a6fb903e"><code>d4eaca5</code></a><code>microsoft/typescript-go#4549</code></li>
    <li>Additional commits viewable in <a href="https://github.com/microsoft/TypeScript/compare/v6.0.3...v7.0.2">compare view</a></li>
    </ul>
    </details>
    <details>
    <summary>Maintainer changes</summary>
    <p>This version was pushed to npm by <a href="https://www.npmjs.com/~microsoft1es">microsoft1es</a>, a new releaser for typescript since your current version.</p>
    </details>
    <br />
    
    
    [![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=typescript&package-manager=npm_and_yarn&previous-version=6.0.3&new-version=7.0.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)
    
    Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.
    
    [//]: # (dependabot-automerge-start)
    [//]: # (dependabot-automerge-end)
    
    ---
    
    <details>
    <summary>Dependabot commands and options</summary>
    <br />
    
    You can trigger Dependabot actions by commenting on this PR:
    - `@dependabot rebase` will rebase this PR
    - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
    - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
    - `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
    - `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
    - `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)
    
    
    </details>

**Changed files:**

- .github/CODEOWNERS
- .github/dependabot.yml
- .github/workflows/dashboard-pages.yml
- .github/workflows/dashboard-publish.yml
- .github/workflows/dashboard.yml
- README.md
- SECURITY.md
- dashboard/build.mjs
- dashboard/progress.json
- dashboard/src/index.html
- dashboard/src/main.ts
- dashboard/tests/build.test.mjs
- dashboard/tests/dashboard.spec.ts
- docs/architecture.md
- docs/ci-cd.md
- docs/github-main-ruleset.json
- docs/github-security-settings.md
- docs/phases/README.md
- docs/project-dashboard.md
- docs/validation-plan.md
- scripts/check\_design.py
- scripts/check\_pages\_source.py
- scripts/collect\_pr\_progress.py
- scripts/publish\_dashboard.py
- scripts/render\_dashboard.py
- scripts/verify\_pages\_artifact.py
- tests/test\_dashboard.py
- tests/test\_dashboard\_delivery.py
- tests/test\_design.py
- tests/test\_pages\_artifact.py
- tests/test\_pages\_deployment.py
- tests/test\_pr\_progress.py

#### Proposed W22 · Keep the tested compiler API instead of silently weakening security lint

**Requirements:** P00-10, P01-01

**How it was done:** Reproduced TypeScript 7.0.2 passing typecheck but crashing lint because ScriptTarget.Latest is absent. Restored TypeScript 6.0.3 and its locked tooling graph, retained AST/DOM/eval checks and deferred automatic major compiler proposals until the security-policy API is explicitly migrated. PR \#17 now carries this correction instead of an unsupported upgrade.

**Recorded validation:** Strict compiler checks, ESLint, six build/security-lint fixtures, 24 desktop/mobile browser tests and npm audit all pass locally; audit reports zero vulnerabilities. Hosted full CI is rerun for the corrected PR head.

**Limits and remaining work:** TypeScript 7 is deliberately not adopted. Migration to its different unstable APIs needs a separate qualified change; a passing compiler CLI alone does not establish equivalent security lint.

**PR-head evidence:** [dashboard/package.json](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/package.json>) · [.github/dependabot.yml](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/dependabot.yml>) · [dashboard/lint.mjs](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/lint.mjs>) · [dashboard/tests/lint.test.mjs](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/tests/lint.test.mjs>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>)


#### Proposed W23 · Verify Pages archives and minimize privileged deployment operations

**Requirements:** P00-10, P01-01, P01-10

**How it was done:** Read-only preflight validates exact main CI, immutable artifact ID, size and SHA-256 digest. A bounded verifier rejects extra/traversing/symlink files and weak browser policy, then packages only HTML/.nojekyll. The separate Pages/OIDC job has no checkout or project-code execution, attempts Actions-only/HTTPS configuration and rechecks main before deployment. Added no-referrer policy, blocked images, CODEOWNERS, a main ruleset template and verified owner settings.

**Recorded validation:** 86 Python tests pass with 98% tooling coverage. Negative archive/CSP tests, actual standalone archive verification, strict types/lint, actionlint, Zizmor, six build/lint fixtures and 24 browser tests pass locally. Live current site returned HTTP 200; Pages API confirms HTTPS and environment main-only deployment policy.

**Limits and remaining work:** These stronger deployment changes await PR merge and a successful main workflow run. The integration cannot mutate admin settings \(HTTP 403\). The job-token Pages configuration step must succeed and read back correctly; no success is claimed in advance. Required review, private vulnerability reporting and other owner settings remain explicit actions. GitHub Pages does not support arbitrary security response headers.

**PR-head evidence:** [.github/workflows/dashboard-pages.yml](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/workflows/dashboard-pages.yml>) · [.github/workflows/dashboard.yml](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/workflows/dashboard.yml>) · [scripts/check\_pages\_source.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/scripts/check_pages_source.py>) · [scripts/verify\_pages\_artifact.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/scripts/verify_pages_artifact.py>) · [tests/test\_pages\_artifact.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/tests/test_pages_artifact.py>) · [tests/test\_pages\_deployment.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/tests/test_pages_deployment.py>) · [dashboard/build.mjs](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/build.mjs>) · [dashboard/src/index.html](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/src/index.html>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>) · [docs/github-main-ruleset.json](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-main-ruleset.json>) · [.github/CODEOWNERS](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/CODEOWNERS>)

#### Proposed problem update: I02 · Merge protection administration is unavailable to the integration

**Proposed status:** open

GitHub rejected ruleset access for this private repository with HTTP 403 and requested a supported plan or public visibility. Passing CI is not enforced merge protection.

**Resolution:** Still open

**Next action:** Owner imports docs/github-main-ruleset.json, enables required review/CI gate and verifies enforcement. Public ruleset listing is empty; legacy branch protection GET returns HTTP 403, so no enforced protection is claimed.

**Provenance:** GitHub API observation recorded during pipeline setup; verify again before production release.

[docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>) · [docs/github-main-ruleset.json](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-main-ruleset.json>)

#### Proposed problem update: I10 · Dashboard access and Pages activation remain unavailable

**Proposed status:** resolved

The app ran inside the cloud workspace, but no user-accessible preview route was established. GitHub returned HTTP 403 for Pages activation; the repository still reports Pages disabled.

**Resolution:** The owner enabled Pages and applied public visibility. Deployment run 44175624652 succeeded for main 824d5760f4f95abb341f625b6ff37ab60dbd5d1f; https://ise-tom.github.io/Babel/ returned HTTP 200 with HTTPS/HSTS. This resolves user access through public hosting, without claiming cloud localhost forwarding works.

**Next action:** Keep CI-gated deployment, apply the proposed artifact hardening and use the stable HTTPS URL.

**Provenance:** Recorded development-session evidence and repository/CI observations; no separate public issue was created.

[docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>)

#### Proposed problem update: I15 · GitHub Actions jobs blocked before startup by account billing

**Proposed status:** resolved

All jobs in PR \#18 CI run 44156039039 have zero executed steps. GitHub annotation: The job was not started because recent account payments have failed or your spending limit needs to be increased. Automatic dashboard refresh jobs are affected too.

**Resolution:** After the owner made Babel public, main CI run 44175150495 executed all 12 jobs successfully. The earlier account-capacity block no longer prevents this verified public run.

**Next action:** Monitor actual CI results; public standard runners do not authorize paid capacity or make all platform limits disappear.

**Provenance:** Observed GitHub run 44156039039, check run 134296912744 annotation; no pipeline commands ran.

[docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>)

#### Proposed problem update: I16 · GitHub integration cannot apply the authorized public visibility setting

**Proposed status:** resolved

The project owner explicitly requested public visibility. PATCH /repos/Ise-Tom/Babel with private=false returned HTTP 403, Resource not accessible by integration, despite repository metadata showing admin=true. The repository remained private on readback.

**Resolution:** The owner applied public visibility and merged PR \#18. GitHub now reports private=false and visibility=public, and the public-compatible dashboard publisher succeeds. The integration itself still lacks administration permissions.

**Next action:** Keep visibility changes explicit owner decisions and track remaining settings permissions separately under I18.

**Provenance:** Direct GitHub API response in the authorized visibility-change task on 2026-11-17; no automatic approval-review rejection occurred and no visibility setting was applied.

[docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>)

#### Proposed problem update: I17 · TypeScript 7 removed the compiler API used by security lint

**Proposed status:** resolved

PR \#17 run 44154241268 passed typecheck but failed dashboard lint with TypeError reading ScriptTarget.Latest. Local reproduction confirmed the major version no longer exposes the JavaScript compiler API; alternate APIs are unstable and require migration.

**Resolution:** The corrected PR retains TypeScript 6.0.3 and the existing AST/DOM/eval protections, with compatible updates still enabled and automatic compiler majors deferred. Local build, lint, browser and audit checks pass.

**Next action:** Verify corrected PR CI. Migrate the policy explicitly before upgrading the compiler major; retain malformed-input and security regressions.

**Provenance:** Observed failed hosted job 134361914270 and local reproduction of the same failure; no check was skipped.

[dashboard/package.json](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/package.json>) · [.github/dependabot.yml](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/dependabot.yml>) · [dashboard/lint.mjs](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/lint.mjs>) · [dashboard/tests/lint.test.mjs](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/tests/lint.test.mjs>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>)

#### Proposed problem update: I18 · GitHub denies repository security and Pages settings writes to the integration

**Proposed status:** open

Pages configuration PUT, environment PUT, private vulnerability reporting enablement and ruleset creation all returned HTTP 403 Resource not accessible by integration. Pages is live with HTTPS, but its observed build type remains legacy; private reporting is disabled, ruleset listing empty and legacy protection/Actions defaults cannot be inspected.

**Resolution:** Still open

**Next action:** Owner applies docs/github-security-settings.md and imports the supplied main ruleset. The revised deployment tries Actions-only/HTTPS with its legitimate Pages-scoped job token and fails if enforcement/readback is denied. Verify actual settings after application; no paid service or broader credential is requested.

**Provenance:** Direct GitHub settings API responses and successful public site/deployment observations on 2026-11-17; these are GitHub permission errors, not automatic approval-review rejections.

[.github/workflows/dashboard-pages.yml](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/workflows/dashboard-pages.yml>) · [.github/workflows/dashboard.yml](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/workflows/dashboard.yml>) · [scripts/check\_pages\_source.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/scripts/check_pages_source.py>) · [scripts/verify\_pages\_artifact.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/scripts/verify_pages_artifact.py>) · [tests/test\_pages\_artifact.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/tests/test_pages_artifact.py>) · [tests/test\_pages\_deployment.py](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/tests/test_pages_deployment.py>) · [dashboard/build.mjs](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/build.mjs>) · [dashboard/src/index.html](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/dashboard/src/index.html>) · [docs/github-security-settings.md](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-security-settings.md>) · [docs/github-main-ruleset.json](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/docs/github-main-ruleset.json>) · [.github/CODEOWNERS](<https://github.com/Ise-Tom/Babel/blob/4ef5b4da9f11461635848669a110d73c58741bad/.github/CODEOWNERS>)


</details>


## Phase 00

**Contract, native-core design and laboratory — In progress**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-00.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P00-01

**Define supported protocol operations, functional levels and exact Windows/Linux client editions/builds. — In progress**

The scope exists, but exact client builds and the approved operation matrix are not complete.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Reviewed matrix maps every AD requirement to expected positive/negative behavior and an owner; unknown/unsupported operations stay visible.

No implemented increment is recorded for this requirement.

### P00-02

**Define stable identities, authorization order, schema rules and local commit semantics. — In progress**

Design invariants are documented; the identity/ACL model is not implemented or accepted.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Design review covers rename, DN collision, ACL inheritance, nested groups, concurrent updates and durable acknowledgment boundaries.

**Implementation explanations:** W12: Threat model and open decision register. See the [implementation journal](#implementation-journal).

### P00-03

**Define attribute replication/versioning and restore epochs before fixing a disk format. — In progress**

Replication and restore contracts are designed; metadata algorithms and failure evidence remain open.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Worked partition/delete/conflict/rollback examples specify observable outcomes and map to MS-ADTS/MS-DRSR.

**Implementation explanations:** W12: Threat model and open decision register. See the [implementation journal](#implementation-journal).

### P00-04

**Choose a memory-safe toolchain and reviewed TLS/Kerberos/storage/parser dependencies. — In progress**

Rust is accepted only for the bounded lab subset; broader crypto/store libraries remain under review.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** ADR records alternatives, supported platforms, license/CVE maintenance and locked build/fuzz/security jobs; no custom crypto accepted.

**Implementation explanations:** W01: Native Rust workspace and reproducible builds. See the [implementation journal](#implementation-journal).

### P00-05

**Provide a disposable Windows reference and Linux host lab with reproducible DNS/time. — Blocked**

No licensed isolated Windows reference lab is recorded.

**Associated features:** [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Two fresh deployments run discovery probes, isolate egress, clean up resources and publish exact image/build identifiers.

No implemented increment is recorded for this requirement.

### P00-06

**Establish project license, contributor terms and specification-use review. — Blocked**

Owner license/contributor decision is required before distribution.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Owner decision and dependency obligations recorded before source distribution; missing decisions block release rather than receiving invented terms.

No implemented increment is recorded for this requirement.

### P00-07

**Establish Tier 0 identities, review ownership, vulnerability intake and an initial threat register. — In progress**

Threat model exists; named contacts and the complete operating security process are not established.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-09: Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Private report route and backup security contacts exercised; every boundary has misuse cases and review responsibility.

**Implementation explanations:** W12: Threat model and open decision register. See the [implementation journal](#implementation-journal).

### P00-08

**Version the compatibility/evidence schema and requirement traceability. — In progress**

Design traceability tooling is implemented; full compatibility/evidence acceptance is not complete.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Evidence records commit, test/client/spec revision, requirement, outcome and redacted artifacts; skipped/unrun are never passing.

**Implementation explanations:** W10: Required native and repository CI gates; W11: Complete phase specifications and traceability; W14: Phase dashboard and portable engineering report; W15: Permanent private GitHub dashboard publication; W18: Open-PR-aware private progress reporting. See the [implementation journal](#implementation-journal).

### P00-09

**Approve the target workload, fault profiles and performance measurement method. — In progress**

Provisional workloads are specified; no production benchmark has ratified them.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Reviewed load model includes mixed successful/denied requests, cold cache, WAN loss/latency, partial outages and hardware costs.

**Implementation explanations:** W12: Threat model and open decision register. See the [implementation journal](#implementation-journal).

### P00-10

**Specify upgrade, recovery and scope-change governance. — In progress**

Delivery gates and source packaging exist; real product upgrade/recovery/governance acceptance remains.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Irreversible schema/key/storage decisions require review and recovery examples; scope exceptions have owner, expiry and production impact.

**Pending PR proposals:** [\#17: Bump typescript from 6.0.3 to 7.0.2 in /dashboard](<https://github.com/Ise-Tom/Babel/pull/17>). See [open PR progress](#open-pull-requests).

**Implementation explanations:** W13: Tested source and lab archive packaging; W14: Phase dashboard and portable engineering report; W15: Permanent private GitHub dashboard publication; W16: Compact interactive interface and verified static-hosting workflow; W18: Open-PR-aware private progress reporting; W19: Remove unpatched vulnerable tooling dependency path; W20: Scope-based phase sizes and explicit owner acceptance reviews; W21: Support public repository dashboard publication and prepare visibility transition. See the [implementation journal](#implementation-journal).

</details>


## Phase 01

**Native core and end-to-end development slice — In progress**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-01.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P01-01

**Add actual native source only with locked build, lint, types, unit/property tests and fuzz smoke. — Accepted**

Current native LDAP component development safeguards accepted by the project owner. Future components and full product qualification remain separate obligations.

**Associated features:** [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** The scope guard is extended in the same reviewed PR; clean Linux build plus malformed-input regression corpus passes.

**Acceptance review:** Project owner \(explicit approval in this conversation\), 2026-11-17. Project owner explicitly answered “Accept this scope” in this conversation on 2026-11-17. Scope: development safeguards for the current native LDAP component, not the full server or future components. PR \#16 and its 12-job successful CI run: https://github.com/Ise-Tom/Babel/pull/16 ; https://github.com/Ise-Tom/Babel/actions/runs/44152161324 . Merged main cd6ad149870a05db4ab2a4f7fbca3e4d461af848 also passed all 12 jobs in run 44153995669.

**Pending PR proposals:** [\#17: Bump typescript from 6.0.3 to 7.0.2 in /dashboard](<https://github.com/Ise-Tom/Babel/pull/17>). See [open PR progress](#open-pull-requests).

**Implementation explanations:** W01: Native Rust workspace and reproducible builds; W02: Bounded BER / LDAP decoder; W06: Independent client and packaged-binary checks; W07: Property tests and core coverage gate; W08: Sanitizer fuzz smoke; W09: Native dependency, license and SBOM checks; W10: Required native and repository CI gates; W13: Tested source and lab archive packaging; W17: Bounded LDAP RootDSE filter discovery; W19: Remove unpatched vulnerable tooling dependency path; W20: Scope-based phase sizes and explicit owner acceptance reviews; W21: Support public repository dashboard publication and prepare visibility transition. See the [implementation journal](#implementation-journal).

### P01-02

**Implement stable identity/schema/ACL primitives before account mutations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Property tests preserve IDs on rename and reject collisions, invalid schema writes and unauthorized inherited/nested access.

No implemented increment is recorded for this requirement.

### P01-03

**Implement a transactionally durable store and versioned recovery journal. — Blocked**

Storage/identity/replication decisions must precede durable credential state.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Kill/restart at each commit boundary yields either the old or new complete state and never acknowledges an undurable successful write.

No implemented increment is recorded for this requirement.

### P01-04

**Implement the declared DNS/LDAP discovery/read subset with bounded results. — In progress**

Read-only RootDSE discovery exists. The development PR extends presence/objectClass equality and boolean filters with strict budgets and Undefined semantics. DNS, real directory queries and Windows discovery evidence remain open.

**Associated features:** [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-05: AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Real client probes and negative paging/filter/referral tests pass; RootDSE success is not counted as domain join.

**Implementation explanations:** W02: Bounded BER / LDAP decoder; W03: Read-only RootDSE queries; W05: TCP framing and session budgets; W06: Independent client and packaged-binary checks; W17: Bounded LDAP RootDSE filter discovery. See the [implementation journal](#implementation-journal).

### P01-05

**Integrate reviewed authentication, password changes and principal-key lifecycle. — Blocked**

Credential rejection is implemented; real Kerberos/password/key behavior awaits design and conformance prerequisites.

**Associated features:** [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Positive/denied bind and AS/TGS flows, replay/expiry/downgrade and password redaction tests pass for declared operations.

**Implementation explanations:** W04: Credential rejection and safe diagnostics. See the [implementation journal](#implementation-journal).

### P01-06

**Implement computer-account membership and secure-channel rollover. — Blocked**

Windows lab, DNS/authentication and membership implementation are missing.

**Associated features:** [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-08: Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** A supported Windows client joins, logs in and rotates its machine password; unsigned/unauthorized membership requests fail.

No implemented increment is recorded for this requirement.

### P01-07

**Implement an initial GPO/SYSVOL delivery path with ACL/version consistency. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-06: Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** A Windows client applies and reverts a declared policy; interrupted writes recover without silently serving contradictory versions.

No implemented increment is recorded for this requirement.

### P01-08

**Provide delegated account/group/password administration through API/CLI and a minimal UI. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Create/disable/reset/group workflows succeed only with correct rights; API and UI denied-operation cases produce matching audit evidence.

No implemented increment is recorded for this requirement.

### P01-09

**Package Linux services with bounded privilege, certificate configuration and health checks. — In progress**

Lab limits and diagnostics are tested; TLS, Linux service lifecycle and production privileges are not.

**Associated features:** [PLAT-02: Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-04: TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Clean install/reboot, invalid DNS/time/certificate and least-privilege file/port tests yield actionable errors without bypassing verification.

**Implementation explanations:** W04: Credential rejection and safe diagnostics; W05: TCP framing and session budgets. See the [implementation journal](#implementation-journal).

### P01-10

**Label and inventory development limitations. — Accepted**

Project owner accepted the current prototype’s scope inventory and limitation reporting. Authentication, storage, domain join and GPO remain unimplemented and Phase 1 remains in progress.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Each public operation has a tested/unsupported status; lab credentials and incomplete protocol behavior cannot be promoted as a production release.

**Acceptance review:** Project owner \(explicit approval in this conversation\), 2026-11-17. Project owner explicitly answered “Accept this scope” in this conversation on 2026-11-17. Scope: documentation, tests and CLI label the current prototype as a loopback-only LDAP discovery lab and disclose missing production/domain functionality. Evidence pinned to merged main: https://github.com/Ise-Tom/Babel/blob/cd6ad149870a05db4ab2a4f7fbca3e4d461af848/docs/phase-01-progress.md ; https://github.com/Ise-Tom/Babel/blob/cd6ad149870a05db4ab2a4f7fbca3e4d461af848/native/babel-ldap/src/main.rs . This accepts scope reporting, not those missing features or production readiness.

**Pending PR proposals:** [\#17: Bump typescript from 6.0.3 to 7.0.2 in /dashboard](<https://github.com/Ise-Tom/Babel/pull/17>). See [open PR progress](#open-pull-requests).

**Implementation explanations:** W14: Phase dashboard and portable engineering report; W15: Permanent private GitHub dashboard publication; W16: Compact interactive interface and verified static-hosting workflow; W17: Bounded LDAP RootDSE filter discovery; W18: Open-PR-aware private progress reporting; W20: Scope-based phase sizes and explicit owner acceptance reviews; W21: Support public repository dashboard publication and prepare visibility transition. See the [implementation journal](#implementation-journal).

</details>


## Phase 02

**Complete directory and AD interoperability contract — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-02.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P02-01

**Complete domain/forest lifecycle, naming contexts and schema/object semantics. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Synthetic import/export and reference queries compare IDs, object attributes, ACLs and schema; incompatible operations have explicit failures.

No implemented increment is recorded for this requirement.

### P02-02

**Complete account and password lifecycle, fine-grained policy and delegated recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-07: Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** User/admin changes, history/lockout/expiry, disable/delete/restore and denied actions pass through every supported protocol/API path.

No implemented increment is recorded for this requirement.

### P02-03

**Complete Kerberos/PAC, SPN and delegation behavior for the supported matrix. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-03: Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Real client/service AS/TGS and delegation cases pass; replay, wrong key, invalid PAC, expired tickets and weak-encryption downgrade are rejected.

No implemented increment is recorded for this requirement.

### P02-04

**Complete LDAP controls, GC, paging/referrals and attribute-level authorization. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** RSAT and LDAP clients agree with the reference for selected controls; unauthorized attributes never appear in search or error output.

No implemented increment is recorded for this requirement.

### P02-05

**Complete secure DNS updates, DC locator and site/subnet discovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-05: AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Signed updates, stale records, wrong-site discovery and DNS failure tests produce the declared outcomes on supported clients.

No implemented increment is recorded for this requirement.

### P02-06

**Complete SMB/RPC/Netlogon, SAMR and LSA membership/administration paths. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-08: Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-02: Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Client join/rejoin, secure-channel reset and service-account operations pass; signing/sealing and least-privilege rejection are verified.

No implemented increment is recorded for this requirement.

### P02-07

**Complete GPO/SYSVOL creation, inheritance/filtering and supported delivery/replication semantics. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-06: Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Actual resultant policy and scripts match the reference; filesystem and directory permissions/versions remain reconciled after failures.

No implemented increment is recorded for this requirement.

### P02-08

**Implement qualified domain/forest functional levels and FSMO transfer/seizure semantics. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Unsupported levels are rejected; role handoff, failed holder and schema upgrade tests preserve a recoverable authoritative state.

No implemented increment is recorded for this requirement.

### P02-09

**Complete trusts and migration/coexistence with SID filtering and selective authentication. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-09: Forest/domain trusts, cross-domain authorization, migration and coexistence with existing AD](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Two reference forests exercise permitted/denied cross-domain access, trust removal and a rehearsed migration/recovery path.

No implemented increment is recorded for this requirement.

### P02-10

**Publish an operation-level compatibility report without unsupported universal-OS claims. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Every AD contract row has real-client evidence with exact builds/spec revisions and no unexplained failure, skip or unrun acceptance case.

No implemented increment is recorded for this requirement.

</details>


## Phase 03

**Multi-site replication, durability and recovery — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-03.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P03-01

**Authenticate and authorize replication membership and secret access. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Unknown, revoked and insufficiently privileged replicas cannot read credential changes or alter membership; every enrollment is audited.

No implemented increment is recorded for this requirement.

### P03-02

**Apply change data and replication cursors atomically and idempotently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Duplicate/reordered/interrupted exchanges do not lose acknowledged local transactions or skip unapplied remote changes.

No implemented increment is recorded for this requirement.

### P03-03

**Resolve concurrent attribute/object changes and deletion/recreation consistently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Model-based tests cover modify/modify, move/rename, group membership, delete/modify and tombstone/lingering-object conflicts.

No implemented increment is recorded for this requirement.

### P03-04

**Handle topology, naming contexts and role ownership under node loss. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-10: Domain/forest functional levels and FSMO role ownership, transfer and failure recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Lose one DC or site, transfer/seize a role through the supported procedure and demonstrate correct client discovery and surviving authentication.

No implemented increment is recorded for this requirement.

### P03-05

**Expose replication freshness and revocation uncertainty. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-09: Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** A partition causes visible stale/unknown warnings with measured convergence; UI/API never claims instant global disable during disconnection.

No implemented increment is recorded for this requirement.

### P03-06

**Protect against unsupported rollback and stale replica reintroduction. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Restore old snapshots with conflicting invocation/progress metadata; reject/quarantine unsafe joins and follow a tested recovery path.

No implemented increment is recorded for this requirement.

### P03-07

**Create encrypted coherent directory/SYSVOL backups with independent custody. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Recover at full dataset size in an isolated clean environment without the original domain or a sole directory-held recovery key.

No implemented increment is recorded for this requirement.

### P03-08

**Meet declared recovery and failover objectives. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Fault-drill reports measure DC &lt;=60 s failover and full-domain &lt;=1 h RPO/&lt;=4 h RTO; exceeded targets block qualification.

No implemented increment is recorded for this requirement.

### P03-09

**Rotate TLS, Kerberos/service/trust keys with explicit overlap and expiry handling. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Test invalid/expired certificates, lost issuer and interrupted rotation; preserve intended authentication without accepting compromised old keys indefinitely.

No implemented increment is recorded for this requirement.

### P03-10

**Recover cleanly from resource and network exhaustion. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Disk-full, queue pressure, clock fault, 24-hour partition/rejoin and process kill have bounded memory/retries and auditable data-loss outcomes.

No implemented increment is recorded for this requirement.

</details>


## Phase 04

**Security, capacity and administrator qualification — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-04.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P04-01

**Run independent integrated security assessment and threat-model review. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-08: Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Report covers protocol, keys, admin UI/API, replication, supply chain and restore; findings have owners, retests and explicit dispositions.

No implemented increment is recorded for this requirement.

### P04-02

**Enforce secure protocol defaults and scoped legacy exceptions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-02: Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-03: Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-04: TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Invalid TLS, anonymous sensitive reads, unsigned channels and weak crypto fail; exceptions carry scope/expiry/audit and cannot silently become defaults.

No implemented increment is recorded for this requirement.

### P04-03

**Measure the full mixed-load contract with real clients and reference requests. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-03: Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-04: LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Publish dataset, hardware, caches, concurrency, rates, percentiles and unexpected errors; each baseline target is met or release-blocking.

No implemented increment is recorded for this requirement.

### P04-04

**Qualify sustained operation and failure headroom. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** 24-hour soak and DC/site failures show bounded queues/storage, no unexplained credential/data corruption and documented degraded behavior.

No implemented increment is recorded for this requirement.

### P04-05

**Demonstrate complete and privacy-preserving security audit. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-09: Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** For each privileged/auth/policy/key operation, expected events and denied cases are present, correlated and redacted; export loss is visible.

No implemented increment is recorded for this requirement.

### P04-06

**Qualify administrator journeys with representative users. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** At least five admins achieve &gt;=90% unassisted completion per declared journey, including delegation, policy, diagnosis and restore; publish time-on-task.

No implemented increment is recorded for this requirement.

### P04-07

**Qualify keyboard/screen-reader accessibility and dangerous-action previews. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** WCAG 2.2 AA audit and manual assistive-technology journeys pass for the administration surface; unsupported settings are never silently discarded.

No implemented increment is recorded for this requirement.

### P04-08

**Test denial and recovery through UI, API and CLI consistently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [IAM-01: Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-05: Web/API admin MFA through phishing-resistant authentication, step-up for privileged actions, scoped sessions/tokens, CSRF protection and reauthentication](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-07: Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Role/session expiry, CSRF, unauthorized export/reset, recovery bypass and stale privilege tests preserve authorization and provide safe actionable errors.

No implemented increment is recorded for this requirement.

### P04-09

**Ratify production sizing and operating limits from results. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-03: Linux host hardening and persistent data integrity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** ADR records DC/backup/audit capacity, retention, bandwidth and expansion triggers; suggested 4-vCPU/16-GiB sizing is not treated as measured beforehand.

No implemented increment is recorded for this requirement.

### P04-10

**Produce a signed-off first-production readiness bundle. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Every baseline requirement maps to current passing evidence; outstanding exceptions, unsupported clients and residual risks are explicit and approved before Phase 5.

No implemented increment is recorded for this requirement.

</details>


## Phase 05

**First production release and controlled deployment — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-05.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P05-01

**Release only artifacts built from the reviewed tested commit. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Package digest, SBOM and provenance resolve to the same source/build identity; rebuilding during production promotion is prohibited.

No implemented increment is recorded for this requirement.

### P05-02

**Enforce release licensing, dependency notices and support metadata. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Approved license/obligations and supported-version matrix ship with artifacts; missing notices or unclear redistribution rights block publication.

No implemented increment is recorded for this requirement.

### P05-03

**Sign and verify artifacts/installer metadata through scoped identities. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Consumer verification rejects modified bytes, wrong signer, expired/untrusted metadata and replayed unsupported releases.

No implemented increment is recorded for this requirement.

### P05-04

**Gate publication on the complete readiness/evidence bundle. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-01: AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Every Phase 0–4 baseline gate has current passing evidence; skipped client/capacity/security acceptance does not count as a pass.

No implemented increment is recorded for this requirement.

### P05-05

**Rehearse clean install and supported upgrade/migration paths. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PLAT-01: All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [PLAT-02: Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Fresh Linux hosts and prior supported versions preserve identities, permissions, keys and policy state; incompatible downgrade is rejected.

No implemented increment is recorded for this requirement.

### P05-06

**Promote exact artifacts through isolated staging with functional checks. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [AD-02: Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-06: Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [AD-07: Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Domain join/login/password/GPO/replication/restore smoke tests pass before production approval, with synthetic credentials and scoped access.

No implemented increment is recorded for this requirement.

### P05-07

**Serialize production rollout by fault domain with explicit abort criteria. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Canary/DC rollout preserves remaining authentication/DNS service; induced health/convergence failure pauses expansion and alerts the operator.

No implemented increment is recorded for this requirement.

### P05-08

**Provide tested rollback, forward-fix or restore per migration class. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-06: Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Runbooks identify irreversible transitions and expected RPO/RTO; exercises recover safely without replaying incompatible schema/key state.

No implemented increment is recorded for this requirement.

### P05-09

**Require independent sensitive-release approval and audit the decision. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-01: Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** No self-approved high-risk publication or privileged fork runner; platform limitations are disclosed, never treated as enforced protection.

**Pending PR proposals:** [\#17: Bump typescript from 6.0.3 to 7.0.2 in /dashboard](<https://github.com/Ise-Tom/Babel/pull/17>). See [open PR progress](#open-pull-requests).

No implemented increment is recorded for this requirement.

### P05-10

**Publish operator/security/support guides and known limitations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [UX-01: Accessible web administration and documented automation API/CLI](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** A new operator verifies/install/updates/restores using shipped docs; unsupported levels/clients and disclosure contacts are explicit.

No implemented increment is recorded for this requirement.

</details>


## Phase 06

**Sustained operations and maintenance — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-06.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P06-01

**Maintain explicit supported versions and security-update commitments. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Published matrix identifies release support/EOL and upgrade paths; advisory intake reaches accountable maintainers.

No implemented increment is recorded for this requirement.

### P06-02

**Monitor online authentication, DNS/time, replication, certificates and capacity. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Synthetic fault injection produces timely actionable alerts; cached offline login and missing telemetry do not count as online service success.

No implemented increment is recorded for this requirement.

### P06-03

**Operate vulnerability triage and coordinated disclosure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Exercises prove private report receipt, severity/impact assessment, patch/mitigation tracking and secure publication without premature sensitive details.

No implemented increment is recorded for this requirement.

### P06-04

**Run regular independent backup verification and restore drills. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Quarterly full-dataset isolated restores meet &lt;=1 h RPO/&lt;=4 h RTO and include credentials, SYSVOL and recovery-key access.

No implemented increment is recorded for this requirement.

### P06-05

**Manage expiry and security exception debt. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Certificate/key/legacy-protocol exceptions have owners and expiry; expired/unowned exceptions cannot silently continue.

No implemented increment is recorded for this requirement.

### P06-06

**Provide privacy-safe support diagnostics. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Export is explicitly scoped/redacted and access-audited; credential material, arbitrary user data and complete environments are excluded.

No implemented increment is recorded for this requirement.

### P06-07

**Keep capacity and reliability reports with meaningful error budgets. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Monthly site-level availability and growth trends include exclusions/outages and remediation; breaches generate owned corrective work.

No implemented increment is recorded for this requirement.

### P06-08

**Maintain dependency/tool/signing updates and reproducible update checks. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Daily/periodic scans actually run, stale results alert, signatures stay verified and urgent advisories do not wait for routine schedules.

No implemented increment is recorded for this requirement.

### P06-09

**Rehearse maintainer/provider loss and emergency service recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-10: Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>); [OPS-01: Backup/restore, upgrades, rotation, audit export, health and capacity visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Separate contacts, signing recovery and backup custody restore operations without a single absent administrator or failed domain provider.

No implemented increment is recorded for this requirement.

### P06-10

**Decommission data and versions through controlled retention policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [SEC-11: Minimize identity data, encrypt backups, document retention/deletion and data residency](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>)

**Acceptance evidence required:** Removal preserves required evidence/backup holds while preventing indefinite unnecessary identity data retention; migrations are auditable.

No implemented increment is recorded for this requirement.

</details>


## Phase 07

**Strong identity and privileged administration — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-07.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P07-01

**Provide secure passkey/hardware-key enrollment and recovery for privileged access. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-01: WebAuthn/FIDO2 passkeys and hardware security keys for administrator login; multiple authenticators and secure enrollment](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [A-03: Recovery hardened against helpdesk impersonation, SIM swapping and MFA fatigue](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Origin/replay/unauthorized enrollment tests fail; multiple factors, replacement and recovery are audited with no SMS-only Tier 0 bypass.

No implemented increment is recorded for this requirement.

### P07-02

**Implement time-bounded just-in-time/just-enough privileges. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-01: Just-in-time and just-enough privilege with expiring grants](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Grant expiry remains enforced after worker restart; tests cover nested groups, stale sessions/tickets and delayed replication with declared limits.

No implemented increment is recorded for this requirement.

### P07-03

**Separate requester/approver/executor for high-risk actions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-02: Dual approval and separation of duties for Tier 0 membership, trusts, replication rights, backup export and key operations](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** UI/API/bulk operations reject self-approval and scope substitution; signed-off target/content changes require reapproval.

No implemented increment is recorded for this requirement.

### P07-04

**Provide scoped managed Windows/Linux service and local-admin credential lifecycles. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [C-01: Windows LAPS-compatible local administrator password rotation and retrieval](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [C-02: Managed service accounts, including gMSA compatibility where selected](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [C-03: Linux service identities, keytab lifecycle and supported workload identity integrations](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Qualified LAPS/gMSA/keytab retrieval, rotation, offline behavior and denied readers pass; secrets never appear in logs or broad inventory.

No implemented increment is recorded for this requirement.

### P07-05

**Implement hardened password/self-service and lifecycle workflows. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-04: Password protection beyond basic policy: locally checked breached/common passwords, contextual exclusions, password history and supported fine-grained policies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [A-05: Adaptive throttling and credential-stuffing/password-spray detection across replicas](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [C-04: Joiner/mover/leaver workflows, ownership and deprovisioning reconciliation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [C-05: Delegated self-service password change/reset, account recovery and group requests](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Spray, enumeration, recovery impersonation and unauthorized reset/group request tests fail; breach checks do not export raw passwords.

No implemented increment is recorded for this requirement.

### P07-06

**Provide effective-permission and privilege-path views with access reviews. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-05: Effective-permission explorer and privilege-path analysis](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [B-06: Periodic access certification, ownership and orphaned-privilege cleanup](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Results match actual ACL/trust/nested-group decisions; unauthorized viewers cannot enumerate protected relationships.

No implemented increment is recorded for this requirement.

### P07-07

**Govern GPO changes through diffs, preview, approval and staged OU rollout. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [D-01: GPO version history, diffs, independent approval and staged OU rollout](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [D-02: Effective policy preview, precedence and resultant-policy troubleshooting](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [D-03: Tested hardening templates for Windows and Linux](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [D-04: Policy integrity/drift detection, safe script distribution and privileged policy ownership](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Version/SYSVOL consistency, out-of-band edits and resultant-policy comparisons are validated; revert restores real client behavior.

No implemented increment is recorded for this requirement.

### P07-08

**Provide monitored break-glass and privileged-workstation guidance. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [B-03: Privileged access workstations and tiered administration guidance](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [B-04: Emergency break-glass access with separate custody and monitored use](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** A rehearsed IdP/provider outage preserves audited emergency access with separate custody and post-use rotation, without permanent hidden bypass.

No implemented increment is recorded for this requirement.

### P07-09

**Enforce exception ownership, expiration and accessible policy workflows. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-02: Policy simulation and explainable access decisions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-03: Safe bulk operations with scope preview, dry run, idempotency and compensating actions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-04: Accessible secure enrollment/recovery and understandable authentication errors](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-05: Security exception register and policy-as-code change review](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Expired grants/exceptions fail closed; keyboard/screen-reader and policy-simulation journeys include safe bulk-change previews.

No implemented increment is recorded for this requirement.

### P07-10

**Qualify advanced privilege features without weakening baseline defaults. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-06: Authentication strength policies, session inventory and bounded revocation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-06: Operator training, trustworthy runbooks and versioned security baselines](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Negative/auth-strength/latency/recovery evidence covers selected feature IDs and mixed load; new security service failures cannot silently bypass MFA.

No implemented increment is recorded for this requirement.

</details>


## Phase 08

**Posture, certificate/federation services and detection — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-08.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P08-01

**Qualify certificate/smart-card authentication and enrollment profiles. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [A-02: Smart-card/certificate-based domain logon through PKINIT and compatible hardware-backed keys](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [E-04: Certificate enrollment and PKI integration, with any AD CS-compatible role separately qualified](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Real supported clients pass valid mapping/rotation and reject invalid templates, SAN escalation, expired/revoked certificates and weak mappings.

No implemented increment is recorded for this requirement.

### P08-02

**Provide secure federation/provisioning connectors with scoped authority. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [C-06: Signed, versioned provisioning integrations such as SCIM and an external secrets manager](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [J-01: OIDC/OAuth2 and SAML federation through separately qualified modules](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Issuer/audience, nonce/state/PKCE where applicable, malicious attributes, duplicate events and cross-organization mix-ups are tested; unknown claims grant no privilege.

No implemented increment is recorded for this requirement.

### P08-03

**Integrate device posture and network-access policies with clear freshness. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [D-05: Device posture and conditional-access integrations](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [D-06: Support for endpoint credential protections and application-control baselines](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [J-02: Network access integrations such as RADIUS/EAP-TLS](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Spoofed/stale/missing posture and provider outage behavior match approved policy; no raw posture flag grants Tier 0 membership.

No implemented increment is recorded for this requirement.

### P08-04

**Maintain certificate/key/trust inventory and renewal visibility. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [E-05: Certificate/key inventory, expiry forecasting and automated rotation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Expiry forecasting, safe overlap, CA/CRL/OCSP failure and renewal tests produce accurate status without disabling verification.

No implemented increment is recorded for this requirement.

### P08-05

**Implement structured protected audit export and investigation timelines. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [G-01: Structured, correlated audit export to SIEM/syslog with externally protected storage](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [G-05: Investigation views: identity timeline, effective permissions and configuration history](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Schema/version/provenance, gap detection, redaction and denied-reader tests pass; root-controlled local files are not claimed tamper-proof.

No implemented increment is recorded for this requirement.

### P08-06

**Develop labeled directory/credential/trust/GPO detection scenarios. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [G-02: Detection for replication abuse, suspicious DC registration, ACL escalation and privileged group changes](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [G-03: Detection for ticket abuse, password sprays, abnormal service-ticket requests and trust/GPO persistence](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Versioned fixtures measure expected alerts and false positives; missing endpoint signals/forged ticket limits are disclosed.

No implemented increment is recorded for this requirement.

### P08-07

**Provide safe canary identities and replayable detection-rule tests. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [G-04: Deception identities and monitored canary credentials](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [G-06: Detection engineering with replayable synthetic event fixtures](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Decoys have no real privilege, trigger approved handling and cannot be accidentally promoted into normal production accounts.

No implemented increment is recorded for this requirement.

### P08-08

**Provide privacy-scoped search/export and retention controls. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [J-03: Attribute-level privacy, scoped directory search and data-export controls](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [J-04: Retention, deletion and legal-hold policy for identity and audit data](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** LDAP/UI/API attribute denials, purpose-scoped exports, deletion/hold and residency policy tests pass without breaking required discovery.

No implemented increment is recorded for this requirement.

### P08-09

**Define organization isolation and external integration boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [J-05: Explicit multi-organization/tenant security boundaries](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Independent deployment/forest boundaries are documented; shared writable DCs are never sold as hostile-tenant isolation based only on UI roles.

No implemented increment is recorded for this requirement.

### P08-10

**Qualify module cost, observability and accessible posture reporting. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-01: Security posture dashboard with actionable, evidence-backed findings](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Reports show freshness, unsupported/unknown state, rule quality, provider dependencies and mixed-load overhead; a module outage does not stop core domain auth.

No implemented increment is recorded for this requirement.

</details>


## Phase 09

**Containment, key custody and compromise resilience — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-09.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P09-01

**Implement typed response workflows with scoped approvals and idempotency. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-01: Audited response workflows for account/device disable, trust suspension and service-key rotation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Disable/quarantine/trust/key actions reject wrong scope, replay, expired approval and unauthorized API calls; execution and cancellation are audited.

No implemented increment is recorded for this requirement.

### P09-02

**Rehearse complete domain-compromise credential recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-02: Domain-compromise recovery plan covering ticket-signing, machine, service, trust and administrator credentials](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Ticket-signing double rotation, service/machine/trust/admin keys and downstream effects are sequenced and verified in an isolated lab.

No implemented increment is recorded for this requirement.

### P09-03

**Quarantine and safely reintroduce suspect replicas. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-03: Replica quarantine and controlled reintroduction after suspected compromise](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** A compromised/stale replica cannot contaminate clean state; evidence preservation, trust revocation, role recovery and controlled reenrollment are exercised.

No implemented increment is recorded for this requirement.

### P09-04

**Qualify read-only branch and password-cache exposure profiles. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [I-01: Read-only/limited-secret branch controller profiles when explicitly implemented by the native core](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Exact RODC/password-replication semantics, permitted caches, theft blast radius and credential reset behavior pass; writable state is never labeled read-only.

No implemented increment is recorded for this requirement.

### P09-05

**Qualify HSM/TPM/KMS integration per key class. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [F-03: Hardware-backed key custody through HSM/TPM or a supported external KMS](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Supported key operations, latency, outage, backup/custody and provider recovery are tested; unsupported AD verifiers/keys are explicitly excluded.

No implemented increment is recorded for this requirement.

### P09-06

**Apply least-privilege host/service and network exposure profiles. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [F-01: Reviewed systemd sandboxing, capability reduction and AppArmor/SELinux profiles](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [F-02: Host security posture: supported Secure Boot, measured boot and disk encryption](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [F-05: Hardened Linux storage, syscall and network profiles for optional container packages](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [F-06: Linux host baseline drift and agent/update integrity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [E-06: Protocol exposure control and network segmentation templates](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Capabilities, systemd sandboxing, LSM policies, RPC ranges and update paths pass functional/denied tests without a privileged-container default.

No implemented increment is recorded for this requirement.

### P09-07

**Maintain clean-room/offline backup recovery with split custody. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [I-02: Immutable/offline encrypted backups with split custody and recovery-key escrow](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [I-05: Recovery environment integrity and safe backup validation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [H-04: Recovery-safe security state restoration](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Independent recovery works after directory/provider loss and reconciles revoked identities, key epochs and directory/SYSVOL consistency.

No implemented increment is recorded for this requirement.

### P09-08

**Provide safe degraded modes for security-service outages. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [I-03: Site isolation, failover and revocation-risk visibility](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [I-04: Security operation budgets and safe degraded modes](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** MFA/audit/KMS/CA failures have explicit per-operation behavior; no silent auth bypass, unbounded audit flood or hidden evidence loss occurs.

No implemented increment is recorded for this requirement.

### P09-09

**Exercise ransomware, insider, maintainer and provider compromise playbooks. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [H-05: Tested response playbooks and tabletop exercises](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Tabletops plus technical drills record response time, operator mistakes, evidence retained and follow-up fixes.

No implemented increment is recorded for this requirement.

### P09-10

**Validate compartmentalization under malicious and resource-exhaustion scenarios. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [F-04: Resource isolation and DoS controls per service/peer](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [E-01: Compatibility-aware legacy authentication retirement](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [E-02: Kerberos delegation, ticket and principal hardening](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [E-03: Trust quarantine and cross-forest entitlement inspection](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Noisy response/relay/query workloads cannot exceed approved blast radius or violate authentication SLOs without an explicit failed qualification.

No implemented increment is recorded for this requirement.

</details>


## Phase 10

**Continuous security assurance and trusted delivery — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-10.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P10-01

**Produce independently verifiable reproducible artifacts and inventories. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-01: Reproducible packages/images, signed provenance/SBOM and dependency license/CVE inventory](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Independent rebuilds compare bytes or documented nondeterminism; SBOM/provenance/commit/artifact identities align and license notices are reviewed.

No implemented increment is recorded for this requirement.

### P10-02

**Protect update channels from wrong signer, rollback and freeze. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-02: Secure update metadata with rollback/freeze protection and key recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Expired/version-replayed metadata and malicious mirrors fail verification; signing-key compromise and offline update recovery are rehearsed.

No implemented increment is recorded for this requirement.

### P10-03

**Maintain multi-protocol parser/state-machine fuzz campaigns. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-03: Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** LDAP/RPC/Kerberos/DNS/policy inputs exercise bounded parsers with sanitizer/property regressions; failures yield minimized tracked cases.

No implemented increment is recorded for this requirement.

### P10-04

**Differentially test protocol semantics against a licensed reference. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-03: Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Versioned selected operations compare real outputs/state effects; divergence is triaged, not accepted solely because a second implementation matches.

No implemented increment is recorded for this requirement.

### P10-05

**Apply focused formal/property analysis to high-risk invariants. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-04: Property-based checks or formal analysis for bounded high-risk logic](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Models for authorization, grant expiry, replication conflict and key transitions state assumptions and find/reject known counterexamples.

No implemented increment is recorded for this requirement.

### P10-06

**Run recurring independent assessments and coordinated research intake. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-05: Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Published program scope, safe-harbor/disclosure handling and funded remediation produce retested findings without exposing active secrets.

No implemented increment is recorded for this requirement.

### P10-07

**Require two-person sensitive release decisions and maintainer continuity. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-06: Hardened release governance and maintainer continuity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Loss/compromise of one signer/reviewer cannot silently publish a trusted update; emergency process and audit remain usable.

No implemented increment is recorded for this requirement.

### P10-08

**Keep accessible posture, policy-as-code and operator education current. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [L-01: Security posture dashboard with actionable, evidence-backed findings](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-02: Policy simulation and explainable access decisions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-03: Safe bulk operations with scope preview, dry run, idempotency and compensating actions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-04: Accessible secure enrollment/recovery and understandable authentication errors](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-05: Security exception register and policy-as-code change review](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [L-06: Operator training, trustworthy runbooks and versioned security baselines](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Freshness/uncertainty, safe previews and exception expiry are tested; new operators complete privileged and emergency runbooks without hidden knowledge.

No implemented increment is recorded for this requirement.

### P10-09

**Monitor governance and platform enforcement limitations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-06: Hardened release governance and maintainer continuity](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Actual required-check/review/ref/environment protections are verified where supported; unavailable private-repo features remain explicit release risks.

**Pending PR proposals:** [\#17: Bump typescript from 6.0.3 to 7.0.2 in /dashboard](<https://github.com/Ise-Tom/Babel/pull/17>). See [open PR progress](#open-pull-requests).

No implemented increment is recorded for this requirement.

### P10-10

**Publish recurring security assurance evidence without certification overclaims. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [K-05: Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>); [K-04: Property-based checks or formal analysis for bounded high-risk logic](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>)

**Acceptance evidence required:** Reports include test/model scope, failures, skips, unsupported platforms and residual risks; a green scanner suite is never labeled proof of security.

No implemented increment is recorded for this requirement.

</details>


## Phase 11

**Endpoint inventory and patch-control foundation — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-11.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P11-01

**Define a supported endpoint/agent/application update matrix. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Exact Windows editions/builds, Linux releases/architectures and selected third-party products have native-engine feasibility and licensing evidence.

No implemented increment is recorded for this requirement.

### P11-02

**Enroll agents with unique revocable mutual authentication. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Replay/cloned tokens, wrong device identities and revoked certificates fail; enrollment/rotation/rescue are audited without embedded domain-admin secrets.

No implemented increment is recorded for this requirement.

### P11-03

**Collect trustworthy bounded hardware/software/update inventory. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-01: Continuous hardware/OS/software inventory and update applicability assessment](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Compare actual OS/native package tools and reboot state; missing/stale/unknown/unsupported observations remain distinguishable.

No implemented increment is recorded for this requirement.

### P11-04

**Build an authenticated applicability/supersedence/dependency catalog. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-02: Trusted patch/vulnerability catalog with dependencies, supersedence and known issues](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Vendor signatures/backports/prerequisites and known-issue fixtures yield correct applicable/not-applicable results beyond version-string matching.

No implemented increment is recorded for this requirement.

### P11-05

**Maintain explicit dynamic-target attributes and provenance. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-04: Dynamic device groups, targeting previews and fixed campaign membership snapshots](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Approved device/OU/tag mappings resist spoofed inventory and unauthorized cross-group changes; hostname reuse does not inherit device authority.

No implemented increment is recorded for this requirement.

### P11-06

**Detect competing update authorities and unsupported endpoints. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** WSUS/Intune/native locks and EOL products surface actionable conflicts; the service does not race another manager into unsupported state.

No implemented increment is recorded for this requirement.

### P11-07

**Separate agent communication and privileged action boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** A malicious inventory payload cannot execute a command, read arbitrary files or gain package-install/EDR/support rights.

No implemented increment is recorded for this requirement.

### P11-08

**Design authenticated content staging/site caching. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Poisoned cache/metadata, wrong recipient and signature failures are rejected; relay possession of payload never authorizes installation.

No implemented increment is recorded for this requirement.

### P11-09

**Set inventory privacy, retention and capacity budgets. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Fields/roles/retention are documented; 10k fleet simulation plus representative real endpoints reports freshness, resource and storage overhead.

No implemented increment is recorded for this requirement.

### P11-10

**Deliver a recoverable Linux-hosted management foundation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Controller/agent restart, certificate expiry and provider outage preserve device identity and show stale state without affecting domain login.

No implemented increment is recorded for this requirement.

</details>


## Phase 12

**Controlled patch campaigns and verified installation — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-12.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P12-01

**Approve exact targets, content and risk before scheduling. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-04: Dynamic device groups, targeting previews and fixed campaign membership snapshots](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Changing membership/digest/privileged scope requires reapproval; self-approval, cross-group API calls and stale authorization fail.

No implemented increment is recorded for this requirement.

### P12-02

**Implement gated canary/pilot/production rings. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-05: Canary/pilot/production rings with configurable dwell, health checks, rollout limits and automatic pause](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Bad patch/health/error-rate fixtures pause later rings; missing report coverage cannot count as promotion success.

No implemented increment is recorded for this requirement.

### P12-03

**Enforce maintenance/deadline/reboot policy with user notice. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-06: Maintenance windows, deadlines, user notifications, reboot deferral and forced-reboot controls](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** DST/time-zone, sleep/offline devices, active sessions, grace/deferral and forced reboot scenarios match explicit approved policy.

No implemented increment is recorded for this requirement.

### P12-04

**Run disk/power/prerequisite/lock and application-health preflight. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-07: Preflight disk/power/network checks, dependency handling and application/service-aware installation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Blocked devices are reported separately; competing native transactions and unsupported reboot suppression are not overridden silently.

No implemented increment is recorded for this requirement.

### P12-05

**Deliver verified packages through throttled resumable site caches. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Vendor signatures plus approved digests survive retries/proxies; tamper, replay, incomplete files and quota failures block installation.

No implemented increment is recorded for this requirement.

### P12-06

**Revalidate typed job authority immediately before privileged execution. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Expired/cancelled jobs cannot run after reconnect; duplicate IDs and lost replies cannot cause repeated install or arbitrary command execution.

No implemented increment is recorded for this requirement.

### P12-07

**Verify actual installation, reboot and post-patch health. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-10: Independent post-install verification of installed version, reboot completion and service health](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Native version/state and health checks confirm remediation; exit zero, downloaded content or offline silence alone never counts as verified.

No implemented increment is recorded for this requirement.

### P12-08

**Provide update-class-specific failure recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-11: Safe uninstall/rollback or tested recovery per update class](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Uninstall works where supported; irreversible kernel/application/state changes follow tested restore/reimage/forward-fix with recorded limitations.

No implemented increment is recorded for this requirement.

### P12-09

**Provide emergency prioritization and controlled overrides. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-12: Emergency remediation and risk-based prioritization](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Known-exploited/exposed asset priority is explainable; override scope, expiry, independent approval and audit prevent unlimited emergency privilege.

No implemented increment is recorded for this requirement.

### P12-10

**Protect identity-service availability during server patching. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-15: Availability-aware server and domain-controller maintenance](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** A controller rollout cannot reboot all site DCs together; induced auth/replication health failure pauses and recovers the campaign.

No implemented increment is recorded for this requirement.

</details>


## Phase 13

**Production patch fleet, compliance and resilience — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-13.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P13-01

**Qualify real OS/application remediation plus large-fleet orchestration. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [PATCH-10: Independent post-install verification of installed version, reboot completion and service health](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Publish exact platform/device counts and real versus simulated roles; containers/simulators cannot replace native install/reboot evidence.

No implemented increment is recorded for this requirement.

### P13-02

**Meet freshness/ack targets with transparent denominators. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-01: Continuous hardware/OS/software inventory and update applicability assessment](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Connected/stale/offline/unsupported categories are explicit; p95 ack and &gt;=99% inventory targets exclude neither unexplained failures nor hidden missing agents.

No implemented increment is recorded for this requirement.

### P13-03

**Bound reconnect storms, work queues and retries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** 10k-agent recovery after controller/site outage preserves authorization/cancellation, avoids duplicate installs and publishes convergence and queue metrics.

No implemented increment is recorded for this requirement.

### P13-04

**Budget payload bandwidth and relay storage from real package sizes. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-08: Bandwidth-aware content distribution with authenticated site relays and approved offline import](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Transfer tests measure cache hits/misses/eviction/retries under configured site limits; control API rate is not reported as distribution throughput.

No implemented increment is recorded for this requirement.

### P13-05

**Produce truthful compliance/SLA and exception reports. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Missing/stale/offline/unverified/EOL devices cannot appear compliant; risk-based overdue time and exception expiry are reproducible from raw receipts.

No implemented increment is recorded for this requirement.

### P13-06

**Provide delegated UI/API/CLI and ticket-system integrations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Role/target/approval/audit behavior agrees across clients; connector outages and duplicate tickets cannot grant new execution rights.

No implemented increment is recorded for this requirement.

### P13-07

**Recover controller/relay state and interrupted upgrades safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [PATCH-11: Safe uninstall/rollback or tested recovery per update class](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Backups, expired certificates, full disks and process failures reconcile endpoint reality before resuming approved campaigns.

No implemented increment is recorded for this requirement.

### P13-08

**Rehearse compromised-controller containment and recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-12: Emergency remediation and risk-based prioritization](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Stop dispatch, revoke/rotate trust, inspect queue/catalog, recover signing/enrollment and reinstall trusted agents through a documented rescue process.

No implemented increment is recorded for this requirement.

### P13-09

**Qualify agent/controller version skew and secure upgrades. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Supported old/new combinations preserve identity and job semantics; staged signed-agent rollout pauses bad versions and retains recovery.

No implemented increment is recorded for this requirement.

### P13-10

**Release the patch service with owned operating limits. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-15: Availability-aware server and domain-controller maintenance](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>)

**Acceptance evidence required:** Independent review, resource/storage/retention sizing, failure runbooks and mixed-load no-directory-SLO-regression evidence are approved before production.

No implemented increment is recorded for this requirement.

</details>


## Phase 14

**Remote desktop and terminal access — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-14.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P14-01

**Qualify actual desktop and terminal behavior by supported OS/session type. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real Windows sessions and Linux headless/X11/Wayland cases have a versioned supported/unsupported matrix and tested maintained protocol engines.

No implemented increment is recorded for this requirement.

### P14-02

**Require unique authenticated devices and scoped operator MFA/step-up. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-03: Separately approved unattended administration](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Wrong-device, replayed/expired tokens and stolen low-privilege accounts cannot open a session or reuse a privileged endpoint credential.

No implemented increment is recorded for this requirement.

### P14-03

**Provide visible attended consent and immediate disconnect. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-02: Attended support with visible user consent and an immediate disconnect action](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Denied/expired/misleading requests fail; local user sees operator identity and can terminate a session without a remote approval.

No implemented increment is recorded for this requirement.

### P14-04

**Gate unattended support separately with time/device boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-03: Separately approved unattended administration](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** No implicit permission from domain membership or patch role; expired device/operator grants fail and administrative access is audited.

No implemented increment is recorded for this requirement.

### P14-05

**Separate terminal/elevation/clipboard/transfer/recording permissions. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [REMOTE-06: Safe operation across OS privileges and session states](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Denied channels cannot be reenabled through protocol/API bypass; locked screens, user switching and OS security prompts remain enforced.

No implemented increment is recorded for this requirement.

### P14-06

**Authenticate and encrypt broker/relay transport with explicit trust. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Certificate/recipient failures close connections; NAT/proxy and relay compromise tests document who can see session content and protect credential custody.

No implemented increment is recorded for this requirement.

### P14-07

**Enforce bounded revocation and outage session policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** A connected session loses authority within a configured, tested &lt;=60 s revocation target; offline/broker-failed cases follow explicit safe expiry rules.

No implemented increment is recorded for this requirement.

### P14-08

**Govern recording and support privacy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Notice, policy, access/retention and sensitive-input boundaries are tested; no covert sessions or indiscriminate credential/key logging is allowed.

No implemented increment is recorded for this requirement.

### P14-09

**Handle reconnect, concurrent operators and privilege changes safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-06: Safe operation across OS privileges and session states](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Session identity and consent are revalidated; no unnoticed takeover, indefinitely cached grant or unintended concurrent control survives switching/restart.

No implemented increment is recorded for this requirement.

### P14-10

**Qualify relay capacity and support compromise recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Published concurrency/bitrate/latency plus compromised-operator/broker rescue tests pass without affecting identity or emergency recovery paths.

No implemented increment is recorded for this requirement.

</details>


## Phase 15

**General server-to-device file delivery — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-15.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P15-01

**Authorize exact file content, device scope, destination and expiry. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-01: Explicit server-originated uploads to one or many selected endpoints](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Target/digest/path changes require renewed approval; upload-only and cross-group operators cannot gain execution, patch or retrieval rights.

No implemented increment is recorded for this requirement.

### P15-02

**Protect staging and source/recipient authenticity. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-02: Secure staging, integrity and recipient verification](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Wrong sender/device, tampered metadata, unauthenticated hash substitution and untrusted TLS are rejected; staged confidential files are access-restricted.

No implemented increment is recorded for this requirement.

### P15-03

**Validate destinations at open/finalization without traversal/race bypass. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-03: Destination and privilege restrictions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real Windows reparse and Linux symlink/rename race tests cannot escape allowed directories or overwrite privileged startup/system files.

No implemented increment is recorded for this requirement.

### P15-04

**Apply explicit ownership, ACL and overwrite policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-03: Destination and privilege restrictions](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Default deny for privileged locations; approved overwrite preserves declared permissions and cannot convert a data upload into executable persistence.

No implemented increment is recorded for this requirement.

### P15-05

**Provide resumable bounded authenticated transfers. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Corrupt/reordered/replayed chunks, offset overflow, connection loss and retries cannot finalize incorrect or unauthorized content.

No implemented increment is recorded for this requirement.

### P15-06

**Finalize atomically where supported and report verified receipt. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Partial files are never treated as delivered; unsupported atomic behavior is visible and staged fallback is tested with interrupted finalization.

No implemented increment is recorded for this requirement.

### P15-07

**Enforce quotas, bandwidth, cancellation and stale-content cleanup. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Full disk, expired/cancelled jobs and abandoned staged data remain bounded; reconnect revalidates authority before continuing.

No implemented increment is recorded for this requirement.

### P15-08

**Apply explicit file-content and malware policy without automatic execution. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Type/size/scanning failures block according to policy; detection limits are documented and uploads cannot silently launch installers/scripts.

No implemented increment is recorded for this requirement.

### P15-09

**Provide privacy-safe audit and separate retrieval policy. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Operator/device/path/digest/outcome are auditable without raw contents; uploading never grants access to user files or unsolicited endpoint surveillance.

No implemented increment is recorded for this requirement.

### P15-10

**Qualify transfer recovery and mixed-load resource isolation. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Concurrent representative real filesystem transfers survive agent/controller restarts and malicious paths without directory SLO regression.

No implemented increment is recorded for this requirement.

</details>


## Phase 16

**Native endpoint detection and response — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-16.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P16-01

**Ship a dedicated securely enrolled signed sensor/agent module. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Per-device identity/revocation, staged signed updates and authorized rescue/uninstall pass; module rights are isolated from support and patch executors.

No implemented increment is recorded for this requirement.

### P16-02

**Qualify supported telemetry on real endpoint OS/kernel builds. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-02: OS-specific endpoint telemetry](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Process lineage/hashes, network, file and selected persistence/security events match fixture ground truth; unavailable sources/blind spots are explicit.

No implemented increment is recorded for this requirement.

### P16-03

**Preserve stable event/process provenance and loss visibility. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-02: OS-specific endpoint telemetry](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** PID reuse, clock changes, reconnect duplicates, reordered events and buffer overflow cannot silently corrupt identity or claim complete healthy telemetry.

No implemented increment is recorded for this requirement.

### P16-04

**Implement signed/versioned bounded detection and indicator rules. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Labeled malicious/benign synthetic scenarios measure precision/recall and alert delay; costly/untrusted rules cannot exhaust endpoint resources.

No implemented increment is recorded for this requirement.

### P16-05

**Provide privacy-scoped investigation and evidence collection. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-04: Investigation and privacy-scoped evidence collection](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Case/timeline/collection actions require scope and audit; evidence hashes/provenance/retention and denied-reader tests pass without blanket memory/credential extraction.

No implemented increment is recorded for this requirement.

### P16-06

**Implement typed authorized process/file containment and quarantine. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Wrong process generation, expired/replayed jobs, protected system targets and unauthorized analysts are rejected; quarantine limitations are documented.

No implemented increment is recorded for this requirement.

### P16-07

**Provide recoverable device isolation and bounded automated response. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Narrow authenticated rescue paths survive isolation; two-person/mass-action limits and false-positive tests prevent fleet/DC lockout; release-from-isolation is rehearsed.

No implemented increment is recorded for this requirement.

### P16-08

**Operate offline buffering and trusted cached rules safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Disk/memory quotas, encryption/access controls, sequence gaps and reconnect backpressure preserve visibility; outages do not stall domain login or fill disks indefinitely.

No implemented increment is recorded for this requirement.

### P16-09

**Detect sensor tamper and define realistic protection boundaries. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-06: Tamper resistance and trustworthy sensor health](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Stopped/stale sensors, changed policy and signer failure alert with provenance; root/kernel control is not claimed containable by local tamper protection.

No implemented increment is recorded for this requirement.

### P16-10

**Qualify detection/prevention behavior and external response integrations. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Real endpoint performance, false positives/negatives, benign safety and SIEM/SOAR connector replay/authorization tests pass before enforcement is enabled.

No implemented increment is recorded for this requirement.

</details>


## Phase 17

**Joint fleet qualification and endpoint service release — Planned**

[Canonical design and dependencies](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/phases/phase-17.md>)

<details>
<summary>10 requirements, associated features and evidence</summary>

### P17-01

**Run the combined supported-endpoint and directory workload. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-03: Windows OS, Linux package/kernel and explicitly selected third-party application patching](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-02: OS-specific endpoint telemetry](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Reports identify real versus simulated endpoints/sessions, platform counts, traffic mix and exact build/rule versions; all individual contracts remain satisfied.

No implemented increment is recorded for this requirement.

### P17-02

**Qualify aggregate concurrency, latency and resource budgets. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** 50 desktop/100 terminal/250 transfer and EDR steady/burst profiles publish CPU/RAM/disk/IOPS/network/retention sizing, cost and endpoint overhead.

No implemented increment is recorded for this requirement.

### P17-03

**Preserve authentication/replication SLOs under endpoint pressure. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-15: Availability-aware server and domain-controller maintenance](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Telemetry floods, relay misses, large transfers and reconnect storms cannot starve core directory services within approved resource isolation limits.

No implemented increment is recorded for this requirement.

### P17-04

**Recover from site/provider/control-plane failures. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [EDR-08: Offline operation and resilience under telemetry/provider outages](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** 24-hour partition, clock/DNS faults, full disks, expired issuers and 10k reconnect preserve authorization, bounded queues and truthful unknown state.

No implemented increment is recorded for this requirement.

### P17-05

**Reconcile pending/partial operations after backup/upgrade recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [FILE-04: Resumable, bandwidth-limited transfer with accurate receipts](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [REMOTE-05: Secure brokering and prompt revocation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-05: Authorized response: stop/quarantine malicious processes/files and isolate a device](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Actual endpoint patch/file/isolation/session states are verified before replay; duplicate, cancelled and expired jobs cannot gain fresh authority.

No implemented increment is recorded for this requirement.

### P17-06

**Exercise cross-module privilege and compromise boundaries independently. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-03: Separately approved unattended administration](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [FILE-01: Explicit server-originated uploads to one or many selected endpoints](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Support/upload/patch/EDR roles cannot exchange execution authority; external review includes enrollment, brokers, privileged executors, signing and recovery.

No implemented increment is recorded for this requirement.

### P17-07

**Rehearse emergency stop and fleet trust recovery. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-14: Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [EDR-07: SIEM/SOAR integration and safe automated response](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Stop dispatch, revoke/rotate identities and rules, inspect queues and reenroll through an independent rescue path; offline stop limits and irreversible actions are explicit.

No implemented increment is recorded for this requirement.

### P17-08

**Qualify privacy and usability for real operator workflows. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [REMOTE-02: Attended support with visible user consent and an immediate disconnect action](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [REMOTE-04: Session control, audit and sensitive-channel separation](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [FILE-05: Content policy, separate execution and audit](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-04: Investigation and privacy-scoped evidence collection](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Notice/consent/recording/evidence retention and accessible triage/patch/support journeys pass; missing data cannot appear as healthy/compliant.

No implemented increment is recorded for this requirement.

### P17-09

**Release immutable versioned endpoint services and agents safely. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-09: Durable campaign orchestration and disconnected endpoint recovery](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [EDR-01: Dedicated installed sensor/agent module with secure enrollment and update lifecycle](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** Signed artifacts, SBOM/provenance, staged agent upgrades/version skew and supported Linux/Windows packages pass with defined rollback/forward-recovery.

No implemented increment is recorded for this requirement.

### P17-10

**Publish final endpoint service readiness and ownership. — Planned**

No implementation or acceptance evidence recorded.

**Associated features:** [PATCH-13: Compliance dashboards, remediation SLAs, exception register and report export](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>); [REMOTE-01: Authenticated desktop and terminal sessions to enrolled, authorized devices](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [FILE-01: Explicit server-originated uploads to one or many selected endpoints](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>); [EDR-03: Behavioral detection, indicator matching and versioned rules](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>)

**Acceptance evidence required:** All PATCH/REMOTE/FILE/EDR and selected security gates have current evidence, operator/support owners and known limits; no unrun acceptance is labeled production ready.

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

**Problems:** I01, I02

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

**Problems:** I10

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

**Problems:** I14, I15

**Source evidence:** [scripts/check\_design.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/scripts/check_design.py>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/scripts/render_dashboard.py>) · [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/dashboard/src/main.ts>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/dashboard/tests/dashboard.spec.ts>) · [tests/test\_design.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/tests/test_design.py>) · [tests/test\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/tests/test_dashboard.py>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/docs/project-dashboard.md>)

### W21 · Support public repository dashboard publication and prepare visibility transition

**Implemented increment**

**Requirements:** P00-10, P01-01, P01-10

**How it was done:** Publisher and PR collector accept either explicit Babel visibility and reject other repository identities or unknown visibility. Retained default-branch-only publication, current-main revision checks, bounded data-only PR imports, metadata-only fork reporting and fast-forward README-only updates. Renamed the publishing workflow and corrected private-only documentation.

**Recorded validation:** 80 Python tests pass with 98% tooling coverage; strict types, lint, documentation links, actionlint and Zizmor pass. Tests cover public/private publication, unknown visibility, unrelated destinations and public fork metadata isolation. Gitleaks scanned fetched branch history with redacted output and found no leaks.

**Limits and remaining work:** Owner explicitly authorized public visibility, but GitHub rejected the integration’s private=false request with HTTP 403. The repository remains private and hosted CI is still blocked by billing. This PR must merge before default-branch publication supports public visibility. No license was invented and no paid capacity was purchased.

**Problems:** I15, I16

**Source evidence:** [scripts/publish\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/scripts/publish_dashboard.py>) · [scripts/collect\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/scripts/collect_pr_progress.py>) · [tests/test\_dashboard\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/tests/test_dashboard_delivery.py>) · [tests/test\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/tests/test_pr_progress.py>) · [.github/workflows/dashboard-publish.yml](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/.github/workflows/dashboard-publish.yml>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/docs/project-dashboard.md>)

## Problems encountered

### I01 · GitHub API initially blocked by egress policy

**Resolved** · Phases 00, 01

Git reads/pushes worked while api.github.com was excluded, so draft PR creation returned Forbidden. The CLI auth error alone did not establish missing credentials.

**Resolution:** The owner opened Internet/API access; the PR retry succeeded without asking for a raw token.

**Next action:** Keep API connectivity distinct from Git and credential readiness.

**Provenance:** Recorded development-session incident; no public issue was created.



### I02 · Mandatory merge protection unavailable on current GitHub plan

**Open** · Phases 00, 01, 05, 10

GitHub rejected ruleset access for this private repository with HTTP 403 and requested a supported plan or public visibility. Passing CI is not enforced merge protection.

**Resolution:** Still open

**Next action:** Owner chooses a supported plan/visibility and configures required checks/reviews. No paid-plan or visibility change has been made.

**Provenance:** GitHub API observation recorded during pipeline setup; verify again before production release.

[docs/ci-cd.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/ci-cd.md>)

### I03 · Project license and contributor policy not selected

**Open** · Phases 00, 01, 05

No project LICENSE is selected. Native crates remain unpublished and source-prerelease creation is blocked by the license gate.

**Resolution:** Still open

**Next action:** Project owner resolves D-01 before public distribution and external contribution policy acceptance.

**Provenance:** Current repository decision register; third-party development license policy does not choose the project license.

[docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/decisions.md>)

### I04 · Licensed isolated Windows reference lab is missing

**Open** · Phases 00, 01, 02

Independent Linux LDAP-client evidence exists, but there is no recorded real Windows join/login/GPO conformance result or qualified reference image matrix.

**Resolution:** Still open

**Next action:** Provide reproducible isolated Windows/reference hosts and exact supported builds before accepting Windows behavior.

**Provenance:** Explicitly outstanding; no Windows test is marked passed.

[docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/decisions.md>) · [docs/phase-01-progress.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/phase-01-progress.md>)

### I05 · Persistent identity, storage and replication decisions remain open

**Open** · Phases 00, 01, 02, 03

The lab has no persistent state. SID/GUID/schema/ACL, transaction/journal format, key custody and compatible replication metadata require reviewed designs and failure tests.

**Resolution:** Still open

**Next action:** Resolve D-04/D-05/D-06 before valuable credential-bearing writes or fixed recovery formats.

**Provenance:** Design blocker, not an implemented storage defect.

[docs/decisions.md](<https://github.com/Ise-Tom/Babel/blob/3a69a6ba9cba6ce717fc712bae8d1fb07420e401/docs/decisions.md>)

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

### I10 · Dashboard access and Pages activation remain unavailable

**Open** · Phases 00, 01

The app ran inside the cloud workspace, but no user-accessible preview route was established. GitHub returned HTTP 403 for Pages activation; the repository still reports Pages disabled.

**Resolution:** Still open

**Next action:** Keep progress available on the private GitHub report; a future hosting change needs an actually verified accessible URL.

**Provenance:** Recorded development-session evidence and repository/CI observations; no separate public issue was created.

[docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/17228586920c9783ef3708f24ec782e542f48140/docs/project-dashboard.md>) · [.github/workflows/dashboard-pages.yml](<https://github.com/Ise-Tom/Babel/blob/17228586920c9783ef3708f24ec782e542f48140/.github/workflows/dashboard-pages.yml>)

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

The design validator forced exactly ten sequential requirements per phase, while the report called those broad contracts substeps. Zero recorded acceptances made implemented increments hard to distinguish from owner-reviewed scope.

**Resolution:** Removed the fixed quota, clarified requirement/increment labels and documented scoped owner acceptance questions. The owner answered “Accept this scope” for P01-01 and P01-10; both carry reviewer/date/evidence records. Unequal-size regression tests pass. Phase acceptance remains outstanding.

**Next action:** Merge the reviewed acceptance records after required checks can run; continue decomposing future work according to scope and dependencies while preserving requirement coverage.

**Provenance:** Project owner requested acceptance questions and said substep counts need not be linear; no separate GitHub issue was created.

[scripts/check\_design.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/scripts/check_design.py>) · [scripts/render\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/scripts/render_dashboard.py>) · [dashboard/src/main.ts](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/dashboard/src/main.ts>) · [dashboard/tests/dashboard.spec.ts](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/dashboard/tests/dashboard.spec.ts>) · [tests/test\_design.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/tests/test_design.py>) · [tests/test\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/tests/test_dashboard.py>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/fbf7cbd89be80e0f18f2464296deb4ad08383ca3/docs/project-dashboard.md>)

### I15 · GitHub Actions jobs blocked before startup by account billing

**Open** · Phases 00, 01

All jobs in PR \#18 CI run 44156039039 have zero executed steps. GitHub annotation: The job was not started because recent account payments have failed or your spending limit needs to be increased. Automatic dashboard refresh jobs are affected too.

**Resolution:** Still open

**Next action:** Repository/account owner checks GitHub Billing &amp; plans and restores Actions capacity, then reruns PR CI and the private dashboard workflow. Local checks do not replace the required hosted gate.

**Provenance:** Observed GitHub run 44156039039, check run 134296912744 annotation; no pipeline commands ran.

[.github/workflows/ci.yml](<https://github.com/Ise-Tom/Babel/blob/cd6ad149870a05db4ab2a4f7fbca3e4d461af848/.github/workflows/ci.yml>) · [.github/workflows/dashboard-publish.yml](<https://github.com/Ise-Tom/Babel/blob/cd6ad149870a05db4ab2a4f7fbca3e4d461af848/.github/workflows/dashboard-publish.yml>)

### I16 · GitHub integration cannot apply the authorized public visibility setting

**Open** · Phases 00, 01

The project owner explicitly requested public visibility. PATCH /repos/Ise-Tom/Babel with private=false returned HTTP 403, Resource not accessible by integration, despite repository metadata showing admin=true. The repository remained private on readback.

**Resolution:** Still open

**Next action:** Owner uses repository Settings → General → Danger Zone → Change repository visibility → Change to public. Rerun latest PR \#18 CI and merge the public-compatible publisher after required checks pass. Verify actual Actions capacity; a remaining account-wide billing restriction requires account attention.

**Provenance:** Direct GitHub API response in the authorized visibility-change task on 2026-11-17; no automatic approval-review rejection occurred and no visibility setting was applied.

[scripts/publish\_dashboard.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/scripts/publish_dashboard.py>) · [scripts/collect\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/scripts/collect_pr_progress.py>) · [tests/test\_dashboard\_delivery.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/tests/test_dashboard_delivery.py>) · [tests/test\_pr\_progress.py](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/tests/test_pr_progress.py>) · [.github/workflows/dashboard-publish.yml](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/.github/workflows/dashboard-publish.yml>) · [docs/project-dashboard.md](<https://github.com/Ise-Tom/Babel/blob/4ecfc729a9cae8d8f160dce73e344be926121457/docs/project-dashboard.md>)

## Feature catalog

| Feature | Capability | Acceptance evidence |
| --- | --- | --- |
| [PLAT-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | All Babel server roles install and operate on the declared Linux baseline without a Windows Server dependency | Clean Linux host provisions a domain; Windows client joins, authenticates and applies GPO; admin API/UI operate with no Windows server present |
| [PLAT-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Repeatable Linux installation, service supervision, reboot recovery, upgrade and removal that preserves directory data by default | Fresh-host install, reboot and interrupted-upgrade tests; documented service ordering, DNS/time/firewall prerequisites and explicit data-deletion procedure |
| [PLAT-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Linux host hardening and persistent data integrity | Verified service identities, minimum required privileges, secret/data file permissions, applicable AppArmor/SELinux policy, filesystem ACL/xattr preservation and backup/restore tests |
| [AD-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | AD-compatible domain and forest creation, schema, objects, SIDs/GUIDs, users, computers, nested groups, ACLs, password policy, delegation, and recycle/restore | Import/export and object/ACL comparison against an isolated Windows AD reference domain; denied-operation cases |
| [AD-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Supported Windows domain join, login, password change/reset, machine password rotation, secure channel, lockout, offline cached login, and reconnect | Disposable Windows 11 and Windows Server 2022/2025 clients; exact editions/builds pinned in a compatibility matrix |
| [AD-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Kerberos AS/TGS, service principals, PAC validation, time synchronization, cross-service SSO, constrained delegation, and trust authentication | Positive/negative Windows and Linux client tests, ticket expiry/replay and delegation abuse cases |
| [AD-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | LDAPv3/LDAPS, AD schema and controls, paging, referrals, ACL filtering, and global catalog | Windows RSAT and standard LDAP clients; paging/filter conformance, unauthorized attributes excluded |
| [AD-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | AD-integrated DNS, SRV discovery, secure dynamic updates, site/subnet placement and DC locator | Discovery, stale records, DNS failover, and unsigned-update rejection |
| [AD-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Group Policy management and application; SYSVOL consistency, logon scripts, security policy, permissions | Real Windows client resultant policy, policy version conflict, script distribution and failover tests; document supported replication mechanism |
| [AD-07](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Multi-controller, multi-site replication, conflict resolution, deletion/tombstones, topology and recovery | Partition/rejoin, concurrent writes, lingering objects, rollback protection and disaster recovery |
| [AD-08](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Required Netlogon, SAMR, LSA, SMB and DCE/RPC behavior for domain membership and administration | Supported Microsoft protocol test cases plus real-client workflows; signed/sealed secure channels |
| [AD-09](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Forest/domain trusts, cross-domain authorization, migration and coexistence with existing AD | Two disposable forests, trust creation/removal, SID filtering, selective authentication and migration rollback |
| [AD-10](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Domain/forest functional levels and FSMO role ownership, transfer and failure recovery | Explicit supported level matrix, role transfer/seizure, schema and functional-level upgrade tests |
| [IAM-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Complete identity and password administration: create/disable/delete/restore accounts, user-driven password change, authorized admin reset, expiry/lockout and fine-grained password policies, with delegated permissions and audit | UI/API and supported client tests for allowed and denied operations, policy enforcement, account enumeration resistance, password redaction and post-reset authentication |
| [OPS-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Backup/restore, upgrades, rotation, audit export, health and capacity visibility | Repeated restore drills, interrupted upgrade, disk-full and certificate-expiry tests |
| [UX-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Accessible web administration and documented automation API/CLI | Tested admin journeys, WCAG 2.2 AA audit and API authorization matrix |
| [SEC-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Treat DCs, directory backups, replication secrets and ticket-signing keys as Tier 0; separate admin identities and delegated roles; no shared superuser UI account | Threat model, privilege matrix, denied-operation integration tests |
| [SEC-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Secure defaults: LDAP signing/channel binding where supported, encrypted simple binds, SMB signing, signed/sealed Netlogon; no anonymous sensitive reads or SMB1 | Protocol downgrade and anonymous access tests with pinned clients |
| [SEC-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Prefer Kerberos AES; disable DES/RC4 and NTLM by default; legacy exceptions must be scoped, visible, time-limited and audited | Kerberos encryption negotiation, NTLM relay/downgrade tests and documented compatibility impact |
| [SEC-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | TLS 1.2 minimum, TLS 1.3 preferred; certificate identity validation and rotation; trust roots managed explicitly | Invalid/expired certificate rejection and live rotation tests; no verification bypass |
| [SEC-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Web/API admin MFA through phishing-resistant authentication, step-up for privileged actions, scoped sessions/tokens, CSRF protection and reauthentication | Browser/API tests for session expiry/revocation, cross-site attacks, role escalation |
| [SEC-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Mature reviewed crypto only; protected password/key storage, no plaintext password logs, controlled key lifecycle, dual rotation of Kerberos signing keys with ticket lifetime planning | Crypto design review, secret/log scan, rotation and backup recovery drills |
| [SEC-07](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Rate limiting resistant to distributed abuse, password policy and breached-password checks without leaking passwords, safe recovery and lockout visibility | Spray, brute-force, denial-of-service and recovery abuse tests |
| [SEC-08](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Validate bounded inputs and LDAP filters; bound queries, nesting, RPC sizes and replication queues; prevent injection and resource exhaustion | Parser fuzzing, adversarial query tests and memory/CPU ceilings |
| [SEC-09](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Append-only exportable audit events for auth, policy, delegation, privileged writes, trust and key changes; protect against modification and never log credentials/tickets | Audit completeness, redaction and external collector outage tests |
| [SEC-10](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Least-privilege services, restricted network exposure, signed updates, dependency inventory, SBOM, provenance, vulnerability response and verified restore | Packaging review, dependency/secret scans, artifact verification and restore exercise |
| [SEC-11](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/requirements.md>) | Minimize identity data, encrypt backups, document retention/deletion and data residency | Privacy review, retention/restore tests and synthetic-only CI fixtures |
| [A-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | WebAuthn/FIDO2 passkeys and hardware security keys for administrator login; multiple authenticators and secure enrollment | Reject origin/RP mismatch and replay; audited enrollment, replacement and revocation; keep usable accessible recovery |
| [A-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Smart-card/certificate-based domain logon through PKINIT and compatible hardware-backed keys | Real supported Windows/Linux client logon, certificate mapping, revocation, expiry and downgrade tests; a web passkey is not automatically a Kerberos credential |
| [A-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Recovery hardened against helpdesk impersonation, SIM swapping and MFA fatigue | No security questions or SMS-only privileged recovery; dual review for Tier 0, notifications and synthetic social-engineering exercises |
| [A-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Password protection beyond basic policy: locally checked breached/common passwords, contextual exclusions, password history and supported fine-grained policies | No raw passwords or unsalted password hashes sent externally; test supported protocol reset/change paths and directory ACLs; avoid routine forced expiry absent a requirement or compromise |
| [A-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Adaptive throttling and credential-stuffing/password-spray detection across replicas | Bound attacker-induced lockout and distributed attempts; test NAT/shared networks, emergency access and behavior during collector/WAN failure |
| [A-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Authentication strength policies, session inventory and bounded revocation | Distinguish phishing-resistant, certificate and password-only authentication; test web logout, API revocation and ticket lifetimes separately; document where legacy protocols cannot enforce MFA |
| [B-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Just-in-time and just-enough privilege with expiring grants | Enforce expiration even when workflow workers fail; test nested membership, tickets with cached privileges, replication delays and denied access after expiry |
| [B-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Dual approval and separation of duties for Tier 0 membership, trusts, replication rights, backup export and key operations | Approver cannot approve their own change or bypass through API/bulk import; audit request, approval, execution and cancellation |
| [B-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Privileged access workstations and tiered administration guidance | Publish tested workstation/server management baselines and safe delegation; directory administrators do not use privileged credentials on lower-trust endpoints |
| [B-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Emergency break-glass access with separate custody and monitored use | Rehearse access without the normal IdP/MFA provider, alert every use, rotate afterward and protect against emergency-account lockout or silent persistence |
| [B-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Effective-permission explorer and privilege-path analysis | Explain ACL inheritance, nested groups, delegation, SID history and trust boundaries; validate against actual access decisions and redact data from unauthorized viewers |
| [B-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Periodic access certification, ownership and orphaned-privilege cleanup | Review privileged/service/stale accounts with accountable owners; preview removals and preserve recovery paths; do not automatically delete based on last-login alone |
| [C-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Windows LAPS-compatible local administrator password rotation and retrieval | Qualify the exact client/schema/encryption profile; tightly restrict password reads, audit retrieval, rotate after use and test offline endpoints |
| [C-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Managed service accounts, including gMSA compatibility where selected | Validate supported KDS/key derivation and authorized password retrieval, rollover and real Windows services; never emulate compatibility by exposing shared plaintext secrets |
| [C-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Linux service identities, keytab lifecycle and supported workload identity integrations | Scoped principals, minimal keytab readers, short lifetimes where supported, automated rotation and revocation; no long-lived administrator credentials in workloads |
| [C-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Joiner/mover/leaver workflows, ownership and deprovisioning reconciliation | Preview group/ACL changes, require approval for sensitive roles, disable access through each integrated system and report failures; measure ticket/session revocation limits |
| [C-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Delegated self-service password change/reset, account recovery and group requests | Validate identity proof, factor replacement and approval boundaries; no account enumeration, unaudited helpdesk impersonation or permanent recovery bypass |
| [C-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Signed, versioned provisioning integrations such as SCIM and an external secrets manager | Treat external sources as scoped authorities; test replay, duplicate events, malicious attributes, tenant mix-ups and outages; do not store arbitrary application secrets in directory attributes |
| [D-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | GPO version history, diffs, independent approval and staged OU rollout | Test both directory and SYSVOL versions/ACLs, conflict resolution and a rollback that actually restores client behavior; audit all management paths |
| [D-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Effective policy preview, precedence and resultant-policy troubleshooting | Model security filtering, inheritance, enforced/block settings and WMI filters; compare predictions with real Windows resultant policy and expose unsupported settings |
| [D-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Tested hardening templates for Windows and Linux | Cover supported firewall, audit, authentication and host protections; Linux policy delivery needs an explicit supported agent/configuration integration rather than assuming Windows GPO applies |
| [D-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Policy integrity/drift detection, safe script distribution and privileged policy ownership | Detect out-of-band SYSVOL edits and dangerous scripts; verify applicable signatures and permissions without inventing incompatible GPO wire formats |
| [D-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Device posture and conditional-access integrations | Qualified endpoint attestation, encryption/patch posture and device identity; define freshness, spoof resistance and fail behavior; posture claims alone must not grant Tier 0 access |
| [D-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Support for endpoint credential protections and application-control baselines | Test compatible Credential Guard, protected-user, LSA protection and application-control profiles; endpoint edition/features determine availability, and enforcement is not performed by the DC alone |
| [E-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Compatibility-aware legacy authentication retirement | Discover NTLM/RC4/unsigned dependencies, offer a migration report and enforce expiring scoped exceptions; first-release secure defaults stay in force |
| [E-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Kerberos delegation, ticket and principal hardening | Detect unsafe unconstrained/resource-based delegation, SPN conflicts, weak service secrets and excessive ticket lifetimes; test constrained delegation and protected accounts on real clients |
| [E-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Trust quarantine and cross-forest entitlement inspection | Validate SID filtering, selective authentication, name suffix routing and SID-history migration boundaries; require approval and audit trust changes |
| [E-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Certificate enrollment and PKI integration, with any AD CS-compatible role separately qualified | Test template/enrollment ACLs, identity mapping, SAN constraints, approval, issuance/revocation and renewal; protect CA keys separately and reject escalation-prone configurations |
| [E-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Certificate/key inventory, expiry forecasting and automated rotation | Exercise TLS, PKINIT, service and trust material separately; support safe overlap, CRL/OCSP outages and core/provider-specific lifecycle constraints |
| [E-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Protocol exposure control and network segmentation templates | Enumerate actual DNS/LDAP/Kerberos/SMB/RPC and replication flows, narrow dynamic RPC ranges where supported, test firewall changes and preserve diagnostic access |
| [F-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Reviewed systemd sandboxing, capability reduction and AppArmor/SELinux profiles | Test per-role requirements, upgrades and restore; document any privileged native-core/OS operations instead of promising all services run unprivileged |
| [F-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Host security posture: supported Secure Boot, measured boot and disk encryption | Document provisioning and recovery-key custody; boot attestation must be verified externally; disk encryption does not protect a running compromised DC |
| [F-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Hardware-backed key custody through HSM/TPM or a supported external KMS | Qualify each key type and key-provider API; do not claim AD password verifiers or every Kerberos key can be moved into an HSM; test latency, outage and recovery |
| [F-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Resource isolation and DoS controls per service/peer | Exercise expensive LDAP searches, nested groups, parser inputs, connection exhaustion, audit floods and replication queues under limits without starving legitimate login |
| [F-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Hardened Linux storage, syscall and network profiles for optional container packages | Validate ACL/xattrs, persistent state, time/DNS, service discovery and restore; no unreviewed privileged-container default; VM/bare-metal hosting stays supported |
| [F-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Linux host baseline drift and agent/update integrity | Detect changed service units, executable/config permissions and obsolete kernels/packages; verify updates and rehearse service continuity during host maintenance |
| [G-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Structured, correlated audit export to SIEM/syslog with externally protected storage | Version schemas, synchronize time, track gaps, redact credentials and enforce export RBAC; an append-only local file is not tamper-proof against root |
| [G-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Detection for replication abuse, suspicious DC registration, ACL escalation and privileged group changes | Labeled authorized lab scenarios, expected alerts and false-positive measurements; some credential theft leaves no definitive directory-only signal |
| [G-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Detection for ticket abuse, password sprays, abnormal service-ticket requests and trust/GPO persistence | Correlate KDC, directory and endpoint signals; do not promise reliable golden/silver-ticket detection solely from server logs |
| [G-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Deception identities and monitored canary credentials | Isolate synthetic decoys with no real privileges, prohibit use in normal workflows and test safe high-confidence alert handling |
| [G-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Investigation views: identity timeline, effective permissions and configuration history | Preserve provenance and access controls; reproducible evidence export, chain of custody and bounded retention; do not expose password hashes/tickets in UI |
| [G-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Detection engineering with replayable synthetic event fixtures | Version rules, test sensitivity/precision, alert latency and collector failure; publish thresholds and capacity overhead at the 10k-identity target |
| [H-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Audited response workflows for account/device disable, trust suspension and service-key rotation | Scope, preview, approval, idempotency and a rescue path; automated detections cannot globally lock out a domain without a separate safety decision |
| [H-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Domain-compromise recovery plan covering ticket-signing, machine, service, trust and administrator credentials | Sequence native-core/provider-specific rotations, including safe double rotation of Kerberos signing keys; prove clean restores and ticket invalidation within documented limits |
| [H-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Replica quarantine and controlled reintroduction after suspected compromise | Protect evidence, revoke replication trust safely, avoid contaminating clean replicas and test topology/role recovery; partitioning alone does not remove stolen credentials |
| [H-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Recovery-safe security state restoration | Reconcile revoked identities, changed privileges, deleted objects and key epochs after restoring older backups; prevent silently reactivating known-compromised access |
| [H-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Tested response playbooks and tabletop exercises | Include lost MFA provider, stolen backup, compromised maintainer, ransomware and malicious insider; track response time, operator mistakes and retained evidence |
| [I-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Read-only/limited-secret branch controller profiles when explicitly implemented by the native core | Qualify exact RODC/password replication policy semantics, cached-secret restrictions, theft impact and credential reset procedure; never market a writable replica as read-only |
| [I-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Immutable/offline encrypted backups with split custody and recovery-key escrow | Separate backup administration, restoration quorum where appropriate, retention verification and regular clean-room restores without depending on the failed domain |
| [I-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Site isolation, failover and revocation-risk visibility | Surface stale replication, stale policy and uncertain revocation; test WAN partitions and clock/DNS faults without claiming global immediate consistency |
| [I-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Security operation budgets and safe degraded modes | Define authentication, MFA, KMS, CA and audit failure behavior separately; backpressure noisy services, alert on queue loss and never silently bypass admin MFA |
| [I-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Recovery environment integrity and safe backup validation | Scan and validate restore media, signed tooling and host images; rehearse total loss and schema incompatibility; ordinary VM snapshot rollback is not assumed safe for a DC |
| [J-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | OIDC/OAuth2 and SAML federation through separately qualified modules | Validate issuer/audience, redirect URI, nonce/state/PKCE, signing keys, claim minimization, logout and key rollover; modern SSO does not replace AD protocols |
| [J-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Network access integrations such as RADIUS/EAP-TLS | Qualify identity/certificate mapping, mutual authentication and revocation behavior; avoid insecure password fallback and document external network-device dependencies |
| [J-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Attribute-level privacy, scoped directory search and data-export controls | Denied attribute/search tests across LDAP and UI/API, purpose-scoped access and export audit; avoid breaking required AD discovery semantics |
| [J-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Retention, deletion and legal-hold policy for identity and audit data | Reconcile tombstones/backups/security investigations and residency obligations; no claim of GDPR or other regulatory certification from feature availability |
| [J-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Explicit multi-organization/tenant security boundaries | Prefer independent domains/forests or deployments for hostile tenants; a shared writable DC and UI RBAC do not create hard tenant isolation; independently assess any shared architecture |
| [K-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Reproducible packages/images, signed provenance/SBOM and dependency license/CVE inventory | Independently rebuild, compare artifacts and verify expected signer/workflow identities; document unreproducible parts and dependency exception expiry |
| [K-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Secure update metadata with rollback/freeze protection and key recovery | Verify signatures, version/expiry and release channel; rehearse signing-key compromise, offline updates and supported emergency rollback without bypassing checks |
| [K-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Longer parser/protocol fuzzing, sanitizers, differential and state-machine tests | Synthetic isolated workloads for LDAP/RPC/Kerberos/DNS and policy handling; compare observable semantics with a licensed AD lab and retain minimized regression cases |
| [K-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Property-based checks or formal analysis for bounded high-risk logic | Prioritize authorization, grant expiry, replication conflict handling and key transitions; publish model assumptions rather than claiming a formally secure whole server |
| [K-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Recurring independent pentests, purple-team exercises and a responsibly funded disclosure program | Public scope/safe-harbor terms, private intake and supported-version response; remediate findings with regression tests and publish appropriate summaries |
| [K-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Hardened release governance and maintainer continuity | Two-person sensitive release review, scoped OIDC, protected builders/refs, signer rotation and tested maintainer-loss recovery; use no privileged fork runners |
| [L-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Security posture dashboard with actionable, evidence-backed findings | Show observation time, affected identities/hosts, severity rationale and safe remediation; never present missing telemetry as healthy |
| [L-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Policy simulation and explainable access decisions | Preview bulk ACL/GPO/role changes against representative identities and devices; show stale/unknown data and compare predictions with actual enforcement |
| [L-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Safe bulk operations with scope preview, dry run, idempotency and compensating actions | Independent approval for mass privileged changes; test partial failure and rollback limits; no plaintext credential exports |
| [L-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Accessible secure enrollment/recovery and understandable authentication errors | Keyboard/screen-reader tests and usability studies include recovery and approvals; messages help legitimate users without revealing account existence or secrets |
| [L-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Security exception register and policy-as-code change review | Every exception has owner, justification, scope, expiry and audit; reject stale exceptions, detect out-of-band drift and protect policy signing/approval keys |
| [L-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/security-roadmap.md>) | Operator training, trustworthy runbooks and versioned security baselines | Rehearse common and emergency tasks with new administrators; publish prerequisite/compatibility warnings and measure unassisted completion and recovery success |
| [PATCH-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Continuous hardware/OS/software inventory and update applicability assessment | Compare installed versions, missing updates, reboot state, device identity and observation timestamps with native tools; distinguish fresh, stale, unknown and unsupported devices |
| [PATCH-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Trusted patch/vulnerability catalog with dependencies, supersedence and known issues | Reproduce applicable/not-applicable decisions, including vendor backports; correlate vendor severity, CVEs and known-exploited data without treating version-string matches as proof of vulnerability |
| [PATCH-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Windows OS, Linux package/kernel and explicitly selected third-party application patching | Use supported Windows Update APIs and supported distribution package managers such as APT/DNF; test vendor prerequisites, licenses, conflicts and package signatures; GPO update settings alone are insufficient |
| [PATCH-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Dynamic device groups, targeting previews and fixed campaign membership snapshots | Scope by approved inventory/domain/OU/tag criteria; show sample devices, exclusions and counts; audit later membership changes and prevent silent expansion of an approved rollout |
| [PATCH-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Canary/pilot/production rings with configurable dwell, health checks, rollout limits and automatic pause | Inject a bad update or failed health check; later rings halt at the approved threshold; low report coverage cannot count as successful promotion |
| [PATCH-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Maintenance windows, deadlines, user notifications, reboot deferral and forced-reboot controls | Test time zones/DST, sleeping devices, user sessions, grace periods, blackout windows and missed windows; unsupported reboot suppression must be surfaced rather than silently overridden |
| [PATCH-07](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Preflight disk/power/network checks, dependency handling and application/service-aware installation | Test low disk, pending reboot, conflicting package transaction, required services, application health and interrupted install; mark blocked devices separately from failed ones |
| [PATCH-08](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Bandwidth-aware content distribution with authenticated site relays and approved offline import | Verify vendor signatures plus approved content digests, resume interrupted transfers, deduplicate/cache payloads and apply per-site/concurrency limits; a relay may serve content but cannot authorize deployment |
| [PATCH-09](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Durable campaign orchestration and disconnected endpoint recovery | Idempotent job identifiers, bounded retries/backoff, resume after agent/controller restart, cancel/expiry checks before execution and reconciliation after lost acknowledgments; no unbounded queued command execution |
| [PATCH-10](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Independent post-install verification of installed version, reboot completion and service health | Separate downloaded, installed, reboot-pending, verified, failed, paused and unknown states; a zero exit code or missing device report is not proof of remediation |
| [PATCH-11](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Safe uninstall/rollback or tested recovery per update class | Advertise rollback only where the vendor supports it; demonstrate restore/reimage/forward-fix for irreversible changes; preserve operator instructions and abort criteria before rollout |
| [PATCH-12](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Emergency remediation and risk-based prioritization | Prioritize exploited/exposed assets with transparent evidence; exceptional maintenance/approval overrides need explicit scope, independent approval, expiry and immutable audit export |
| [PATCH-13](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Compliance dashboards, remediation SLAs, exception register and report export | Show coverage denominator, overdue/stale/offline devices, unsupported/EOL products and expiring exceptions; track time-to-remediate by risk; do not report unknown endpoints as compliant |
| [PATCH-14](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Delegated patch administration, API/CLI, change-ticket integration and auditable campaign history | Separate catalog approval, targeting, execution, exception and reporting rights; test unauthorized cross-group actions, approver self-approval, API bypass and scoped automation credentials |
| [PATCH-15](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/patch-management-roadmap.md>) | Availability-aware server and domain-controller maintenance | Serialize DC maintenance by site/failure domain, preserve DNS/KDC/replication quorum where applicable, respect service topology and recovery checks; a workstation policy must never reboot every DC together |
| [REMOTE-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Authenticated desktop and terminal sessions to enrolled, authorized devices | Real Windows/Linux session tests including headless Linux, NAT/proxy/relay paths and explicit unsupported configurations; choose maintained protocols/components rather than inventing a remote-control protocol |
| [REMOTE-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Attended support with visible user consent and an immediate disconnect action | Reject denied/expired consent and misleading session requests; show operator identity and active session; no covert access mode |
| [REMOTE-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Separately approved unattended administration | Explicit device policy, scoped operator rights, time-bounded grants, admin MFA/step-up and maintenance restrictions; no unattended access inferred from domain membership |
| [REMOTE-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Session control, audit and sensitive-channel separation | Record actor/device, approvals, start/end and actions available to the operator; independently authorize elevation, clipboard, transfer and recording; test clipboard/drive redirection restrictions |
| [REMOTE-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Secure brokering and prompt revocation | Per-session authorization, authenticated encrypted transport and device verification; no domain-admin credentials in the agent; bounded disconnect after revocation and defined behavior during broker/identity-provider failure |
| [REMOTE-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Safe operation across OS privileges and session states | Test lock screen, user switching, terminal privilege escalation, reconnect and concurrent operators; honor OS security boundaries and document elevation requirements; no bypass of OS credential protection |
| [FILE-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Explicit server-originated uploads to one or many selected endpoints | Preview exact recipients, content digest, size, expiry and destination; approve bulk/sensitive delivery and prevent recipient expansion after approval |
| [FILE-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Secure staging, integrity and recipient verification | Authenticate uploader/source/device, encrypt in transit and protect staged content at rest; verify hashes against authenticated metadata, not an attacker-supplied hash alone |
| [FILE-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Destination and privilege restrictions | Per-role/device allowed paths, canonicalization, symlink/race and traversal defenses, disk quota, ownership/mode preservation rules and explicit overwrite policy; prohibit silent writes into privileged startup/system locations |
| [FILE-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Resumable, bandwidth-limited transfer with accurate receipts | Test interruptions, duplicate requests, stale jobs, full disks and agent restarts; stage then atomically finalize where supported; report partial/expired/failed/verified states and clean up abandoned content |
| [FILE-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Content policy, separate execution and audit | Apply approved type/size/malware policies without promising scanners detect every threat; uploaded files are not automatically executed; record who sent what to which device and destination, without exposing confidential file contents in logs |
| [EDR-01](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Dedicated installed sensor/agent module with secure enrollment and update lifecycle | Signed/verifiable packages and policy, mutual authentication, per-device identity/revocation, staged updates and rescue/uninstall flow; module isolation from remote support and patch execution |
| [EDR-02](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | OS-specific endpoint telemetry | Qualified process lineage, executable hashes/signatures, network connections, file and relevant persistence/security events using supported APIs; document blind spots, event loss and OS/privilege prerequisites |
| [EDR-03](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Behavioral detection, indicator matching and versioned rules | Labeled synthetic scenarios, expected detections, measured false positives/negatives and tuning/exclusion audit; verify rules and bound their CPU/memory cost; no claim of universal malware detection |
| [EDR-04](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Investigation and privacy-scoped evidence collection | Process/device timeline, alert correlation and case workflow; approved minimal evidence capture with provenance, hashes, access controls and retention; no indiscriminate memory, credential or user-file collection |
| [EDR-05](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Authorized response: stop/quarantine malicious processes/files and isolate a device | Separate response RBAC, approvals and bounded automation; preserve narrow authenticated management/recovery paths, define reboot persistence and test release from isolation; protect DC/service topology from fleet-wide lockout |
| [EDR-06](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Tamper resistance and trustworthy sensor health | Detect stopped/stale sensors, policy/signature changes and telemetry gaps; audit exceptions and uninstall; qualify protections per OS and acknowledge a compromised kernel/root can defeat local evidence |
| [EDR-07](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | SIEM/SOAR integration and safe automated response | Authenticated scoped connectors, deduplicated alerts, expiring/idempotent actions and auditable decisions; false detections must not autonomously disable the whole domain or isolate the whole fleet |
| [EDR-08](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/endpoint-operations-roadmap.md>) | Offline operation and resilience under telemetry/provider outages | Bounded encrypted event buffering, trusted cached rules, freshness/loss indicators and controlled reconnect; avoid login disruption, disk exhaustion and treating missing events as a healthy device |

## Recorded CI observation

[Evidence snapshot CI](<https://github.com/Ise-Tom/Babel/actions/runs/44153995669>): passed, 12 passing checks when checked. Recorded main-branch snapshot: PRs 4–7 and 9–16 were merged when checked. All 12 main CI jobs passed. Open PR proposals are reported separately; acceptance still requires an explicit review.

[Dashboard maintenance and interactive build guide](<https://github.com/Ise-Tom/Babel/blob/824d5760f4f95abb341f625b6ff37ab60dbd5d1f/docs/project-dashboard.md>)

Generated from reviewed repository facts. This report does not query live CI in the browser. Edit the source facts through a PR; the dashboard-live branch is owned by automation.
