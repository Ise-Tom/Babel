# Contributing

Read the [requirements](docs/requirements.md), [roadmap](docs/roadmap.md), and
[architecture decisions](docs/architecture.md) and the [phase specifications](docs/phases/README.md) before proposing implementation.
Map changes to global and Pxx requirement IDs, update affected designs/ADRs and
acceptance scenarios, and never label planned evidence as a passing product test.
Use small pull requests with a problem statement, security implications,
tests, and migration/rollback impact. Never include real credentials, directory
dumps, production identities, or customer network captures in issues or tests.

Every development PR must update `dashboard/progress.json` alongside the code:
map granular work to its Pxx requirements and record how, validation, limitations,
problems/resolutions and immutable `source_revision` evidence. Include progress
changes already in the PR; do not wait until merge to describe them. The GitHub
report reads proposed work from open PRs and labels it pending merge;
it never adds those proposals to main-branch acceptance totals. Public static
artifacts do not include private PR descriptions or proposal overlays.

When a requirement is ready for an owner decision, link its deliverable PR and
its pinned scope/evidence packet. If the owner approves that scope during review,
record the decision in the same PR. For scopes delivered earlier, use the
[Owner review queue](https://ise-tom.github.io/Babel/#view=review) to collect a
single decision covering the selected packets.

Update `dashboard/capabilities.json` whenever implemented functional scope changes.
Record the implemented subset, missing behavior, supporting work IDs and blockers;
keep experiments and engineering tools distinct from product features. Unlisted
capabilities stay planned. See the [tracker guide](docs/capability-tracker.md).
Requirement acceptance never automatically accepts a complete capability.

Run the commands in the [README](README.md). CI requires formatting, lint,
strict types, security/dependency scans and at least 90% combined statement/branch
coverage for repository tools. New source/build trees fail the scope gate until
their executable checks and reviewed scope policy are added. Code changes must introduce their
language's build, lint, type checks, unit tests, and dependency lockfiles in CI
alongside the first implementation. Protocol code needs interoperability and
negative tests; authorization changes need explicit denied-operation tests.
Changes to security boundaries, cryptography, replication, or release workflows
need a maintainer review with security expertise before merge. In the current
solo-maintainer development profile, the owner reviews the diff and passing CI
and merges through the PR; no second-person approval or self-approval event is
required. PRs, up-to-date CI and resolved conversations remain mandatory. This
is not independent security review; production qualification gates remain open.

Use synthetic fixtures and disposable test domains. Follow [SECURITY.md](SECURITY.md)
for vulnerabilities rather than posting exploitation details publicly.

## License and contribution certification

Babel is licensed under [Apache-2.0](LICENSE), selected by the project owner on
17 November 2026. External contributions are accepted under the same license;
there is no contributor copyright assignment or separate CLA.

By submitting external contributions, certify your right to submit them under the
[Developer Certificate of Origin 1.1](DCO). Add your own sign-off to each commit:

```sh
git commit -s
```

The trailer is `Signed-off-by: Your Name <your-email>`. Use an identity you can
stand behind; sign-off metadata becomes public with the contribution. Review
third-party and AI-assisted material for rights, attribution and correctness.
Never add another person’s certification, fabricate historical sign-offs or treat
a bot as a human certifier. Dependency automation still requires maintainer review.

DCO review is currently a maintainer merge responsibility; no automated DCO check
is claimed. Existing owner-directed work is covered by the owner’s explicit
license selection; this policy does not invent retroactive contributor signatures.
Keep third-party copyright/license notices. Protocol specification, reference
image and fixture redistribution rights remain separately reviewed under D-01.
