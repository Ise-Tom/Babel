# Remote operations and EDR capability contract

Status: proposed final roadmap expansion, following endpoint patch management.
The scope includes remote desktop/terminal support, general server-to-device
file upload and native endpoint detection and response (EDR) for supported
Windows and Linux devices. These capabilities are planned, not implemented. Complete conception and
acceptance are specified in [Phase 14](phases/phase-14.md),
[Phase 15](phases/phase-15.md), [Phase 16](phases/phase-16.md) and joint
[Phase 17](phases/phase-17.md). All 19 stable REMOTE/FILE/EDR IDs below remain
normative and traced. The phase designs now include proposed concurrency, event
and outage profiles; those are ratification targets rather than measurements.
They do not change the first production AD-like server contract.

All management services and session/transfer/telemetry relays run on Linux.
Windows/Linux endpoint agents provide the required local integration. Evaluate
sharing secure enrollment, device identity and transport with the patch agent,
while keeping remote support, file delivery and EDR modules separately enabled,
authorized and supervised. A support operator does not automatically become a
security responder or patch approver. A module failure must not stop domain
login, patch recovery or another module's safety controls.

## Final roadmap phases

| Phase | Deliverables | Exit gate |
| --- | --- | --- |
| 14 — Remote device access | Authorized attended/unattended support, Windows/Linux desktop where supported, terminal access, session broker and revocation | Qualified protocol/OS matrix; MFA, consent, delegation and session-termination tests; no open inbound endpoint ports required by default |
| 15 — General file delivery | Upload files from the Linux management server to selected devices, with policy, resumable delivery, receipts and protected destination handling | Integrity/authentication tests, denied-path/authorization coverage, partial transfer recovery and verified endpoint receipt; uploading does not execute a file |
| 16 — Native EDR | Endpoint telemetry, behavioral detections, triage, evidence collection and authorized containment through a dedicated agent/module | OS-specific sensor qualification, labeled detection/false-positive reports, safe response and privacy controls; independent security review |
| 17 — Fleet qualification | Joint remote-support/file-delivery/EDR operation alongside patch management at 10,000 devices across three sites | Resource/bandwidth/retention evidence, abuse and outage tests, compromised-agent/controller recovery and no directory SLO regression |

Supported Windows editions, Linux distributions, desktop environments, kernel
versions, sensor APIs and session protocols must be selected and versioned before
implementation. Terminal support can cover headless Linux; desktop support is
qualified separately for Windows session behavior and Linux X11/Wayland.
macOS/mobile support is a separately qualified future extension.

## Remote access requirements

| ID | Capability | Acceptance evidence |
| --- | --- | --- |
| REMOTE-01 | Authenticated desktop and terminal sessions to enrolled, authorized devices | Real Windows/Linux session tests including headless Linux, NAT/proxy/relay paths and explicit unsupported configurations; choose maintained protocols/components rather than inventing a remote-control protocol |
| REMOTE-02 | Attended support with visible user consent and an immediate disconnect action | Reject denied/expired consent and misleading session requests; show operator identity and active session; no covert access mode |
| REMOTE-03 | Separately approved unattended administration | Explicit device policy, scoped operator rights, time-bounded grants, admin MFA/step-up and maintenance restrictions; no unattended access inferred from domain membership |
| REMOTE-04 | Session control, audit and sensitive-channel separation | Record actor/device, approvals, start/end and actions available to the operator; independently authorize elevation, clipboard, transfer and recording; test clipboard/drive redirection restrictions |
| REMOTE-05 | Secure brokering and prompt revocation | Per-session authorization, authenticated encrypted transport and device verification; no domain-admin credentials in the agent; bounded disconnect after revocation and defined behavior during broker/identity-provider failure |
| REMOTE-06 | Safe operation across OS privileges and session states | Test lock screen, user switching, terminal privilege escalation, reconnect and concurrent operators; honor OS security boundaries and document elevation requirements; no bypass of OS credential protection |

Prefer endpoint-initiated outbound connections through authenticated relays over
exposing RDP/SSH directly to the Internet. MFA on the web portal does not by
itself secure a reusable underlying RDP/SSH credential. Define endpoint-to-broker
and operator-to-broker trust, credential custody, certificate validation and relay
visibility explicitly. Broker termination of encryption must be documented; do
not claim end-to-end confidentiality if a relay can read session content.

Session recording is not blanket keystroke/credential capture. Enable it only
under explicit policy with notice, access restrictions and retention limits;
credentials and sensitive input need a documented redaction/recording boundary.
Remote terminal access can execute arbitrary commands and therefore requires
its own high-trust authorization, not the patch module's allowlisted executor.

## Server-to-device file delivery requirements

| ID | Capability | Acceptance evidence |
| --- | --- | --- |
| FILE-01 | Explicit server-originated uploads to one or many selected endpoints | Preview exact recipients, content digest, size, expiry and destination; approve bulk/sensitive delivery and prevent recipient expansion after approval |
| FILE-02 | Secure staging, integrity and recipient verification | Authenticate uploader/source/device, encrypt in transit and protect staged content at rest; verify hashes against authenticated metadata, not an attacker-supplied hash alone |
| FILE-03 | Destination and privilege restrictions | Per-role/device allowed paths, canonicalization, symlink/race and traversal defenses, disk quota, ownership/mode preservation rules and explicit overwrite policy; prohibit silent writes into privileged startup/system locations |
| FILE-04 | Resumable, bandwidth-limited transfer with accurate receipts | Test interruptions, duplicate requests, stale jobs, full disks and agent restarts; stage then atomically finalize where supported; report partial/expired/failed/verified states and clean up abandoned content |
| FILE-05 | Content policy, separate execution and audit | Apply approved type/size/malware policies without promising scanners detect every threat; uploaded files are not automatically executed; record who sent what to which device and destination, without exposing confidential file contents in logs |

Patch packages continue through the patch approval/verification path. General
uploads must not bypass signed patch policy or become an unaudited software
execution route. If device-to-server retrieval is later added for support or
forensics, give it separate permissions, consent/legal policy, collection scope
and retention controls; upload permission is not permission to read user files.

## Native EDR requirements

| ID | Capability | Acceptance evidence |
| --- | --- | --- |
| EDR-01 | Dedicated installed sensor/agent module with secure enrollment and update lifecycle | Signed/verifiable packages and policy, mutual authentication, per-device identity/revocation, staged updates and rescue/uninstall flow; module isolation from remote support and patch execution |
| EDR-02 | OS-specific endpoint telemetry | Qualified process lineage, executable hashes/signatures, network connections, file and relevant persistence/security events using supported APIs; document blind spots, event loss and OS/privilege prerequisites |
| EDR-03 | Behavioral detection, indicator matching and versioned rules | Labeled synthetic scenarios, expected detections, measured false positives/negatives and tuning/exclusion audit; verify rules and bound their CPU/memory cost; no claim of universal malware detection |
| EDR-04 | Investigation and privacy-scoped evidence collection | Process/device timeline, alert correlation and case workflow; approved minimal evidence capture with provenance, hashes, access controls and retention; no indiscriminate memory, credential or user-file collection |
| EDR-05 | Authorized response: stop/quarantine malicious processes/files and isolate a device | Separate response RBAC, approvals and bounded automation; preserve narrow authenticated management/recovery paths, define reboot persistence and test release from isolation; protect DC/service topology from fleet-wide lockout |
| EDR-06 | Tamper resistance and trustworthy sensor health | Detect stopped/stale sensors, policy/signature changes and telemetry gaps; audit exceptions and uninstall; qualify protections per OS and acknowledge a compromised kernel/root can defeat local evidence |
| EDR-07 | SIEM/SOAR integration and safe automated response | Authenticated scoped connectors, deduplicated alerts, expiring/idempotent actions and auditable decisions; false detections must not autonomously disable the whole domain or isolate the whole fleet |
| EDR-08 | Offline operation and resilience under telemetry/provider outages | Bounded encrypted event buffering, trusted cached rules, freshness/loss indicators and controlled reconnect; avoid login disruption, disk exhaustion and treating missing events as a healthy device |

Evaluate native Windows event/security APIs and Linux audit/eBPF facilities
against the exact supported OS matrix. Use kernel drivers only where justified
and independently reviewed, with required platform signing and compatibility
tests. Do not disable Secure Boot, OS protections or signature verification to
make sensors work. Integration with existing endpoint protection may be useful,
but external alerts alone do not satisfy the planned native EDR capability.
Detection-only versus prevention enforcement must be visible and separately
qualified; quarantining a file does not undo earlier malicious actions.

## Fleet security, capacity and release gates

The provisional scale is the patch module's **10,000 enrolled computer endpoints
across three sites**. This is separate from 10,000 human identities and is not a
benchmark result. Ratify per-service capacity/SLOs before Phase 17, including
expected simultaneous desktop/terminal sessions, concurrent transfer counts,
payload sizes, telemetry events/second per endpoint, evidence upload limits and
retention. Ten thousand enrolled devices does not mean ten thousand simultaneous
desktop streams. Benchmark event storms and offline reconnect as well as steady
state, with CPU/RAM/disk and endpoint battery/agent overhead measured by module.

Isolate directory, support/transfer and EDR resources, credentials and network
access. Use backpressure, priority queues, storage quotas and site bandwidth
limits so remote traffic or telemetry cannot starve authentication/replication.
Simulate controller/relay compromise, stolen session tokens, malicious upload
paths, poisoned agents/rules, replayed commands and forged events. Mass-response
and mass-upload operations need explicit blast-radius limits and emergency stop.
Revocation or emergency stop cannot be guaranteed instantaneous on offline
endpoints; enforce job expiry and reauthorization on reconnect.

Add real OS session, file-permission, sensor, reboot and response integration
tests with implementation, plus fuzzing of message/file parsers, dependency
scans and signed agent/rule artifact verification. Include locked/privileged
sessions, consent denial, expired approvals, path traversal/symlink races,
malicious replay, partial transfer, sensor outage and isolation recovery cases.
Detection tests use authorized, isolated labs and synthetic fixtures; no real
malware or endpoint operations run against developer/production devices.

Before each module's release, publish its support matrix, independent security
assessment, measured performance/false-positive limits, operator runbooks,
privacy/recording policy and compromised-controller/agent recovery procedure.
Owners must select supported versions and accept residual risk explicitly;
green repository/documentation CI is not functional evidence for these modules.
