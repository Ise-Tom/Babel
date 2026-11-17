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
| Repository checks | Reject unsupported source/build trees and symlinks, local Markdown links, Ruff formatting/lint, strict mypy, source-archive smoke test and checksum verification |
| Tests (3.12), Tests (3.13) | Existing utility/integrity tests plus source-packaging and CI-scope regression tests; minimum 90% combined statement/branch coverage of callable script code |
| Static security and dependency audit | Bandit on all shipped Python tools, offline Zizmor workflow-security checks, strict pip-audit of the complete locked CI dependency graph; known advisories block regardless of severity |
| Workflow lint | actionlint, including shell analysis when provided by the runner |
| Secret scan | Redacted Gitleaks scan of full available Git history and checked-out files |
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

The [binary installer](../scripts/install_ci_tools.py) separately pins Gitleaks
and actionlint HTTPS archives and their SHA-256 digests. It extracts only the
expected executable after verification and installs via a unique temporary
file. Review upstream checksums/notes monthly and promptly for advisories;
Dependabot does not update these binary pins. Workflow actions are SHA-pinned.
Zizmor runs offline for deterministic, no-token PR analysis; online-only action
advisory checks are outside its coverage. One documented low-severity syntax
exception retains the caller-commit `./` reusable-workflow reference because
the pinned actionlint does not yet support Zizmor's suggested `$/` syntax.
Bandit has scoped suppressions for reviewed fixed-argv Git subprocess calls,
HTTPS-only downloads and the subprocess imports; there is no global security
rule disable list. Tests are functional fixtures, not shipped executable code,
and are linted/tested but excluded from Bandit's production-tool scan.

The [scope guard](../scripts/check_ci_scope.py) deliberately supports only this
repository's docs, workflow definitions and Python tooling. New application
source/manifests, Dockerfiles or scripts in another language fail until the
contributor adds locked build/lint/type/unit/integration/security/dependency
and packaging checks and updates the reviewed policy. This detects unfamiliar
trees; it cannot infer whether Python placed under `scripts/` is really a new
application or defend against a maintainer weakening the guard. Review is still
required for workflow/policy changes.

There is still no application build, real domain/client integration, load/soak,
fuzzing, independent security assessment or live deployment to exercise. Add
these with the corresponding implementation and trusted lab infrastructure;
they remain production blockers in the [roadmap](roadmap.md). Code coverage
excludes CLI entry-point dispatch; CLI scope/docs/packaging receive workflow
smoke tests, and packaging also has committed-source integration tests.
Markdown links inside fences, external URLs and anchors are not checked.

## Required merge gate and current platform limitation

Configure **CI gate** as a required status check with a PR/review ruleset, and
require independent review of workflow/policy changes. A successful job is not
itself enforced merge protection. During this change GitHub reported this
repository as private and rejected ruleset access with HTTP 403, requesting a
plan upgrade or a public repository. No visibility or paid-plan changes were
made. Until the owner chooses a supported option, maintainers must enforce the
same policy manually; a repository administrator can merge a failing PR.
CodeQL/dependency-review features requiring unavailable private-repository
entitlements are not substituted with always-green jobs: the open-source
Bandit/Zizmor/pip-audit checks above run without those entitlements.

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
runners currently validate repository tooling only; they do not prove Babel
can yet be hosted on Linux. Additional distributions/architectures and container
images need dedicated validation before being advertised as supported.

Every future deploy must name an immutable artifact, snapshot/backup and schema
migration prerequisites, readiness checks, rollback limits, abort conditions
and operator ownership. Identity infrastructure cannot be deployed safely with
a generic SSH copy/restart workflow.
