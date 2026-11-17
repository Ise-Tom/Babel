"""Render the validated progress model as a private, browser-readable GitHub report."""

import argparse
import html
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

from build_dashboard import REPO, ROOT, build

LIVE_URL = f"{REPO}/blob/dashboard-live/README.md"
LABELS = {
    "planned": "Planned",
    "in_progress": "In progress",
    "blocked": "Blocked",
    "accepted": "Accepted",
}


def escaped(value: str) -> str:
    """Treat all authored text as text, including in tables and HTML disclosure blocks."""
    return re.sub(r"([\\`*_{}\[\]()#+!|>~])", r"\\\1", html.escape(value)).replace("\n", " ")


def link(label: str, url: str) -> str:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or not parsed.path.startswith("/Ise-Tom/Babel/")
    ):
        raise ValueError("Report links must stay within the HTTPS project repository")
    return f"[{escaped(label)}](<{quote(url, safe=':/#?=&%+-._~')}>)"


def source_links(items: list[dict[str, str]]) -> str:
    return " · ".join(link(item["path"], item["url"]) for item in items)


def render(data: dict[str, Any], *, preview: bool = False) -> str:
    phases = data["phases"]
    work = data["workItems"]
    problems = data["problems"]
    features = {item["id"]: item for item in data["features"]}
    snapshot = data["snapshot"]
    accepted = sum(phase["status"] == "accepted" for phase in phases)
    revision = data["buildRevision"]
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Invalid source revision")
    lines = [
        "<!-- Generated report. Edit canonical phase documents and dashboard/progress.json. -->",
        "# Babel project dashboard",
        "",
        "Read this page in your browser using the repository's existing GitHub access. "
        "Bookmark this URL; no download or additional account is needed.",
        "",
        "> **Development preview.** Automatic updates start after the dashboard PR is merged."
        if preview
        else "> Updated automatically after the full CI gate passes on main. "
        "A failed build preserves the last published report.",
        "",
        f"Report source: {link(revision[:7], f'{REPO}/tree/{revision}')}. "
        f"Recorded implementation evidence: {escaped(snapshot['date'])}, "
        f"{link(snapshot['commit'][:7], f'{REPO}/tree/{snapshot["commit"]}')}. "
        "These are separate revisions. "
        "Rebuilding does not accept requirements or refresh evidence.",
        "",
        f"**{len(phases)} phases · {sum(len(p['steps']) for p in phases)} substeps · "
        f"{len(features)} features · {accepted} phases accepted · "
        f"{len(work)} recorded increments · "
        f"{sum(p['status'] == 'open' for p in problems)} open problems**",
        "",
        "Implemented increments can be narrower than their parent requirement. "
        "Design records and passing CI do not establish AD compatibility or production readiness.",
        "",
        f"**Current focus:** Phase {data['focusPhase']:02} — {escaped(data['focusSummary'])}",
        "",
        "[Phase board](#phase-board) · [Implementation journal](#implementation-journal) · "
        "[Problems encountered](#problems-encountered) · [Feature catalog](#feature-catalog)",
        "",
        "Use your browser's Find command to search. Expand a phase's substeps to read its details. "
        "The standalone HTML adds interactive search/filtering and JSON export; "
        "this GitHub view is the persistent report.",
        "",
        "## Phase board",
        "",
        "| Phase | Status | Accepted substeps | Recorded increments |",
        "| --- | --- | --- | --- |",
    ]
    for phase in phases:
        number = phase["id"]
        count = sum(step["status"] == "accepted" for step in phase["steps"])
        increments = sum(
            any(r.startswith(f"P{number:02}-") for r in item["requirements"]) for item in work
        )
        lines.append(
            f"| [{number:02} · {escaped(phase['title'])}](#phase-{number:02}) "
            f"| {LABELS[phase['status']]} | {count}/{len(phase['steps'])} | {increments} |"
        )
    for phase in phases:
        number = phase["id"]
        lines.extend(
            [
                "",
                f"## Phase {number:02}",
                "",
                f"**{escaped(phase['title'])} — {LABELS[phase['status']]}**",
                "",
                link("Canonical design and dependencies", phase["url"]),
                "",
                "<details>",
                f"<summary>{len(phase['steps'])} substeps, "
                "associated features and evidence</summary>",
                "",
            ]
        )
        for step in phase["steps"]:
            lines.extend(
                [
                    f"### {escaped(step['id'])}",
                    "",
                    f"**{escaped(step['title'])} — {LABELS[step['status']]}**",
                    "",
                    escaped(step["note"]),
                    "",
                    "**Associated features:** "
                    + "; ".join(
                        link(
                            f"{identifier}: {features[identifier]['title']}",
                            features[identifier]["url"],
                        )
                        for identifier in step["features"]
                    ),
                    "",
                    f"**Acceptance evidence required:** {escaped(step['verification'])}",
                    "",
                ]
            )
            if step["acceptance"]:
                proof = step["acceptance"]
                lines.extend(
                    [
                        f"**Acceptance review:** {escaped(proof['reviewer'])}, "
                        f"{escaped(proof['date'])}. {escaped(proof['evidence'])}",
                        "",
                    ]
                )
            associated = [item for item in work if step["id"] in item["requirements"]]
            lines.append(
                "**Implementation explanations:** "
                + "; ".join(
                    f"{escaped(item['id'])}: {escaped(item['title'])}" for item in associated
                )
                + ". See the [implementation journal](#implementation-journal)."
                if associated
                else "No implemented increment is recorded for this substep."
            )
            lines.append("")
        lines.extend(["</details>", ""])
    lines.extend(["## Implementation journal", ""])
    for item in work:
        lines.extend(
            [
                f"### {escaped(item['id'])} · {escaped(item['title'])}",
                "",
                "**Design recorded**" if item["kind"] == "design" else "**Implemented increment**",
                "",
                f"**Substeps:** {', '.join(escaped(r) for r in item['requirements'])}",
                "",
                f"**How it was done:** {escaped(item['how'])}",
                "",
                f"**Recorded validation:** {escaped(item['verification'])}",
                "",
                f"**Limits and remaining work:** {escaped(item['limitations'])}",
                "",
                "**Problems:** "
                + (", ".join(escaped(p) for p in item["problems"]) or "None recorded"),
                "",
                f"**Source evidence:** {source_links(item['sources'])}",
                "",
            ]
        )
    lines.extend(["## Problems encountered", ""])
    for problem in problems:
        lines.extend(
            [
                f"### {escaped(problem['id'])} · {escaped(problem['title'])}",
                "",
                f"**{escaped(problem['status'].capitalize())}** · "
                f"Phases {', '.join(f'{p:02}' for p in problem['phases'])}",
                "",
                escaped(problem["detail"]),
                "",
                f"**Resolution:** {escaped(problem.get('resolution') or 'Still open')}",
                "",
                f"**Next action:** {escaped(problem['next_action'])}",
                "",
                f"**Provenance:** {escaped(problem['provenance'])}",
                "",
                source_links(problem["sources"]),
                "",
            ]
        )
    lines.extend(
        [
            "## Feature catalog",
            "",
            "| Feature | Capability | Acceptance evidence |",
            "| --- | --- | --- |",
        ]
    )
    for feature in features.values():
        lines.append(
            f"| {link(feature['id'], feature['url'])} | {escaped(feature['title'])} "
            f"| {escaped(feature['verification'])} |"
        )
    lines.extend(
        [
            "",
            "## Recorded CI observation",
            "",
            f"{link('Evidence snapshot CI', snapshot['ci_url'])}: "
            f"{escaped(snapshot['ci_result'])}, {snapshot['checks_passed']} passing checks "
            f"when checked. {escaped(snapshot['note'])}",
            "",
            link(
                "Dashboard maintenance and interactive build guide",
                f"{REPO}/blob/{revision}/docs/project-dashboard.md",
            ),
            "",
            "Generated from reviewed repository facts. "
            "This report does not query live CI in the browser. "
            "Edit the source facts through a PR; the dashboard-live branch is owned by automation.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/dashboard.md")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        render(build(ROOT, args.revision), preview=args.preview), encoding="utf-8"
    )
    print(f"Rendered private dashboard: {args.output}")
