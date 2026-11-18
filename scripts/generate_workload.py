"""Generate bounded, deterministic synthetic workload data; never contact a directory."""

import argparse
import hashlib
import json
import re
import uuid
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, BinaryIO

VERSION = 1
ROOT = Path(__file__).resolve().parents[1]
INPUTS = ("docs/phase-00-workload.md", "lab/compatibility.json")
NAMESPACE = uuid.UUID("ff649a40-a784-50fd-92f8-fd259bfbbd0e")
SITES = ("site-a", "site-b", "site-c")
FILES = ("objects.ndjson", "memberships.ndjson", "negative-fixtures.json")


@dataclass(frozen=True)
class Profile:
    users: int = 10000
    computers: int = 10000
    groups: int = 2000
    ous: int = 100
    gpos: int = 50

    def validate(self) -> None:
        for field, maximum in (
            ("users", 10000),
            ("computers", 10000),
            ("groups", 2000),
            ("ous", 100),
        ):
            value = getattr(self, field)
            if type(value) is not int or not 20 <= value <= maximum or value % 20:
                raise ValueError(f"{field}: bounded positive multiple of 20 required")
        if self.groups < 100 or type(self.gpos) is not int or not 1 <= self.gpos <= 50:
            raise ValueError("At least 100 groups and 1..50 policy fixtures required")


PROFILES = {"full": Profile(), "smoke": Profile(20, 20, 100, 20, 5)}


def encoded(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode()


def score(seed: str, purpose: str, index: int) -> bytes:
    return hashlib.sha256(f"{VERSION}/{seed}/{purpose}/{index}".encode()).digest()


def identifier(seed: str, label: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{VERSION}/{seed}/{label}"))


def buckets(
    seed: str, purpose: str, count: int, values: tuple[int, ...], weights: tuple[int, ...]
) -> list[int]:
    if sum(weights) != 100 or len(values) != len(weights) or any(count * w % 100 for w in weights):
        raise ValueError("Distribution requires exact integer proportions")
    assignments = [0] * count
    order = sorted(range(count), key=lambda i: score(seed, purpose, i))
    offset = 0
    for value, weight in zip(values, weights, strict=True):
        end = offset + count * weight // 100
        for index in order[offset:end]:
            assignments[index] = value
        offset = end
    return assignments


def choose_groups(seed: str, principal: int, count: int, groups: int) -> list[int]:
    if not 1 <= count <= groups:
        raise ValueError("Invalid membership sample size")
    # SHA-256 counter sampling, rejection of modulo bias and duplicate values.
    result: list[int] = []
    seen: set[int] = set()
    limit = 2**64 - 2**64 % groups
    for counter in range(16 * count + 1024):
        value = int.from_bytes(score(seed, f"membership/{principal}", counter)[:8], "big")
        if value >= limit:
            continue
        group = value % groups
        if group not in seen:
            result.append(group)
            seen.add(group)
        if len(result) == count:
            return sorted(result)
    raise ValueError("Bounded membership sampling exhausted")


class Writer:
    def __init__(self, path: Path) -> None:
        self.stream: BinaryIO = path.open("xb")
        self.sha = hashlib.sha256()
        self.size = 0
        self.rows = 0

    def append(self, value: Any) -> None:
        raw = encoded(value)
        self.stream.write(raw)
        self.sha.update(raw)
        self.size += len(raw)
        self.rows += 1

    def close(self) -> dict[str, Any]:
        self.stream.close()
        return {"sha256": self.sha.hexdigest(), "bytes": self.size, "records": self.rows}


def negative_fixtures(seed: str) -> dict[str, Any]:
    cycle = [identifier(seed, f"negative-cycle/{i}") for i in range(3)]
    deep = [identifier(seed, f"negative-depth/{i}") for i in range(10)]
    return {
        "scope": "synthetic graph inputs, not executed server denial tests",
        "group_budget": 8,
        "cases": [
            {
                "id": "cycle",
                "expected": "reject_cycle",
                "nodes": cycle,
                "edges": [[cycle[i], cycle[(i + 1) % 3]] for i in range(3)],
            },
            {
                "id": "over-budget",
                "expected": "reject_depth",
                "nodes": deep,
                "edges": [[deep[i], deep[i + 1]] for i in range(9)],
            },
        ],
    }


def generate(
    output: Path, *, seed: str, source_revision: str, profile: Profile = Profile()
) -> dict[str, Any]:
    profile.validate()
    if not re.fullmatch(r"[a-z0-9-]{1,64}", seed):
        raise ValueError("Seed must be a bounded lowercase synthetic label")
    if not re.fullmatch(r"[a-f0-9]{40}", source_revision):
        raise ValueError("Exact source revision required")
    absolute = output.absolute()
    if any(p.is_symlink() for p in (absolute, *absolute.parents)):
        raise ValueError("Output path must not contain symlinks")
    output.mkdir(mode=0o700)  # Exclusive: never overwrite an existing output directory.
    writers: list[Writer] = []
    try:
        objects = Writer(output / FILES[0])
        writers.append(objects)
        members = Writer(output / FILES[1])
        writers.append(members)
        principal_count = profile.users + profile.computers
        payloads = buckets(
            seed, "payload", principal_count + profile.groups, (512, 2048, 8192), (70, 25, 5)
        )
        memberships = buckets(
            seed, "memberships", principal_count, (1, 5, 20, 100), (20, 50, 25, 5)
        )
        ou_sites = buckets(seed, "ou-sites", profile.ous, (0, 1, 2), (40, 35, 25))
        ous = [identifier(seed, f"ou/{i}") for i in range(profile.ous)]
        group_ids = [identifier(seed, f"group/{i}") for i in range(profile.groups)]
        by_site = [[i for i, site in enumerate(ou_sites) if site == target] for target in range(3)]
        sid_parts = [int.from_bytes(score(seed, "domain-sid", i)[:4], "big") or 1 for i in range(3)]
        domain_sid = "S-1-5-21-" + "-".join(map(str, sid_parts))
        for index, guid in enumerate(ous):
            objects.append(
                {
                    "kind": "ou",
                    "guid": guid,
                    "name": f"ou{index:03}",
                    "site": SITES[ou_sites[index]],
                    "dn_label": f"OU=ou{index:03},DC=babel,DC=example,DC=test",
                }
            )
        position = 0
        for kind, count, rid_start in (
            ("user", profile.users, 1000),
            ("computer", profile.computers, 11000),
            ("group", profile.groups, 21000),
        ):
            sites = buckets(seed, f"{kind}-sites", count, (0, 1, 2), (40, 35, 25))
            for index in range(count):
                guid = identifier(seed, f"{kind}/{index}")
                site = sites[index]
                options = by_site[site]
                ou = options[
                    int.from_bytes(score(seed, f"{kind}-ou", index)[:8], "big") % len(options)
                ]
                name = f"{kind}-{index:05}"
                payload_size = payloads[position]
                objects.append(
                    {
                        "kind": kind,
                        "guid": guid,
                        "sid": f"{domain_sid}-{rid_start + index}",
                        "name": name,
                        "site": SITES[site],
                        "enabled": True,
                        "ou_guid": ous[ou],
                        "dn_label": f"CN={name},OU=ou{ou:03},DC=babel,DC=example,DC=test",
                        "acl_pattern": ("inherited-reader", "delegated-helpdesk", "restricted")[
                            score(seed, "acl", position)[0] % 3
                        ],
                        "payload": hashlib.shake_256(
                            score(seed, "payload-bytes", position)
                        ).hexdigest(payload_size // 2),
                    }
                )
                if kind != "group":
                    for group in choose_groups(
                        seed, position, memberships[position], profile.groups
                    ):
                        members.append(
                            {
                                "kind": "principal",
                                "member_guid": guid,
                                "group_guid": group_ids[group],
                            }
                        )
                position += 1
        offset = 0
        for depth in (1, 3, 8):
            for index in range(depth):
                members.append(
                    {
                        "kind": "nested",
                        "group_guid": group_ids[offset + index],
                        "member_guid": group_ids[offset + index + 1],
                    }
                )
            offset += depth + 1
        for index in range(profile.gpos):
            objects.append(
                {
                    "kind": "gpo",
                    "guid": identifier(seed, f"gpo/{index}"),
                    "name": f"policy-{index:03}",
                    "linked_ou_guid": ous[index % profile.ous],
                }
            )
        inventory = {FILES[0]: objects.close(), FILES[1]: members.close()}
        raw = encoded(negative_fixtures(seed))
        with (output / FILES[2]).open("xb") as stream:
            stream.write(raw)
        inventory[FILES[2]] = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "records": 2,
        }
        manifest = {
            "schema_version": 1,
            "generator_version": VERSION,
            "seed": seed,
            "source_revision": source_revision,
            "input_sha256": {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in INPUTS
            },
            "sid_history_values": 0,
            "not_generated": [
                "domain-root",
                "schema",
                "configuration",
                "deleted-objects",
                "credentials",
                "SYSVOL",
            ],
            "status": "synthetic_fixture_only",
            "import_supported": False,
            "profile": asdict(profile),
            "domain_sid": domain_sid,
            "files": inventory,
            "direct_memberships": dict(sorted(Counter(memberships).items())),
            "payload_bytes": dict(sorted(Counter(payloads).items())),
            "nesting_depths": [1, 3, 8],
            "topology": [{"site": name, "planned_dc_count": 2} for name in SITES],
            "unmeasured": dict.fromkeys(
                (
                    "token_bytes",
                    "database_index_bytes",
                    "storage_expansion",
                    "throughput",
                    "latency",
                )
            ),
            "limits": (
                "Logical synthetic labels and ACL/GPO patterns only; "
                "no schema/config import, credentials, SYSVOL, access checks, "
                "AD RID allocation or client/benchmark evidence."
            ),
        }
        with (output / "manifest.json").open("xb") as stream:
            stream.write(encoded(manifest))
        return manifest
    finally:
        for writer in writers:
            writer.stream.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", default="babel-phase0-v1")
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--profile", choices=PROFILES, default="full")
    args = parser.parse_args()
    try:
        manifest = generate(
            args.output,
            seed=args.seed,
            source_revision=args.source_revision,
            profile=PROFILES[args.profile],
        )
    except (ValueError, OSError) as error:
        raise SystemExit(f"Synthetic dataset generation failed: {error}") from error
    print(
        f"Synthetic fixture generated ({args.profile}); "
        "no directory, endpoint or benchmark was run."
    )
