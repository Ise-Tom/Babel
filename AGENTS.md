# Babel repository instructions

## Branch names

Use a descriptive `dev/` branch for Babel development work. The name must start
with a scope such as `phase0`, `dashboard` or `ci`, followed by at least two
lowercase words that identify the actual change. Separate words with hyphens.

Examples:

- `dev/phase0-protocol-operation-matrix`
- `dev/phase0-security-intake-readiness`
- `dev/dashboard-owner-review-queue`

Use the compliant name specified in the task when one is provided. Reuse a
compliant branch for the same work through review and approval. Before pushing,
check the current branch name against the task and the convention. Include that
branch name in the handoff.

The required CI gate checks branches from this repository targeting `main`.
See [the CI guide](docs/ci-cd.md#development-branch-names).
