# Project progress dashboard

A read-only engineering dashboard for all 18 phases and their canonical requirements. It is
separate from the future product administration UI: it cannot create accounts,
change passwords, deploy patches or operate endpoints. Viewing needs no API token;
evidence links open the repository normally. The automated publisher uses its
GitHub Actions job token. The GitHub report follows repository visibility and
supports both public and private Babel repositories.

## Public repository transition

The owner applied public visibility and merged PR #18 on 17 November 2026.
Main CI run 44175150495 passed all 12 jobs. The dashboard was successfully
published by run 44175624652 and is live at **https://ise-tom.github.io/Babel/**.
The earlier billing and visibility blockers are resolved. This does not grant
this integration administration access: settings writes still return HTTP 403.
See [security settings and owner actions](github-security-settings.md) for the
observed state, ready-to-import main ruleset and remaining controls.

The fetched branch history, including the generated report branch, was scanned
with Gitleaks using redacted output; no leaks were detected. This is a secret
pattern scan, not certification of the project’s product security or licensing.
The owner has now selected Apache-2.0 plus DCO 1.1; remaining third-party and
specification/reference-fixture obligations stay explicit in D-01.

## Interactive interface

The preferred interface is the compact interactive board: all 18 phases fit in
the tested 1440×1000 desktop viewport, with one phase picker and searchable cards.
Choose a phase, then a requirement; implementation explanations and problem histories
open individually. Design and acceptance details remain available on demand.
Cards can be opened anywhere, keyboard focus moves to the selected page, and
mobile layouts use two columns plus the direct phase picker.

The interactive build is a single static HTML file. Public static hosting has
been approved for the dashboard; repository visibility is an owner setting. The Pages
workflow below publishes only the tested HTML build. The GitHub-rendered report
is a fallback for repository browsing, not the preferred dashboard interface.

## Activate public web hosting once

1. Merge the dashboard hosting PR after its required CI checks pass.
2. An owner opens [Settings → Pages](https://github.com/Ise-Tom/Babel/settings/pages)
   and selects **Build and deployment → Source → GitHub Actions**. Repository
   visibility is a separate owner decision. GitHub’s hosting action cannot enable
   Pages with the default job token; the integration’s last attempt also received
   HTTP 403 for Pages administration.
3. Successful main CI automatically starts **Publish interactive dashboard**. If
   it ran before Pages was enabled, run that publishing workflow manually on main.
   It reuses successful CI for the exact revision, so no manual rebuild/upload is needed.
4. Open the **github-pages** environment/deployment URL shown by that workflow and
   bookmark it. A subsequent successful main CI replaces the dashboard at that URL.

This is a one-time owner setting. The
[official hosting action](https://github.com/actions/configure-pages/blob/45bfe0192ca1faeb007ade9deae92b16b8254a0d/action.yml)
documents the additional permissions needed to enable a site. No owner PAT is
requested or stored. Public repository visibility was explicitly authorized by
the owner; publishing workflows never change visibility or purchase a paid plan.
A deployment must succeed before a site is advertised as live. The current site
has a verified successful deployment. PR #17’s hardening is merged; a follow-up
fix removes a denied administration write from its deployment path.

The [workflow](../.github/workflows/dashboard-pages.yml) verifies the successful
main CI run and its unexpired standalone artifact. A read-only job downloads the
immutable artifact ID, verifies its archive SHA-256 digest and accepts only a
bounded regular `index.html` with the strict CSP and no-referrer policy. It packages
that verified site before the separate Pages/OIDC job runs. The privileged job
has no source checkout; it reads and verifies Actions-only publishing/HTTPS without administration writes, and rechecks
main immediately before deployment. Only that HTML and a `.nojekyll` marker are published. Source archives, reports and credentials are
excluded. Failed/foreign/PR/tag/scheduled CI and outdated main revisions cannot
publish; manual retries are restricted to main with matching successful CI.
The previous deployed site remains available if verification or deployment fails.

The Pages site is public, including its engineering facts. Source links follow
repository access controls. Progress remains reviewed source data, not inferred
completion; reload the stable web address to see a newly deployed snapshot.

## Permanent view without downloads

**[Open the GitHub dashboard](https://github.com/Ise-Tom/Babel/blob/dashboard-live/README.md).**
Bookmark this URL. It follows the repository’s existing GitHub permissions and
is publicly readable when Babel is public. No separate hosting account is needed.
The page
shows a phase board, expandable requirements, feature definitions, implementation
explanations and the issue journal. Use the browser's Find command to search.
The standalone HTML provides the richer interactive filters/export interface.

The GitHub report also shows open PR descriptions, files, draft/review and CI
state, and proposed work/problem updates from each PR's `dashboard/progress.json`.
Those entries link to immutable PR-head evidence and to affected requirements. They
are shown separately from the checked main revision: an implemented increment
inside a PR is pending merge, and does not accept a requirement or phase.
The collector bounds untrusted JSON/text and reads it only through GitHub APIs;
it never checks out or executes PR source. Fork PRs retain description/file/CI
metadata but their structured progress is not imported. Missing/invalid progress
produces an explicit note instead of fabricated completion.

PR CI requested/in-progress/completed events refresh the report, including failed
PR checks; main CI state changes and a manual main dispatch can refresh it too.
The publisher executes only default-branch code and records current main CI health,
including failures. This GitHub report is not a deployment or release gate; public
Pages still requires successful main CI. A PR closed without another CI event is removed on
the next refresh; it is not a live browser feed. Metadata records its check time.
Listings are bounded to 50 PRs/100 files per PR and flag truncation. This overlay
is GitHub-report-only: standalone HTML/Pages artifacts never fetch PR bodies.
The report supports public and private Babel repositories. It checks repository
identity and explicit visibility, and refuses unrelated destinations. Public PR
metadata is rendered as untrusted text; fork source is never executed or imported.

Development previews are labeled explicitly. After the PR tracking change is
merged, the separate publishing workflow includes proposals automatically.
Outdated report revisions and publication failures retain the previous report.
Progress explanations still need reviewed source changes; publishing does not
infer acceptance from green checks or rewrite the evidence snapshot date.

The automation-owned `dashboard-live` branch contains only a generated README;
it cannot trigger a main-branch build loop. Source facts remain on main. The
publisher has write permission only in the trusted post-gate job, checks that
the destination is exactly Babel with explicit visibility, skips outdated main
revisions, and uses fast-forward updates. It refuses to replace a branch containing unexpected files. Do not
edit that generated branch manually. Repository visibility is never changed.

For maintainers, render a review copy without publishing:

```sh
python scripts/render_dashboard.py --revision <full-source-commit> --preview
```

The [publisher](../scripts/publish_dashboard.py) uses the runner's GitHub CLI and
job token to update only `dashboard-live`. The [collector](../scripts/collect_pr_progress.py)
reads PR metadata as data; no PR-head code executes with the publishing token.
If a repository policy denies the job write access, its error
appears in the publishing workflow; the previous report remains available. The publisher never bypasses
that policy. This route uses GitHub's Markdown rendering, not GitHub Pages; the
current integration cannot configure Pages (HTTP 403). A separately hosted full
interactive UI remains a hosting/access-control decision.

## What it shows

- Phase board and direct phase navigation, including design, state/interfaces,
  security/failure, capacity and dependency notes from the canonical phase files.
- Every requirement as an expandable item with associated capability IDs and
  the acceptance evidence still required. Feature dialogs show the full contract.
- Narrow implemented increments with how, recorded validation, limitations and
  links to the source revision. Design artifacts are labeled separately.
- Open/resolved problems, their provenance, resolution and next action. These are
  internal reporting records, not automatically created GitHub issues.
- Search, requirement-status filters, a journal, deep links, keyboard-accessible
  feature dialogs and a downloadable complete JSON snapshot.

## Build and view

Use Python 3.12+ and Node 24.22.1 (tested Node major 24). From the repository root:

```sh
cd dashboard
npm ci --ignore-scripts
npm run build
npm run preview
```

Open the preview using the host's supported browser access. The build is a single
self-contained `dashboard/dist/index.html` with embedded data, styles and script,
so it can also be copied/downloaded and opened where browser policy permits file
URLs. The managed cloud Chromium currently blocks file navigation; use the HTTP
preview there. No browser policy bypass is needed. Navigation/search/export work
without network after loading; following GitHub evidence links needs GitHub access.

The **dashboard-standalone** Actions artifact contains the built HTML. No public
site/Pages deployment is performed. The preview serves a static report with no
login; hosting private project data externally needs a deliberate access/hosting
choice. No production identities, credentials or customer evidence belong here.

## Sources of truth and status meaning

[Phase documents](phases/README.md) own requirements/design; the four capability
catalogs own feature definitions. [Associations](../dashboard/associations.json)
map every requirement to existing features. [Progress facts](../dashboard/progress.json)
provide dated overrides, implemented work, incidents and evidence references.
The [model builder](../scripts/build_dashboard.py) combines and validates these.

Requirement counts and granular work increments are independent and may differ
between phases. There is no ten-item quota or requirement for contiguous IDs.
Existing scope and IDs remain intact; adding or splitting tasks must follow the
actual work and dependencies, not a target count. Counts do not measure effort.
Independent work can overlap when its documented entry dependencies are met.

A **planned** requirement has no implementation evidence recorded. **In progress**
means partial work, not acceptance. **Blocked** records an explicit unmet
prerequisite. **Accepted** requires a reviewer/date/evidence record plus an
implementation/explanation record. Phase acceptance additionally requires every
requirement accepted and separate phase approval. No current phase is accepted.
An **implemented increment** can be much smaller than its parent requirement:
rejecting credentials does not implement authentication. Design records do not
count as completed domain functionality, and counts are not effort percentages.

The initial evidence snapshot is main commit `3a69a6b`, checked on 17 November
2026. PRs 4–7 were merged at that check; all 11 main-branch CI jobs passed.
This historical observation is labeled everywhere as a snapshot, not current main,
live CI or production status. The design build revision is reported separately.
Rebuilding does not rewrite the evidence date. Future updates need actual source/
test/review evidence, not an automatically incremented completion counter.

## Update process

1. Update canonical phase/feature definitions when scope/design changes. Maintain
   stable IDs and the existing design review rules.
2. Update associations for changed requirements; unknown/missing IDs fail validation.
3. Add granular work records with what/how, verified behavior, limits and real
   source files. Keep false starts/resolved incidents with truthful provenance.
4. Ask the project owner concrete acceptance questions when an increment meets a
   requirement: identify the ID, exact scope, source/PR, tests and remaining limits.
   Offer acceptance, keeping it pending, or requesting changes. Record an explicit
   affirmative answer as reviewer/date/evidence on that requirement. A pending
   question or silence leaves acceptance unchanged. If the delivered scope is
   narrower than the requirement, keep the requirement open and propose a stable
   child requirement with its own criteria before requesting its acceptance.
   Green CI alone is insufficient; phase acceptance remains a separate review.
5. Refresh snapshot commit/date/CI/PR observations when actually checked. Set
   `source_revision` on work/problem records to preserve historical source links
   independently of that snapshot. Review
   facts as code; this reporting tool does not grant release authority.
6. Build and run tests. Do not commit generated HTML, installed dependencies,
   test output or browser binaries; CI retains the reviewed build artifact.

For source archives without `.git`, run the Python builder with an explicit
`--revision` containing the archive's full source commit, then `node dashboard/build.mjs`.
Do not invent a source revision. Source path escapes, unknown IDs/states, empty
completion evidence, duplicate work/incident IDs and unsafe CI URLs are rejected.

## Validation and boundaries

```sh
python scripts/build_dashboard.py --check
cd dashboard
npm run typecheck
npm run lint
npm run build
npm run test:build
npx --no-install playwright install chromium
npm run test:e2e
npm audit --audit-level=low
```

Use `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium` with the provided
local Chromium; CI installs the package-pinned browser. Automated tests cover
Chromium at desktop/mobile viewport sizes, not real mobile OS/Safari/Firefox.
Axe checks are useful accessibility regression evidence, not WCAG certification.

Metadata is rendered using text DOM operations. JSON embedded in HTML escapes
script delimiters, and CSP hashes match the exact bundled script/style bytes.
No remote fonts/assets, live API, secrets, analytics, untrusted HTML or install
scripts are required. Keep these boundaries when adding functionality. The
existing CI gate waits for dashboard checks and audits the complete npm tooling
graph; this does not make GitHub merge protection available on an unsupported plan.

## Problem list scope

The problem list tracks product and development activity: implementation bugs,
dependency failures, design gaps and missing interoperability infrastructure.
GitHub account, billing, repository permissions, review settings and Pages setup
are excluded. Operational setup remains in the [GitHub settings guide](github-security-settings.md)
and Git history; removing those entries does not mean an unresolved setting was fixed.
Existing development problem IDs stay stable and are not renumbered.

## Phase execution versus related preparation

Phase status follows explicit requirement activity/acceptance. Merely linking a
license, design, CI or source-prerelease record never starts a phase. Phase cards
count **related records**, and planned requirements explain when shared preparation
is present. This keeps useful traceability without claiming product work has begun.

Requirements are read from the canonical phase tables, whose composite obligations
have been split by independent acceptance evidence. There is no ten-item quota or
hardcoded total in dashboard/export tests. Existing accepted scopes are preserved;
refinement adds no automatic acceptance and starts no later phase.
