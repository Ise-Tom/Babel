"""Independently audit synthetic fixture relationships, counts and artifact integrity."""

import argparse
import hashlib
import json
import re
import uuid
from collections import Counter
from collections.abc import Iterator
from graphlib import CycleError, TopologicalSorter
from pathlib import Path
from typing import Any

from generate_workload import FILES, INPUTS, ROOT, SITES, Profile, encoded

MAX_FILE = 128 * 1024 * 1024
MAX_LINE = 16384


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def regular(path: Path, maximum: int) -> None:
    require(
        not any(p.is_symlink() for p in (path, *path.parents)),
        "Symlink dataset paths are forbidden",
    )
    require(
        path.is_file() and path.stat().st_size <= maximum,
        "Missing, non-regular or oversized fixture",
    )


def read_json(path: Path) -> Any:
    regular(path, 65536)
    with path.open("rb") as stream:
        raw = stream.read(65537)
    require(len(raw) <= 65536, "JSON fixture too large")
    return json.loads(raw)


def rows(path: Path, metadata: dict[str, Any]) -> Iterator[dict[str, Any]]:
    regular(path, MAX_FILE)
    sha = hashlib.sha256()
    size = count = 0
    with path.open("rb") as stream:
        while raw := stream.readline(MAX_LINE + 1):
            require(
                len(raw) <= MAX_LINE and raw.endswith(b"\n"), "Oversized or incomplete NDJSON row"
            )
            size += len(raw)
            count += 1
            require(size <= MAX_FILE and count <= 500000, "Dataset resource budget exceeded")
            sha.update(raw)
            row = json.loads(raw)
            require(isinstance(row, dict), "Object record required")
            yield row
    require(
        metadata == {"sha256": sha.hexdigest(), "bytes": size, "records": count},
        "Dataset digest/size/count mismatch",
    )


def graph_info(
    nodes: set[str], edges: list[tuple[str, str]]
) -> tuple[dict[str, set[str]], dict[str, int]]:
    parents: dict[str, set[str]] = {node: set() for node in nodes}
    children: dict[str, set[str]] = {node: set() for node in nodes}
    for parent, child in edges:
        require(parent in nodes and child in nodes, "Unknown nested group reference")
        require(child not in children[parent], "Duplicate nested membership")
        parents[child].add(parent)
        children[parent].add(child)
    try:
        order = list(TopologicalSorter(parents).static_order())
    except CycleError as error:
        raise ValueError("Group cycle detected") from error
    depths = {node: 0 for node in nodes}
    for node in order:
        depths[node] = max((depths[parent] + 1 for parent in parents[node]), default=0)
    return parents, depths


def audit_negative(path: Path, metadata: dict[str, Any], positive: set[str]) -> None:
    data = read_json(path)
    require(set(data) == {"scope", "group_budget", "cases"}, "Unexpected negative fixture fields")
    raw = path.read_bytes()
    require(
        metadata == {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "records": 2},
        "Negative fixture digest mismatch",
    )
    require(
        data.get("group_budget") == 8 and len(data.get("cases", [])) == 2,
        "Negative fixture scope mismatch",
    )
    cases = {c["id"]: c for c in data["cases"]}
    require(set(cases) == {"cycle", "over-budget"}, "Missing negative cases")
    for name, case in cases.items():
        require(
            set(case) == {"id", "expected", "nodes", "edges"}, "Unexpected negative case fields"
        )
        nodes = set(case["nodes"])
        require(
            len(nodes) == len(case["nodes"]) and not nodes & positive,
            "Negative fixture identity overlap",
        )
        for node in nodes:
            require(str(uuid.UUID(node)) == node, "Invalid negative fixture ID")
        edges = [tuple(edge) for edge in case["edges"]]
        if name == "cycle":
            require(case["expected"] == "reject_cycle", "Wrong cycle expectation")
            try:
                graph_info(nodes, edges)
            except ValueError as error:
                require(str(error) == "Group cycle detected", "Malformed cycle fixture")
            else:
                raise ValueError("Cycle fixture is acyclic")
        else:
            require(case["expected"] == "reject_depth", "Wrong depth expectation")
            _, depths = graph_info(nodes, edges)
            require(max(depths.values(), default=0) > 8, "Negative depth fixture is within budget")


def verify(directory: Path) -> dict[str, Any]:
    require(directory.is_dir() and not directory.is_symlink(), "Dataset directory required")
    require(
        {p.name for p in directory.iterdir()} == {*FILES, "manifest.json"},
        "Unexpected or incomplete dataset files",
    )
    manifest = read_json(directory / "manifest.json")
    require(
        set(manifest)
        == {
            "schema_version",
            "generator_version",
            "seed",
            "source_revision",
            "input_sha256",
            "status",
            "import_supported",
            "profile",
            "domain_sid",
            "files",
            "direct_memberships",
            "payload_bytes",
            "nesting_depths",
            "topology",
            "unmeasured",
            "limits",
            "sid_history_values",
            "not_generated",
        },
        "Unexpected dataset manifest fields",
    )
    require(
        type(manifest["sid_history_values"]) is int
        and manifest["sid_history_values"] == 0
        and manifest["not_generated"]
        == ["domain-root", "schema", "configuration", "deleted-objects", "credentials", "SYSVOL"],
        "Unsupported fixture scope claim",
    )
    require(
        type(manifest.get("schema_version")) is int
        and manifest["schema_version"] == 1
        and type(manifest.get("generator_version")) is int
        and manifest["generator_version"] == 1,
        "Unknown dataset version",
    )
    require(
        manifest.get("status") == "synthetic_fixture_only"
        and manifest.get("import_supported") is False,
        "Dataset cannot claim import/product support",
    )
    require(
        bool(re.fullmatch(r"[a-f0-9]{40}", manifest.get("source_revision", "")))
        and bool(re.fullmatch(r"[a-z0-9-]{1,64}", manifest.get("seed", ""))),
        "Source/seed metadata required",
    )
    require(
        manifest.get("input_sha256")
        == {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in INPUTS},
        "Stale workload/compatibility input binding",
    )
    profile = Profile(**manifest["profile"])
    profile.validate()
    files = manifest["files"]
    require(set(files) == set(FILES), "Unexpected fixture inventory")
    unmeasured = manifest.get("unmeasured")
    require(
        isinstance(unmeasured, dict)
        and set(unmeasured)
        == {"token_bytes", "database_index_bytes", "storage_expansion", "throughput", "latency"}
        and all(value is None for value in unmeasured.values()),
        "Synthetic data cannot claim measured runtime results",
    )
    require(
        manifest.get("topology") == [{"site": name, "planned_dc_count": 2} for name in SITES],
        "Unexpected planned topology",
    )
    domain = manifest.get("domain_sid", "")
    require(
        bool(re.fullmatch(r"S-1-5-21-(?:[1-9]\d{0,9}-){2}[1-9]\d{0,9}", domain))
        and all(int(p) < 2**32 for p in domain.split("-")[4:]),
        "Invalid synthetic domain SID",
    )
    counts: Counter[str] = Counter()
    sites: Counter[tuple[str, str]] = Counter()
    payloads: Counter[int] = Counter()
    objects: dict[str, str] = {}
    ous: dict[str, str] = {}
    ou_names: dict[str, str] = {}
    principals: dict[str, int] = {}
    groups: dict[str, int] = {}
    sids: set[str] = set()
    names: set[str] = set()
    for row in rows(directory / FILES[0], files[FILES[0]]):
        kind, guid = row["kind"], row["guid"]
        require(
            str(uuid.UUID(guid)) == guid and guid not in objects,
            "Duplicate or invalid object identity",
        )
        require(row["name"] not in names, "Duplicate object name")
        names.add(row["name"])
        objects[guid] = kind
        counts[kind] += 1
        if kind == "ou":
            require(
                set(row) == {"kind", "guid", "name", "site", "dn_label"}, "Unexpected OU fields"
            )
            require(
                row["dn_label"] == f"OU={row['name']},DC=babel,DC=example,DC=test",
                "Invalid synthetic OU DN",
            )
            require(
                bool(re.fullmatch(r"ou\d{3}", row["name"])) and int(row["name"][2:]) < profile.ous,
                "Invalid OU name",
            )
            ous[guid] = row["site"]
            ou_names[guid] = row["name"]
        elif kind == "gpo":
            require(
                set(row) == {"kind", "guid", "name", "linked_ou_guid"}
                and row["linked_ou_guid"] in ous,
                "Invalid logical policy fixture",
            )
            continue
        else:
            require(kind in {"user", "computer", "group"}, "Unknown object kind")
            require(
                set(row)
                == {
                    "kind",
                    "guid",
                    "sid",
                    "name",
                    "site",
                    "enabled",
                    "ou_guid",
                    "dn_label",
                    "acl_pattern",
                    "payload",
                },
                "Unexpected principal fields",
            )
            require(
                row["enabled"] is True
                and row["acl_pattern"] in {"inherited-reader", "delegated-helpdesk", "restricted"},
                "Invalid synthetic principal state",
            )
            require(
                row["ou_guid"] in ous and ous[row["ou_guid"]] == row["site"],
                "Missing or wrong-site OU reference",
            )
            require(
                row["sid"] not in sids and row["sid"].startswith(domain + "-"),
                "Duplicate or wrong-domain SID",
            )
            match = re.fullmatch(kind + r"-(\d{5})", row["name"])
            require(match is not None, "Invalid synthetic principal name")
            index = int(match[1]) if match else -1
            require(
                0 <= index < getattr(profile, kind + "s")
                and row["sid"]
                == f"{domain}-{dict(user=1000, computer=11000, group=21000)[kind] + index}",
                "Synthetic SID range/name mismatch",
            )
            sids.add(row["sid"])
            require(
                row["dn_label"]
                == f"CN={row['name']},OU={ou_names[row['ou_guid']]},DC=babel,DC=example,DC=test",
                "Principal DN/OU reference mismatch",
            )
            payload = row["payload"]
            require(
                isinstance(payload, str)
                and len(payload) in {512, 2048, 8192}
                and bool(re.fullmatch(r"[0-9a-f]+", payload)),
                "Invalid synthetic payload",
            )
            payloads[len(payload)] += 1
            if kind == "group":
                groups[guid] = len(groups)
            else:
                principals[guid] = 0
        require(row["site"] in SITES, "Unknown site")
        sites[kind, row["site"]] += 1
    expected = {
        "user": profile.users,
        "computer": profile.computers,
        "group": profile.groups,
        "ou": profile.ous,
        "gpo": profile.gpos,
    }
    require(dict(counts) == expected, "Object counts disagree with profile")
    for kind in ("user", "computer", "group", "ou"):
        require(
            [sites[kind, site] for site in SITES]
            == [expected[kind] * w // 100 for w in (40, 35, 25)],
            "Incorrect site distribution",
        )
    total_payloads = profile.users + profile.computers + profile.groups
    require(
        dict(payloads)
        == {n: total_payloads * w // 100 for n, w in ((512, 70), (2048, 25), (8192, 5))}
        and manifest["payload_bytes"] == {str(k): v for k, v in payloads.items()},
        "Incorrect payload distribution",
    )
    nested: list[tuple[str, str]] = []
    direct_edges = 0
    for row in rows(directory / FILES[1], files[FILES[1]]):
        require(
            set(row) == {"kind", "member_guid", "group_guid"} and row["group_guid"] in groups,
            "Invalid membership reference/fields",
        )
        member, group = row["member_guid"], row["group_guid"]
        if row["kind"] == "principal":
            require(member in principals, "Unknown principal membership")
            bit = 1 << groups[group]
            require(not principals[member] & bit, "Duplicate principal membership")
            principals[member] |= bit
            direct_edges += 1
        else:
            require(row["kind"] == "nested" and member in groups, "Invalid nested membership")
            nested.append((group, member))
    distribution = Counter(bits.bit_count() for bits in principals.values())
    total = profile.users + profile.computers
    require(
        dict(distribution)
        == {n: total * w // 100 for n, w in ((1, 20), (5, 50), (20, 25), (100, 5))}
        and manifest["direct_memberships"] == {str(k): v for k, v in distribution.items()},
        "Incorrect direct membership distribution",
    )
    parents, depths = graph_info(set(groups), nested)
    require(
        max(depths.values()) == 8 and len(nested) == 12 and manifest["nesting_depths"] == [1, 3, 8],
        "Unexpected nesting depths/edge count",
    )
    children: dict[str, set[str]] = {g: set() for g in groups}
    for parent, child in nested:
        children[parent].add(child)
    require(
        all(len(v) <= 1 for v in parents.values()) and all(len(v) <= 1 for v in children.values()),
        "Nested fixtures must be disjoint chains",
    )
    chain_depths = []
    for node in groups:
        if children[node] and not parents[node]:
            depth = 0
            while children[node]:
                node = next(iter(children[node]))
                depth += 1
            chain_depths.append(depth)
    require(sorted(chain_depths) == [1, 3, 8], "Incorrect nested chain profiles")
    ancestors: dict[str, int] = {}
    for group in TopologicalSorter(parents).static_order():
        value = 0
        for parent in parents[group]:
            value |= (1 << groups[parent]) | ancestors[parent]
        ancestors[group] = value
    nested_bits = {groups[group]: bits for group, bits in ancestors.items() if bits}
    maximum = 0
    for bits in principals.values():
        effective = bits
        for index, inherited in nested_bits.items():
            if bits & (1 << index):
                effective |= inherited
        maximum = max(maximum, effective.bit_count())
    audit_negative(directory / FILES[2], files[FILES[2]], set(objects))
    return {
        "status": "synthetic_fixture_verified",
        "profile": manifest["profile"],
        "source_revision": manifest["source_revision"],
        "seed": manifest["seed"],
        "objects": sum(counts.values()),
        "principal_membership_edges": direct_edges,
        "nested_group_edges": len(nested),
        "max_effective_group_count": maximum,
        "manifest_sha256": hashlib.sha256((directory / "manifest.json").read_bytes()).hexdigest(),
        "unmeasured": manifest["unmeasured"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    args = parser.parse_args()
    try:
        summary = verify(args.dataset)
    except (ValueError, OSError, KeyError, TypeError, AttributeError, RecursionError) as error:
        raise SystemExit(f"Synthetic fixture rejected: {error}") from error
    print(encoded(summary).decode(), end="")
