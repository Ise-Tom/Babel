"""Run isolated post-install setup and first probes inside a disposable Linux guest.

Requires root, Python 3, iproute2, systemd-resolved, chrony, dig and dpkg-query
from the licensed staged image/packages. Never downloads or adds a default route.
"""

import argparse
import hashlib
import json
import os
import re
import socket
import subprocess  # nosec B404
from collections.abc import Callable
from pathlib import Path
from typing import Any

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


def run(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True, timeout=90, check=False)  # nosec B603
    if result.returncode:
        raise RuntimeError(f"Guest command failed: {args[0]} (exit {result.returncode})")
    return result.stdout.strip()


def checkpoint(path: Path, report: dict[str, Any]) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def validated(config: dict[str, Any]) -> None:
    if config.get("role") not in {"linux_probe", "babel_linux_dc"}:
        raise ValueError("Linux guest role required")
    if not re.fullmatch(r"[a-f0-9]{32}", config.get("run_id", "")):
        raise ValueError("Invalid run ID")
    if not re.fullmatch(r"[a-f0-9]{64}", config.get("plan_sha256", "")):
        raise ValueError("Invalid plan digest")
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", config.get("interface", "")):
        raise ValueError("Invalid guest interface")
    if config.get("default_gateway") is not None:
        raise ValueError("Default route forbidden")
    if config.get("dns_server") != config.get("time_server"):
        raise ValueError("DNS/time source disagreement")


def execute(
    config_path: Path,
    report_path: Path,
    *,
    system_root: Path = Path("/"),
    command: Callable[..., str] | None = None,
) -> dict[str, Any]:
    call = command or run
    config = json.loads(config_path.read_text(encoding="utf-8"))
    validated(config)
    script_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if script_sha256 != config.get("script_sha256"):
        raise ValueError("Guest script differs from prepared bundle")
    if os.name != "posix" or getattr(os, "geteuid", lambda: 1)() != 0:
        raise ValueError("Disposable Linux guest root required")
    report: dict[str, Any] = {
        "schema_version": 1,
        "run_id": config["run_id"],
        "plan_sha256": config["plan_sha256"],
        "guest_id": config["guest_id"],
        "vm": config["vm"],
        "script_sha256": script_sha256,
        "status": "incomplete",
        "steps": {step: "pending" for step in STEPS},
        "observed": {},
    }
    checkpoint(report_path, report)
    step = "updates_verified"
    try:
        directory = config_path.parent.resolve()
        updates = []
        for entry in config["updates"]:
            filename = entry["filename"]
            if not re.fullmatch(r"update-[1-9][0-9]*\.deb", filename):
                raise ValueError("Only staged .deb updates are allowed")
            path = directory / filename
            if path.is_symlink() or not path.is_file():
                raise ValueError("Staged update unavailable")
            with path.open("rb") as source:
                if hashlib.file_digest(source, "sha256").hexdigest() != entry["sha256"]:
                    raise ValueError("Staged update digest mismatch")
            updates.append(path)
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "updates_installed"
        for path in updates:
            call("dpkg", "-i", str(path))
        report["observed"]["applied_update_sha256"] = [
            entry["sha256"] for entry in config["updates"]
        ]
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "network_configured"
        interface = config["interface"]
        address = f"{config['address']}/{config['prefix_length']}"
        links = call("ip", "-o", "link", "show").splitlines()
        physical = [line for line in links if not re.search(r"\d+: lo:", line)]
        if len(physical) != 1 or interface not in physical[0]:
            raise ValueError("Exactly one planned non-loopback interface required")
        if call("ip", "-4", "route", "show", "default"):
            raise ValueError("Preexisting default route")
        call("ip", "link", "set", interface, "up")
        current = call("ip", "-4", "-o", "addr", "show", "dev", interface)
        if current and address not in current:
            raise ValueError("Unexpected IPv4 address on private interface")
        if not current:
            call("ip", "addr", "add", address, "dev", interface)
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "dns_configured"
        dns_dir = system_root / "etc/systemd/resolved.conf.d"
        dns_dir.mkdir(parents=True, exist_ok=True)
        (dns_dir / "90-babel-lab.conf").write_text(
            f"[Resolve]\nDNS={config['dns_server']}\nDomains={config['dns_suffix']}\nFallbackDNS=\n",
            encoding="utf-8",
        )
        call("systemctl", "restart", "systemd-resolved")
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "time_configured"
        chrony = system_root / "etc/chrony/chrony.conf"
        if not chrony.is_file():
            raise ValueError("Staged chrony installation required")
        if config["role"] == "babel_linux_dc":
            time_config = f"local stratum 10\nallow {config['address'].rsplit('.', 1)[0]}.0/24\n"
        else:
            time_config = f"server {config['time_server']} iburst\n"
        chrony.write_text(time_config + "makestep 1.0 3\nrtcsync\n", encoding="utf-8")
        call("systemctl", "restart", "chrony")
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "platform_observed"
        os_release = (system_root / "etc/os-release").read_text(encoding="utf-8")
        version = re.search(r'^VERSION_ID="?([^"\n]+)', os_release, re.M)
        kernel = call("uname", "-r")
        packages = {
            name: call("dpkg-query", "-W", "-f=${Version}", name)
            for name in config["expected_packages"]
        }
        report["observed"].update(
            {
                "build": kernel,
                "os_version": version.group(1) if version else "unknown",
                "packages": packages,
            }
        )
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "dns_probe"
        suffix = config["dns_suffix"]
        server = config["dns_server"]
        a_lines = call("dig", "+short", "A", f"dc.{suffix}", f"@{server}").splitlines()
        a_value = a_lines[0] if a_lines else ""
        srv_lines = call("dig", "+short", "SRV", f"_ldap._tcp.{suffix}", f"@{server}").splitlines()
        srv_target = srv_lines[0].split()[-1].rstrip(".") if srv_lines else ""
        try:
            with socket.create_connection((server, 389), timeout=3):
                ldap_open = True
        except OSError:
            ldap_open = False
        report["observed"]["probes"] = {
            "dc_a": {
                "expected": server,
                "observed": a_value,
                "status": "passed" if a_value == server else "failed",
            },
            "ldap_srv": {
                "expected": f"dc.{suffix}",
                "observed": srv_target,
                "status": "passed" if srv_target == f"dc.{suffix}" else "failed",
            },
            "ldap_tcp": {
                "expected": True,
                "observed": ldap_open,
                "status": "passed" if ldap_open else "failed",
            },
        }
        if any(p["status"] != "passed" for p in report["observed"]["probes"].values()):
            raise ValueError("Discovery probe mismatch")
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "time_probe"
        tracking = call("chronyc", "tracking")
        match = re.search(r"Last offset\s*:\s*([-+]?[0-9.]+)\s+seconds", tracking)
        if not match:
            raise ValueError("Chrony offset unavailable")
        offset = float(match.group(1)) * 1000
        report["observed"]["time_offset_ms"] = offset
        if abs(offset) > 5000:
            raise ValueError("Clock offset exceeds five seconds")
        report["steps"][step] = "passed"
        checkpoint(report_path, report)

        step = "egress_probe"
        try:
            with socket.create_connection(("203.0.113.1", 443), timeout=3):
                denied = False
        except OSError:
            denied = True
        routes = call("ip", "-4", "route", "show", "default")
        dns = call("resolvectl", "dns", interface)
        servers = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", dns)
        domain = call("resolvectl", "domain", interface)
        effective_domains = [part.lstrip("~") for part in domain.partition(":")[2].split()]
        addresses = call("ip", "-4", "-o", "addr", "show", "dev", interface)
        effective_ip = re.search(r"\binet\s+((?:\d{1,3}\.){3}\d{1,3})/", addresses)
        report["observed"].update(
            {
                "address": effective_ip.group(1) if effective_ip else "",
                "dns_servers": servers,
                "dns_suffix": config["dns_suffix"]
                if config["dns_suffix"] in effective_domains
                else "",
                "default_routes": routes.splitlines(),
                "denied_egress": denied,
            }
        )
        if (
            routes
            or servers != [server]
            or not denied
            or not effective_ip
            or effective_ip.group(1) != config["address"]
            or config["dns_suffix"] not in effective_domains
        ):
            raise ValueError("Isolation probe failed")
        report["steps"][step] = "passed"
        report["status"] = "complete"
        checkpoint(report_path, report)
        return report
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, KeyboardInterrupt):
        report["steps"][step] = "failed"
        report["status"] = "incomplete"
        checkpoint(report_path, report)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        execute(args.config, args.report)
        return 0
    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.TimeoutExpired,
        KeyboardInterrupt,
    ) as error:
        parser.exit(2, f"Linux guest setup incomplete: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
