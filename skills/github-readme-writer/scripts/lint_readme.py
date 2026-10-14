#!/usr/bin/env python3
"""Check a README for problems that do not need judgment. Standard library only.

Errors (exit 1):   no H1, more than one H1, first heading not the H1,
                   unbalanced code fences, unfilled {{TEMPLATE}} tokens,
                   missing relative link or image targets.
Warnings (exit 0): images without alt text, fences without a language,
                   skipped heading levels, more than six badges near the top,
                   hype words from references/writing-style.md, TODO markers,
                   badges for CI services with no matching config, length.

Usage: lint_readme.py README.md [--repo-root DIR] [--json]
       lint_readme.py --self-test
"""

from __future__ import annotations

import json
import re
import sys
from itertools import pairwise
from pathlib import Path

HYPE = re.compile(
    r"\b(blazing(ly)? fast|lightning[- ]fast|revolutionary|game[- ]?changer|cutting[- ]edge|"
    r"next[- ]generation|seamless(ly)?|effortless(ly)?|world[- ]class|supercharge)\b",
    re.IGNORECASE,
)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_IMG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
TOKEN = re.compile(r"\{\{[A-Z0-9_|#: .-]+\}\}")
TODO = re.compile(r"\b(TODO|FIXME|XXX)\b")
BADGE = re.compile(
    r"!\[[^\]]*\]\((https://(img\.shields\.io|github\.com/[^)]+/badge\.svg|[^)]*badge)[^)]*)\)"
)
CI_BADGES = {
    "travis-ci": ".travis.yml",
    "circleci.com": ".circleci",
    "appveyor": "appveyor.yml",
}


def lint(text: str, root: Path | None) -> tuple[list[str], list[str]]:
    """Lint README text.

    Args:
        text: The README content.
        root: Directory that relative links resolve against, or None to skip link checks.

    Returns:
        A pair of (errors, warnings), each a list of human-readable messages.
    """
    errors: list[str] = []
    warnings: list[str] = []
    lines = text.splitlines()
    fence: str | None = None
    prose: list[tuple[int, str]] = []

    for n, line in enumerate(lines, 1):
        m = FENCE.match(line)
        if m:
            marker, info = m.group(1), m.group(2).strip()
            if fence is None:
                fence = marker
                if not info:
                    warnings.append(f"line {n}: code fence without a language")
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not info:
                fence = None
            continue
        if fence is None:
            prose.append((n, line))
    if fence is not None:
        errors.append("unbalanced code fence: a block is never closed")

    headings = [
        (n, len(m.group(1)), m.group(2))
        for n, line in prose
        if (m := HEADING.match(line))
    ]
    h1s = [h for h in headings if h[1] == 1]
    if not h1s:
        errors.append("no H1: start with '# ProjectName'")
    elif len(h1s) > 1:
        errors.append(f"{len(h1s)} H1 headings: use one, then H2 for sections")
    if headings and headings[0][1] != 1:
        errors.append(f"line {headings[0][0]}: the first heading is not the H1")
    for (_, prev, _), (n, level, title) in pairwise(headings):
        if level > prev + 1:
            warnings.append(
                f"line {n}: heading level jumps from H{prev} to H{level} ('{title}')"
            )

    top_badges = sum(len(BADGE.findall(line)) for n, line in prose if n <= 25)
    if top_badges > 6:
        warnings.append(
            f"{top_badges} badges near the top: keep six or fewer real ones"
        )

    for n, line in prose:
        clean = re.sub(r"`[^`]*`", "", line)
        if TOKEN.search(clean):
            errors.append(
                f"line {n}: unfilled template token {TOKEN.search(clean).group(0)}"
            )
        if TODO.search(clean):
            warnings.append(
                f"line {n}: {TODO.search(clean).group(1)} marker left in the README"
            )
        if m := HYPE.search(clean):
            warnings.append(
                f"line {n}: hype word '{m.group(0)}': replace it with a specific fact"
            )
        for tag in HTML_IMG.findall(clean):
            alt = re.search(r'\balt\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
            if not alt or not alt.group(1).strip():
                warnings.append(f"line {n}: <img> without alt text")
        for bang, label, target in MD_LINK.findall(clean):
            if bang and not label.strip():
                warnings.append(f"line {n}: image without alt text ({target})")
            for host, config in CI_BADGES.items():
                if host in target and root is not None and not (root / config).exists():
                    warnings.append(
                        f"line {n}: {host} badge but no {config} in the repository"
                    )
            if root is None or re.match(r"^[a-z][a-z0-9+.-]*:|^#|^//", target):
                continue
            path = target.split("#", 1)[0]
            if path and not (root / path).exists():
                errors.append(f"line {n}: relative target not found: {target}")

    if len(lines) > 400:
        warnings.append(
            f"{len(lines)} lines: consider moving reference material to docs/ or a site"
        )
    if len(text.encode()) > 500 * 1024:
        errors.append("over 500 KiB: GitHub truncates the rendered README")
    return errors, warnings


def self_test() -> None:
    """Run built-in assertions against small fixtures and print a confirmation."""
    good = "# Name\n\nOne line.\n\n## Install\n\n```bash\npip install x\n```\n"
    assert lint(good, None) == ([], []), lint(good, None)
    bad = "## Start\n# A\n# B\n![](x.png)\n```\nno lang\n{{TOKEN}} blazing fast\n"
    errors, warnings = lint(bad, None)
    assert any("2 H1" in e for e in errors) and any(
        "first heading" in e for e in errors
    )
    assert any("unbalanced" in e for e in errors)
    assert any("alt text" in w for w in warnings) and any(
        "without a language" in w for w in warnings
    )
    text = "# T\n\n{{NAME}} and blazing fast\n"
    errors, warnings = lint(text, None)
    assert any("{{NAME}}" in e for e in errors) and any(
        "blazing fast" in w for w in warnings
    )
    print("self-test passed")


def main(argv: list[str]) -> int:
    """Run the linter from the command line.

    Args:
        argv: Command-line arguments without the program name.

    Returns:
        The process exit code: 0 clean or warnings only, 1 errors, 2 bad usage.
    """
    if "--self-test" in argv:
        self_test()
        return 0
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__.strip().splitlines()[-2].strip(), file=sys.stderr)
        return 2
    readme = Path(args[0])
    root = (
        Path(argv[argv.index("--repo-root") + 1])
        if "--repo-root" in argv
        else readme.parent
    )
    errors, warnings = lint(readme.read_text(encoding="utf-8"), root)
    if "--json" in argv:
        print(json.dumps({"errors": errors, "warnings": warnings}, indent=2))
    else:
        for e in errors:
            print(f"ERROR   {e}")
        for w in warnings:
            print(f"WARNING {w}")
        print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
