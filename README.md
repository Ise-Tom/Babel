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

Python 3.12 or 3.13 and Linux x86-64 are the tested repository-tooling targets.
This does not select the future server implementation language.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements-ci.txt -r requirements-ci.in
python scripts/check_ci_scope.py
python scripts/check_docs.py
ruff format --check scripts tests
ruff check scripts tests
mypy
coverage run -m unittest discover -s tests -v
coverage report
bandit -c pyproject.toml -r scripts
zizmor --offline --strict-collection .github/workflows
pip-audit --strict --disable-pip --require-hashes -r requirements-ci.txt
python scripts/install_ci_tools.py --directory /tmp/babel-ci-tools
/tmp/babel-ci-tools/actionlint
/tmp/babel-ci-tools/gitleaks git --redact --no-banner .
/tmp/babel-ci-tools/gitleaks dir --redact --no-banner .
```

CI also tests deterministic source packaging and retains coverage, security
reports and a CycloneDX inventory of **CI dependencies**, not a future server
SBOM. New source trees/manifests fail the scope check until their executable
gates are added. Source packaging is not an application build or deployment.
See [CI/CD operation](docs/ci-cd.md) for remaining product and GitHub-plan gates.

## License

Open source distribution is the goal, but a license has not yet been selected
by the owner. Until a LICENSE is adopted, normal copyright restrictions apply;
this project must not claim to grant open source reuse rights. License selection
and dependency compatibility are release blockers.
