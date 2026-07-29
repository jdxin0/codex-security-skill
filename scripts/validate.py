#!/usr/bin/env python3
"""Validate the repository's Agent Skills and manifests.

No third-party dependencies — runs on a stock Python 3.10+.
Checks, for every skills/*/SKILL.md:
  - frontmatter block exists and is well formed
  - name matches ^[a-z0-9-]+$ and equals the directory name
  - description is present, non-empty, and <= 1024 characters
  - every referenced references/*.md link resolves to a real file
Plus: all *.json files parse, and install.sh passes `sh -n`.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESC_LIMIT = 1024
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def field(fm: str, key: str) -> str | None:
    """Extract a scalar or folded/blocked value for `key` from frontmatter."""
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    if not m:
        return None
    first = m.group(1).strip()
    if first not in (">-", ">", "|", "|-", ""):
        return first
    # Folded/literal block: gather subsequent more-indented lines.
    lines = fm.splitlines()
    start = next(i for i, ln in enumerate(lines) if re.match(rf"^{key}:", ln))
    body = []
    for ln in lines[start + 1:]:
        if ln.strip() and not ln.startswith((" ", "\t")):
            break
        body.append(ln.strip())
    return " ".join(p for p in body if p).strip()


def validate_skill(skill_md: pathlib.Path) -> None:
    rel = skill_md.relative_to(ROOT)
    fm = frontmatter(skill_md.read_text())
    if fm is None:
        fail(f"{rel}: missing or malformed frontmatter block")
        return

    name = field(fm, "name")
    if not name:
        fail(f"{rel}: frontmatter has no 'name'")
    else:
        if not re.fullmatch(r"[a-z0-9-]+", name):
            fail(f"{rel}: name '{name}' must match ^[a-z0-9-]+$")
        if name != skill_md.parent.name:
            fail(f"{rel}: name '{name}' != directory '{skill_md.parent.name}'")

    desc = field(fm, "description")
    if not desc:
        fail(f"{rel}: frontmatter has no 'description'")
    elif len(desc) > DESC_LIMIT:
        fail(f"{rel}: description is {len(desc)} chars (limit {DESC_LIMIT})")

    for link in re.findall(r"\]\((references/[^)]+)\)", skill_md.read_text()):
        if not (skill_md.parent / link).exists():
            fail(f"{rel}: broken reference link -> {link}")


def main() -> int:
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        fail("no skills found under skills/*/SKILL.md")
    for s in skills:
        validate_skill(s)

    for jf in sorted(ROOT.glob("**/*.json")):
        if any(part in (".git", "codex-security", ".claude") for part in jf.parts):
            continue
        try:
            json.loads(jf.read_text())
        except json.JSONDecodeError as e:
            fail(f"{jf.relative_to(ROOT)}: invalid JSON ({e})")

    install = ROOT / "install.sh"
    if install.exists():
        r = subprocess.run(["sh", "-n", str(install)], capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"install.sh: shell syntax error\n{r.stderr.strip()}")

    if errors:
        print("FAIL — skill validation found problems:\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK — validated {len(skills)} skill(s), manifests, and install.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
