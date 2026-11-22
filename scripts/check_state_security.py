"""Check Phase 0 state/security/reference contracts, never simulate AD conformance."""

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess  # nosec B404
from pathlib import Path
from typing import Any

from check_conformance import digest, indexed, references, require, text
from check_phase0_contract import requirement_ids

ROOT = Path(__file__).resolve().parents[1]
LOCAL_CASES = {
    "S-RENAME",
    "S-CROSS-DOMAIN-SID",
    "S-COLLISION",
    "S-SCHEMA",
    "S-ACL-ORDER",
    "S-INHERITANCE",
    "S-NESTED-GROUPS",
    "S-REVOKE-RACE",
    "S-DURABLE-ACK",
}
REPLICA_CASES = {
    "R-INDEPENDENT",
    "R-SCALAR",
    "R-GUID-ORDER",
    "R-VERSION-WRAP",
    "R-LINK-LIFETIME",
    "R-NAME-CONFLICT",
    "R-DELETE-MODIFY",
    "R-CURSOR-COMMIT",
    "R-RESTORE-EPOCH",
    "R-RETENTION",
    "R-RID-AUTHORITY",
}
BOUNDARIES = {
    "B-WIRE",
    "B-AUTHORITY",
    "B-STORE-KEYS",
    "B-REPLICATION",
    "B-WEB",
    "B-RECOVERY",
    "B-SUPPLY",
    "B-EXTERNAL",
    "B-FLEET",
    "B-SUPPORT-FILES",
    "B-EDR-RESPONSE",
}


def source_file(root: Path, name: Any) -> Path:
    require(isinstance(name, str), "Asset source path required")
    path = Path(name)
    require(
        bool(path.parts) and not path.is_absolute() and ".." not in path.parts,
        "Asset must stay in the repository",
    )
    target = root / path
    require(
        target.is_file()
        and target.resolve().is_relative_to(root.resolve())
        and not any(
            (root / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)
        ),
        "Existing regular asset without symlink ancestors required",
    )
    return target


def authorize_asset(root: Path, registry: dict[str, Any], identifier: str, purpose: str) -> None:
    """A distribution-planning check, not authentication or a license grant."""
    assets = indexed(registry.get("assets"), "assets")
    require(identifier in assets, "Unknown asset is denied")
    asset = assets[identifier]
    require(
        asset.get("kind") == "project_synthetic"
        and asset.get("rights") == "owner_selected_project_license"
        and text(asset.get("review_evidence")),
        "Unprovided external-image/capture rights block use/distribution",
    )
    require(purpose in asset.get("allowed_uses", []), "Asset purpose not approved")
    target = source_file(root, asset.get("path"))
    require(
        digest(asset.get("sha256"))
        and 0 < target.stat().st_size <= 8 * 1024 * 1024
        and hashlib.sha256(target.read_bytes()).hexdigest() == asset["sha256"],
        "Asset source digest changed; rights review must be rebound",
    )


def validate(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    state = json.loads((root / "lab/state-security-contract.json").read_text())
    registry = json.loads((root / "lab/specification-pins.json").read_text())
    matrix = json.loads((root / "lab/compatibility.json").read_text())
    require(
        type(state.get("schema_version")) is int
        and state["schema_version"] == 1
        and type(registry.get("schema_version")) is int
        and registry["schema_version"] == 1,
        "Unknown state/reference contract schema",
    )
    require(
        state.get("status") == "design_only" and state.get("format_status") == "not_frozen",
        "State design cannot claim fixed formats or runtime qualification",
    )
    require(
        state.get("production_assessment") == "not_performed", "No production assessment inferred"
    )
    require(
        state.get("source_documents") == "lab/specification-pins.json",
        "State references must bind the reviewed document registry",
    )
    require(
        registry.get("status") == "reference_review_only"
        and registry.get("default_asset_disposition") == "deny_without_explicit_rights",
        "Reference review is not a blanket distribution grant",
    )
    docs = indexed(registry.get("documents"), "documents")
    specs = indexed(matrix.get("specifications"), "matrix specifications")
    require(
        set(docs) == set(specs)
        and {"MS-ADTS", "MS-DRSR", "MS-DTYP", "MS-FRS2", "RFC4511"} <= set(docs),
        "All actual matrix documents must be pinned; DFS-R is MS-FRS2",
    )
    for id, doc in docs.items():
        require(
            text(doc.get("title")) and text(doc.get("reviewer")), "Document title/reviewer required"
        )
        dt.date.fromisoformat(doc.get("reviewed_on", ""))
        require(
            digest(doc.get("sha256"))
            and digest(doc.get("notice_sha256"))
            and type(doc.get("bytes")) is int
            and 0 < doc["bytes"] <= 32 * 1024 * 1024,
            "Bounded document/notice digests required",
        )
        require(
            doc.get("revision") == specs[id].get("revision") and text(doc.get("revision")),
            "Matrix/reference revision drift",
        )
        require(doc.get("landing") == specs[id].get("url"), "Matrix/reference location drift")
        if id.startswith("MS-"):
            require(
                bool(re.fullmatch(r"v\d{8}", doc["revision"])), "Exact Microsoft edition required"
            )
            require(
                doc.get("url", "").startswith(
                    "https://winprotocoldocs-bhdugrdyduf5h2e4.b02.azurefd.net/" + id + "/"
                )
                and doc["url"].endswith(".pdf"),
                "Reviewed publisher PDF required",
            )
            require(
                doc.get("copyright_notice") == "microsoft_open_specifications_notice",
                "Actual Microsoft copyright/patent notice required",
            )
        else:
            require(
                re.fullmatch(r"RFC[0-9]+", id) is not None
                and re.fullmatch(id + r"-[A-Za-z]+-[0-9]{4}", doc["revision"]) is not None
                and doc.get("url") == f"https://www.rfc-editor.org/rfc/{id.lower()}.txt"
                and doc.get("landing") == f"https://www.rfc-editor.org/info/{id.lower()}/"
                and re.fullmatch(
                    id.lower()
                    + r"_(publication_status|internet_society|bcp78)_"
                    + doc["revision"][-4:],
                    doc.get("copyright_notice", ""),
                )
                is not None,
                "Use the RFC's actual dated rights notice, not a retroactive license",
            )
        require(
            doc.get("document_use") == "implementation_reference_only"
            and doc.get("patent_coverage") == "not_established"
            and doc.get("image_fixture_rights") == "not_granted_by_document"
            and doc.get("redistribution_approval") is None,
            "Do not convert reference permission into patent/image/redistribution clearance",
        )
    cases = indexed(state.get("cases"), "state cases")
    require(LOCAL_CASES | REPLICA_CASES <= set(cases), "Original state exit cases incomplete")
    for id, case in cases.items():
        expected = "P00-02" if id.startswith("S-") else "P00-03"
        require(
            case.get("requirement") == expected and (id.startswith("S-") or id.startswith("R-")),
            "State case requirement mismatch",
        )
        for field in (
            "title",
            "owner",
            "initial_state",
            "operation",
            "expected",
            "denied_or_interrupted",
        ):
            require(text(case.get(field)), "Complete state case review material required")
        require(
            case.get("runtime_outcome") == "unrun"
            and case.get("review") == "specified_for_owner_review",
            "Design cases cannot become passing product observations",
        )
        refs = case.get("references")
        if not isinstance(refs, list) or not refs:
            raise ValueError("Pinned section references required")
        for ref in refs:
            require(
                ref.get("document") in docs
                and text(ref.get("title"))
                and bool(re.fullmatch(r"\d+(?:\.\d+)*", ref.get("section", "")))
                and text(ref.get("heading"))
                and digest(ref.get("heading_sha256"))
                and hashlib.sha256(ref["heading"].encode()).hexdigest() == ref["heading_sha256"],
                "Source section/heading binding invalid",
            )
    threats = set(
        re.findall(r"^\| (T-\d{2}) \|", (root / "docs/threat-model.md").read_text(), re.M)
    )
    require(bool(threats), "Canonical threat register required")
    boundaries = indexed(state.get("boundaries"), "boundaries")
    require(BOUNDARIES <= set(boundaries), "Trust boundary missing")
    covered = set()
    known = requirement_ids(root)
    for boundary in boundaries.values():
        for field in ("title", "accountable_owner", "required_denial_or_fault", "residual_risk"):
            require(text(boundary.get(field)), "Boundary owner/misuse/residual review required")
        for field in ("assets", "misuse_cases"):
            require(
                isinstance(boundary.get(field), list)
                and bool(boundary[field])
                and all(text(v) for v in boundary[field]),
                "Boundary assets/misuse required",
            )
        references(boundary.get("threats"), threats, "threats")
        references(boundary.get("implementation_gates"), known, "implementation gates")
        covered.update(boundary["threats"])
        require(
            boundary.get("review_model") == "solo_owner_and_CI"
            and boundary.get("runtime_outcome") == "unrun"
            and boundary.get("independent_assessment") == "not_performed",
            "Solo design review cannot claim independent/runtime qualification",
        )
    require(covered == threats, "Every threat needs accountable boundary coverage")
    assets = indexed(registry.get("assets"), "assets")
    require(
        {"state-design-examples", "windows-reference-image", "macos-reference-image"}
        <= set(assets),
        "Missing synthetic/external asset dispositions",
    )
    for id, asset in assets.items():
        if asset.get("kind") == "project_synthetic":
            authorize_asset(root, registry, id, "source_distribution")
        else:
            require(
                asset.get("rights") == "unprovided"
                and asset.get("allowed_uses") == []
                and asset.get("path") is None
                and asset.get("sha256") is None
                and asset.get("review_evidence") is None,
                "Unacquired external assets cannot be approved",
            )
    return state, registry


def matches_heading(source: str, section: str, heading: str) -> bool:
    if not section[0].isdigit():
        # RFC 2782 uses unnumbered headings.
        return re.search(r"^" + re.escape(heading) + r"$", source, re.M) is not None
    match = re.search(r"^\f?" + re.escape(section) + r"(?:\.| -)?[ \t]+([^\n]+)", source, re.M)
    return match is not None and " ".join(match.group(1).split()) == heading


def verify_cache(cache: Path, state: dict[str, Any], registry: dict[str, Any]) -> int:
    """Reproduce raw-byte and actual heading checks with caller-supplied public documents."""
    texts: dict[str, str] = {}
    for doc in registry["documents"]:
        id = doc["id"]
        candidates = [cache / (id + suffix) for suffix in (".pdf", "-current.pdf", ".txt")]
        matches = [
            p
            for p in candidates
            if p.is_file()
            and not p.is_symlink()
            and p.stat().st_size == doc["bytes"]
            and hashlib.sha256(p.read_bytes()).hexdigest() == doc["sha256"]
        ]
        require(len(matches) == 1, "Exact reviewed document bytes unavailable or changed: " + id)
        path = matches[0]
        if path.suffix == ".pdf":
            # Fixed text extractor and exact pinned input bytes.
            result = subprocess.run(  # nosec B603, B607
                ["pdftotext", "-layout", str(path.resolve()), "-"],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            texts[id] = result.stdout
            require(
                "[" + id + "]:" in result.stdout and doc["revision"] in result.stdout,
                "Readable matching document edition required",
            )
        else:
            texts[id] = path.read_text(encoding="utf-8")
    count = 0
    for case in state["cases"]:
        for ref in case["references"]:
            require(
                matches_heading(texts[ref["document"]], ref["section"], ref["heading"]),
                "Reviewed heading no longer matches document bytes",
            )
            count += 1
    for doc in registry["documents"]:
        for section, heading in doc.get("sections", {}).items():
            require(
                matches_heading(texts[doc["id"]], section, heading),
                f"{doc['id']}#{section}: Pinned operation heading does not match document bytes",
            )
            count += 1
    return count


def check(root: Path, revision: str, cache: Path | None = None) -> dict[str, Any]:
    require(digest(revision, 40), "Full source revision required")
    state, registry = validate(root)
    result = {
        "requirements": ["P00-02", "P00-03", "P00-07"],
        "source_revision": revision,
        "scope": "Phase 0 design review/integrity; no native AD or legal clearance",
        "input_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "lab/state-security-contract.json",
                "lab/specification-pins.json",
                "lab/compatibility.json",
                "docs/threat-model.md",
                "docs/adr/0005-directory-and-replication-invariants.md",
            )
        },
        "state_cases": len(state["cases"]),
        "boundaries": len(state["boundaries"]),
        "document_pins": len(registry["documents"]),
        "native_runtime_outcomes": "unrun",
        "rights_disposition": "reference_use_only; patent/image/fixture clearance not granted",
        "independent_assessment": "not_performed",
        "owner_acceptance": "not_inferred",
    }
    if cache is not None:
        result["verified_document_section_bindings"] = verify_cache(cache, state, registry)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--document-cache", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.root, args.revision, args.document_cache), indent=2))
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        AttributeError,
        subprocess.SubprocessError,
    ) as error:
        raise SystemExit(f"Phase 0 state/security contract rejected: {error}") from error
