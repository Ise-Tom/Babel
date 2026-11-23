# Protocol reference editions and use-rights review

Status: **reference-use inventory and source archive reviewed; P00-16 remains
blocked**. The [registry](../lab/specification-pins.json) records each edition,
raw byte size/SHA-256, notice identity and use policy. The
[P00-16 review packet](validation/p00-16.md) records actual uses, packaging
evidence and the missing implementation, image and fixture rights.

The DFS-R protocol is **MS-FRS2**, not the former nonexistent `MS-DFSR` reference.
MS-DNSP describes DNS server management. The [P00-01 matrix](validation/p00-01.md)
keeps that administrative candidate separate from DNS query, SRV discovery,
dynamic update and GSS-TSIG wire mappings. It also uses MS-DTYP for
descriptor/SID/GUID rules and MS-SFU for constrained delegation.

## Pinned editions

| Document and publisher terms | Exact selected edition | Use policy |
| --- | --- | --- |
| [MS-ADTS](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-ADTS/%5bMS-ADTS%5d-260824.pdf) | v20260824 | Open Specifications notice |
| [MS-DNSP](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-DNSP/%5bMS-DNSP%5d-260928.pdf) | v20260928 | Open Specifications notice |
| [MS-DRSR](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-DRSR/%5bMS-DRSR%5d-251121.pdf) | v20251121 | Open Specifications notice |
| [MS-DTYP](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-DTYP/%5bMS-DTYP%5d-231212.pdf) | v20231212 | Open Specifications notice |
| [MS-FRS2](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-FRS2/%5bMS-FRS2%5d-210407.pdf) | v20210407 | Open Specifications notice |
| [MS-GPOL](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-GPOL/%5bMS-GPOL%5d-210625.pdf) | v20210625 | Open Specifications notice |
| [MS-KILE](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-KILE/%5bMS-KILE%5d-260928.pdf) | v20260928 | Open Specifications notice |
| [MS-LSAD](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-LSAD/%5bMS-LSAD%5d.pdf) | v20250610 | Open Specifications notice |
| [MS-NRPC](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-NRPC/%5bMS-NRPC%5d-260209.pdf) | v20260209 | Open Specifications notice |
| [MS-PAC](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-PAC/%5bMS-PAC%5d.pdf) | v20240610 | Open Specifications notice |
| [MS-SAMR](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-SAMR/%5bMS-SAMR%5d-260309.pdf) | v20260309 | Open Specifications notice |
| [MS-SFU](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-SFU/%5bMS-SFU%5d-260330.pdf) | v20260330 | Open Specifications notice |
| [MS-SMB2](https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/MS-SMB2/%5bMS-SMB2%5d-260714.pdf) | v20260714 | Open Specifications notice |
| [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.txt) | RFC1035-November-1987 | As-published status |
| [RFC 2136](https://www.rfc-editor.org/rfc/rfc2136.txt) | RFC2136-April-1997 | As-published status |
| [RFC 2696](https://www.rfc-editor.org/rfc/rfc2696.txt) | RFC2696-September-1999 | Internet Society notice |
| [RFC 2782](https://www.rfc-editor.org/rfc/rfc2782.txt) | RFC2782-February-2000 | Internet Society notice |
| [RFC 3244](https://www.rfc-editor.org/rfc/rfc3244.txt) | RFC3244-February-2002 | Internet Society notice |
| [RFC 3645](https://www.rfc-editor.org/rfc/rfc3645.txt) | RFC3645-October-2003 | Internet Society notice |
| [RFC 4120](https://www.rfc-editor.org/rfc/rfc4120.txt) | RFC4120-July-2005 | Dated BCP 78/79 notice |
| [RFC 4511](https://www.rfc-editor.org/rfc/rfc4511.txt) | RFC4511-June-2006 | Dated BCP 78/79 notice |

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

The publisher program and promise indexes are linked in the registry. The
recorded matches are candidates for exact implementation and distribution
review. Publisher documentation permissions, promise and program terms, and
trademark rights each have their own scope.
[Microsoft programs and map](https://learn.microsoft.com/en-us/openspecs/dev_center/ms-devcentlp/13571077-e344-4e6f-a477-369894979798) ·
[Open Specification Promise](https://learn.microsoft.com/en-us/openspecs/dev_center/ms-devcentlp/1c24c7c8-28b0-4ce1-a47d-95fe1ff504bc)

RFC 4511 and RFC 4120 reference the BCP 78/79 terms of their editions. The
older RFCs retain their as-published Internet Society notices or publication
status statements. The registry preserves each dated notice identity and digest
for reference use. Babel cites protocol sections and writes original test
expectations. Source archives contain only the reference metadata and citations.

The unprovided image, external fixture and capture records have empty allowed-use
lists. Exact assets and appropriate license/channel, hardware and VM conditions
are required before qualification. The registry records the existing digest-pinned
PostgreSQL CI pull separately from the lab's unselected reference VM images.
The [lab preflight rights review](validation/p00-05-p00-12.md#p00-16-dispositions-for-those-assets)
records publisher terms for the proposed uses and versions, the available Linux
checksums and the outstanding exact Windows VM entitlements and Apple host rights.

The registered project-owned fixtures and redacted reports have a source path, digest and
declared use under Babel's project terms. The source packager verifies these
against the tar members. Review separately identifies original authorship and the
rights for any proposed external material.

## Reproduce the reference and integrity checks

Required CI checks all matrix-to-registry revision/location bindings, every state
case's source sections, all threat/boundary owners, the fixture digests and the
denial of unprovided external assets. CI retains the state-security report and the
source archive's separate `source-rights-audit.json` in `phase0-contract-evidence`.

For exact raw-byte and heading checks, acquire the public editions from the
registry into an owned cache, without adding them to the repository, then run:

```sh
python scripts/check_state_security.py --revision "$(git rev-parse HEAD)" \
  --document-cache /path/to/public-reference-cache
```

The optional check compares all 21 raw documents, the 161 operation headings and
the 58 existing state-case reference bindings. It uses `pdftotext` for the pinned
PDFs and rejects changed bytes, unreadable editions and mismatched locators.
Default CI validates committed metadata offline. Human review, runtime
conformance and copyright/patent/image rights have their own criteria.
