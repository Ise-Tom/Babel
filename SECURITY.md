# Security policy

Babel is pre-implementation. There are no supported production versions and it
must not be used as a production identity provider or domain controller yet.

Do not post vulnerabilities, secrets, or real directory data in public issues.
Use GitHub's **Report a vulnerability** (private vulnerability reporting) when
available on this repository. Maintainers must enable it before accepting users.
If that entry is unavailable, request a private contact through a public issue
without including vulnerability details; wait for a private channel before
sharing sensitive evidence. No security email address or response SLA exists yet.

Reports should include affected commit, synthetic reproduction, expected versus
observed behavior, and impact. Maintainers should acknowledge within two working
days and provide a triage update within seven days once a security team and
private channel exist; these are proposed operating targets, not current SLAs.

Before public previews, appoint at least two security contacts, test the private
reporting route, define embargo and coordinated disclosure rules, and publish a
version support policy. Critical exploited issues require immediate triage and
credential/key rotation guidance, not only a code patch.

The [native-system threat model](docs/threat-model.md) and
[phase verification plan](docs/validation-plan.md) define planned security evidence.
Their existence is not an audit result or supported-version announcement.
