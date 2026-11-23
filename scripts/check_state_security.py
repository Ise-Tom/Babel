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


ASSET_LIMIT = 8 * 1024 * 1024


def asset_for_use(asset: dict[str, Any], purpose: str) -> None:
    require(
        asset.get("kind") == "project_synthetic"
        and asset.get("rights") == "owner_selected_project_license"
        and text(asset.get("review_evidence")),
        "Unprovided external-image/capture rights block use/distribution",
    )
    uses = asset.get("allowed_uses")
    require(
        isinstance(uses, list)
        and all(use in ("source_distribution", "unit_testing") for use in uses)
        and purpose in uses,
        "Asset purpose not approved",
    )


def verify_asset_bytes(asset: dict[str, Any], raw: bytes) -> None:
    require(
        digest(asset.get("sha256"))
        and 0 < len(raw) <= ASSET_LIMIT
        and hashlib.sha256(raw).hexdigest() == asset["sha256"],
        "Asset source digest changed; rights review must be rebound",
    )


def authorize_asset(root: Path, registry: dict[str, Any], identifier: str, purpose: str) -> None:
    """Check the declared use against the reviewed source bytes."""
    assets = indexed(registry.get("assets"), "assets")
    require(identifier in assets, "Unknown asset is denied")
    asset = assets[identifier]
    asset_for_use(asset, purpose)
    target = source_file(root, asset.get("path"))
    require(target.stat().st_size <= ASSET_LIMIT, "Asset exceeds review size limit")
    verify_asset_bytes(asset, target.read_bytes())


def pending_external_asset(asset: dict[str, Any]) -> None:
    terms = asset.get("publisher_terms")
    require(
        asset.get("rights") == "unprovided"
        and asset.get("allowed_uses") == []
        and all(
            key in asset and asset[key] is None
            for key in ("path", "sha256", "review_evidence", "selected_version")
        )
        and text(asset.get("candidate"))
        and text(asset.get("missing_evidence"))
        and isinstance(terms, list)
        and (bool(terms) or asset.get("kind") == "external_capture")
        and all(text(term) and term.startswith("https://") for term in terms),
        "Unacquired external assets cannot be approved without exact rights evidence",
    )


def verify_use_inventory(root: Path, registry: dict[str, Any]) -> None:
    review = registry.get("use_review", {})
    dt.date.fromisoformat(review.get("reviewed_on", ""))
    terms = review.get("publisher_terms")
    require(
        review.get("full_rights_disposition") == "unresolved"
        and text(review.get("scope"))
        and isinstance(terms, dict)
        and bool(terms)
        and all(text(url) and url.startswith("https://") for url in terms.values()),
        "Review requires exact publisher terms and unresolved disposition",
    )
    program = review.get("microsoft_program_index", {})
    require(
        text(program.get("data_url"))
        and program["data_url"].startswith("https://")
        and digest(program.get("sha256"))
        and type(program.get("bytes")) is int
        and program["bytes"] > 0,
        "Microsoft program observations require the publisher index pin",
    )
    policies = indexed(review.get("document_policies"), "document use policies")
    for name, policy in policies.items():
        require(
            policy.get("cite") == "bibliographic_metadata"
            and policy.get("develop")
            == (
                "private_reference_under_edition_notice"
                if name == "microsoft-notice"
                else "independent_reference_only"
            )
            and policy.get("redistribute") == "excluded"
            and text(policy.get("conditions")),
            "Reference policies retain scope and exclude redistribution",
        )
        references(policy.get("terms"), set(terms), "publisher terms")

    for doc in registry["documents"]:
        notice = doc["copyright_notice"]
        expected = (
            "microsoft-notice"
            if doc["id"].startswith("MS-")
            else "rfc-publication-status"
            if "_publication_status_" in notice
            else "rfc-internet-society"
            if "_internet_society_" in notice
            else "rfc-bcp78"
        )
        require(
            doc.get("use_policy") == expected and expected in policies,
            "Every pinned edition must bind its applicable use policy",
        )
        observations = doc.get("patent_index_observations", {})
        rows = observations.get("program_map_rows")
        require(
            type(observations.get("osp_identifier_listed")) is bool
            and type(observations.get("community_promise_identifier_listed")) is bool
            and isinstance(rows, list)
            and (bool(rows) or not doc["id"].startswith("MS-")),
            "Record publisher index observations separately from patent clearance",
        )
        for row in rows:
            require(
                type(row.get("row_id")) is int
                and row["row_id"] > 0
                and type(row.get("patent_numbers_listed")) is bool
                and type(row.get("patent_applications_listed")) is bool,
                "Publisher index row requires observed metadata",
            )
            programs = row.get("programs")
            require(
                isinstance(programs, list) and bool(programs) and all(text(p) for p in programs),
                "Publisher index row requires observed programs",
            )

    images = indexed(review.get("pulled_ci_images"), "pulled CI images")
    for image in images.values():
        manifest = source_file(root, image.get("manifest"))
        publisher = image.get("publisher_terms")
        require(
            text(image.get("image"))
            and re.fullmatch(r"[^\s]+@sha256:[a-f0-9]{64}", image["image"]) is not None
            and f"FROM {image['image']}" in manifest.read_text(encoding="utf-8").splitlines()
            and image.get("use") == "isolated_ci_pull_and_run"
            and image.get("redistribute") == "excluded"
            and isinstance(publisher, list)
            and bool(publisher)
            and all(text(url) and url.startswith("https://") for url in publisher)
            and text(image.get("conditions")),
            "CI image use requires a pinned manifest, publisher terms and no bundled layers",
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
        {
            "state-design-examples",
            "windows-reference-image",
            "windows-client-image",
            "macos-reference-image",
            "linux-lab-image",
            "vendor-reference-fixture",
            "external-reference-capture",
        }
        <= set(assets),
        "Missing synthetic/external asset dispositions",
    )
    for id, asset in assets.items():
        if asset.get("kind") == "project_synthetic":
            require(
                asset.get("publisher_terms") == ["LICENSE", "CONTRIBUTING.md"],
                "Project fixtures require the Babel contribution and license terms",
            )
            authorize_asset(root, registry, id, "source_distribution")
        else:
            pending_external_asset(asset)
    verify_use_inventory(root, registry)
    return state, registry


def matches_heading(source: str, section: str, heading: str) -> bool:
    if not section[0].isdigit():
        # RFC 2782 uses unnumbered headings.
        return re.search(r"^" + re.escape(heading) + r"$", source, re.M) is not None
    words = r"(?:[ \t]+|\n[ \t]+)".join(re.escape(word) for word in heading.split())
    pattern = r"^\f?" + re.escape(section) + r"(?:\.| -)?[ \t]+" + words + r"[ \t]*$"
    return re.search(pattern, source, re.M) is not None


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
            match = re.search(
                r"^(?:\f)?" + re.escape(ref["section"]) + r"\s+([^\n]+)",
                texts[ref["document"]],
                re.M,
            )
            require(
                match is not None and " ".join(match.group(1).split()) == ref["heading"],
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
