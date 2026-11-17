# Project progress dashboard

A read-only engineering dashboard for all 18 phases and 180 requirements. It is
separate from the future product administration UI: it cannot create accounts,
change passwords, deploy patches or operate endpoints. Viewing needs no API token;
evidence links open the repository normally. The automated publisher uses its
GitHub Actions job token, and the private GitHub view uses your existing login.

## Interactive interface

The preferred interface is the compact interactive board: all 18 phases fit in
the tested 1440×1000 desktop viewport, with one phase picker and searchable cards.
Choose a phase, then a substep; implementation explanations and problem histories
open individually. Design and acceptance details remain available on demand.
Cards can be opened anywhere, keyboard focus moves to the selected page, and
mobile layouts use two columns plus the direct phase picker.

The interactive build is a single static HTML file. Public static hosting has
been approved for the dashboard; the repository remains private. The Pages
workflow below publishes only the tested HTML build. The GitHub-rendered report
is a fallback for repository browsing, not the preferred dashboard interface.

## Activate public web hosting once

1. Merge the dashboard hosting PR after its required CI checks pass.
2. An owner opens [Settings → Pages](https://github.com/Ise-Tom/Babel/settings/pages)
   and selects **Build and deployment → Source → GitHub Actions**. Keep repository
   visibility private. GitHub's hosting action cannot enable Pages with the default
   job token; this integration also gets HTTP 403 for Pages administration.
3. Successful main CI automatically starts **Publish interactive dashboard**. If
   it ran before Pages was enabled, run that publishing workflow manually on main.
   It reuses successful CI for the exact revision, so no manual rebuild/upload is needed.
4. Open the **github-pages** environment/deployment URL shown by that workflow and
   bookmark it. A subsequent successful main CI replaces the dashboard at that URL.

This is a one-time owner setting. The
[official hosting action](https://github.com/actions/configure-pages/blob/45bfe0192ca1faeb007ade9deae92b16b8254a0d/action.yml)
documents the additional permissions needed to enable a site. No owner PAT is
requested or stored. If the account cannot host Pages for a private repository,
choose another static host; do not make the source repository public as a workaround.
The site is not live until a Pages deployment succeeds.

The [workflow](../.github/workflows/dashboard-pages.yml) verifies the successful
main CI run and its unexpired standalone artifact before granting a separate
deployment job Pages/OIDC permissions. That job does not check out the source
repository. It downloads only the verified artifact and refuses files other than
a regular, bounded `index.html` with the dashboard CSP. Only that HTML and a
`.nojekyll` marker are published. Source archives, reports and credentials are
excluded. Failed/foreign/PR/tag/scheduled CI and outdated main revisions cannot
publish; manual retries are restricted to main with matching successful CI.
The previous deployed site remains available if verification or deployment fails.

The page is public, including its engineering facts. GitHub source links still
require repository access. Progress remains reviewed source data, not inferred
completion; reload the stable web address to see a newly deployed snapshot.

## Permanent view without downloads

**[Open the GitHub dashboard](https://github.com/Ise-Tom/Babel/blob/dashboard-live/README.md).**
Bookmark this URL. It uses the private repository's existing GitHub permissions;
no new hosting account, token, public site or plan upgrade is needed. The page
shows a phase board, expandable substeps, feature definitions, implementation
explanations and the issue journal. Use the browser's Find command to search.
The standalone HTML provides the richer interactive filters/export interface.

The initial report is labeled **development preview**. After the dashboard PR
is merged, a separate publishing workflow updates the report automatically on pushes
to main, after the full CI workflow succeeds. Manual CI runs on
main can also refresh it. Failed CI leaves the previous report available.
Progress explanations still need reviewed source changes; publishing does not
infer acceptance from green checks or rewrite the evidence snapshot date.

The automation-owned `dashboard-live` branch contains only a generated README;
it cannot trigger a main-branch build loop. Source facts remain on main. The
publisher has write permission only in the trusted post-gate job, checks that
the repository is private, skips outdated main revisions, and uses fast-forward
updates. It refuses to replace a branch containing unexpected files. Do not
edit that generated branch manually. Repository visibility is never changed.

For maintainers, render a review copy without publishing:

```sh
python scripts/render_dashboard.py --revision <full-source-commit> --preview
```

The [publisher](../scripts/publish_dashboard.py) uses the runner's GitHub CLI and
job token to update only `dashboard-live`. Pull requests, forks, tags and scheduled
runs do not publish. If a repository policy denies the job write access, its error
appears in the publishing workflow; the previous report remains available. The publisher never bypasses
that policy. This route uses GitHub's Markdown rendering, not GitHub Pages; the
current integration cannot configure Pages (HTTP 403). A separately hosted full
interactive UI remains a hosting/access-control decision.

## What it shows

- Phase board and direct phase navigation, including design, state/interfaces,
  security/failure, capacity and dependency notes from the canonical phase files.
- Every requirement as an expandable substep with associated capability IDs and
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
map every substep to existing features. [Progress facts](../dashboard/progress.json)
provide dated overrides, implemented work, incidents and evidence references.
The [model builder](../scripts/build_dashboard.py) combines and validates these.

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
2. Update associations for changed substeps; unknown/missing IDs fail validation.
3. Add granular work records with what/how, verified behavior, limits and real
   source files. Keep false starts/resolved incidents with truthful provenance.
4. Change requirement status only with an explicit explanation. Record acceptance
   review separately; green CI or a documentation edit alone is insufficient.
5. Refresh snapshot commit/date/CI/PR observations when actually checked. Review
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
