# GitHub hosting and repository security

The dashboard is live at **https://ise-tom.github.io/Babel/**. The successful
Pages deployment for main `6dc9b06` is run 44183656847. Public visibility,
Actions-only Pages publishing, HTTPS, the main-only Pages environment and disabled
Pages admin bypass are verified through GitHub APIs.

On 17 November 2026 the owner applied `Protect main` (27498979), initially
with team-only review requirements. The owner is the sole maintainer, so the
current development policy is **PR required, zero external approvals**, with
up-to-date **CI gate** (GitHub Actions app 15368), resolved conversations,
no bypass actors and no force pushes/deletion. CODEOWNERS records ownership;
it does not require an unavailable second reviewer. This is not independent review.

The proposed template implements that solo policy. At the latest API readback,
only the approval count was zero: code-owner, last-push and unattributed-change
approvals were still enabled. They must also be disabled in the owner UI. The
integration received HTTP 403 attempting the update; no successful settings write
is claimed. Private vulnerability reporting is enabled; a submitted private report
has not been exercised.

The owner also confirmed read-only Actions defaults, disabled Actions PR approval
and approval for all outside collaborators. Those three observations are explicitly
**owner-confirmed**, because the integration still receives HTTP 403 when reading
the Actions administration endpoints. No broader token is requested.

The owner also corrected an own-actions-only restriction after run 44191621036
failed before starting any job. Under Actions → General, select **Allow Ise-Tom,
and select non-Ise-Tom, actions and reusable workflows**, then **Allow actions
created by GitHub**; leave Marketplace creators disabled. The owner confirmed this
change. The workflows retain their full commit SHA pins, including the inspected
nested official actions. Allowing the GitHub publisher does not widen job-token
permissions or permit arbitrary Marketplace actions. Own-actions-only mode blocks
`actions/checkout`, setup, artifact and Pages actions even when commit-pinned.

The remaining release blocker is concrete: `source-release` returned HTTP 404.
The proposed preflight refuses a missing/inadequately protected release
environment before the normal workflow can automatically create one. No release
or repository setting has been changed by this development work.

## Apply owner settings

1. **[Pages](https://github.com/Ise-Tom/Babel/settings/pages):** select **Source:
   GitHub Actions** and keep **Enforce HTTPS** checked. The observed source was
   legacy branch publishing from `main` `/` during the earlier setup. It is now
   verified as `workflow` with HTTPS enabled. The prior deployment still attempted
   an unnecessary settings write and failed with HTTP 403; the fix verifies the
   settings without requesting administration access. The revised deployment
   reads and requires those settings; it never requests administration writes.
   If either setting is wrong, apply these UI settings and retry. A failed read
   or incorrect setting stops deployment rather than silently bypassing it.
2. **[Rules → Rulesets](https://github.com/Ise-Tom/Babel/settings/rules):** import
   [Protect main](github-main-ruleset.json), inspect it and activate it. For the
   solo profile, set required approvals to **0** and disable code-owner review,
   approval of the last push and extra approval for unattributed changes. Keep
   PRs, resolved conversations, the up-to-date GitHub Actions **CI gate**, no bypass
   actors and force-push/deletion protection. The owner reviews the diff and CI,
   then uses the normal merge button; GitHub does not permit self-approval.
   [CODEOWNERS](../.github/CODEOWNERS) remains an ownership record. When a second
   trusted maintainer actually joins, explicitly adopt an independent-review
   policy rather than requiring an unavailable reviewer now. Legacy branch
   protection administration cannot be read; no additional legacy protection is claimed.
3. **[Actions → General](https://github.com/Ise-Tom/Babel/settings/actions):** use
   read-only default workflow permissions; disable Actions approving/creating
   PRs. Require approval for all outside collaborators before running their fork
   PR workflows. Do not send write tokens or secrets to fork PRs. Restrict allowed
   actions to reviewed publishers and full commit SHAs where the setting is
   available. Current workflows pin external actions and grant write/OIDC only
   to the dedicated report, Pages or source-release jobs. These defaults are owner-confirmed; they still cannot be inspected through
   the integration.
4. **[Code security](https://github.com/Ise-Tom/Babel/settings/security_analysis):**
   keep private vulnerability reporting enabled (verified), dependency alerts
   and security updates, secret scanning and push protection where included for
   this public repository. Do not enable a paid service without a separate owner
   decision. Exercise the private report route before claiming it works; do not
   post real vulnerabilities or credentials in public issues.
5. **[Environments](https://github.com/Ise-Tom/Babel/settings/environments):** keep
   `github-pages` restricted to the `main` branch, with no deployment secrets;
   disable admin bypass where supported. Its policy is verified as main-only with
   admin bypass disabled. For **draft source-only prereleases**, create
   `source-release` with **no required reviewers**, admin bypass disabled and a
   custom deployment policy allowing only **tags** matching `v*` (not branches).
   The environment is still absent at the latest check. A read-only preflight
   verifies these settings before the write job; missing settings block release.
   CI, license, main ancestry, provenance and draft/prerelease restrictions still
   apply. No tag or release is created by this change. A future team may switch
   the checker to `--mode team` and configure independent reviewers/self-review
   prevention together. Planned independent production security qualification
   remains required; the solo development profile does not provide it.

After applying settings, verify their actual state in GitHub, rerun current CI
and dispatch **Publish interactive dashboard** on main. The owner merged PR #20 and its read-only Pages fix deployed successfully.
The new storage/release-preflight work is proposed for review and requires merge
and verification before becoming active. Restrict
release-tag creation to authorized maintainers as well: an environment check in
the reviewed workflow is not protection against arbitrary rewritten tag workflows.

## Controls in the revised workflow

A read-only job uses default-branch code, verifies successful CI for the exact
current main revision, selects the immutable artifact ID and checks its SHA-256
archive digest. It accepts exactly one bounded regular `index.html`; extra files,
path traversal, symlinks, oversized content and weak browser policies fail.
CI checks that the built dashboard satisfies the same deployment verifier.

Only verified HTML and `.nojekyll` enter the Pages artifact. The privileged Pages
job has no source checkout or project code execution. It verifies the existing
site settings without administration writes, rechecks main immediately before deployment
and uses pinned official hosting actions. Verification/publication failures retain
the previous site. The revision recheck reduces stale deployment races; it is not
an atomic lock on GitHub branch updates.

The page has hash-authorized scripts/styles, no remote assets, no network API,
no forms, no images and a no-referrer policy. Exporting JSON remains local.
GitHub Pages does not let this project set arbitrary HTTP response headers:
CSP `frame-ancestors`, Permissions-Policy and similar header-only controls are not
claimed. A CSP meta tag cannot enforce `frame-ancestors`. A hosting service with
configurable headers would be needed for those additional controls. HTTPS/HSTS
are provided by GitHub; no custom domain or external proxy was introduced.

## TypeScript major update

PR #17’s TypeScript 7.0.2 update passed typechecking but crashed security lint:
`ScriptTarget.Latest` was unavailable because the JavaScript compiler API was
removed. TypeScript 7 exposes different unstable APIs; adopting them is a distinct
migration of a security check, not a version-only dependency update.

The correction retains pinned TypeScript 6.0.3, its working AST/transpilation
security policy and all audit/lint/tests. Dependabot still proposes compatible
updates; automatic major compiler proposals are deferred. Before adopting 7,
qualify the replacement parser/emitter, malformed input handling, explicit-any
policy, DOM/eval detection, declarations and the full browser/build suite. No
compiler API shim or skipped check is presented as equivalent protection.
