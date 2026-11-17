# CI/CD operation

## What runs today

[CI](../.github/workflows/ci.yml) runs on pull requests, main pushes, merge queue
checks, manual invocation, reusable calls and daily scheduled security rechecks.
There are no path filters that can omit a required job. All runners are ephemeral
GitHub-hosted Ubuntu 24.04; jobs have timeouts and read-only repository tokens.
Fork PRs receive no secrets; no `pull_request_target` or privileged self-hosted
runner executes contributor code. Checkout credentials are not persisted. PR
runs cancel superseded runs; releases wait for their own full CI invocation.

| Job | Executable gate |
| --- | --- |
| Repository checks | Reject unsupported source/build trees and symlinks, all 18 phase specifications and requirement traceability, local Markdown links, Ruff formatting/lint, strict mypy, source-archive smoke test and checksum verification |
| Tests (3.12), Tests (3.13) | Existing utility/integrity tests plus source-packaging and CI-scope regression tests; minimum 90% combined statement/branch coverage of callable script code |
| Static security and dependency audit | Bandit on all shipped Python tools, offline Zizmor workflow-security checks, strict pip-audit of the complete locked CI dependency graph; known advisories block regardless of severity |
| Workflow lint | actionlint, including shell analysis when provided by the runner |
| Secret scan | Redacted Gitleaks scan of full available Git history and checked-out files |
| Native LDAP lab | Pinned Rust build/format/Clippy, property/transport tests and independent ldap3 process smoke, >=90% instrumented core line coverage, address-sanitizer fuzz, Cargo.lock advisory/license/source audit and CycloneDX inventory |
| Project dashboard | Validated phase/progress model, strict TypeScript, ESLint/DOM security rules, deterministic HTML/CSP tests, full npm audit/SBOM and Chromium desktop/mobile flows/accessibility checks |
| CI gate | Always-run aggregate; any failed, skipped or cancelled prerequisite blocks success |

Security/coverage evidence is uploaded with 14-day retention, including a
CycloneDX SBOM with the **CI tooling dependency inventory**. It is not an
application SBOM or proof of license compliance. Audit failures and advisory
service failures are not converted into success. Daily schedules apply once
merged onto the default branch; GitHub can suspend schedules on inactive repos,
so maintainers must monitor actual runs.

`requirements-ci.in` pins direct Python tools; `requirements-ci.txt` locks their
transitive dependencies with hashes. Installation passes both files with
`--require-hashes`, so divergent direct pins fail instead of running old tools.
Dependabot checks GitHub Actions and Python requirements weekly. When refreshing
the lock with `uv pip compile --generate-hashes --universal --python-version 3.12
requirements-ci.in -o requirements-ci.txt`, review the entire diff and run all
checks; rehashing an unexpected artifact is not a verification fix. Pin the
chosen lock-generator version in the update process before automating refreshes.

The [binary installer](../scripts/install_ci_tools.py) separately pins Gitleaks, actionlint
and Syft HTTPS archives and their SHA-256 digests. It extracts only the
expected executable after verification and installs via a unique temporary
file. Review upstream checksums/notes monthly and promptly for advisories;
Dependabot does not update these binary pins. Workflow actions are SHA-pinned.
Zizmor runs offline for deterministic, no-token PR analysis; online-only action
advisory checks are outside its coverage. Documented low-severity syntax
exception retains the caller-commit `./` reusable-workflow reference because
the pinned actionlint does not yet support Zizmor's suggested `$/` syntax.
Bandit has scoped suppressions for reviewed fixed-argv Git subprocess calls,
HTTPS-only downloads and the subprocess imports; there is no global security
rule disable list. Tests are functional fixtures, not shipped executable code,
and are linted/tested but excluded from Bandit's production-tool scan.

The design integrity check rejects missing phase specs, duplicate/unknown IDs,
empty acceptance rows and global requirements not assigned to any phase. It is
a document-consistency gate, not proof of protocol/security correctness. See the
[validation plan](validation-plan.md) for product evidence still required.

The [scope guard](../scripts/check_ci_scope.py) deliberately supports this
repository's docs, workflow definitions, Python tooling and the explicitly
registered native/babel-ldap plus fuzz components. Unregistered native components
and other-language files still fail. New application
source/manifests, Dockerfiles or scripts in another language fail until the
contributor adds locked build/lint/type/unit/integration/security/dependency
and packaging checks and updates the reviewed policy. This detects unfamiliar
trees; it cannot infer whether Python placed under `scripts/` is really a new
application or defend against a maintainer weakening the guard. Review is still
required for workflow/policy changes.

The native lab now has executable build, independent RootDSE-client, fuzz,
coverage and supply-chain gates; see [Phase 1 progress](phase-01-progress.md).
There is still no full domain/client integration, load/soak,
independent security assessment or production deployment to exercise. Add
these with the corresponding implementation and trusted lab infrastructure;
they remain production blockers in the [roadmap](roadmap.md). Code coverage
excludes CLI entry-point dispatch; CLI scope/docs/packaging receive workflow
smoke tests, and packaging also has committed-source integration tests.
Markdown links inside fences, external URLs and anchors are not checked.

## Required merge gate and current platform limitation

Configure **CI gate** as a required status check with a PR/review ruleset, and
require independent review of workflow/policy changes. A successful job is not
itself enforced merge protection. The earlier private-repository configuration
rejected ruleset access with HTTP 403. The owner has now explicitly authorized a
public repository. Protection settings still require API verification; visibility
alone does not establish enforced review or release approval. Bandit, Zizmor and
pip-audit remain required; additional available security services must not replace
those checks with unconditional success.

Standard GitHub-hosted Ubuntu runners are used throughout the current workflows.
Public repositories qualify for free standard runner usage under GitHub’s policy;
private repository allowances, paid larger runners, storage and other platform
limits are separate considerations. Visibility does not resolve an account-wide
billing suspension automatically. Do not purchase capacity or weaken required
checks to bypass a platform failure. Failed runs must be rerun and verified after
capacity becomes available.

## Source prereleases

[Source prerelease](../.github/workflows/release.yml) reacts to `v*` tags and
reruns CI. It only accepts `v0.MINOR.PATCH-alpha.N`, `-beta.N`, or `-rc.N`, rejects
commits not reachable from main, and requires a root LICENSE. Stable releases
are deliberately rejected until this foundation is replaced by product gates.
A `source-release` environment separates the write-enabled job from CI. The job
archives the tested commit with deterministic gzip metadata, computes SHA-256,
creates GitHub build provenance via OIDC, then creates a **draft**, prerelease
GitHub release containing the source archive and checksum file. It does not
publish a package, image or server. Draft publication remains a maintainer act.
The license gate currently blocks draft creation because the owner has not
selected a license.

Once configured, a maintainer creates a protected prerelease tag on a reviewed
main commit, e.g. `v0.1.0-alpha.1`. Never move/reuse release tags. A failed run
before draft creation can be rerun; if a draft already exists, inspect its
assets and attestation before deliberately replacing or completing it. The
workflow fails on an existing release instead of silently overwriting assets.
Consumers can verify with `sha256sum -c SHA256SUMS` and
`gh attestation verify Babel-v0.1.0-alpha.1.tar.gz --repo Ise-Tom/Babel`.
Checksum files detect corruption; attestation ties bytes to a workflow identity.
Neither proves absence of malicious code. Consumers must trust the expected
repository and reviewed workflow identity.

## Required repository settings (manual administrator actions)

These controls are not enabled by committing YAML. Apply them before relying
on this pipeline; GitHub plan/visibility can limit features:

1. Protect main with a ruleset: PRs required, at least one independent maintainer
   approval, stale approvals dismissed, review of latest push, conversation
   resolution, no force-push/deletion and no ordinary bypass. Require status
   check **CI gate**, selecting the actual GitHub Actions check after the first
   successful run. This requires an eligible repository plan/visibility.
2. Restrict Actions to approved actions, require full commit SHA pins where
   supported, set default workflow token to read-only, and disable Actions
   creating/approving PRs. Use ephemeral hosted runners for untrusted PRs.
3. Create environment **source-release**, require independent reviewer approval,
   disallow self-review/admin bypass where available, restrict deployment refs
   to protected release tags. A workflow's environment name alone does not
   configure approval. If protection is unavailable, keep tag creation limited
   and rely on reviewed draft publication; do not claim enforced approval.
4. Protect `v*` tags against creation/update/deletion by untrusted actors through
   a tag ruleset; limit creation to release maintainers. A tag on an unreviewed
   commit could change the workflow itself, so the main-ancestry check alone is
   not a sufficient release security boundary.
5. Enable private vulnerability reporting, dependency graph/alerts, and secret
   scanning/push protection where supported. Configure two actual security
   contacts and a real CODEOWNERS team for workflow/security reviews; no
   invented GitHub usernames are committed here.
6. Confirm GitHub artifact attestations are available for this repository's
   visibility/plan and Actions has the required permissions. Keep the provenance
   gate fail-closed if unavailable; choose an independently reviewed signing
   route rather than removing verification to get a green release.
7. Set Actions retention to an appropriate short duration (suggestion: 14 days),
   restrict who can modify workflows and audit permission changes. Treat public
   logs as public: never print directory secrets or production fixtures.

The original PR had successful hosted CI runs. The expanded workflow requires
its own hosted validation; report the actual PR run results separately. Other
protection/environment settings have not been established by these files.

## Future deployment boundary

Production hosting must use Linux servers for all Babel roles. A standalone
Babel domain must not require Windows Server. The initial proposed validation
baseline is Ubuntu Server 24.04 LTS x86-64 with systemd-managed services; exact
supported versions need Phase 0 qualification. Cloud/on-premises provider,
application runtime, state storage, Windows test-runner licensing, package
registry and production credentials remain undecided. Do not add long-lived cloud secrets
now. Prefer OIDC with repository/ref/environment-scoped trust for a selected
provider. Separate staging and production service identities and approval rules.
Do not run fork contributions on domain-joined or cloud-privileged self-hosted
runners; trusted integration must run only reviewed main code in disposable,
network-isolated labs with per-run synthetic credentials and cleanup.

With the first server implementation, add clean-install, service startup/reboot,
upgrade and restore jobs on the qualified Linux baseline, plus Windows client
join/login/GPO tests against those Linux-hosted controllers. Keep Windows AD
reference-domain tests separate from the standalone Linux-only server test so
an accidental Windows Server runtime dependency is detected. Ubuntu workflow
runners now validate repository tooling and a loopback LDAP lab; that does not
qualify full Linux domain-controller hosting. Additional distributions/architectures and container
images need dedicated validation before being advertised as supported.

Every future deploy must name an immutable artifact, snapshot/backup and schema
migration prerequisites, readiness checks, rollback limits, abort conditions
and operator ownership. Identity infrastructure cannot be deployed safely with
a generic SSH copy/restart workflow.

## Native lab CI boundary

The reusable native workflow is a required prerequisite of `CI gate`, including
source-prerelease reuse. It pins Rust 1.100.0, nightly-2026-11-17, cargo-llvm-cov
0.9.1, cargo-deny 0.21.0 and cargo-fuzz 0.13.2; installs use official toolchain
verification or checksum-verified/locked registry artifacts. Review these pins
for compiler/tool advisories; Dependabot covers both Cargo manifests/locks but
does not update toolchain or installed CLI pins automatically. No untrusted
build cache, fork secret or privileged runner is introduced.

Core coverage is >=90% lines, excluding test/CLI-dispatch files; the actual
instrumented service is exercised by the independent client. The PR fuzzer runs
up to 20k iterations/20 seconds with 16-KiB input/512-MiB RSS bounds; schedules use
200k iterations/120 seconds. Both decode/respond and transport framing are fuzzed.
Crashes retain synthetic reproductions; no production credentials enter corpora.

Cargo audit/license/source policy includes development/build dependencies for the
core and fuzz graphs. MIT/Apache/NCSA cover current development dependencies;
NCSA is required by the libFuzzer harness. Only unpublished workspace-package
license checks are exempt while D-01 remains open (Cargo package privacy means
`publish = false`, independently of GitHub repository visibility); all public product/registry
releases stay blocked. Duplicate versions are warnings, while unknown/yanked or
advised dependencies, unapproved licenses/sources and wildcard dependencies fail.
Native SBOM is a source Cargo.lock inventory including test/fuzz dependencies,
not a claim those dependencies are present in the zero-runtime-dependency lab
binary or that all product licensing decisions have been approved.

The lab-binary tar/checksum is a 14-day CI artifact visible to repository readers, not a production
release/installer. No native source change completes Phase 1 as a whole. Windows
join/authentication, storage/ACL, DNS, TLS and GPO remain explicit future gates.

## Project dashboard gate

The read-only [dashboard](project-dashboard.md) has its own required reusable CI
job. Node 24.22.1 and exact npm development dependencies are integrity-locked;
installation scripts are disabled. Browser installation uses the pinned
Playwright package's supported route with normal artifact/TLS verification.
There is no runtime CDN, backend API, external telemetry or browser token. The
verification job is read-only. Separate post-CI workflows publish the reports;
repository visibility is never changed.

Python validates facts/source paths/feature mappings and prevents accepted status
without review evidence; TypeScript uses text-only DOM operations for document
data. Hash-based CSP disallows network connections and unapproved inline scripts.
Node tests verify deterministic packing/JSON escaping/CSP bytes. Browser tests
exercise all phases, filtering, evidence/issue history, keyboard dialog handling,
export, hostile text and accessibility at desktop/mobile viewport sizes. The
managed local Chromium blocks file URLs; tests serve the same standalone artifact
through local HTTP and verify interaction/export after switching offline.

The standalone HTML and browser/security evidence are retained for 14 days.
`npm audit` covers development dependencies and fails on any reported severity;
report/test tool failures remain failures. The npm CycloneDX report inventories
build/test tooling, not a deployed AD product. Automated accessibility and
Chromium viewport checks do not establish a complete WCAG or real-device audit.

The tooling graph deliberately excludes TypeScript-ESLint's glob dependency path
after GHSA-fc5q-39xc-vjpf affected all published picomatch versions through 4.0.7.
ESLint 10 and TypeScript 6 remain supported and pinned; audit severity checks are
unchanged. The compiler checks strict types/unused declarations, and a small
compiler-AST policy rejects explicit `any` before erasure. ESLint/DOM-security
rules inspect compiler-erased JavaScript with no bundling, minification or code
execution; diagnostics for this view use `.ts.lint.js` virtual paths. Separate
fixtures prove unsafe HTML writes, type-cast HTML sinks, eval and explicit any
still fail. This replaces TypeScript-ESLint recommended-style rules rather than
claiming every former style rule is equivalent. Node type definitions remain on
the tested Node 24 major; major runtime/type upgrades require coordinated review.
Progress facts are a dated, source-controlled snapshot; a fresh build does not
silently refresh old evidence or mark planned work accepted.

The separate GitHub-report workflow executes only the default branch at its
immutable GitHub context SHA, never a PR head. It can refresh when PR CI is
requested/running/completed (including failure), when main CI changes state, or on
a manual main dispatch. It records current main CI health (including failures),
then reads bounded PR metadata/progress JSON through read-only APIs.
Proposals and proposed problem resolutions remain separate from main totals and
acceptance. Fork structured facts are not imported, malformed data is noted, and
PR overlays never enter standalone HTML/Pages artifacts. A closed PR is removed on the
next CI/manual refresh rather than through a live browser subscription.

That publisher alone receives `contents: write` plus PR/Actions read permissions.
It accepts public or private Babel repositories with explicit visibility, rejects
other repository identities, and writes only the automation-owned `dashboard-live`
branch through its fixed destination, skips outdated main revisions, uses
fast-forward updates and refuses unexpected files. PR/reusable release checks
remain read-only. Publication failure retains the previous report. The stable
URL does not expire with downloadable artifacts. Every development PR carries
its implementation facts and immutable source revisions alongside its code;
automatic publication remains distinct from reviewed acceptance.

Public static hosting has been approved for the interactive dashboard. The Pages
workflow accepts only successful CI for current main from this repository. A
read-only preflight validates the run/workflow/event/source SHA and standalone
artifact; a separate Pages/OIDC job downloads that immutable artifact without a
source checkout and validates its file boundary before deployment. PR/fork/tag/
scheduled/failed/outdated runs cannot publish. Manual main retries select matching
successful CI. Official hosting actions are commit-pinned and covered by Dependabot.

An owner must enable Pages with **Source: GitHub Actions** once, as documented in
the [hosting guide](project-dashboard.md#activate-public-web-hosting-once). The
default job token cannot perform initial site enablement, and the current
integration lacks that administration access. No owner credential is stored or
repository visibility changed. A site is advertised as live only after a successful
deployment; failures retain the prior site and are visible in the publishing run.
