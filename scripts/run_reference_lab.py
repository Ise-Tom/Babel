"""Plan and operate one disposable Hyper-V reference lab run.

The private state directory is the only authority for cleanup. A failed or
interrupted process can be resumed with ``teardown`` using the same journal.
Guest installation and in-guest DNS/time/discovery evidence are separate from
host resource creation; this tool never calls a guest boot a conformance pass.
"""

import argparse
import hashlib
import ipaddress
import json
import os
import re
import subprocess  # nosec B404
import sys
import tomllib
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from check_lab_definition import PROFILE, validate
from preflight_reference_lab import check, host_inventory

SCRIPT = Path(__file__).with_name("reference_lab_hyperv.ps1")
RUN_ID = re.compile(r"[a-f0-9]{32}\Z")


def plan(profile: dict[str, Any], run_id: str, storage_root: Path) -> dict[str, Any]:
    validate(profile)
    if not RUN_ID.fullmatch(run_id):
        raise ValueError("Run ID must be a 32-character lowercase hex UUID")
    if not storage_root.is_dir() or storage_root.is_symlink():
        raise ValueError("Storage root must be an existing ordinary directory")
    base = storage_root.resolve() / f"babel-lab-{run_id}"
    networks = []
    for net in profile["networks"]:
        networks.append(
            {
                "id": net["id"],
                "switch": f"babel-{run_id}-{net['id']}",
                "type": "Private",
                "cidr": net["cidr"],
                "dns_zone": net["domain"],
                "dns_source": f"{net['id']}-dc",
                "time_source": f"{net['id']}-dc",
                "dns_server": str(ipaddress.ip_network(net["cidr"]).network_address + 10),
                "time_server": str(ipaddress.ip_network(net["cidr"]).network_address + 10),
                "default_gateway": None,
                "external_dns": None,
                "probes": [
                    "isolated_dns_answer",
                    "time_offset",
                    "no_default_route",
                    "denied_external_egress",
                ],
            }
        )
    guests = []
    addresses = {
        network["id"]: ipaddress.ip_network(network["cidr"]) for network in profile["networks"]
    }
    for machine in profile["machines"]:
        suffix = {
            "windows_reference_dc": 10,
            "babel_linux_dc": 10,
            "windows_client": 20,
            "linux_probe": 30,
        }[machine["role"]]
        guests.append(
            {
                "id": machine["id"],
                "vm": f"babel-{run_id}-{machine['id']}",
                "disk": str(base / f"{machine['id']}.vhdx"),
                "switch": f"babel-{run_id}-{machine['network']}",
                "role": machine["role"],
                "cpus": machine["cpus"],
                "memory_mib": machine["memory_mib"],
                "disk_gib": machine["disk_gib"],
                "address": str(addresses[machine["network"]].network_address + suffix),
                "prefix_length": addresses[machine["network"]].prefixlen,
                "dns_suffix": next(
                    n["domain"] for n in profile["networks"] if n["id"] == machine["network"]
                ),
                "dns_server": str(addresses[machine["network"]].network_address + 10),
                "default_gateway": None,
                "time_source": f"{machine['network']}-dc",
                "time_server": str(addresses[machine["network"]].network_address + 10),
                "probes": [
                    "vm_state",
                    "switch_attachment",
                    "guest_build",
                    "installed_packages",
                    "dns_answer",
                    "time_offset",
                    "routes",
                    "denied_egress",
                ],
            }
        )
    return {
        "schema_version": 1,
        "run_id": run_id,
        "storage_dir": str(base),
        "networks": networks,
        "guests": guests,
        "cycles": "one_run_only",
        "guest_configuration": "operator_supplied_verified_media_and_in_guest_setup_required",
    }


class Backend(Protocol):
    def call(self, action: str, item: dict[str, Any]) -> dict[str, Any]: ...


class HyperV:
    def call(self, action: str, item: dict[str, Any]) -> dict[str, Any]:
        if sys.platform != "win32":
            raise RuntimeError("Hyper-V backend requires Windows")
        command = [
            str(
                Path(os.environ.get("SystemRoot", r"C:\Windows"))
                / "System32/WindowsPowerShell/v1.0/powershell.exe"
            ),
            "-NoProfile",
            "-NonInteractive",
            "-File",
            str(SCRIPT),
            "-Action",
            action,
        ]
        result = subprocess.run(  # nosec B603: fixed local script and action, JSON on stdin
            command,
            input=json.dumps(item),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(
                f"Hyper-V {action} failed (exit {result.returncode}); inspect private operator log"
            )
        response: dict[str, Any] = json.loads(result.stdout)
        return response


def save(path: Path, record: dict[str, Any]) -> None:
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    temporary.replace(path)


def resources(plan_record: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for network in plan_record["networks"]:
        result.append(
            {"kind": "switch", "name": network["switch"], "run_id": plan_record["run_id"]}
        )
    for guest in plan_record["guests"]:
        result.append(
            {
                "kind": "disk",
                "name": guest["disk"],
                "run_id": plan_record["run_id"],
                "size_gib": guest["disk_gib"],
            }
        )
        result.append(
            {
                "kind": "vm",
                "name": guest["vm"],
                "run_id": plan_record["run_id"],
                "disk": guest["disk"],
                "switch": guest["switch"],
                "cpus": guest["cpus"],
                "memory_mib": guest["memory_mib"],
                "guest_id": guest["id"],
            }
        )
    return result


def preflight(
    profile: dict[str, Any], media: dict[str, Any], manifest_dir: Path, storage_root: Path
) -> dict[str, Any]:
    return check(
        profile, host_inventory(storage_root), media, manifest_dir, datetime.now(UTC).date()
    )


def verified_media_paths(media: dict[str, Any], manifest_dir: Path) -> dict[str, Path]:
    """Repeat byte verification immediately before creating any Hyper-V resource."""
    root = manifest_dir.resolve()
    paths = {}
    for guest_id, record in media.items():
        raw = record["path"]
        relative = Path(raw)
        if (
            relative.is_absolute()
            or relative.drive
            or raw.startswith(("\\", "//"))
            or relative.suffix.lower() != ".iso"
        ):
            raise ValueError(f"{guest_id}: local relative ISO path required")
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root) or not path.is_file():
            raise ValueError(f"{guest_id}: media must be an ordinary file under manifest directory")
        with path.open("rb") as content:
            digest = hashlib.file_digest(content, "sha256").hexdigest()
        if digest != record["sha256"]:
            raise ValueError(f"{guest_id}: media digest changed after preflight")
        paths[guest_id] = path.resolve()
    return paths


def provision(
    profile: dict[str, Any],
    media: dict[str, Any],
    manifest_dir: Path,
    storage_root: Path,
    state_root: Path,
    backend: Backend,
    run_id: str,
) -> tuple[Path, dict[str, Any]]:
    result = preflight(profile, media, manifest_dir, storage_root)
    if result["status"] != "ready_for_provisioner_review" or set(result["media"].values()) != {
        "digest_verified"
    }:
        raise ValueError("Preflight blocked: " + ", ".join(result["blockers"]))
    media_paths = verified_media_paths(media, manifest_dir)
    lab_plan = plan(profile, run_id, storage_root)
    state_root.mkdir(parents=True, exist_ok=True)
    journal = state_root / f"babel-lab-{run_id}.json"
    if journal.exists() or Path(lab_plan["storage_dir"]).exists():
        raise ValueError("Run state or storage already exists; use teardown on its exact journal")
    # Refuse an existing collision before creating any resource. The names are
    # random, but existence checks are still required.
    listed = resources(lab_plan)
    for item in listed:
        if backend.call("inspect", item).get("exists"):
            raise ValueError("Planned Hyper-V resource already exists")
    record: dict[str, Any] = {
        "schema_version": 1,
        "plan": lab_plan,
        "preflight": result,
        "resources": [{"item": item, "state": "pending"} for item in listed],
        "phase": "provisioning",
        "guest_discovery": "unrun",
    }
    save(journal, record)
    Path(lab_plan["storage_dir"]).mkdir()
    try:
        for entry in record["resources"]:
            item = entry["item"]
            if item["kind"] == "vm":
                # Private media paths are passed only to the backend, never to
                # the public plan or retained journal.
                item = dict(
                    item,
                    media_path=str(media_paths[item["guest_id"]]),
                    media_sha256=media[item["guest_id"]]["sha256"],
                )
            backend.call("create", item)
            entry["state"] = "created"
            save(journal, record)
        record["phase"] = "provisioned"
        save(journal, record)
    except BaseException:
        # Pending entries are also inspected: a process can be interrupted
        # between successful Hyper-V creation and the journal update.
        teardown(journal, backend)
        raise
    return journal, record


def teardown(journal: Path, backend: Backend) -> dict[str, Any]:
    record = json.loads(journal.read_text(encoding="utf-8"))
    if record.get("schema_version") != 1 or not RUN_ID.fullmatch(record["plan"]["run_id"]):
        raise ValueError("Invalid run journal")
    expected = resources(record["plan"])
    if [x.get("item") for x in record["resources"]] != expected:
        raise ValueError("Journal resource list does not match its plan")
    failures = []
    for entry in reversed(record["resources"]):
        if entry["state"] == "deleted":
            continue
        item = entry["item"]
        try:
            observed = backend.call("inspect", item)
            if observed.get("exists"):
                if not observed.get("owned"):
                    raise ValueError("Resource ownership mismatch")
                backend.call("delete", item)
            entry["state"] = "deleted"
            save(journal, record)
        except (RuntimeError, ValueError, OSError) as error:
            failures.append({"kind": item["kind"], "name": item["name"], "reason": str(error)})
    if not failures:
        directory = Path(record["plan"]["storage_dir"])
        if directory.name != f"babel-lab-{record['plan']['run_id']}" or directory.is_symlink():
            failures.append(
                {"kind": "directory", "name": str(directory), "reason": "Invalid run directory"}
            )
        elif directory.exists():
            try:
                directory.rmdir()  # Empty only; foreign files are never removed.
            except OSError:
                failures.append(
                    {
                        "kind": "directory",
                        "name": str(directory),
                        "reason": "Run directory is not empty",
                    }
                )
    record["phase"] = "teardown_incomplete" if failures else "torn_down"
    save(journal, record)
    return {"phase": record["phase"], "failures": failures, "journal": str(journal)}


def discover(journal: Path, backend: Backend) -> dict[str, Any]:
    record = json.loads(journal.read_text(encoding="utf-8"))
    if record["phase"] != "provisioned":
        raise ValueError("Run is not provisioned")
    observations = {}
    for entry in record["resources"]:
        item = entry["item"]
        if item["kind"] in {"vm", "switch"}:
            observed = backend.call("inspect", item)
            if not observed.get("exists") or not observed.get("owned"):
                raise ValueError("Lab resource missing or no longer owned")
            if item["kind"] == "vm" and "switches" in observed:
                if observed["switches"] != [item["switch"]]:
                    raise ValueError("VM has unexpected switch attachment")
            observations[item["name"]] = observed
    # Hyper-V cannot prove in-guest DNS, time, routes, package state or AD
    # discovery. Those probes remain unrun until independent guest evidence.
    return {
        "run_id": record["plan"]["run_id"],
        "host_resources": observations,
        "guest_probes": "unrun",
        "p00_05_cycle_complete": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["plan", "provision", "discover", "teardown"])
    parser.add_argument("--run-id", default=uuid.uuid4().hex)
    parser.add_argument("--storage-root", type=Path, default=Path.cwd())
    parser.add_argument("--state-root", type=Path)
    parser.add_argument("--media", type=Path)
    parser.add_argument("--journal", type=Path)
    args = parser.parse_args()
    try:
        profile = tomllib.loads(PROFILE.read_text(encoding="utf-8"))
        if args.action == "plan":
            result = plan(profile, args.run_id, args.storage_root)
        elif args.action == "provision":
            if not args.media or not args.state_root:
                raise ValueError("provision needs --media and --state-root")
            media = tomllib.loads(args.media.read_text(encoding="utf-8"))
            journal, record = provision(
                profile,
                media,
                args.media.parent,
                args.storage_root,
                args.state_root,
                HyperV(),
                args.run_id,
            )
            result = {"journal": str(journal), "phase": record["phase"], "guest_probes": "unrun"}
        else:
            if not args.journal:
                raise ValueError("discover/teardown needs --journal")
            result = (
                discover(args.journal, HyperV())
                if args.action == "discover"
                else teardown(args.journal, HyperV())
            )
        print(json.dumps(result, indent=2))
        return 0 if result.get("phase") != "teardown_incomplete" else 2
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        parser.exit(2, f"Lab runner refused: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
