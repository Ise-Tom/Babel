"""Read-only preflight for the six-guest Windows/Linux lab on Hyper-V."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess  # nosec B404
import sys
import tomllib
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from check_lab_definition import PROFILE, validate

MIB = 1024**2
GIB = 1024**3
HYPER_V_INVENTORY = r"""
$ErrorActionPreference = 'Stop'
$os = Get-CimInstance Win32_OperatingSystem
$build = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
$computer = Get-CimInstance Win32_ComputerSystem
$service = Get-Service vmms -ErrorAction SilentlyContinue
$vmCount = $null
$switchCount = $null
try { $vmCount = @(Get-VM -ErrorAction Stop).Count } catch {}
try { $switchCount = @(Get-VMSwitch -ErrorAction Stop).Count } catch {}
[ordered]@{
    edition = $build.EditionID
    release = $build.DisplayVersion
    build = "$($os.Version).$($build.UBR)"
    architecture = switch ($computer.SystemType) {
        'x64-based PC' { 'x86_64' }
        'ARM64-based PC' { 'aarch64' }
        default { 'unknown' }
    }
    logical_cpus = $computer.NumberOfLogicalProcessors
    total_memory_mib = [math]::Floor($os.TotalVisibleMemorySize / 1024)
    available_memory_mib = [math]::Floor($os.FreePhysicalMemory / 1024)
    hypervisor_present = $computer.HypervisorPresent
    vmms_running = ($null -ne $service -and $service.Status -eq 'Running')
    vm_count = $vmCount
    switch_count = $switchCount
} | ConvertTo-Json -Compress
"""


def host_inventory(storage_root: Path) -> dict[str, Any]:
    if sys.platform != "win32":
        return {"inventory": "windows_host_required"}
    powershell = (
        Path(os.environ.get("SystemRoot", r"C:\Windows"))
        / "System32"
        / "WindowsPowerShell"
        / "v1.0"
        / "powershell.exe"
    )
    try:
        # The system executable receives a fixed query with no manifest interpolation.
        result = subprocess.run(  # nosec B603
            [str(powershell), "-NoProfile", "-NonInteractive", "-Command", HYPER_V_INVENTORY],
            capture_output=True,
            check=True,
            text=True,
            timeout=30,
        )
        host: dict[str, Any] = json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, ValueError):
        return {"inventory": "windows_query_failed"}
    host["inventory"] = "observed"
    try:
        if storage_root.is_dir():
            host["available_storage_gib"] = shutil.disk_usage(storage_root).free // GIB
    except OSError:
        pass
    return host


def media_status(record: Any, manifest_dir: Path, today: date) -> str:
    if record is None:
        return "missing"
    if not isinstance(record, dict):
        return "invalid_metadata"
    for field in ("id", "edition", "build", "path", "sha256"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            return "invalid_metadata"
    if record.get("architecture") != "x86_64" or not re.fullmatch("[a-f0-9]{64}", record["sha256"]):
        return "invalid_metadata"
    packages = record.get("packages")
    if not isinstance(packages, dict) or not packages:
        return "invalid_metadata"
    if any(
        not name.strip() or not isinstance(pin, str) or not pin.strip()
        for name, pin in packages.items()
    ):
        return "invalid_metadata"
    terms = record.get("publisher_terms")
    try:
        url = urlsplit(terms) if isinstance(terms, str) else None
        valid_terms = url is not None and url.scheme == "https" and bool(url.hostname)
    except ValueError:
        valid_terms = False
    rights_record = record.get("rights_record")
    if (
        record.get("approved_use") != "private_isolated_install_and_run"
        or not valid_terms
        or not isinstance(rights_record, str)
        or not rights_record.strip()
    ):
        return "rights_unresolved"
    if "expires_on" in record:
        expires = record["expires_on"]
        if type(expires) is not date:
            return "invalid_metadata"
        if expires <= today:
            return "rights_expired"
    if record["path"].startswith(("\\", "//")):
        return "nonlocal_path"
    try:
        path = manifest_dir / record["path"]
        if not path.is_file():
            return "file_unavailable"
        with path.open("rb") as image:
            digest = hashlib.file_digest(image, "sha256").hexdigest()
    except (OSError, ValueError):
        return "file_unavailable"
    return "digest_verified" if digest == record["sha256"] else "digest_mismatch"


def check(
    plan: dict[str, Any],
    host: dict[str, Any],
    media: dict[str, Any],
    manifest_dir: Path,
    today: date,
) -> dict[str, Any]:
    validate(plan)
    machines = plan["machines"]
    required = {
        "guest_vcpus": sum(guest["cpus"] for guest in machines),
        "guest_memory_mib": sum(guest["memory_mib"] for guest in machines),
        "guest_storage_gib": sum(guest["disk_gib"] for guest in machines),
    }
    blockers = []
    if host["inventory"] != "observed":
        blockers.append(host["inventory"])
    else:
        if host.get("architecture") != "x86_64":
            blockers.append("x86_64_hyper_v_host_required")
        if not host.get("hypervisor_present") or not host.get("vmms_running"):
            blockers.append("hyper_v_not_running")
        if host.get("vm_count") is None or host.get("switch_count") is None:
            blockers.append("hyper_v_inventory_unavailable")
        for available, minimum, reason in (
            ("logical_cpus", "guest_vcpus", "logical_cpu_capacity"),
            ("available_memory_mib", "guest_memory_mib", "guest_memory_capacity"),
            ("available_storage_gib", "guest_storage_gib", "guest_storage_capacity"),
        ):
            observed = host.get(available)
            if observed is None:
                blockers.append(f"{reason}_unmeasured")
            elif observed < required[minimum]:
                blockers.append(f"{reason}_shortfall")
    if media.keys() - {guest["id"] for guest in machines}:
        raise ValueError("Unknown guest in the private media manifest")
    media_results = {}
    for guest in machines:
        machine_id = guest["id"]
        status = media_status(media.get(machine_id), manifest_dir, today)
        media_results[machine_id] = status
        if status != "digest_verified":
            blockers.append(f"{machine_id}:media_{status}")
    return {
        "date_utc": today.isoformat(),
        "backend": "hyper-v",
        "status": "blocked" if blockers else "ready_for_provisioner_review",
        "required": required,
        "host": host,
        "media": media_results,
        "blockers": blockers,
        "provisioning_cycles": ["unrun", "unrun"],
        "macos": "separate_track",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storage-root", type=Path, default=Path.cwd())
    parser.add_argument("--media", type=Path, help="Optional private TOML with one table per guest")
    args = parser.parse_args()
    try:
        plan = tomllib.loads(PROFILE.read_text(encoding="utf-8"))
        media = tomllib.loads(args.media.read_text(encoding="utf-8")) if args.media else {}
        report = check(
            plan,
            host_inventory(args.storage_root),
            media,
            args.media.parent if args.media else Path.cwd(),
            datetime.now(UTC).date(),
        )
    except (OSError, ValueError):
        parser.exit(2, "Could not read or validate the lab plan or private media manifest.\n")
    print(json.dumps(report, indent=2))
    return 2 if report["blockers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
