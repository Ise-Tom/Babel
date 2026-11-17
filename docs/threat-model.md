# Initial threat model

Status: design input, not a completed audit. Revisit on every architecture or
trust-boundary change. Link tests to SEC IDs in the requirements.

## Assets and boundaries

Highest-value assets are password verifiers, Kerberos/replication/trust keys,
privileged group membership, ACLs, schema, GPO/SYSVOL content, backups and update
signing identity. A directory controls downstream workstation/server trust.
Boundaries include untrusted domain clients -> protocol listeners; browser ->
admin API -> directory; DC -> DC over WAN; agent -> update service; backup ->
restore domain; fork PR -> CI runner; release workflow -> artifact consumer.

Trust the selected OS, reviewed native-core components/libraries and administrator-controlled
root keys only to the stated level. Writable DC compromise gives domain-wide
credentials and authority. Isolate test domains from the host and corporate
networks. Production identity data is prohibited in public CI.

| Attacker / failure | Attack path and impact | Required mitigation and evidence |
| --- | --- | --- |
| Unauthenticated network client | Malformed LDAP/RPC/Kerberos input, amplification or expensive queries exhaust DCs or execute code | Bounded parsing/queries, fuzzing and resource budgets; SEC-02/08 |
| Compromised workstation or low-privilege user | Relay, replay, ticket theft, weak delegation or ACL escalation grants domain admin | Signing/channel binding, replay checks, least delegation, denied-operation matrix and red-team scenarios; SEC-01/02/03 |
| Stolen admin session / malicious website | CSRF, XSS or session replay changes privileged policy | Admin MFA, CSP, CSRF, secure cookies, short sessions, step-up and revocation tests; SEC-05 |
| Rogue replica or network partition | Unauthorized replication leaks all password hashes; stale policy or conflicts preserve access | Authenticate/authorize replicas, protect replication keys, audit DCSync-like access; partition and convergence tests; SEC-01/06/09 |
| Backup theft or destructive insider | Exfiltrates credentials or destroys recoverability | Encryption with separate key custody, immutable copies, dual control and isolated restore tests; SEC-06/10/11 |
| Malicious contributor / dependency | PR executes privileged CI or poisoned artifact reaches a DC | No PR secrets, read-only token, ephemeral runners, pinned actions/tools, reviewed locks, verified provenance and protected release refs; SEC-10 |
| Disk-full, clock skew or expired certificate | Login outage, inconsistent replication or failed recovery | Capacity alarms, time/DNS health, rotation, fault injection and documented recovery; OPS-01 |

## Required design reviews

Review protocol downgrade behavior, account recovery and lockout abuse, password
reset versus key rotation semantics, constrained/resource-based delegation,
trust SID filtering, GPO script execution, certificate enrollment/PKINIT and
schema extensions. For the [native core](native-core-plan.md), review identity/ACL
semantics, parser bounds, credential formats, durable acknowledgments, replication
metadata and restore/upgrade transitions before storing valuable credentials.
Reuse reviewed cryptography and assess library CVE response. Babel owns parser/
state-machine correctness and integrated protocol security; memory safety alone
does not prevent authorization or replication flaws.

Bind management only to an explicitly configured trusted network until secured.
Enumerate ports by the selected implementation, including dynamic RPC ranges;
separate replication/admin traffic where feasible. Validate DNS and time before
protocol diagnosis. Protect audit export separately from domain-admin control,
and document what evidence is lost when a DC itself is compromised.

## Extended feature trust boundaries

The [extended security roadmap](security-roadmap.md) introduces additional
boundaries to review before implementation: recovery operators and approvers;
CA/HSM/KMS providers; device posture agents; federation/provisioning sources;
SIEM collectors; and automated incident responders. Test stolen recovery
factors, malicious identity claims, false posture, CA/template abuse, approval
bypass, audit tampering and destructive false-positive response. Each module
needs explicit authority, failure behavior, secret custody and blast-radius
limits. External provider claims must not silently grant domain privilege.

## Future endpoint patch-management boundary

The [later patch-management module](patch-management-roadmap.md) adds highly
privileged endpoint executors, enrollment/signing authorities, catalog sources
and site relays. Treat malicious campaigns, compromised catalog/agent updates,
replayed offline jobs, stolen device identities and mass reboot as distinct
fleet-wide threats. Enforce approval/scope separation, authenticated expiring
commands, verified native packages, rollout limits and independent post-install
evidence. Relay compromise must not grant deployment authority. Keep patch
service failures and credentials isolated from core directory operation, and
rehearse controller compromise before releasing that module.

## Future remote operations and EDR boundaries

The [final endpoint operations phases](endpoint-operations-roadmap.md) add remote
session brokers, general upload paths, telemetry/rule pipelines and privileged
response agents. Assess stolen operator sessions, consent/elevation bypass,
relay visibility, malicious destination paths, forged/suppressed endpoint events
and false-positive mass containment. Separate support, transfer, patch and EDR
authority; enforce session/job expiry, recording/privacy policy, command scope
and a tested rescue path. A compromised root/kernel or fleet controller can
defeat local monitoring; sensor health and independent audit are evidence, not
proof of endpoint integrity.

## Residual risks and release conditions

Legacy Windows/application compatibility can conflict with secure defaults.
Any weakening needs a documented threat, scoped exception, expiry, visibility,
and an explicit release decision. A passing secret scanner cannot prove absence
of secrets; rotate leaked keys even after deleting history. A green CI result
currently validates only the delivery foundation. Independent assessment,
protocol interop and recovery tests remain mandatory before production.
