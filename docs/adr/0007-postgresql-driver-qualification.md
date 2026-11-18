# ADR 0007 — Rust PostgreSQL driver candidate qualification

Date: 18 November 2026. Status: **Full Phase 0 P00-15 driver/transaction gate accepted by the project owner on
18 November 2026; decision and evidence in the [exit packet](../validation/p00-15.md)**. PostgreSQL's backend-family
selection remains owner-approved under [ADR 0003](0003-postgresql-directory-state.md).
This increment extends the [SQL experiment](0004-synthetic-postgresql-state-experiment.md)
with a real Rust client; it does not add native directory storage.

## Candidate and alternatives

Select **tokio-postgres 0.7.18** with only its `runtime` feature, and **Tokio
1.54.1** with explicit runtime/time features. Tests additionally enable Tokio's
macros/net and tempfile 3.27.0. Exact transitives/checksums are in Cargo.lock;
no ORM, dynamic SQL generator or custom authentication cryptography is introduced.
The helper forbids unsafe Rust; Tokio/Mio/socket and OS dependencies still contain
unsafe/platform code requiring target-specific review. Client Unicode handling
does not select AD DN/schema or password-policy normalization rules.
Sources are the crates.io packages from
[rust-postgres](https://github.com/rust-postgres/rust-postgres) and
[Tokio](https://github.com/tokio-rs/tokio).

Direct async calls permit explicit connection/query deadlines and cancellation
without putting a synchronous driver on protocol threads. The synchronous
`postgres` wrapper is simpler for command tools but would need a bounded blocking
boundary in an async service. SQLx offers a broader API and query tooling but
adds abstraction/build/schema decisions. libpq bindings add a native library/FFI
and packaging boundary. These are alternatives, not qualified production choices.
The selected initial profile uses no connection pool. Pool introduction requires requalification. Every logical DC still owns independent local storage;
database replication does not implement AD replication.

## Fixture ownership and authentication

The harness accepts no connection string, external host or production credentials.
It creates its own digest-pinned PostgreSQL 18 container, retaining the existing
no-network/no-ports, read-only rootfs, no-new-privileges, 512-MiB/one-CPU/128-process
limits. TCP listening is disabled and actual inspect/settings are checked.

The optional socket fixture adds exactly one bind mount: a generated socket-only
child beneath a private 0700 temporary directory. The child is 0777 so container
PostgreSQL can create sockets; the private parent prevents access by unrelated
host users. PostgreSQL's default internal socket remains in tmpfs. Neither
database files nor arbitrary host paths are shared. Root/Docker administrators
remain trusted in this lab; this is not a production host-access policy.

An ephemeral dedicated non-superuser role has access only to synthetic fixture
tables. Its HBA rule requires SCRAM-SHA-256. The harness proves passwordless access
is rejected after asynchronous reload; the Rust test rejects a wrong password
and checks denied schema/admin operations and role attributes. The initialization
admin remains local to the owned lab. Only synthetic random test passwords are
used; diagnostics replace the generated value and report no credentials. The
test controller's psql setup variables are not a product credential loader.

`NoTls` is restricted to this local Unix-socket experiment; no TCP endpoint is
accepted. Upstream also supports trust, cleartext and MD5 authentication. This
experiment does **not** establish a client-side SCRAM-only negotiation policy,
remote database TLS or a production peer-authentication policy. The MD5 transitive
dependency implements upstream legacy protocol capability, not a new approved
Babel authentication method. Unicode password/SASLprep, hostile-server crypto
resource limits and credential zeroization/custody need further qualification.

## Executed interface and failure cases

The library is a qualification helper with fixed role/database and a bounded typed mutation API, not a public
administration or AD directory interface. Raw SQL and transaction entry points
are compiled only with the explicit qualification feature. Real
tests qualify parameter binding for quoted/Unicode text, null and binary values;
client type errors and SQLSTATE failures have static redacted categories.

The fixture uses ordinary small records and a journal with a deferred foreign
key. It does not define GUID/SID/schema/ACL or stable disk formats. Commit and
explicit/drop rollback are observed across actual statements. A tracked statement
failure forces rollback and an `Aborted` result instead of treating PostgreSQL's
successful response to a rolled-back `COMMIT` as an acknowledged mutation.
Other unconfirmed commit errors conservatively report `UnknownCommit`, discard
the session and never retry automatically. Deferred constraint failure and a
terminated owned transaction both exercise that result. A controlled Unix relay now withholds the actual server COMMIT response; an
independent connection first verifies the committed object, journal, audit intent
and receipt. Lost replies and dropped caller futures recover the same durable
result without repeating the mutation. Concurrent identical requests serialize;
changed payload and locally revoked actors are denied, including receipt replay.

Connection establishment has a two-second asynchronous deadline. Helper queries
and transaction steps have 600-ms deadlines; the default server statement and
lock timeouts are 300/100 ms. An expired or caller-dropped operation poisons and closes its connection,
including BEGIN, mutation, rollback and COMMIT futures. There is no pool for an
uncertain transaction to reenter. Streaming reads cap 128 rows, 32 columns and
65,536 retained field bytes; statements/parameters cap at 4,096 bytes/32. Normal
typed mutations have smaller fixed bounds. Tests exercise an unresponsive Unix peer, server
statement/lock timeouts, explicit cancellation after an observed active-query
barrier, and client/transaction deadlines when the server timeout is deliberately
disabled in the disposable fixture. Effective durable settings and PostgreSQL
major 18 are checked on connection and before helper transactions. A session
with synchronous commit disabled is rejected. This does not prove hardware flush.

Serialization conflict, denied actions, constraint failure, canceled operations,
lock contention and unavailable connections have separate classifications.
Serialization is a retryable category, not permission to retry a possibly committed
mutation. Durable request identities and reauthorization remain adapter work.

## CI and rights

The required native gate now includes a dedicated real-database driver job with
an independent **90% library line-coverage gate**. Other protocol coverage cannot
hide untested driver code. Default workspace tests do not run the database test
target; its `qualification` feature is enabled explicitly by this job, which
requires every declared scenario to pass with none ignored. All-feature Clippy
compiles that target. Harness/fixture regressions supplement the real run.
No new packet parser is written; existing protocol sanitizer targets remain
required and upstream-driver protocol/parser assessment remains an open boundary.

Run using the pinned Rust toolchain, Python and local Docker:

```sh
python -m scripts.qualify_store_driver
python -m scripts.qualify_store_driver --coverage
```

The JSON report retains the exact image, PostgreSQL version, scenario IDs and
outcomes, CI source revision and observed isolation/cleanup. Library LCOV and
actual selected normal-dependency/Rust-library notices are retained for 14 days.
The two existing protocol-binary archives do not contain this library; its source
and test graph are included in native SBOM/advisory/license/source checks.

Tokio/rust-postgres use MIT OR Apache-2.0. The selected identifier, Unicode
normalization/property crates additionally require **Unicode-3.0** under AND
expressions. Their actual LICENSE-UNICODE texts were reviewed: retain copyright
and permission notices with copies or documentation, retain disclaimers, and do
not use copyright-holder names for promotion without authorization. The Cargo
allowlist adds this reviewed permissive family; it does not ignore findings or
clear unrelated specification/image rights. Actual nested terms are retained and
digest-verified. No new test binary is published as a product artifact.

Review upstream/toolchain advisories on scheduled CI, proposed dependency updates,
feature/crypto changes and target-platform support. Rerun these cases and rights
inventory after upgrades. The [P00-15 packet](../validation/p00-15.md) records the completed criterion table
and selected local profile. Two mandatory Python-coordinated SIGKILL/restart
checkpoints now prove driver recovery before commit and after a confirmed commit.
The fixture schema is not an AD format. Native identity/schema/ACL integration,
real directory journal/receipts, service provisioning and valuable credential/key
custody remain P01-02/P01-03/P01-09/P01-11/P01-12/P01-14 implementation gates.
Domain replication/backup/upgrade, physical host/disk failures and capacity remain
P03/P04 qualification gates. These later obligations no longer obscure completion
of the Phase 0 library/transaction review. All 60 AD/client scenarios remain unrun.
