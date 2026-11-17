# Contributing

Read the [requirements](docs/requirements.md), [roadmap](docs/roadmap.md), and
[architecture decisions](docs/architecture.md) and the [phase specifications](docs/phases/README.md) before proposing implementation.
Map changes to global and Pxx requirement IDs, update affected designs/ADRs and
acceptance scenarios, and never label planned evidence as a passing product test.
Use small pull requests with a problem statement, security implications,
tests, and migration/rollback impact. Never include real credentials, directory
dumps, production identities, or customer network captures in issues or tests.

Run the commands in the [README](README.md). CI requires formatting, lint,
strict types, security/dependency scans and at least 90% combined statement/branch
coverage for repository tools. New source/build trees fail the scope gate until
their executable checks and reviewed scope policy are added. Code changes must introduce their
language's build, lint, type checks, unit tests, and dependency lockfiles in CI
alongside the first implementation. Protocol code needs interoperability and
negative tests; authorization changes need explicit denied-operation tests.
Changes to security boundaries, cryptography, replication, or release workflows
need a maintainer review with security expertise before merge.

Use synthetic fixtures and disposable test domains. Follow [SECURITY.md](SECURITY.md)
for vulnerabilities rather than posting exploitation details publicly.

A project license and contributor terms (DCO or CLA) are owner decisions before
accepting external code for distribution; they are not implicitly selected here.
