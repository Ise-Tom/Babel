# GitHub hosting and repository security

The dashboard is live at **https://ise-tom.github.io/Babel/**. On 17 November
2026, public visibility, HTTPS enforcement, the main-only Pages environment
branch policy and a successful deployment were verified through GitHub APIs.
The site returned HTTP 200 and GitHub’s HSTS header. PR #18 is merged and all
12 jobs of main CI run 44175150495 passed.

The chat integration cannot administer these settings: Pages updates, environment
updates, private vulnerability reporting and ruleset creation returned HTTP 403,
“Resource not accessible by integration”. Repository metadata showing `admin=true`
does not grant the integration those API permissions. No owner token is requested.
The changes in PR #17 harden workflows; they do not prove owner settings are applied.

## Apply owner settings

1. **[Pages](https://github.com/Ise-Tom/Babel/settings/pages):** select **Source:
   GitHub Actions** and keep **Enforce HTTPS** checked. The observed source was
   still legacy branch publishing from `main` `/`; this can compete with the
   tested dashboard deployment and should be changed. The revised deployment
   first attempts and verifies Actions-only mode/HTTPS with its existing
   `pages: write` job token. If GitHub denies that request, apply these UI settings
   and retry; failure is kept visible rather than silently bypassed.
2. **[Rules → Rulesets](https://github.com/Ise-Tom/Babel/settings/rules):** import
   [Protect main](github-main-ruleset.json), inspect it and activate it. It requires
   PRs, an owner review, approval of the last push, dismissal of stale approvals,
   resolved review threads and the GitHub Actions **CI gate** on an up-to-date
   branch. It blocks force pushes/deletion and grants no bypass actors.
   [CODEOWNERS](../.github/CODEOWNERS) names the actual repository owner; it only
   enforces review after the rule is active. A contributor cannot approve their
   own PR; add another trusted maintainer before needing self-authored changes
   reviewed. The ruleset list was empty; legacy branch protection could not be
   inspected, so enforcement is not claimed.
3. **[Actions → General](https://github.com/Ise-Tom/Babel/settings/actions):** use
   read-only default workflow permissions; disable Actions approving/creating
   PRs. Require approval for all outside collaborators before running their fork
   PR workflows. Do not send write tokens or secrets to fork PRs. Restrict allowed
   actions to reviewed publishers and full commit SHAs where the setting is
   available. Current workflows pin external actions and grant write/OIDC only
   to the dedicated report, Pages or source-release jobs. These repository-wide
   defaults could not be inspected through the integration.
4. **[Code security](https://github.com/Ise-Tom/Babel/settings/security_analysis):**
   enable private vulnerability reporting (observed disabled), dependency alerts
   and security updates, secret scanning and push protection where included for
   this public repository. Do not enable a paid service without a separate owner
   decision. Exercise the private report route before claiming it works; do not
   post real vulnerabilities or credentials in public issues.
5. **[Environments](https://github.com/Ise-Tom/Babel/settings/environments):** keep
   `github-pages` restricted to the `main` branch, with no deployment secrets;
   disable admin bypass where supported. Its observed policy permits only main
   but still allows admin bypass. Create `source-release` with a trusted reviewer,
   prevent self-review and restrict it to authorized `v*` tags. That release
   environment was absent. The workflow still requires a license, successful CI,
   a main-ancestor commit and draft-only prereleases; public visibility does not
   make Babel ready for production or resolve the open license decision.

After applying settings, verify their actual state in GitHub, rerun current CI
and dispatch **Publish interactive dashboard** on main. Merge PR #17 only after
its full CI passes and its workflow/policy changes have been independently reviewed.

## Controls in the revised workflow

A read-only job uses default-branch code, verifies successful CI for the exact
current main revision, selects the immutable artifact ID and checks its SHA-256
archive digest. It accepts exactly one bounded regular `index.html`; extra files,
path traversal, symlinks, oversized content and weak browser policies fail.
CI checks that the built dashboard satisfies the same deployment verifier.

Only verified HTML and `.nojekyll` enter the Pages artifact. The privileged Pages
job has no source checkout or project code execution. It configures the existing
site with its narrow Pages permission, rechecks main immediately before deployment
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
