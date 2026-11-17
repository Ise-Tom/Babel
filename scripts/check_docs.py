"""Check inline local Markdown file links; external URLs/fragments need separate review."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check(root: Path) -> list[str]:
    errors = []
    for document in root.rglob("*.md"):
        if any(part.startswith(".") for part in document.relative_to(root).parts):
            continue
        text = re.sub(r"```.*?```", "", document.read_text(encoding="utf-8"), flags=re.S)
        for match in re.finditer(r"!?\[[^\]]*\]\(([^\s)]+)\)", text):
            link = match.group(1).strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (document.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                errors.append(f"{document.relative_to(root)}: invalid local link {link}")
    return errors


if __name__ == "__main__":
    failures = check(ROOT)
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print("Local Markdown file links passed (external URLs and anchors not checked)")
