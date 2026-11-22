# P00-01 conformance follow-up

[Pinned PR #40 review](https://github.com/Ise-Tom/Babel/blob/93e1dc956263db27d07fe1192e74205c60294032/docs/validation/p00-01.md)
covers the original matrix design for 30 families. This follow-up adds seven
wire mappings and one workflow, verifies 161 distinct operation sections
against the pinned editions, and identifies what each of the 12 open route
decisions requires. The full gate is blocked.

## PR #40 open mappings

All rows inherit Ise-Tom as accountable owner. The
[operation matrix](../../lab/compatibility.json) records the expected success,
refusal and evidence for each candidate. Implementation and client
selection remain independently reviewable.

| Open row | Resolved from the pinned references or project scope | Specific remaining test or decision |
| --- | --- | --- |
| join-login/join-variants | Separate new account creation and pre-staged account reuse from the protected machine channel. MS-ADTS §3.1.1.5.2, MS-SAMR §3.1.5.4.4 and MS-NRPC §3.5.4.4.2 identify the account and channel boundaries. | Windows 11 Pro/Enterprise and Server 2022/2025 builds must expose the actual join path, reuse settings and refusals. Babel needs the network directory write, protected channel and online logon. |
| ldap-directory/control-variants | MS-ADTS §§3.1.1.3.4.1.3, .13 and .17 identify DirSync, server-side sort and VLV. §3.1.1.3.1.3.3 defines range retrieval through an attribute option. | Capture installed RSAT flags and combinations, including continuation and negative authorization. Implement controlled directory search and authorized attribute results in Babel. |
| dns-locator/legacy-discovery | MS-ADTS §§6.3.5 and 6.3.6.2 identify mailslot ping and NetBIOS-based discovery. The matrix has separate DNS and LDAP-ping paths. | Observe exact Windows policy, packet path and bounded behavior under DNS loss. The supported fallback policy and native DNS/locator behavior remain open. |
| dns-update/management-rpc | MS-DNSP §§3.1.4.5, 3.1.4.10 and 3.1.4.11 pin record-management opnums 4, 9 and 10. The third adds zone/scope selection. Machine-owned signed UPDATE is separately mapped. | Choose the supported DNS management journeys/versions and compare authorized update, access denial and record state on an exact tool build. Babel needs secure DNS updates and any selected management RPC. |
| gpo/extensions | MS-GPOL §3.2.5.1.10 maps per-user/per-computer extension selection by CSE GUID and extension invocation. Registry policy runs first. An extension failure leaves the other extension sequences independent. | Select versions and file formats for scripts and security policy, implement publication, and observe real Windows resultant settings and per-extension failure on both targets. |
| sysvol/dfsr | MS-FRS2 §§3.2.4.1.2, .3, .5 and .7 identify Windows reference connection/session/version/record operations. The [2016 profile](../functional-level-profile.md) excludes FRS fallback. | Choose a native SYSVOL replication mechanism and the Windows coexistence scope. Implement publication and compare interrupted convergence and refused peers using disposable multi-DC sites. |
| rpc-membership/rpc-variants | MS-NRPC §2.1 and Appendix A pin interface UUID/version and transport. §§3.5.4.4.2, .4 and .5 identify Authenticate3, Authenticate2 and Authenticate. | Observe exact transport, opnums, protection and faults on patched clients. Babel needs native protected RPC/channel behavior and downgrade refusals. |
| rpc-admin/rsat-surface | MS-LSAD §3.1.4.4 and MS-SAMR §3.1.5.11.2 identify the LSA policy and SAMR lookup candidates. | Capture actual RSAT package, administrative journeys, information levels and any LDAP leg, including denial. Implement delegated native authority and audit. |
| migration/migration-tool | MS-ADTS §3.1.1.5.4.2 and MS-DRSR §4.1.15 identify the same-forest move path. MS-DRSR §§4.1.2 and 4.1.2.3 distinguish the inter-forest SID-history variant, which retains the source principal. | Choose an authorized cross-forest tool and credential/cutover policy. Implement the selected path and test rollback and identity/secret handling on a disposable qualified forest pair. |
| fsmo/seizure | MS-ADTS §3.1.1.5.3.1.2 specifies role-specific access rights for a role-owner attribute change. §§6.1.5 and 6.1.5.3 define role and RID authority. | Select the forced transfer interface and implement authority fencing. Fault/rejoin comparisons must prove former-owner exclusion and RID non-reuse on multiple DCs. |
| non-windows-clients/enrollment | The scope keeps Windows GPO out of Linux/macOS qualification. MS-ADTS §3.1.1.5.2 and RFC 4120 §§3.1–3.2 identify common account/authentication stages. | Capture actual Ubuntu/Debian enrollment tooling, SSSD, Kerberos and PAM packages, and native macOS binding on eligible Apple Silicon and Intel. Compare enrollment, online login/SSO, password, refusal and cleanup. |
| admin-ux/admin-api | The project contract requires delegated, audit-correlated journeys and prevention of misleading partial success. | Publish and implement the versioned Babel CLI/API, authorization and error schema. Run real success, denial, and partial-failure journeys on Babel. |

The technical mappings above describe published behavior. The 12 identifiers
continue to track actual tool/route selection or unresolved implementation scope.
A patched client can select a subset of protocol variants. Changing the enabled
scope or dropping a profile requires an explicit project decision.

## Observations and exit criteria

The Windows preflight rerun on 23 November 2026 Paris time returned exit 2.
It observed Windows 11 Pro 26H2 x86-64 build 10.0.26300.10075, 13,207 MiB
available RAM, 268 GiB free on the only fixed volume and unavailable Hyper-V VM
and switch inventory. All six media entries were missing. The existing
[owner-approved preflight route](p00-05-p00-12.md#owner-option-and-remaining-gate-evidence)
still needs the actual eligible host, scoped access and entitled Windows media
with the staged Linux assets. Both lab cycles remain unrun. The
[asset-use dispositions](p00-05-p00-12.md#p00-16-dispositions-for-those-assets)
leave exact guest entitlements and staged assets unresolved. macOS needs its
own Apple hardware and release-specific rights.

One [local LDAP smoke](p00-01-ldap-smoke.md) ran against a release build of Babel
from main. The independent ldap3 client successfully read the anonymous
RootDSE. Credential bind and unsupported subtree/matching requests were
refused. That smoke uses an unqualified WSL environment, no licensed clients,
no Windows reference, and no populated AD directory.

| Readiness criterion | Result | Remaining evidence |
| --- | --- | --- |
| Ownership, positive and negative behavior, pinned sections | Structural pass. 30 owned families, 67 wire mappings, 13 workflows and 161 cited operation sections. | Keep unknown exchanges visible under the existing general intake rule. |
| Unresolved mappings | 12 unresolved route and scope decisions. | The named implementation, decisions and comparisons in the table above. |
| Native implementation | 30 production operation families are planned or lab-only. | Implement the supported families. The local anonymous RootDSE subset remains lab-only. |
| Exact profiles | 9 unqualified. | Actual selected OS builds, packages and verified image digests for each Windows, Linux and macOS profile. |
| Specification rights | 21 entries still pending full scope review. | The editions are pinned for the documented reference use. Full implementation rights and exact image/fixture use require their applicable records. |
| Declared positive and negative comparison scenarios | 60 unrun across 30 families, with no qualified executions. | On each applicable exact client, run both assertions against Babel and the Windows reference where the matrix declares both. Retain target builds, source revisions, exact inputs, and redacted artifacts. |
| Review | Full contract approval and scenario review pending. | Review the qualifying comparisons before requesting full acceptance. PR #40's scoped design decision is already recorded. |

The existing [scenario inventory](../../lab/conformance-evidence.json) retains
every case outcome, reason, execution and review. Its only change is the matrix
digest. Unsupported local behavior stays in the local smoke receipt, separate
from the still-unrun product comparisons. The checker continues validating
evidence shape and refuses qualification on the current inputs.

## Reproduce

Run from a clean checkout with Git's committed file bytes preserved.

~~~sh
revision="$(git rev-parse HEAD)"
python scripts/check_conformance.py --revision "$revision"
python scripts/check_conformance.py --require-ready
python scripts/check_state_security.py --revision "$revision" \
  --document-cache /path/to/public-reference-cache
~~~

The first command includes a machine-readable readiness breakdown. Strict
readiness exits 1 with the planned/lab-only implementation blocker. The
offline source check verified all 21 exact publisher files and 221 total
operation and state section checks. CI retains the JSON report as
phase0-contract-evidence. Publisher files and raw traffic stay outside the
source archive.
