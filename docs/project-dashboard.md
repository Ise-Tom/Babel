# Project progress dashboard

A read-only engineering dashboard for all 18 phases and 180 requirements. It is
separate from the future product administration UI: it cannot create accounts,
change passwords, deploy patches or operate endpoints. Viewing needs no API token;
evidence links open the repository normally. The automated publisher uses its
GitHub Actions job token, and the private GitHub view uses your existing login.

## Permanent view without downloads

**[Open the GitHub dashboard](https://github.com/Ise-Tom/Babel/blob/dashboard-live/README.md).**
Bookmark this URL. It uses the private repository's existing GitHub permissions;
no new hosting account, token, public site or plan upgrade is needed. The page
shows a phase board, expandable substeps, feature definitions, implementation
explanations and the issue journal. Use the browser's Find command to search.
The standalone HTML provides the richer interactive filters/export interface.

The initial report is labeled **development preview**. After the dashboard PR
is merged, the existing CI workflow updates the report automatically on pushes
to main, after every required quality/security job succeeds. Manual CI runs on
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
appears in CI; the previous report remains available. The publisher never bypasses
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
