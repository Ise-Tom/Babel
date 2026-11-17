# ADR 0004 — Synthetic PostgreSQL local-state experiment

Status: **implemented local experiment, not a product storage adapter or accepted
phase requirement**. PostgreSQL was selected by the owner in
[ADR 0003](0003-postgresql-directory-state.md). This increment exercises part of
that contract against a real database without connecting it to the LDAP server.

## Dependency and execution boundary

The official `postgres:18-bookworm` test dependency is pinned by digest in
[the dependency manifest](../../experiments/postgres_store/Dockerfile).
The observed server and psql client are **18.7, Debian 18.7-1.pgdg12+2**.
The test controller uses that image’s official psql over its Unix socket. It does
not select or qualify a Rust production driver; that remains a D-03/D-04 step.
Dependabot is configured to propose reviewed image updates without automatically
moving to another PostgreSQL major.

The controller creates only its own disposable container, using no network,
published ports, host bind mounts or privileged mode. The root filesystem is
read-only; PostgreSQL data uses the image’s anonymous volume and the socket/temp
directory uses bounded private tmpfs. Limits are one CPU, 512 MiB and 128 processes.
TCP listening is disabled. The generated initialization password is synthetic,
passed through a dedicated environment variable and never exported in diagnostics.
No production connection string, image, credentials or domain data are accepted.

Only a full container ID returned by this creation operation is targeted. Cleanup
removes that container and its anonymous volumes; it never prunes arbitrary
resources. Initialization must reach the final postgres process, not merely the
image’s temporary initialization server. Readiness/transaction waits are bounded.
The controller is test tooling and requires local Docker access; no server or
endpoint service executes Docker commands on behalf of a client.

## Deliberately limited data and transaction contract

[The SQL schema](../../experiments/postgres_store/schema.sql) supports only create
and rename for synthetic UUID objects, fixed-domain synthetic SIDs and bounded
ASCII labels. They are not general DNs, real SID allocation, schema, attributes,
passwords or Windows security descriptors. Object UUID/SID remain immutable;
unique constraints reject collisions. There is no delete/recycle, replication,
credential API or stable migration/backup format.

The actor-active table is a **synthetic allow/deny test input**, not authentication
or AD ACL evaluation. Calls are made by the isolated test controller. Public
schema/table/function grants are revoked and an unprivileged test role cannot
use the mutation function or read tables. This does not qualify the future
Babel core’s principal authentication or delegated authorization.

All mutations lock one transactional allocator row before other mutation locks.
Object state, local journal position, protected audit intent and idempotency
receipt commit together. An ordinary sequence is not used as a commit watermark.
Concurrent writers cannot commit a later position while an earlier writer holds
the allocator. Rollback exposes none of the partial records or allocated position.
This intentionally serializes writes; no throughput target is claimed.

A receipt binds actor/request identity to the exact bounded operation payload.
Retry returns the same local position; changing the payload for that identity
fails. The actor is checked again before receipt lookup, so revocation also blocks
result retrieval. Exact JSONB payload equality is used in this experiment; no
unqualified digest/canonicalization or cross-controller idempotency protocol is
introduced. Mutations reject `fsync`, `full_page_writes` or `synchronous_commit`
being disabled. The controller waits for psql completion before returning its
result; a value printed inside a still-open transaction is not an acknowledgement.

## Measured local evidence

The integration suite uses the real pinned database for:

- Create/rename identity preservation and coupled state/journal/audit/receipts.
- Idempotent retry, conflicting reuse, duplicate IDs/SIDs/labels, invalid input
  and quoted-variable SQL injection attempts with unchanged failed-operation state.
- Unknown/revoked test actors, stale versions, unsafe commit settings, exhausted
  local journal positions, immutable identity and unprivileged-role denial.
- Explicit rollback and two concurrent writers held at observable PostgreSQL
  transaction/lock barriers; both commit and rollback ordering are checked.
- Container/process SIGKILL before commit followed by real recovery: old complete
  state remains and no partial journal/audit/receipt is visible.
- A committed operation whose client result is deliberately not consumed, then
  SIGKILL/recovery/retry: the committed state survives and is not applied twice.
- Actual container isolation, resource settings, disabled TCP and scoped cleanup.

Controller regressions separately check pinned dependency manifests, argv-only
execution, owned IDs, redacted failures, bounded input, unavailable images,
unsupported server major, deadlines and failed cleanup/crash reporting.
These controller tests are not substituted for the real database scenarios.

This is process/container crash evidence on the current Docker/Linux filesystem.
It does not emulate a physical power cut, corrupt sectors, disk exhaustion,
PostgreSQL failover, backup/restore, schema upgrades, AD invocation rollback,
Windows behavior or three-site replication. It does not establish hardware
flush guarantees, credential/key safety or the 10k-identity production SLOs.

## CI and remaining work

The same increment registers only these experiment files in the default-deny
scope guard. PostgreSQL parses/types the actual SQL and the integration tests
exercise its constraints and transaction branches. Ruff, strict Python types
and Bandit cover the controller; tests enforce at least 90% branch-inclusive
controller coverage. The required CI gate includes the dedicated database job.
The pinned image is inventoried as a CycloneDX test-dependency SBOM; this is not
a production image, product SBOM or a claim that all container packages are free
of advisories. Existing language dependency/security checks remain required.

Run from the repository root:

```sh
python -m coverage run --source=experiments.postgres_store.experiment -m unittest discover -s experiments/postgres_store -v
python -m coverage report --fail-under=90
```

Docker may pull the pinned official dependency when absent. No image is built or
published. The future Rust adapter, full identity/schema/ACL model, crash/upgrade/
restore expansion, key custody and AD replication qualification remain open in
I05/D-03/D-04/D-05/D-06. No requirement acceptance is inferred from these results.
