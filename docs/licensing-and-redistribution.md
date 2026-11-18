# Project licensing, contributions and redistribution register

Status: **full P00-06 Phase 0 criterion packet complete; owner validation pending**.
The project owner explicitly selected **Apache-2.0 + DCO** on 17 November 2026.
The full [LICENSE](../LICENSE), [NOTICE](../NOTICE), verbatim [DCO 1.1](../DCO) and
[contribution terms](../CONTRIBUTING.md) are applied. This records the actual
choice and obligations; it does not certify third-party copyright ownership.

## Contribution terms

External contributions use Apache-2.0 with DCO 1.1, without copyright assignment
or a separate CLA. Contributors sign off their own commits after reviewing their
right to contribute and third-party/AI-assisted material. Never fabricate a
historical sign-off, another person's certification or a human DCO certification
by a bot. Existing owner-directed work follows the owner's explicit license
selection; DCO review remains the maintainer's merge responsibility. There is no
claimed automated DCO or legal-certification check.

## Reviewed terms and distribution obligations

| Terms in the selected graphs | Retained obligations / boundary |
| --- | --- |
| Apache-2.0 | Give recipients the license, retain applicable attribution/NOTICE, identify modifications where required; patent/trademark terms remain those of the actual license |
| MIT | Retain copyright and permission notice in copies/substantial portions |
| ISC | Retain copyright and permission/disclaimer text |
| BSD-3-Clause | Retain copyright, conditions/disclaimer and non-endorsement restriction |
| Unicode-3.0 | Retain applicable copyright, permission/disclaimer and holder-name restrictions for selected identifier/normalization/property data |
| NCSA | Retain copyright/permission/disclaimer; selected libFuzzer is development tooling, not parser runtime code |
| System shared libraries | ELF records libc/libgcc/loader names separately from Cargo crates. GNU/Linux artifacts retain actual glibc/libgcc package copyright catalogs and LGPL-2.1/LGPL-3/GPL-2/GPL-3 texts, alongside the Rust catalog’s GCC Runtime Library Exception. Shared libraries remain replaceable and are not copied into the archive. Broader installers/containers must review their actual OS contents |
| Rust library bundle | Retain actual `COPYRIGHT-library.html` and its referenced license texts. The catalog can list components not linked into Babel; it is not a binary-link inventory |

Exact package versions, selected SPDX expressions and actual nested notice files
are recorded by the locked graph audits, SBOM and notice manifests. Rustls/ring/
WebPKI/subtle and the PostgreSQL driver's Unicode-bearing dependencies have their
actual selected terms retained, including nested upstream notices. OR expressions
permit a selected offered license; AND expressions require all applicable terms.
No other license family is silently accepted by `deny.toml`. Changes need a fresh
rights/notice review; a current green advisory/license scan is time-bound evidence.

## Current distribution surfaces and enforced checks

| Surface | Concrete handling |
| --- | --- |
| Source archive | `git archive` includes the project's full LICENSE/NOTICE/DCO and contributor terms, without vendoring Cargo/npm/pip caches. Downstream dependencies retain their upstream terms |
| Internal native protocol archive | Actual project, selected normal/runtime dependency notices Rust catalog/license texts and actual GNU system-runtime terms accompany binaries; extraction verifies a manifest digest captured before archiving, all notice bytes, required files and package/file accounting |
| Driver qualification artifact | Actual selected driver dependency notices, Rust catalog and GNU system-runtime terms, with file hashes and strict complete-tree verification; this is not a published product library/package |
| Public/standalone dashboard | Full project license/notice and actual esbuild build-tool license text are safely retained inside an inert HTML template. Bundled inputs must remain project TypeScript sources; adding a runtime npm/vendor input fails until its redistribution policy is reviewed and implemented |
| CI tooling | Hash/version-locked Python/npm/Rust tooling has dependency inventories/audits. Installing tools in ephemeral CI does not mean they are bundled in the dashboard/native artifact; distributing an installer/container must assess its own complete contents |

The [notice collector/verifier](../scripts/collect_native_notices.py) now refuses
missing required project/Rust/system-runtime files, omitted/unlisted files, symlinked roots/trees/
manifests, missing/duplicate/unaccounted package inventories and mismatched bytes.
The trusted pre-archive manifest digest also detects a rewritten manifest even
when an attacker changes both a notice and its self-reported hash. That CI digest
is not a public release signature or independent copyright determination.

The [dashboard builder](../dashboard/build.mjs) escapes notice text and substitutes
all template fields in one pass. User-authored build-placeholder text stays literal
instead of consuming a later replacement. Tests cover retained full license texts,
inert escaping, unknown bundled inputs and placeholder/data integrity. CSP and
standalone Pages artifact restrictions remain enforced.

## Remaining separate rights and release gates

P00-16 owns exact protocol-document revisions/use terms, licensed Windows/macOS
images and reference-fixture rights. No external specification text or licensed
image is imported by this work. Unclear image/fixture rights still block their
distribution; choosing Apache-2.0 cannot license someone else's material.

Before any broader binary/container/installer/SDK/agent distribution, review the
actual target/features, linked and bundled components, upstream terms and notice
completeness. Product release, signing/provenance and production qualification
retain their own gates. This completes the original Phase 0 **project-license,
contribution and obligation-recording** requirement, not future product clearance.
