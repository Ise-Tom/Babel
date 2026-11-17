# CI/CD operation

## What runs today

[CI](../.github/workflows/ci.yml) runs on pull requests, main pushes, manual
invocation and a weekly schedule. It checks local Markdown file links, tests
the link checker and release policy, validates Actions workflows with pinned
actionlint, and scans full available Git history with pinned Gitleaks. Fork PRs
receive no secrets and no write token. Checkout credentials are not persisted;
there is no `pull_request_target` or execution of PR code on privileged runners.
Jobs use GitHub-hosted Ubuntu 24.04, read-only permissions and bounded timeouts.
PR runs cancel superseded runs; a release waits for its own CI invocation.

The tool installer supports Linux x86-64 only and verifies fixed SHA-256
archive digests before extracting only the expected executable. Tool upgrades
must review upstream release notes/checksums and update the version plus digest
in [the installer](../scripts/install_ci_tools.py). Dependabot proposes weekly
GitHub Action updates; it does not update these binary pins. Review these pins
monthly and promptly for security advisories. SHA pinning is immutability, not
a guarantee that an old version remains safe.

No application build, SAST/dependency scan, SBOM, image scan, Windows integration,
load test, or production deployment currently exists. Add them with the first
corresponding source/packaging rather than installing a meaningless language
pipeline into an empty repository. The [roadmap](roadmap.md) makes these release
prerequisites. Markdown links inside fenced examples, external URLs and heading
anchors are outside the current link check's coverage.

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
   checks **Repository checks** and **Secret scan**, selecting the actual GitHub
   Actions checks after the first successful run.
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

Remote settings and hosted Actions execution have not been verified by local
validation. Existing Git read access is independent of GitHub API permissions.

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
