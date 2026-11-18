# Initial domain and forest functional-level profile

Status: **Phase 0 design complete; P00-11 owner validation pending**. This specifies
Babel's initial compatibility contract. No native DC currently implements or
advertises a functional level. The server remains Linux-hosted; Windows, Linux
and macOS devices remain explicit clients. Full identity, password and GPO scope
is unchanged.

## Selected levels and controller versus client compatibility

The owner selected **2016 domain / 2016 forest** on 18 November 2026. A domain
cannot have a level below its forest. The first native creation design is a new,
isolated forest with both levels set together; subsequent domains must preserve
the same profile. Levels from 2000 through 2012 R2 and the 2025 level are outside
the initial creation profile. There are no separate 2019 or 2022 functional levels.

Microsoft's pinned current level table allows Windows Server 2016, 2019, 2022 and
2025 **reference DC operating systems** at 2016 levels. This does not select a
Windows server runtime for Babel, qualify any exact build, or prove mixed
Windows/Babel DC replication. Windows Server 2025 as a *member/client OS* likewise
does not require a 2025 functional level. The exact-build matrix and licensed
reference hosts remain P00-12/P00-05 obligations.

Workstation and member-server operating systems do not define the domain level.
Keep Windows 11 Pro/Enterprise and Server 2022/2025 clients, Ubuntu/Debian with
SSSD/Kerberos, and macOS on Intel/Apple Silicon from the
[compatibility matrix](../lab/compatibility.json). Linux/macOS directory, login,
password and policy integration needs its own qualified behavior; Windows GPO is
not an assertion that every non-Windows client implements Windows policy engines.
Cross-platform endpoint policy/patch/remote/EDR agents retain their roadmap scope.

## Behavior required by the selected profile

| Area | Contract and incompatible behavior |
| --- | --- |
| Inherited AD behavior | All default capabilities inherited by the 2016 level remain in scope. Naming/schema, linked-value replication, Kerberos/PAC, access checks, password policies, trust, GPO and recovery need their full operation/client gates; a level label cannot stand in for them |
| 2016-specific behavior | Inventory and qualify PKINIT freshness, smart-card/password-secret policy and applicable domain-joined-device authentication restrictions. PAM/MIM integration is an explicit optional-feature/provider boundary, not an automatically enabled claim |
| Earlier optional/security features | Recycle state, Protected Users, authentication policies/silos and other optional features require declared enablement, prerequisites and operation evidence. Do not silently enable unsupported features or downgrade authentication |
| SYSVOL | No FRS fallback. Complete first-production policy consistency and replication remain required. Windows-DC coexistence additionally requires its qualified DFSR profile; simple file copying does not establish interoperability |
| 2025 level | Outside the selected level profile, including the optional 32-KiB AD database-page feature. PostgreSQL page size has no equivalence to that AD feature |
| Mixed DCs and migration | No implementation of mixed Windows/Babel DCs, legacy-forest adoption, raise/lower or in-place level migration is implied. Their own requirements remain unrun; the initial fresh-forest design does not waive them |
| Security policy versus compatibility | Refusing unsafe legacy cryptography must have explicit supported/unsupported client results. Do not silently substitute weaker crypto to make an advertised level appear compatible |

The complete wire-operation decomposition remains P00-01 and the native semantics
remain their implementation phases. P00-11 fixes which level/transition contract
they must qualify; it does not accept those implementations.

## Transition and failure review

| Requested action / observation | Required disposition |
| --- | --- |
| Fresh isolated forest, domain=2016 and forest=2016 | Defined creation design only. No executable deployment is authorized by the planning checker; product readiness remains unrun |
| Additional domain | Must retain the selected 2016/2016 profile and pass its own native multi-domain gates; not implemented by this plan |
| Domain below forest, mismatched levels, unknown/2019/2022 levels | Refuse before changing level/schema state; no partial advertised update |
| Raise a domain or forest to 2025 | Unsupported initial transition. Review exact new features, all eligible DCs/domains, recovery and rerun affected evidence before extending the profile |
| Lower either level or roll back by changing a value/binary | Unsupported. Microsoft has conditional rollback exceptions for certain earlier-level combinations; Babel implements none. At the selected 2016/2016 pair, lowering only a domain would also violate the forest floor |
| Add an older/incompatible DC or unqualified mixed Windows DC | Refuse that topology; do not assume reference OS support proves Babel replica interoperability |
| Crash after staging a future transition | Retain explicit incomplete state; stop incompatible writes, recover a coherent checkpoint/backup, reconcile keys/SYSVOL/replica epoch, verify before service. A binary rollback is insufficient |
| Missing exact builds, unrun tests or failed feature evidence | Keep the compatibility result unqualified and block that claim; do not fill advertised levels from the intended profile |

The [machine-readable contract](../lab/phase0-contract.json) deliberately has
`advertised_levels: []`. The current read-only LDAP lab is unchanged and does not
publish `domainFunctionality`/`forestFunctionality` as implemented levels. Native
RootDSE level/optional-feature publication must later be bound to the actual
qualified controller state, not copied from this design file.

## Reference review and evidence

Reviewed 18 November 2026, using immutable MicrosoftDocs source revisions:

- [Current functional-level table and features, revision 6dd2bb8](https://github.com/MicrosoftDocs/windowsserverdocs/blob/6dd2bb888a637412b091d421dab23ed1e09d52e7/WindowsServerDocs/identity/ad-ds/active-directory-functional-levels.md).
- [Upgrade and conditional rollback discussion, revision b551232](https://github.com/MicrosoftDocs/windowsserverdocs/blob/b55123260d473dccfec52516efbec3c19eb0bb40/WindowsServerDocs/identity/ad-ds/deploy/upgrade-domain-controllers.md).

The upgrade article still says no functional levels were added after 2016; this
conflicts with the current functional-level table's explicit 2025 level. Use the
current table for level/OS availability and only the applicable upgrade/rollback
discussion from the second source. Do not perpetuate that stale claim. These are
reviewed design references; exact MS-ADTS/MS-DRSR sections and reference fixtures
remain their protocol/rights gates. No article or licensed VM is redistributed.

Required CI cross-checks the profile against the existing matrix, rejects dropped
non-Windows clients, changed/advertised levels, unsupported transitions, missing
feature/failure review and mutable reference URLs. Source/digest-bound CI evidence
is a **design-contract** result. All 60 product conformance scenarios remain unrun.
See the [P00-11 criterion packet](validation/p00-11.md).
