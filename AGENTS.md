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

## Owner decisions in worker chats

Ask for a decision in the current worker chat when the owner can act on it.
Ask one short question with the requirement or action, exact scope, a pinned
evidence link and what approval will change. Offer **Approve** and **Hold**
when the chat supports choices. A direct reply works as well.

Routine PR review and partial progress need no separate sign-off. Report
remaining gaps as blockers. Request requirement acceptance once its exit
evidence is complete. Keep policy changes, permission to take an external
action, and requirement acceptance separate. For an external action, specify
the exact actor, target and action before requesting authorization.

Record an explicit decision once. If the PR is open, record the approved
scope, owner, date and source in that PR and update the dashboard as
appropriate. A PR comment volunteered by the owner also counts. Reuse the
decision through rebases and CI retries if its scope and evidence still apply.
Use the management chat for a batch of decisions on work already merged.
