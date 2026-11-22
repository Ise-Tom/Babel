# Security policy

Babel has an experimental loopback-only LDAP lab. There are no supported
production versions and it
must not be used as a production identity provider or domain controller yet.

Do not post vulnerabilities, secrets, or real directory data in public issues.
Use GitHub's **Report a vulnerability** (private vulnerability reporting) when
available on this repository. Maintainers must enable it before accepting users.
If that entry is unavailable, request a private contact through a public issue
without including vulnerability details; wait for a private channel before
sharing sensitive evidence. No security email address or response SLA exists yet.

Reports should include affected commit, synthetic reproduction, expected versus
observed behavior, and impact.

There is no supported production version and no active response SLA. During solo
development, a public experimental preview must state that it is unsupported
and that only one responder is available. Before soliciting external preview
users, the owner must run and privately close a benign live reporting drill that
independently verifies owner notification, private receipt and acknowledgment;
publish only redacted outcome metadata. If the route fails, do not solicit
reports or external testers until repaired. The two-working-day acknowledgment
and seven-day update intervals remain proposed targets, not promises.

Before any supported production release, appoint two genuinely available
security contacts, verify each one's private access and independent
receipt/escalation in a benign drill, publish supported-version and
coordinated-disclosure policies, complete independent security assessment and
rehearse compromise containment, clean recovery and credential/key rotation.
Supported response targets require named staffing and evidence that the targets
can be met. A shared mailbox, saved draft, bot or untested nominee is not backup
coverage.

Critical exploited issues require immediate triage and credential/key rotation
guidance, not only a code patch.

The [native-system threat model](docs/threat-model.md) and
[phase verification plan](docs/validation-plan.md) define planned security evidence.
Their existence is not an audit result or supported-version announcement.
