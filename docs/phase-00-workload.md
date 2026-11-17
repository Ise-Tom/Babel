# Phase 0 workload and measurement contract

Status: proposed engineering method, **not benchmark results**. The owner target
is 10,000 identities / three sites. The existing [requirements](requirements.md)
remain the normative provisional SLOs; measurements and an ADR must ratify them.

## Reproducible synthetic dataset

Use a recorded generator version and seed, fixed UUID namespace and only synthetic
`.test` identities. Generate 10,000 enabled users, 10,000 computer accounts and
2,000 groups; report additional schema/configuration/deleted objects separately.
Allocate 40%/35%/25% of users and computers across three sites. Use 100 OUs,
50 GPOs and group membership distributions of 1/5/20/100 memberships per principal
with recorded proportions 20%/50%/25%/5%. Include acyclic nesting depths 1/3/8 and
separate explicit cycle/over-budget denial fixtures. Report total membership edges,
attribute byte distributions, maximum token size and index/storage expansion.
Those distributions are proposals; a generator must validate them before any run.

Payloads include 0.5/2/8 KiB non-secret object attributes (70%/25%/5%), bounded
paged searches and declared inherited/delegated ACL patterns. Secrets, if later
required for authentication, are per-run synthetic values and never retained in
public evidence. Record the complete generated manifest/hash; changing seed,
normalization, distribution or index design requires a new comparison run.

## Mixed traffic and scheduling

Use six independent DCs, two per site. Separate load generators, DNS/time sources,
management plane and observation collectors from the measured servers. Propose
4 vCPU / 16 GiB RAM / 100 GiB SSD per DC (24 vCPU / 96 GiB / 600 GiB total before
backup, audit, generators and Windows VMs). This is a sizing hypothesis, not
allocated capacity or a purchase request.

Drive an open-loop schedule and retain offered, started, completed, timed-out and
rejected counts; bound outstanding requests so overload is visible. Include queue
and timeout latency rather than measuring only fast completions. Seed the mix:

| Class | Sustained successful rate | Additional expected denied traffic |
| --- | --- | --- |
| Kerberos | 100/s for 60 minutes, with declared AS/TGS split 40%/60% | 10/s invalid/expired/replayed credentials, tracked separately |
| LDAP indexed reads | 500/s, including object lookup, page continuation and group/ACL evaluation | 50/s denied attributes, invalid filters or bounded expensive queries |
| Directory writes | 20/s across create, rename, membership, policy and credential rotation where implemented | 2/s collision, stale epoch, unauthorized write or rejected policy |

Run all classes together. A five-minute auth burst raises successful auth to
500/s plus 50/s expected denied traffic while directory traffic continues.
Do not claim an AS/TGS/password workload from RootDSE requests or substitute a
SQL microbenchmark for the native server. Unimplemented classes are **unrun**,
not omitted or counted as successful simulated requests.

Run cold start, warm steady state, burst, failure/recovery and a 24-hour soak
separately. Cold means declared empty process/query caches and recorded storage
cache state; do not secretly warm one candidate. Schedule hot-key, skewed site
and concurrent rename/revocation workloads as separately identified cases.

## Network and fault profiles

Baseline: <=2 ms site LAN RTT; inter-site RTT 50 ms, 1% loss and at least
20 Mbit/s available. Degraded WAN: 150 ms, the same declared bandwidth, measured
loss/reorder/jitter. Record whether figures are RTT or one-way injection.
Never shape the host's production/default network; the future runner must own its
isolated VM/network resources and prove cleanup.

Test one DC unavailable at full sustained traffic, complete site loss, a 24-hour
site partition and rejoin, asymmetric links, DNS/DC locator failure, clock skew,
key-provider outage, expired trust, process/host kill, disk-full and audit-collector
loss. Capture correctness and degraded behavior as well as performance. Account
disable during partition has observable stale-state limits; do not promise global
instant revocation. Offline cached login is not online authentication success.

## Measurements, acceptance and cost

Retain per-operation/per-site histograms (p50/p95/p99/max), offered/achieved rate,
unexpected errors, expected denials, timeout/cancel counts, concurrent requests,
CPU, RSS/working set, disk bytes/IOPS/fsync latency, network bytes, journal/replica
lag and audit backlog. Avoid coordinated omission and averaging percentiles
across sites. Separate protocol time from injected network time; disclose clocks,
sampling, warmup, observation gaps and histogram overflow.

Provisional gates remain LAN p95 <=100 ms / p99 <=300 ms for KDC and bounded
indexed reads; local write p95 <=500 ms; <0.1% unexpected errors; healthy-site
replication p99 <=5 s and inter-site <=60 s. At sustained load with one DC down,
CPU <=70%, memory <=80%, bounded queues and no lost acknowledged local writes.
Measure DNS/client failover <=60 s, clean whole-domain RPO <=1 h / RTO <=4 h and
99.95% monthly healthy-site auth availability using real online probes.

Use three repetitions with distinct recorded run IDs/seeds and report every run,
including failures, variance and deviations. A monthly availability SLO cannot be
proved by a one-hour run. Retention, backup/restore and audit storage are separate
measured budgets. Record provider/region or physical host, CPU model/oversubscription,
RAM, storage/filesystem/flush policy, OS/kernel/packages, images/digests, VM-hours,
Windows licensing rights, storage/egress and actual currency/unit prices. No cost
estimate is asserted until a real host/provider is selected. Published artifacts
must be redacted and bound to source/contract/dataset revisions.
