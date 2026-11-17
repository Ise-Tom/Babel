# Babel

Babel aims to be an open source Active Directory replacement with a clearer,
safer administration experience. **An experimental Rust LDAP RootDSE lab slice is implemented. No domain
controller or production-ready identity service exists yet.**

The first production release must be **hosted on Linux servers**, providing
Windows domain compatibility for **10,000 identities across three sites**.
Linux hosts run the directory/domain controllers and administration services;
Windows machines are clients or interoperability test references. A standalone
Babel domain must not require a Windows Server host. These are acceptance
targets, not measured capabilities.

The core product includes identity and password lifecycle management, users and
groups, delegated permissions, Windows domain join, Kerberos/LDAP, DNS, Group
Policy (GPO/SYSVOL), trusts, replication, backup and recovery, plus a web UI and
automation API/CLI. Babel will build its own native AD-compatible core, with
reviewed libraries and a protocol conformance harness; Samba AD DC will not be a
required production runtime. Advanced security capabilities extend this core product.

- [Phase 1 implementation progress and native commands](docs/phase-01-progress.md)
- [Product, security, and capacity requirements](docs/requirements.md)
- [Complete phase designs and acceptance specifications](docs/phases/README.md)
- [Verification plan](docs/validation-plan.md) and [open design decisions](docs/decisions.md)
- [Threat model](docs/threat-model.md) and [extended security roadmap](docs/security-roadmap.md)
- [Delivery roadmap and release gates](docs/roadmap.md)
- [Later endpoint patch management](docs/patch-management-roadmap.md)
- [Final remote access, file delivery and EDR phases](docs/endpoint-operations-roadmap.md)
- [Architecture decisions](docs/architecture.md) and [native-core implementation plan](docs/native-core-plan.md)
- [CI/CD operation and repository settings](docs/ci-cd.md)
- [Contributing](CONTRIBUTING.md) and [security reporting](SECURITY.md)

## Project progress dashboard

**[Open the live dashboard](https://ise-tom.github.io/Babel/).**

The preferred interface is a compact, searchable phase board: select a phase,
then open the requirements, implementation evidence and problems you need. The
interactive build is hosted on GitHub Pages; successful main CI updates the same
web address automatically. See the
[hosting setup](docs/project-dashboard.md#activate-public-web-hosting-once) and
[security settings](docs/github-security-settings.md).

The **[GitHub progress report](https://github.com/Ise-Tom/Babel/blob/dashboard-live/README.md)**
follows repository visibility and refreshes on CI state changes, including failed checks.
Open PR proposals remain separate from main-branch totals. It remains available while interactive hosting is configured.

The [dashboard guide](docs/project-dashboard.md) explains how to build/open the
portable phase board, inspect implementation evidence and maintain progress facts.
It covers all 18 phases, 180 current requirements, feature associations, completed increments
and problems/resolutions. It is a read-only engineering report, not the planned
directory administration console or a live production/GitHub status service.

```sh
cd dashboard
npm ci --ignore-scripts
npm run build
npm run preview
```

The build also produces a self-contained `dashboard/dist/index.html`, available
as the **dashboard-standalone** CI artifact. The Pages job publishes only this
tested build. The publisher supports public and private Babel repositories;
workflows never change repository visibility.

## Validate the repository

Python 3.12 or 3.13 and Linux x86-64 are the tested repository-tooling targets.
This does not select the future server implementation language.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements-ci.txt -r requirements-ci.in
python scripts/check_ci_scope.py
python scripts/check_design.py
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
