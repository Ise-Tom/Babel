"""Validate an unprovisioned isolated lab definition; never launch VMs or claim conformance."""

import argparse
import ipaddress
import re
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "lab/windows-reference.toml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(profile: dict[str, Any], *, require_images: bool = False) -> None:
    require(
        type(profile.get("schema_version")) is int and profile["schema_version"] == 1,
        "Unknown lab schema",
    )
    require(profile.get("status") == "definition_only", "Only a lab definition is qualified here")
    require(
        profile.get("provider") == "unselected", "Host/provider selection requires a new review"
    )
    safety = profile.get("safety", {})
    for flag in ("production_bridge", "default_route", "external_dns", "automatic_image_downloads"):
        require(safety.get(flag) is False, f"Unsafe or missing lab control: {flag}")
    require(safety.get("credentials") == "generated_per_run", "No shared lab credentials")
    require(safety.get("evidence") == "synthetic_redacted_only", "Only redacted synthetic evidence")
    networks = profile.get("networks")
    if not isinstance(networks, list) or len(networks) != 2:
        raise ValueError("Two isolated networks required")
    ranges = {}
    for network in networks:
        name = network.get("id")
        require(name in {"reference", "babel"} and name not in ranges, "Invalid/duplicate network")
        address = ipaddress.ip_network(network.get("cidr", ""), strict=True)
        require(
            address.version == 4 and not address.is_global, "Non-public IPv4 lab network required"
        )
        require(24 <= address.prefixlen <= 28, "Bounded lab subnet required")
        domain = network.get("domain", "")
        require(
            isinstance(domain, str) and bool(re.fullmatch(r"[a-z0-9.-]+\.test", domain)),
            "Lab DNS must use .test",
        )
        ranges[name] = address
    require(not ranges["reference"].overlaps(ranges["babel"]), "Lab networks must not overlap")
    machines = profile.get("machines")
    if not isinstance(machines, list) or len(machines) != 6:
        raise ValueError("Six scoped lab machines required")
    names: set[str] = set()
    topology = []
    for machine in machines:
        name = machine.get("id", "")
        require(
            isinstance(name, str)
            and bool(re.fullmatch(r"[a-z][a-z0-9-]{0,31}", name))
            and name not in names,
            "Invalid/duplicate machine ID",
        )
        names.add(name)
        topology.append((machine.get("network"), machine.get("role")))
        for key, minimum, maximum in (
            ("cpus", 1, 8),
            ("memory_mib", 1024, 16384),
            ("disk_gib", 16, 128),
        ):
            value = machine.get(key)
            require(type(value) is int and minimum <= value <= maximum, f"Invalid resource: {key}")
        for field in ("image_id", "image_sha256", "build", "edition"):
            value = machine.get(field)
            require(isinstance(value, str) and len(value) <= 512, f"Invalid image field: {field}")
            if require_images:
                require(bool(value.strip()), f"Missing {field} for {name}")
        require(
            type(machine.get("image_license_accepted")) is bool, "Explicit image rights required"
        )
        if require_images:
            require(
                machine["image_license_accepted"] is True, f"Image rights not approved for {name}"
            )
            require(
                bool(re.fullmatch(r"[a-f0-9]{64}", machine["image_sha256"])), "Invalid image digest"
            )
    require(
        sorted(topology)
        == sorted(
            [
                ("reference", "windows_reference_dc"),
                ("reference", "windows_client"),
                ("reference", "linux_probe"),
                ("babel", "babel_linux_dc"),
                ("babel", "windows_client"),
                ("babel", "linux_probe"),
            ]
        ),
        "Reference and Babel hosts must stay on separate networks",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=PROFILE)
    parser.add_argument("--require-images", action="store_true")
    args = parser.parse_args()
    try:
        validate(tomllib.loads(args.profile.read_text()), require_images=args.require_images)
    except (ValueError, OSError, TypeError, AttributeError, KeyError) as error:
        raise SystemExit(f"Lab definition rejected: {error}") from error
    print("Lab definition validated. No VMs provisioned or Windows tests executed.")
