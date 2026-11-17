"""Validate the native-core design baseline's phase and requirement traceability."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOBAL_SOURCES = (
    "requirements.md",
    "security-roadmap.md",
    "patch-management-roadmap.md",
    "endpoint-operations-roadmap.md",
)
GLOBAL_ID = r"(?:PLAT|AD|IAM|OPS|UX|SEC|PATCH|REMOTE|FILE|EDR|[A-L])-\d{2}"
SECTIONS = (
    "Scope and entry",
    "Design and interfaces",
    "Data and lifecycle",
    "Security and failure handling",
    "Capacity and operations",
    "Requirements and acceptance",
    "Evidence and exit",
    "Dependencies and traceability",
)
BASELINE_IDS = (
    {f"PLAT-{i:02}" for i in range(1, 4)}
    | {f"AD-{i:02}" for i in range(1, 11)}
    | {f"SEC-{i:02}" for i in range(1, 12)}
    | {"IAM-01", "OPS-01", "UX-01"}
)


def check(root: Path) -> list[str]:
    errors: list[str] = []
    registry: set[str] = set()
    for name in GLOBAL_SOURCES:
        path = root / "docs" / name
        if not path.is_file():
            errors.append(f"Missing requirement catalog: {name}")
            continue
        for identifier in re.findall(rf"^\| ({GLOBAL_ID}) \|", path.read_text(), re.M):
            if identifier in registry:
                errors.append(f"Duplicate global requirement: {identifier}")
            registry.add(identifier)
    for missing in sorted(BASELINE_IDS - registry):
        errors.append(f"Missing baseline requirement: {missing}")

    expected = {f"phase-{number:02}.md" for number in range(18)}
    actual = {path.name for path in (root / "docs/phases").glob("phase-*.md")}
    for missing in sorted(expected - actual):
        errors.append(f"Missing phase specification: {missing}")
    for extra in sorted(actual - expected):
        errors.append(f"Unregistered phase specification: {extra}")

    covered: set[str] = set()
    for number in range(18):
        path = root / f"docs/phases/phase-{number:02}.md"
        if not path.is_file():
            continue
        text = path.read_text()
        if not text.startswith(f"# Phase {number:02} — "):
            errors.append(f"{path.name}: wrong phase heading")
        if "Status: specified; product acceptance not demonstrated." not in text:
            errors.append(f"{path.name}: explicit non-acceptance status missing")
        for section in SECTIONS:
            match = re.search(rf"^## {re.escape(section)}\n\n(.+?)(?=\n## |\Z)", text, re.M | re.S)
            if match is None or not match.group(1).strip():
                errors.append(f"{path.name}: missing or empty {section}")
        rows = re.findall(r"^\| (P\d{2}-\d{2}) \|([^|]*)\|([^|]*)\|$", text, re.M)
        identifiers = [row[0] for row in rows]
        wanted = {f"P{number:02}-{item:02}" for item in range(1, 11)}
        if set(identifiers) != wanted or len(identifiers) != len(wanted):
            errors.append(f"{path.name}: require ten unique sequential phase IDs with acceptance")
        if any(
            not requirement.strip() or not evidence.strip() for _, requirement, evidence in rows
        ):
            errors.append(f"{path.name}: empty requirement or acceptance evidence")
        links = re.findall(r"^Traceability: (.+)$", text, re.M)
        if len(links) != 1:
            errors.append(f"{path.name}: require one explicit traceability line")
            continue
        references = {part.strip() for part in links[0].split(",")}
        for unknown in sorted(references - registry):
            errors.append(f"{path.name}: unknown requirement reference {unknown}")
        covered.update(references & registry)
    for missing in sorted(registry - covered):
        errors.append(f"Unassigned global requirement: {missing}")
    return errors


if __name__ == "__main__":
    failures = check(ROOT)
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print("Design baseline passed: 18 phases, 180 phase requirements; all catalog IDs assigned")
