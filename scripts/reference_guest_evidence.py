"""Prepare private guest bundles and assess six guest reports against a lab journal.

Guest output is operator-supplied evidence, never an owner acceptance. A complete
cycle record requires all six reports, prior host discovery and clean teardown.
"""

import argparse
import hashlib
import json
import math
import re
import shutil
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from run_reference_lab import save

ROOT = Path(__file__).resolve().parents[1]
HEX = re.compile(r"[a-f0-9]{64}\Z")
STEPS = (
    "updates_verified",
    "updates_installed",
    "network_configured",
    "dns_configured",
    "time_configured",
    "platform_observed",
    "dns_probe",
    "time_probe",
    "egress_probe",
)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def plan_digest(plan: dict[str, Any]) -> str:
    return digest(json.dumps(plan, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load_journal(path: Path) -> dict[str, Any]:
    record: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    if record.get("schema_version") != 1 or len(record.get("plan", {}).get("guests", [])) != 6:
        raise ValueError("Expected a six-guest runner journal")
    return record


def approved_update(record: dict[str, Any], root: Path, guest_id: str) -> tuple[Path, str]:
    raw = record.get("path")
    sha = record.get("sha256")
    rights = record.get("rights_record")
    url = record.get("publisher_terms")
    if not isinstance(raw, str) or not isinstance(sha, str) or not HEX.fullmatch(sha):
        raise ValueError(f"{guest_id}: update path/digest missing")
    relative = Path(raw)
    if relative.is_absolute() or relative.drive or raw.startswith(("\\", "//")):
        raise ValueError(f"{guest_id}: update must be a relative local file")
    if relative.suffix.lower() not in {".msu", ".cab", ".deb"}:
        raise ValueError(f"{guest_id}: unsupported update type")
    if (
        record.get("approved_use") != "private_isolated_install_and_run"
        or not isinstance(rights, str)
        or not rights.strip()
        or not isinstance(url, str)
        or urlsplit(url).scheme != "https"
        or not urlsplit(url).hostname
    ):
        raise ValueError(f"{guest_id}: update rights not approved")
    expiry = record.get("expires_on")
    if expiry is not None and date.fromisoformat(expiry) <= datetime.now(UTC).date():
        raise ValueError(f"{guest_id}: update rights expired")
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root) or not path.is_file():
        raise ValueError(f"{guest_id}: update outside private manifest directory")
    with path.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != sha:
            raise ValueError(f"{guest_id}: staged update digest mismatch")
    return path.resolve(), sha


def prepare(journal: Path, staging_manifest: Path, output_root: Path) -> dict[str, Any]:
    record = load_journal(journal)
    if record.get("phase") != "provisioned" or "media_pins" not in record:
        raise ValueError("Runner must have provisioned and pinned all six guest media")
    if output_root.resolve().is_relative_to(ROOT) or output_root.exists():
        raise ValueError("Choose a new private output directory outside the repository")
    staging: dict[str, Any] = json.loads(staging_manifest.read_text(encoding="utf-8"))
    entries = staging.get("guests")
    guests = record["plan"]["guests"]
    if (
        staging.get("schema_version") != 1
        or not isinstance(entries, dict)
        or set(entries) != {guest["id"] for guest in guests}
    ):
        raise ValueError("Staging manifest must name exactly the six runner guests")
    root = staging_manifest.parent.resolve()
    prepared = []
    expectations = {}
    for guest in guests:
        guest_id = guest["id"]
        entry = entries[guest_id]
        interface = entry.get("interface")
        build = entry.get("expected_build")
        packages = entry.get("expected_packages")
        updates = entry.get("updates")
        if (
            not isinstance(interface, str)
            or not re.fullmatch(r"[A-Za-z0-9 ._-]{1,64}", interface)
            or not isinstance(build, str)
            or not build.strip()
            or not isinstance(packages, dict)
            or not packages
            or any(
                not isinstance(k, str) or not isinstance(v, str) or not k or not v
                for k, v in packages.items()
            )
            or not isinstance(updates, list)
        ):
            raise ValueError(f"{guest_id}: interface/build/package/update pins required")
        paths = [approved_update(item, root, guest_id) for item in updates]
        extensions = (
            {".msu", ".cab"}
            if guest["role"] in {"windows_reference_dc", "windows_client"}
            else {".deb"}
        )
        if any(path.suffix.lower() not in extensions for path, _ in paths):
            raise ValueError(f"{guest_id}: staged update does not match guest OS")
        script = Path(__file__).with_name(
            "reference_guest_windows.ps1"
            if guest["role"] in {"windows_reference_dc", "windows_client"}
            else "reference_guest_linux.py"
        )
        expectations[guest_id] = {
            "build": build,
            "packages": packages,
            "update_sha256": [sha for _, sha in paths],
            "script_sha256": digest(script.read_bytes()),
        }
        prepared.append((guest, interface, paths, script))
    output_root.mkdir(parents=True)
    for guest, interface, paths, script in prepared:
        directory = output_root / guest["id"]
        directory.mkdir()
        shutil.copyfile(script, directory / script.name)
        copied = []
        for index, (source, sha) in enumerate(paths, start=1):
            filename = f"update-{index}{source.suffix.lower()}"
            target = directory / filename
            shutil.copyfile(source, target)
            with target.open("rb") as content:
                if hashlib.file_digest(content, "sha256").hexdigest() != sha:
                    raise ValueError("Copied update bytes changed")
            copied.append({"filename": filename, "sha256": sha})
        config = {
            "schema_version": 1,
            "run_id": record["plan"]["run_id"],
            "plan_sha256": plan_digest(record["plan"]),
            "guest_id": guest["id"],
            "vm": guest["vm"],
            "role": guest["role"],
            "interface": interface,
            "address": guest["address"],
            "prefix_length": guest["prefix_length"],
            "dns_server": guest["dns_server"],
            "dns_suffix": guest["dns_suffix"],
            "time_server": guest["time_server"],
            "default_gateway": None,
            "expected_build": expectations[guest["id"]]["build"],
            "expected_packages": expectations[guest["id"]]["packages"],
            "script_sha256": expectations[guest["id"]]["script_sha256"],
            "updates": copied,
        }
        save(directory / "config.json", config)
    record["guest_expectations"] = expectations
    save(journal, record)
    return {
        "run_id": record["plan"]["run_id"],
        "plan_sha256": plan_digest(record["plan"]),
        "bundles": [x[0]["id"] for x in prepared],
        "status": "prepared_private_guest_bundles",
    }


def assess(journal: Path, reports_root: Path) -> dict[str, Any]:
    record = load_journal(journal)
    plan = record["plan"]
    pin = plan_digest(plan)
    blockers = []
    if record.get("phase") != "torn_down" or any(
        x.get("state") != "deleted" for x in record["resources"]
    ):
        blockers.append("teardown_incomplete")
    if record.get("host_discovery", {}).get("status") != "passed":
        blockers.append("host_discovery_missing")
    expectations = record.get("guest_expectations")
    if not isinstance(expectations, dict):
        blockers.append("guest_bundle_preparation_missing")
        expectations = {}
    guests = {}
    for guest in plan["guests"]:
        guest_id = guest["id"]
        path = reports_root / guest_id / "report.json"
        if (
            path.is_symlink()
            or not path.resolve().is_relative_to(reports_root.resolve())
            or not path.is_file()
        ):
            blockers.append(f"{guest_id}:report_missing")
            continue
        raw = path.read_bytes()
        if len(raw) > 1024 * 1024:
            blockers.append(f"{guest_id}:report_oversized")
            continue
        try:
            report = json.loads(raw)
        except (ValueError, UnicodeError):
            blockers.append(f"{guest_id}:report_invalid")
            continue
        if not isinstance(report, dict):
            blockers.append(f"{guest_id}:report_invalid")
            continue
        reasons = []
        for field, expected in (
            ("schema_version", 1),
            ("run_id", plan["run_id"]),
            ("plan_sha256", pin),
            ("guest_id", guest_id),
            ("vm", guest["vm"]),
            ("status", "complete"),
            ("script_sha256", expectations.get(guest_id, {}).get("script_sha256")),
        ):
            if report.get(field) != expected:
                reasons.append(f"{field}_mismatch")
        steps = report.get("steps")
        if not isinstance(steps, dict) or any(steps.get(step) != "passed" for step in STEPS):
            reasons.append("steps_incomplete")
        observed = report.get("observed")
        expected_pin = expectations.get(guest_id, {})
        if not isinstance(observed, dict):
            reasons.append("observations_missing")
            observed = {}
        if not expected_pin or observed.get("build") != expected_pin.get("build"):
            reasons.append("build_mismatch")
        if observed.get("packages") != expected_pin.get("packages"):
            reasons.append("package_mismatch")
        if observed.get("applied_update_sha256") != expected_pin.get("update_sha256"):
            reasons.append("staged_updates_mismatch")
        for field, expected in (
            ("address", guest["address"]),
            ("dns_servers", [guest["dns_server"]]),
            ("dns_suffix", guest["dns_suffix"]),
            ("default_routes", []),
            ("denied_egress", True),
        ):
            if observed.get(field) != expected:
                reasons.append(f"{field}_mismatch")
        offset = observed.get("time_offset_ms")
        if (
            isinstance(offset, bool)
            or not isinstance(offset, (int, float))
            or not math.isfinite(offset)
            or abs(offset) > 5000
        ):
            reasons.append("time_offset_invalid")
        probes = observed.get("probes")
        if not isinstance(probes, dict) or any(
            probes.get(key) != {"expected": expected, "observed": expected, "status": "passed"}
            for key, expected in (
                ("dc_a", guest["dns_server"]),
                ("ldap_srv", f"dc.{guest['dns_suffix']}"),
                ("ldap_tcp", True),
            )
        ):
            reasons.append("discovery_probe_mismatch")
        guests[guest_id] = {
            "report_sha256": digest(raw),
            "build": observed.get("build"),
            "packages": observed.get("packages"),
            "dns_servers": observed.get("dns_servers"),
            "time_offset_ms": offset,
            "denied_egress": observed.get("denied_egress"),
            "probes": probes,
            "status": "complete" if not reasons else "incomplete",
            "reasons": reasons,
        }
        blockers.extend(f"{guest_id}:{reason}" for reason in reasons)
    return {
        "schema_version": 1,
        "run_id": plan["run_id"],
        "plan_sha256": pin,
        "journal_sha256": digest(journal.read_bytes()),
        "guest_results": guests,
        "blockers": blockers,
        "cycle_record_complete": not blockers,
        "p00_05_accepted": False,
        "evidence_class": "operator_supplied_guest_reports_for_independent_review",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "assess"])
    parser.add_argument("--journal", type=Path, required=True)
    parser.add_argument("--staging-manifest", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--reports-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "prepare":
            if not args.staging_manifest or not args.output_root:
                raise ValueError("prepare requires --staging-manifest and --output-root")
            result = prepare(args.journal, args.staging_manifest, args.output_root)
        else:
            if not args.reports_root:
                raise ValueError("assess requires --reports-root")
            result = assess(args.journal, args.reports_root)
            if args.output:
                if args.output.resolve().is_relative_to(ROOT):
                    raise ValueError("Cycle evidence must remain outside the repository")
                save(args.output, result)
        print(json.dumps(result, indent=2))
        return 0 if args.action == "prepare" or result["cycle_record_complete"] else 2
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Guest evidence refused: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
