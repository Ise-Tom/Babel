# Native Babel threat model and phase controls

Status: design baseline, not a completed assessment. Applies to the native core,
Linux operations and all later endpoint services. Every detailed [phase](phases/README.md)
contains its own security/failure requirements; this register links shared attack
paths to design and executable-evidence obligations. Revisit it when an interface,
provider, supported protocol, privileged actor or persistence format changes.

## Assets, trust and non-goals

Tier 0 assets include directory ACLs/schema/IDs, password verifiers, ticket/service/
trust/replication keys, GPO/SYSVOL, DC hosts and coherent encrypted recovery state.
Separate high-impact assets include fleet enrollment/signing/dispatch authority,
remote sessions, uploaded content, sensor/rule provenance and forensic evidence.
A compromised writable DC is domain compromise. A compromised endpoint kernel/root
may defeat local monitoring. Shared management UI roles do not provide hostile-
tenant isolation over one privileged directory or unrestricted executor.

Trust only declared components at their reviewed boundary: protocol client to
listener/core; core to transactional store/key provider; DC to authenticated DC;
browser/API to delegated mutation; backup to clean restore; CI to signer/consumer;
external IdP/CA/posture source to scoped connector; agent/relay/operator to scoped
patch/support/file/EDR authority. Authenticate identity and data provenance at each
boundary; transport encryption alone is not action approval or trustworthy state.

## Attacks, failure cases and required evidence

| ID | Threat / consequence | Required control and proof | Primary phases |
| --- | --- | --- | --- |
| T-01 | Unauthenticated malformed LDAP/RPC/Kerberos/DNS or expensive nested queries cause execution/exhaustion | Bounded parser/query/state-machine budgets, fuzz/property corpus and DoS measurements; no unbounded allocations | 0–4, 10 |
| T-02 | Wrong ACL/normalization/schema handling leaks attributes or grants privilege | One core authority, stable identifiers, denied-operation/property tests and reference access comparisons | 0–2, 4 |
| T-03 | Stolen tickets, weak service credentials or flawed PAC/delegation/replay validation permit impersonation | Reviewed crypto, key custody/lifetimes, PAC/delegation/replay/downgrade and rotation tests; disclose detection limits | 1–4, 7–9 |
| T-04 | NTLM relay, unsigned binds/channels or legacy fallback bypass auth policy | Secure LDAP/SMB/Netlogon defaults and expiring scoped compatibility exceptions, tested on actual clients | 1–4, 7–9 |
| T-05 | GPO/SYSVOL edits, scripts or partial version updates persist privileged code | Approved policy scope/diffs, correct file/AD ACLs, staged consistency/reconciliation and actual resultant-policy/revert tests | 1–4, 7 |
| T-06 | CSRF/XSS/session theft/helpdesk recovery or MFA enrollment takeover changes domain policy | Phishing-resistant admin auth, session/CSRF controls, scoped recovery/step-up and browser/API denial/abuse tests | 1, 4, 7 |
| T-07 | Forged external claims, connector SSRF or certificate-template/mapping abuse escalates identity | Scoped issuers/destinations, no arbitrary privileged URL fetch, claim/audience/nonce/template authorization and provider-loss tests | 0, 8–9 |
| T-08 | Unauthorized replication, stale restore, conflict/RID errors or partial cursor commits leak credentials or corrupt identity | Replica ACLs, native metadata invariants, atomic progress, partition/conflict/rollback and clean replica recovery tests | 0–4, 9 |
| T-09 | Backup theft, lost keys or insider destruction makes compromise/recovery permanent | Independent encryption/custody, immutable/offline copies, coherent state and full-dataset clean-room restore/rotation | 0, 3–6, 9 |
| T-10 | Malicious dependency/contributor/builder/signer distributes domain compromise | Locked/verified artifacts, least-privilege ephemeral CI, scoped signing and actual review/ref protection; independent rebuild/update replay tests | 0–1, 4–6, 10 |
| T-11 | Approver self-approval, stale grants, nested privilege or scope replacement bypasses least privilege | Expiring exact-scope grants, separation of duty, real effective-access tests and audited exception expiry | 1–4, 7 |
| T-12 | Cloned device identity, enrollment replay or poisoned inventory changes fleet targets | Unique mTLS enrollment, revocation/rotation, authenticated timestamped inventory and denied target-change tests | 11–17 |
| T-13 | Poisoned patch/catalog/relay or replayed offline install executes across the fleet | Vendor/content verification, immutable campaign scope, native typed executor, cancellation/expiry, canary pause and receipt reconciliation | 11–13, 17 |
| T-14 | Remote session theft, consent/elevation bypass or relay visibility exposes users/admins | Separate channel grants, visible attended consent, explicit unattended policy, encrypted authenticated paths and bounded disconnect/rescue | 14, 17 |
| T-15 | Upload traversal/symlink/reparse races, overwrite or autoexecution creates persistence | Destination-at-open/finalization validation, quotas, staged receipts, separate execution rights and real filesystem race tests | 15, 17 |
| T-16 | Sensor/rule tamper, forged events, PID reuse or dropped telemetry hides threats | Signed rules/agents, provenance/gap visibility, supported native sensors, labeled detection tests and honest root/kernel limits | 16–17 |
| T-17 | False detections or stolen response authority isolate every DC/device | Typed scoped expiring response, independent mass-action approval, blast-radius limits and isolation/rescue/emergency-stop drills | 9, 16–17 |
| T-18 | Endpoint traffic, cache misses or event storm starves core authentication | Independent credentials/resources, priorities/quotas/backpressure and combined fleet/directory WAN/load/fault qualification | 3–4, 11–17 |
| T-19 | Recording/inventory/evidence/diagnostic overcollection leaks personal or secret data | Purpose/field minimization, consent/access/retention, redaction and unauthorized collection/export tests | All; especially 6, 8, 14–17 |
| T-20 | Disk-full, audit loss, clock skew, expired provider trust or unavailable queue creates unsafe success | Durable security/audit transition rules, explicit conservative/degraded behavior, bounded queues and restart/provider/time fault tests | 1–6, 8–17 |

## Response and residual risk

Baseline secure defaults and first-production requirements cannot be deferred to
advanced features. Any legacy exception has an owner, scope, expiry, visibility
and explicit release effect. Web MFA does not impose MFA on every legacy domain
protocol. Offline devices/partitioned replicas cannot honor instantaneous global
revocation; expose known/unknown state and reauthorize expiring actions on reconnect.

For domain compromise, isolate evidence, revoke/quarantine through a rehearsed
plan, restore clean state and rotate affected administrator, service, machine,
trust and ticket-signing credentials with correct sequencing. For fleet compromise,
stop dispatch, rotate enrollment/signing authority, inspect content/rules/queued
jobs and recover through an independent rescue channel. File/process quarantine
does not reverse earlier execution; restoring an old image does not prove safe
schema/key/replication state. Test irreversible cases explicitly.

A secret scan cannot prove no secrets exist; rotate leaked credentials even after
history removal. Static analysis, memory-safe languages and green CI are useful
controls, not proof of conformance/security. Independent assessments, real-client
negative tests, capacity faults and current recovery evidence gate production.
The [validation plan](validation-plan.md) defines required results; the
[decision register](decisions.md) names unresolved authority/infrastructure choices.
