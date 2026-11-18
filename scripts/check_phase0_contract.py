"""Check Phase 0 planning contracts; never authorize a live directory transition."""

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from check_design import BASELINE_IDS, GLOBAL_ID, GLOBAL_SOURCES

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "lab/phase0-contract.json"
KINDS = {"schema", "credential_keys", "domain_restore", "functional_level", "storage", "gpo"}
RECOVERY = {
    "schema": {"exclusive_authority", "version_checkpoint", "incompatible_writes_stopped"},
    "credential_keys": {"dual_read", "provider_loss_denies", "recover_before_retirement"},
    "domain_restore": {
        "coherent_backup",
        "isolated_start",
        "epoch_quarantine",
        "revocation_reconcile",
    },
    "functional_level": {
        "all_dc_inventory",
        "no_binary_downgrade",
        "unsupported_transition_denied",
    },
    "storage": {"identity_acl_comparison", "audit_cursor_mapping", "original_retained"},
    "gpo": {"directory_sysvol_versions", "incomplete_publication_hidden", "reconcile_or_revert"},
}
IMPACTS = {"security", "capacity", "formats", "protocols", "api"}
TRANSITIONS = {"create", "raise_domain", "raise_forest", "lower_domain", "lower_forest", "coexist"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(label)
    return value


def records(value: Any, label: str) -> list[dict[str, Any]]:
    require(isinstance(value, list), label)
    return [mapping(item, label) for item in value]


def words(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 4096


def string_set(value: Any) -> set[str]:
    require(
        isinstance(value, list) and all(words(v) for v in value) and len(value) == len(set(value)),
        "Expected distinct nonempty strings",
    )
    return set(value)


def utc(value: Any) -> dt.datetime:
    require(isinstance(value, str) and value.endswith("Z"), "Explicit UTC timestamp required")
    result = dt.datetime.fromisoformat(value[:-1] + "+00:00")
    require(result.tzinfo == dt.UTC, "Explicit UTC timestamp required")
    return result


def level_plan(operation: str, domain: str, forest: str) -> str:
    """Only a new 2016/2016 forest has a specified creation design; nothing executes."""
    require(operation in TRANSITIONS, "Unknown functional transition")
    if operation == "create" and domain == forest == "2016":
        return "design_only"
    return "unsupported"


def requirement_ids(root: Path) -> set[str]:
    paths = [root / "docs" / name for name in GLOBAL_SOURCES]
    paths.extend((root / "docs/phases").glob("phase-*.md"))
    return {
        identifier
        for path in paths
        for identifier in re.findall(
            rf"^\| (P\d{{2}}-\d{{2}}|{GLOBAL_ID}) \|", path.read_text(), re.M
        )
    }


def validate_change(change: dict[str, Any], known: set[str]) -> None:
    """Validate a review record's contents, not its truth, identity or runtime approval."""
    require(change.get("kind") in KINDS, "Unknown irreversible change kind")
    for field in (
        "id",
        "owner",
        "scope",
        "forward",
        "interrupted",
        "recovery",
        "production_impact",
    ):
        require(words(change.get(field)), f"Missing change field: {field}")
    ids = string_set(change.get("requirements"))
    require(
        bool(ids) and ids <= known and all(re.fullmatch(r"P\d{2}-\d{2}", v) for v in ids),
        "Known phase requirement IDs required",
    )
    impacts = mapping(change.get("impacts"), "All five impacts required")
    require(set(impacts) == IMPACTS, "All five impacts required")
    require(all(words(v) for v in impacts.values()), "Explain every impact, including none")
    require(
        string_set(change.get("recovery_controls")) == RECOVERY[change["kind"]],
        "Kind-specific recovery controls incomplete",
    )
    require(change.get("binary_revert_is_recovery") is False, "Binary revert is not data recovery")
    require(
        change.get("runtime_outcome") == "unrun", "Design records cannot claim runtime recovery"
    )
    invalidation = mapping(change.get("evidence_invalidation"), "Evidence invalidation required")
    require(
        string_set(invalidation.get("on_change"))
        == {"source", "profile", "schema", "key_class", "scope", "expected_result"},
        "Source/profile/schema/key/scope/assertion changes invalidate evidence",
    )
    require(words(invalidation.get("rerun")), "Affected rerun procedure required")
    review = mapping(change.get("review"), "Review disposition required")
    require(review.get("disposition") == "proposed", "Examples are proposed, not owner approvals")
    require(words(review.get("accountable_owner")), "Review owner required")


def validate_exception(exception: dict[str, Any], now: dt.datetime, known: set[str]) -> None:
    require(now.tzinfo == dt.UTC, "Exception clock must be UTC")
    for field in (
        "id",
        "owner",
        "operation",
        "client",
        "site",
        "scope",
        "reason",
        "control",
        "production_impact",
    ):
        require(words(exception.get(field)), f"Missing exception field: {field}")
    waived = string_set(exception.get("waived_requirements"))
    require(bool(waived) and not (waived & BASELINE_IDS), "Cannot waive first-production baseline")
    require(
        waived <= known and all(re.fullmatch(GLOBAL_ID, v) for v in waived),
        "Only known optional global IDs may be waived; phase gates cannot be bypassed",
    )
    start, end = utc(exception.get("activation")), utc(exception.get("expiry"))
    require(start <= now < end, "Exception inactive or expired; release blocked")
    review = mapping(exception.get("review"), "Exception review required")
    require(
        review.get("disposition") == "owner_reviewed" and words(review.get("evidence")),
        "Explicit recorded exception review required",
    )
    require(
        exception.get("changes_observed_outcomes") is False, "Exceptions cannot rewrite outcomes"
    )


def validate(
    contract: dict[str, Any], matrix: dict[str, Any], now: dt.datetime, known: set[str]
) -> None:
    require(
        type(contract.get("schema_version")) is int and contract["schema_version"] == 1,
        "Unknown contract schema",
    )
    require(contract.get("status") == "design_only", "No product qualification in this contract")
    profile = mapping(contract.get("functional_profile"), "Functional profile required")
    require(profile.get("domain") == profile.get("forest") == "2016", "Owner baseline is 2016/2016")
    require(
        matrix.get("functional_level", {}).get("domain") == profile["domain"], "Matrix domain drift"
    )
    require(
        matrix.get("functional_level", {}).get("forest") == profile["forest"], "Matrix forest drift"
    )
    require(profile.get("advertised_levels") == [], "Unqualified levels cannot be advertised")
    require(profile.get("host_os") == "linux", "Linux hosting required")
    require(
        string_set(profile.get("client_profiles"))
        == {p["id"] for p in matrix["profiles"] if p["role"] != "server"},
        "Windows/Linux/macOS clients must match the compatibility matrix",
    )
    require(
        profile.get("transitions")
        == {op: level_plan(op, "2016", "2016") for op in sorted(TRANSITIONS)},
        "Only fresh 2016/2016 creation design is specified; no raise/lower/coexist claim",
    )
    require(
        profile.get("reference_dc_os") == ["2016", "2019", "2022", "2025"],
        "Reference DC OS is distinct from functional level",
    )
    features = mapping(profile.get("incompatibilities"), "Feature incompatibilities required")
    require(
        set(features)
        == {
            "legacy_levels",
            "level_2025",
            "frs",
            "optional_features",
            "mixed_dc",
            "client_os",
            "rollback",
        }
        and all(words(v) for v in features.values()),
        "Review every incompatible/optional behavior",
    )
    references = records(contract.get("references"), "Reference pins required")
    require(
        len(references) == 2,
        "Two reviewed reference pins required",
    )
    require(len({r.get("url") for r in references}) == 2, "Distinct references required")
    for reference in references:
        require(words(reference.get("review")), "Reference review and conflicts required")
        require(
            bool(
                re.fullmatch(
                    r"https://github.com/MicrosoftDocs/windowsserverdocs/blob/[a-f0-9]{40}/WindowsServerDocs/identity/ad-ds/[a-z/-]+\.md",
                    reference.get("url", ""),
                )
            ),
            "Immutable reference URL required",
        )
    changes = records(contract.get("worked_changes"), "Worked transitions required")
    require(
        len(changes) == len(KINDS),
        "All six worked transitions required",
    )
    require({c.get("kind") for c in changes} == KINDS, "Duplicate or missing transition kind")
    require(len({c.get("id") for c in changes}) == len(changes), "Duplicate change ID")
    for change in changes:
        validate_change(change, known)
    exceptions = records(contract.get("active_exceptions"), "Explicit exception register required")
    require(len({e.get("id") for e in exceptions}) == len(exceptions), "Duplicate exception ID")
    for exception in exceptions:
        validate_exception(exception, now, known)


def check(root: Path, revision: str, now: dt.datetime) -> dict[str, Any]:
    require(bool(re.fullmatch(r"[a-f0-9]{40}", revision)), "Full source revision required")
    raw = (root / "lab/phase0-contract.json").read_bytes()
    matrix = (root / "lab/compatibility.json").read_bytes()
    validate(json.loads(raw), json.loads(matrix), now, requirement_ids(root))
    return {
        "requirements": ["P00-10", "P00-11"],
        "scope": (
            "Phase 0 design-contract validation; no runtime upgrade, restore or AD conformance"
        ),
        "source_revision": revision,
        "contract_sha256": hashlib.sha256(raw).hexdigest(),
        "matrix_sha256": hashlib.sha256(matrix).hexdigest(),
        "checked_at": now.isoformat(),
        "worked_transition_kinds": sorted(KINDS),
        "functional_profile": "2016-domain-2016-forest-linux-host",
        "advertised_levels": [],
        "runtime_recovery": "unrun",
        "owner_acceptance": "not_inferred",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.root, args.revision, dt.datetime.now(dt.UTC)), indent=2))
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        raise SystemExit(f"Phase 0 planning contract rejected: {error}") from error
