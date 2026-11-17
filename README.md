# Babel

Babel aims to be an open source Active Directory replacement with a clearer,
safer administration experience. **This repository is a planning and delivery
foundation; no directory server or production-ready identity service exists yet.**

The first production release must be **hosted on Linux servers**, providing
Windows domain compatibility for **10,000 identities across three sites**.
Linux hosts run the directory/domain controllers and administration services;
Windows machines are clients or interoperability test references. A standalone
Babel domain must not require a Windows Server host. These are acceptance
targets, not measured capabilities.

The core product includes identity and password lifecycle management, users and
groups, delegated permissions, Windows domain join, Kerberos/LDAP, DNS, Group
Policy (GPO/SYSVOL), trusts, replication, backup and recovery, plus a web UI and
automation API/CLI. Advanced security capabilities extend this core product.

- [Product, security, and capacity requirements](docs/requirements.md)
- [Threat model](docs/threat-model.md) and [extended security roadmap](docs/security-roadmap.md)
- [Delivery roadmap and release gates](docs/roadmap.md)
- [Later endpoint patch management](docs/patch-management-roadmap.md)
- [Final remote access, file delivery and EDR phases](docs/endpoint-operations-roadmap.md)
- [Architecture decisions](docs/architecture.md)
- [CI/CD operation and repository settings](docs/ci-cd.md)
- [Contributing](CONTRIBUTING.md) and [security reporting](SECURITY.md)

## Validate the repository

Python 3.12+ and Linux x86-64 are sufficient for the current checks:

```sh
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
python3 scripts/install_ci_tools.py --directory /tmp/babel-ci-tools
/tmp/babel-ci-tools/actionlint
/tmp/babel-ci-tools/gitleaks git --redact --no-banner .
```

Tool archives are version-pinned and checked against SHA-256 digests recorded
from the publishers' release checksums. No application build, integration suite,
or deployable artifact is claimed by these checks. See the roadmap for the
checks that must be added alongside implementation.

## License

Open source distribution is the goal, but a license has not yet been selected
by the owner. Until a LICENSE is adopted, normal copyright restrictions apply;
this project must not claim to grant open source reuse rights. License selection
and dependency compatibility are release blockers.
