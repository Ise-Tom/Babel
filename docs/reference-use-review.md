# Protocol reference editions and use-rights review

Status: **pinned reference-use review; P00-16 remains in progress**. Exact public
reference editions are recorded in [the registry](../lab/specification-pins.json),
with publisher URLs, revision, raw byte size/SHA-256, inspection date and actual
rights-notice identity. The compatibility/evidence schema remains version 1; its
60 existing scenarios were rebound to the changed matrix and all remain unrun.
No existing product pass or owner acceptance was created.

The DFS-R protocol is **MS-FRS2**, not the former nonexistent `MS-DFSR` reference.
MS-DNSP describes DNS server management. The [P00-01 matrix](validation/p00-01.md)
keeps that administrative candidate separate from DNS query, SRV discovery,
dynamic update and GSS-TSIG wire mappings. It also uses MS-DTYP for
descriptor/SID/GUID rules and MS-SFU for constrained delegation.

| Document | Selected edition |
| --- | --- |
| MS-ADTS | v20260824 |
| MS-DRSR | v20251121 |
| MS-DTYP | v20231212 |
| MS-FRS2 | v20210407 |
| MS-DNSP | v20260928 |
| MS-GPOL | v20210625 |
| MS-KILE | v20260928 |
| MS-LSAD | v20250610 |
| MS-NRPC | v20260209 |
| MS-PAC | v20240610 |
| MS-SAMR | v20260309 |
| MS-SFU | v20260330 |
| MS-SMB2 | v20260714 |
| RFC 1035 | November 1987 |
| RFC 2136 | April 1997 |
| RFC 2696 | September 1999 |
| RFC 2782 | February 2000 |
| RFC 3244 | February 2002 |
| RFC 3645 | October 2003 |
| RFC 4120 | July 2005 |
| RFC 4511 | June 2006 |

These are selected editions, not an assertion that each is the newest publication
or proves compatibility with every patched Windows build. Two dated archive PDF
links returned a protected-document wrapper rather than readable protocol content.
They were not decrypted or treated as reviewed content. The publisher's publicly
offered, readable current MS-LSAD/MS-PAC PDFs were inspected instead and their
actual editions/digests are pinned. Where a publisher URL is mutable, a changed
byte digest fails revalidation and requires a new explicit review.

## Copyright, patents and fixtures are different approvals

The inspected Microsoft Open Specifications notice permits documentation copies
for developing described implementations, necessary portions in implementations/
documentation, and included schema/IDL/sample use under its stated conditions.
It also expressly says the documentation notice is **not a patent license** and
does not grant trademark rights. Do not relicense Microsoft's material as Babel
Apache-2.0 merely because it is publicly readable.

The publicly available [Open Specification Promise](https://learn.microsoft.com/en-us/openspecs/dev_center/ms-devcentlp/1c24c7c8-28b0-4ce1-a47d-95fe1ff504bc)
was inspected. Its scope/conditions depend on specifically covered specifications
and versions; coverage of these selected Windows protocol editions has **not**
been established here. It is not an automatic grant inferred from the PDF notice.
Patent/program/trademark and concrete downstream use review remain unresolved
parts of P00-16. This is a record of observed terms, not legal certification.

RFC 4511 and RFC 4120 reference the BCP 78/79 terms of their editions. The
older RFCs retain their as-published Internet Society notices or publication
status statements. The registry preserves each dated notice identity and digest
for reference use. Babel cites protocol sections and writes original test
expectations. Source archives contain only the reference metadata and citations.

The registry gives **no** permission to download, run or redistribute a Windows
or macOS image. Both image records have no path/digest/rights evidence and no
allowed uses. Unknown assets/purposes are denied. Mac hardware/virtualization and
vendor evaluation/subscription terms need their actual license/profile review.
No licensed image, third-party directory capture or vendor PDF is committed.

The original synthetic state examples have an explicit project-source path and
hash under the owner's existing project terms. This demonstrates source binding,
not automated proof of authorship. A new/changed external fixture requires its own
recorded rights before use; an unrelated asset cannot borrow that approval.

## Reproduce the reference and integrity checks

Required CI checks all matrix-to-registry revision/location bindings, every state
case's source sections, all threat/boundary owners, the synthetic-asset digest and
the denial of unprovided external assets. It emits a source/input-digest-bound
`state-security-contract.json` report inside `phase0-contract-evidence`.

For exact raw-byte and heading checks, acquire the public editions from the
registry into an owned cache, without adding them to the repository, then run:

```sh
python scripts/check_state_security.py --revision "$(git rev-parse HEAD)" \
  --document-cache /path/to/public-reference-cache
```

The optional check compares all 21 raw documents, the 153 operation headings and
the 58 existing state-case reference bindings. It uses `pdftotext` for the pinned
PDFs and rejects changed bytes, unreadable editions and mismatched locators.
Default CI validates committed metadata offline. Human review, runtime
conformance and copyright/patent/image rights have their own criteria.
