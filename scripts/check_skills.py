#!/usr/bin/env python3
"""Validate the skill package. Exit 1 with one line per problem.

Checks:
  1. Every skills/*/SKILL.md has YAML frontmatter that a strict loader parses,
     follows the Agent Skills naming rules, and stays within size limits.
     `claude plugin validate` does not check skill frontmatter (verified with
     Claude Code 2.1.284), and a skill whose frontmatter fails to parse is
     skipped silently at load time.
  2. Relative Markdown links and #anchors resolve (code blocks and templates
     are skipped: template links point into the user's repository).
  3. .claude/skills/<name> is a symlink to ../../skills/<name> for every skill.
  4. README.md links every skill, and only real ones.
  5. plugin.json and marketplace.json agree on name and version.
  6. Every skill has at least three eval cases under evals/<name>/.

Usage: python3 scripts/check_skills.py [--self-test]
Requires PyYAML (pip install pyyaml).
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_KEYS = {  # the Agent Skills spec set, enforced by skills-ref
    "name", "description", "license", "compatibility", "metadata", "allowed-tools",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
MIN_EVALS = 3


def strip_code(text: str) -> str:
    """Blank out fenced code blocks and inline code, keeping line count."""
    out, fence = [], None
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = m.group(2)
            out.append("")
            continue
        if fence is not None:
            if (
                m
                and m.group(2)[0] == fence[0]
                and len(m.group(2)) >= len(fence)
                and not line.strip()[len(m.group(2)) :].strip()
            ):
                fence = None
            out.append("")
            continue
        out.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def slug(heading: str) -> str:
    """GitHub-style heading anchor."""
    text = re.sub(r"<[^>]+>", "", heading).strip().lower()
    text = re.sub(r"[`*_]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", text)
    kept = "".join(c for c in text if c in " -_" or unicodedata.category(c)[0] in "LN")
    return kept.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    """Collect the GitHub-style anchors for every heading in a Markdown file.

    Args:
        path: The Markdown file to scan.

    Returns:
        The set of anchor slugs, with -1, -2 suffixes for repeated headings.
    """
    seen: dict[str, int] = {}
    result = set()
    for line in strip_code(path.read_text(encoding="utf-8")).splitlines():
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        base = slug(m.group(1))
        n = seen.get(base, 0)
        seen[base] = n + 1
        result.add(base if n == 0 else f"{base}-{n}")
    return result


def check_frontmatter(skill_md: Path, problems: list[str]) -> None:
    """Validate one SKILL.md frontmatter block against the naming and size rules.

    Args:
        skill_md: Path to the SKILL.md file.
        problems: List that receives one message per problem found.
    """
    rel = skill_md.relative_to(ROOT)
    text = skill_md.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    if not m:
        problems.append(f"{rel}: no YAML frontmatter block")
        return
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        problems.append(
            f"{rel}: frontmatter does not parse ({str(exc).splitlines()[0]})"
        )
        return
    if not isinstance(data, dict):
        problems.append(f"{rel}: frontmatter is not a mapping")
        return
    for key in sorted(set(data) - KNOWN_KEYS):
        problems.append(f"{rel}: unknown frontmatter key '{key}'")
    name, desc = data.get("name"), data.get("description")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        problems.append(f"{rel}: name must be 1-64 chars of a-z, 0-9, single hyphens")
    elif name != skill_md.parent.name:
        problems.append(
            f"{rel}: name '{name}' does not match directory '{skill_md.parent.name}'"
        )
    elif "claude" in name or "anthropic" in name:
        problems.append(f"{rel}: name contains a reserved word")
    if not isinstance(desc, str) or not desc.strip():
        problems.append(f"{rel}: description is missing or empty")
        return
    if len(desc) > 1024:
        problems.append(f"{rel}: description is {len(desc)} chars (max 1024)")
    if re.search(r"<[A-Za-z/][^>]*>", desc):
        problems.append(f"{rel}: description contains an XML-like tag")
    if "—" in desc or "–" in desc:
        problems.append(f"{rel}: description contains an em or en dash")
    if "Not for" not in desc:
        problems.append(
            f"{rel}: description lacks a 'Not for ... (use ...)' disambiguation"
        )
    body_lines = text[m.end() :].count("\n")
    if body_lines > 500:
        problems.append(f"{rel}: body is {body_lines} lines (keep under 500)")


def check_links(md: Path, problems: list[str]) -> None:
    """Check that relative links and anchors in a Markdown file resolve.

    Args:
        md: The Markdown file to check.
        problems: List that receives one message per broken link.
    """
    rel = md.relative_to(ROOT)
    for lineno, line in enumerate(
        strip_code(md.read_text(encoding="utf-8")).splitlines(), 1
    ):
        for target in LINK_RE.findall(line):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or "{{" in target:
                continue
            path_part, _, anchor = target.partition("#")
            dest = md if not path_part else (md.parent / path_part).resolve()
            if not dest.exists():
                problems.append(f"{rel}:{lineno}: broken link '{target}'")
            elif (
                anchor
                and dest.is_file()
                and dest.suffix == ".md"
                and anchor not in anchors(dest)
            ):
                problems.append(
                    f"{rel}:{lineno}: missing anchor '#{anchor}' in {path_part or md.name}"
                )


def main() -> int:
    """Run every package check and print the problems found.

    Returns:
        The process exit code: 0 when clean, 1 when any problem is found.
    """
    problems: list[str] = []
    skills = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        problems.append("no skills found under skills/")

    for name in skills:
        check_frontmatter(ROOT / "skills" / name / "SKILL.md", problems)
        link = ROOT / ".claude" / "skills" / name
        if not link.is_symlink() or os.readlink(link) != f"../../skills/{name}":
            problems.append(
                f".claude/skills/{name}: must be a symlink to ../../skills/{name}"
            )
        cases = [
            d
            for d in (ROOT / "evals" / name).glob("*")
            if (d / "case.yaml").exists() or (d / "prompt.md").exists()
        ]
        if len(cases) < MIN_EVALS:
            problems.append(
                f"evals/{name}: {len(cases)} cases (need at least {MIN_EVALS})"
            )
    mirror = ROOT / ".claude" / "skills"
    for extra in sorted(p.name for p in mirror.iterdir()) if mirror.is_dir() else []:
        if extra not in skills:
            problems.append(f".claude/skills/{extra}: no matching skill")

    for md in sorted(ROOT.rglob("*.md")):
        parts = md.relative_to(ROOT).parts
        if ".git" in parts or "results" in parts or "templates" in parts:
            continue
        check_links(md, problems)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"\(skills/([a-z0-9-]+)/SKILL\.md\)", readme))
    for name in sorted(set(skills) - listed):
        problems.append(f"README.md: skill '{name}' is not linked")
    for name in sorted(listed - set(skills)):
        problems.append(f"README.md: links unknown skill '{name}'")

    plugin = json.loads(
        (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    market = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    entry = next(
        (p for p in market.get("plugins", []) if p.get("name") == plugin["name"]), None
    )
    if entry is None:
        problems.append("marketplace.json: no entry named like plugin.json")
    elif entry.get("version") != plugin.get("version"):
        problems.append(
            f"version mismatch: plugin.json {plugin.get('version')} vs marketplace.json {entry.get('version')}"
        )

    for p in problems:
        print(p)
    print(f"{len(skills)} skills checked, {len(problems)} problem(s)")
    return 1 if problems else 0


def self_test() -> None:
    """Run built-in assertions for the slug and code-stripping helpers."""
    assert slug("Example 1: new README for a CLI") == "example-1-new-readme-for-a-cli"
    assert slug("A. Front door") == "a-front-door"
    assert slug("When to move docs to a site") == "when-to-move-docs-to-a-site"
    code = "text\n````markdown\n[x](missing.md)\n```bash\nls\n```\n````\n[y](z.md)"
    stripped = strip_code(code)
    assert "missing.md" not in stripped and "z.md" in stripped, stripped
    assert strip_code("see `[a](b)` here") == "see  here"
    print("self-test passed")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
        sys.exit(0)
    sys.exit(main())
