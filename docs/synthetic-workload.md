# Reproducible synthetic workload fixtures

The [approved workload method](phase-00-workload.md) now has an executable dataset
generator and independent structural/relational auditor. These are Python test
tools, not the native server. They create no credentials, connect to no service
and qualify no authentication, ACL, GPO, replication or performance behavior.

## Inputs and exact distributions

| Profile | Users | Computers | Groups | OUs | Logical GPOs | Total objects |
| --- | --- | --- | --- | --- | --- | --- |
| `full` | 10,000 | 10,000 | 2,000 | 100 | 50 | 22,150 |
| `smoke` | 20 | 20 | 100 | 20 | 5 | 165 |

Every user/computer is enabled. Each user/computer/group/OU category has exact
40%/35%/25% allocation to three sites. Six DCs are **planned topology metadata**,
not provisioned hosts or generated domain-controller accounts.

Across users and computers combined, 20%/50%/25%/5% have respectively
1/5/20/100 distinct direct group memberships. The full fixture has **254,000**
direct principal edges and **12** nested-group edges. Three disjoint group chains
have edge depths 1, 3 and 8. The auditor computes maximum effective group count
through ancestor closure; this is not a Windows access-token or PAC size.

Across users, computers and groups combined, exact 70%/25%/5% proportions have
512/2,048/8,192-byte ASCII-hex non-secret payloads. This controls byte length and
reproducible content; it does not model AD encoding, index/compression overhead or
every production attribute. Three ACL-pattern tags describe intended future
inherited-reader/delegated-helpdesk/restricted fixtures; no security descriptor or
real access check is encoded. Logical GPO-to-OU links contain no policy files or
SYSVOL content. Names and DN labels use the reserved `.test` domain.

SID history is zero. Domain-root, schema/configuration, deleted objects, credential
records and SYSVOL are explicitly not generated. Real domain/store adapters must
account for their additional objects and qualify matching, ACL and encoding rules.
`import_supported` is false: this JSON format is not an AD import or a production
storage schema. Synthetic GUID/SID/RID labels do not qualify native allocation,
rename/restore, AD replication or irreversible disk formats.

## Reproducibility and artifact format

Version 1 uses a fixed UUID namespace, UUIDv5 labels, SHA-256 ordering/counter
sampling and SHAKE-256 payload bytes. Sampling rejects duplicates and modulo bias
with a finite attempt budget. These algorithms generate public test data, not
keys, passwords or secure random credentials. Seeds are bounded public labels.
There are no wall-clock timestamps or platform-dependent random sampling calls.
Same version/seed/profile/source/input files produce byte-identical artifacts;
changing any input requires a new manifest and comparison run.

A new output directory contains exactly four files:

- `objects.ndjson`: bounded logical object records.
- `memberships.ndjson`: direct and nested membership edges.
- `negative-fixtures.json`: separate cyclic and over-budget graphs.
- `manifest.json`: version, source/seed/profile, input-file digests, inventory hashes,
  byte/record counts, distributions, planned topology and explicit unmeasured fields.

The manifest binds the current workload-method and compatibility-file bytes.
Auditing with changed inputs fails; use the recorded source/input revision when
examining historical data. The source argument is recorded, not authenticated by
the tool. Trusted CI execution and its artifact provenance are separate evidence.

The negative graphs never contaminate the normal dataset. The cycle is truly
cyclic and the over-budget graph exceeds its declared synthetic depth budget of
8; that budget is not a universal AD nesting limit. Auditing proves their shape,
**not that a server denied them**. All 60 client conformance scenarios remain unrun.

## Run and inspect

Use a fresh output path; an existing directory is never overwritten:

```sh
python scripts/generate_workload.py --profile full --seed babel-phase0-v1 \
  --source-revision "$(git rev-parse HEAD)" --output /tmp/babel-workload-demo
python scripts/check_workload.py --dataset /tmp/babel-workload-demo
```

The generator streams payloads/edges instead of holding the full files in memory.
Profiles and sampling work are bounded. The auditor streams at most 128 MiB per
NDJSON file, limits individual rows to 16 KiB and retains bounded identity/group
indexes. It rejects symlink paths, unexpected files/fields, invalid or duplicate
IDs/SIDs/names, inconsistent OU/site links, wrong distributions, missing references,
duplicate edges, normal-graph cycles and artifact digest/size/count changes. Hashes
alone cannot authenticate a deliberately rewritten manifest; structural checks are
independent additional safeguards, not a substitute for trusted evidence review.

The manifest is written last. A failed write leaves an incomplete owned directory
that auditing rejects; inspect/remove only that generated directory before retrying.
The tool does not remove or replace another output, import data or clean up remote
resources. Generated payloads can be large; use `smoke` for unit/development work.

Required repository CI generates and audits the **full** profile. It retains only
the small manifest and audit summary for 14 days, not the large NDJSON files. Tests
cover deterministic replay, seed changes, sampling bounds, write failure,
rehash-resistant semantic failures, malformed references and false runtime claims.
No benchmark/load harness or OS/client provisioning is run by this job.

`token_bytes`, database index bytes, storage expansion, throughput and latency stay
null/unmeasured. Report those only after actual encoders, stores and native mixed
traffic have produced measured results under the approved method. Dataset counts,
file sizes and graph closure are genuine fixture measurements; they are not proof
that Babel can serve a 10,000-identity domain.
