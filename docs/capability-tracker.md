# Capability implementation tracker

The dashboard's **Capabilities** tab tracks all 130 global requirements from
[requirements.md](requirements.md). Search by ID, behavior, implementation or gap;
filter by implementation status and open individual cards for details. Each card
links its phase requirements, implementation work, immutable source evidence and
development blockers. Direct links use `#view=capabilities&capability=AD-04`.
The GitHub-rendered report includes the same state and explicit scope.

## What the states mean

| State | Meaning |
| --- | --- |
| Planned | No functional implementation is claimed; related design or experiments can exist |
| Prototype | A limited executable subset exists, with explicit gaps |
| Partial | Some behavior exists, but the capability's complete contract is unmet |
| Implemented | An explicit complete implementation claim; separate owner acceptance is still needed |

The category identifies **product**, **runtime lab**, **qualification experiment**
or **engineering tooling**. A standalone TLS probe is a qualification experiment.
The project dashboard is engineering tooling, not the domain administration UI.
The PostgreSQL experiment does not implement native directory backup/restore.
No complete product capability is currently accepted.

## Maintaining claims

`dashboard/capabilities.json` is a versioned sparse register keyed by canonical
global ID. Omitted IDs receive a planned default with their canonical verification
contract as a gap. Add an explicit claim only when it improves the information:

- State and category, plus a precise scope.
- Implemented behavior and missing behavior, using concrete operations.
- Existing `dashboard/progress.json` work IDs and development blocker IDs.
- `acceptance: null` until the owner explicitly accepts the full capability.

Non-planned claims require implemented behavior and an implementation work record.
The work supplies how it was built, actual validation, limitations and pinned
source files. Planned claims cannot assert implemented behavior. Incomplete
claims must list gaps. Full acceptance requires product category, implemented
state, no remaining gaps and the normal reviewer/date/evidence proof. CI validates
these structural rules; it cannot establish that a claim is true by itself.

Requirement associations and shared preparatory work are also displayed for
navigation. They never change implementation or acceptance state automatically,
and they never start a future phase. The four existing owner-accepted scopes stay
separate from capability acceptance. Keep PR work in the progress register so the
GitHub report can label proposed work pending merge; Pages shows trusted main
after merge and successful deployment.

Run `python scripts/build_dashboard.py --check`, the repository tests and the
dashboard build/browser checks described in [ci-cd.md](ci-cd.md). These check the
tracker and interface, not product conformance.
