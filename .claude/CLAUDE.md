# Maintainer conventions for github-presence-skills

Read this before changing anything in this repository. These rules keep nine skills consistent and loadable.

This file lives in `.claude/` rather than at the repository root on purpose: the repository root is also the plugin root, and `claude plugin validate` warns about a `CLAUDE.md` at a plugin root.

## Layout

- Skills live in `skills/<name>/`. `.claude/skills/<name>` is a relative symlink to `../../skills/<name>`. Adding or renaming a skill means adding or renaming its symlink. A missing symlink fails silently for anyone using a clone.
- Shared rules live in `references/`, the only place to edit them. Each skill holds a generated copy in `skills/<name>/references/shared/`, so a skill installed on its own (for example with `npx skills add`) keeps its rules. Skills cite the copy as `references/shared/<file>.md` from `SKILL.md`, and as `shared/<file>.md` from a skill's own `references/` files. After editing `references/`, run `python3 scripts/check_skills.py --sync-shared`; CI fails if a copy drifts or a link leaves its skill folder.
- `templates/` holds files that a skill fills in for the user's repository. Links inside templates point into that repository, so `check_skills.py` does not check them.

## Skill rules

- **Frontmatter:** `name` equals the directory name, using lowercase letters, digits, and single hyphens, and never contains "claude" or "anthropic". `description` is in the third person, says what the skill does and when to use it, ends with "Not for X (use Y)", stays under 1,024 characters (aim for about 500), and contains no em or en dashes and no XML tags.
- **Body sections, in order:** When to use, Input, Output, Workflow (with a copyable checklist), Hard rules (starting with the shared-rules link), Example, Reference files, Related skills.
- `SKILL.md` stays under 500 lines. Reference files longer than 100 lines start with a Contents list.
- Bundled scripts are referenced as `${CLAUDE_SKILL_DIR}/scripts/...`, because the working directory is the user's project, not the skill.
- **Remote changes** (`gh repo edit`, `gh release create`, `gh pr create`, `gh api -X ...`, `git push`) are always shown as exact commands and run only after the user's explicit approval. See `references/operating-rules.md`.
- **Platform numbers and rules** come from `references/github-facts.md`. When you add or re-check a fact, include the source and update the "Last verified" date.
- **Examples** use fictional accounts (`acme-labs`, `dmitri-v`) and say so. Real lookups (such as topic counts) carry their date.
- **Descriptions must trigger.** Claude tends to under-trigger skills, so each description includes "Make sure to use this skill whenever the user mentions ...", listing concrete trigger words. Check trigger rates with the `skill-fired` grader in evals after any description change.

## Evals

- Cases live in `evals/<skill>/<case>/case.yaml`, three or more per skill. Case names start with a per-skill prefix: `audit-`, `readme-`, `community-`, `disc-`, `release-`, `hardening-`, `profile-`, `family-`, `upstream-`.
- Each case has a `skill-fired` grader (`tool_used` on `Skill`) plus at least one grader on the result.
- Prompts must contain all facts the skill needs. Eval runs start in an empty workspace with read-only tools, so this also tests the "pasted text" data tier.

## Skill names are public

Renaming a skill breaks users' habits and their eval filters. If you must rename one, update:
1. The directory and the frontmatter `name`
2. The `.claude/skills/` symlink
3. The README skill table and diagram
4. Every cross-reference in other skills' "Related skills" sections and examples
5. `evals/<name>/`, and the `input_match` in its graders
6. CHANGELOG.md

## Versioning

- `version` in `.claude-plugin/plugin.json` and in the `marketplace.json` entry must match. `check_skills.py` enforces this.
- Follow SemVer. Removing or renaming a skill, or changing its approval behavior, is a breaking change.
- Release with the package's own `github-release-writer` skill: update CHANGELOG.md, then `gh release create vX.Y.Z --draft`.

## Before every push

```bash
python3 scripts/check_skills.py --sync-shared   # only after editing references/
python3 scripts/check_skills.py --self-test
python3 scripts/check_skills.py
python3 skills/github-readme-writer/scripts/lint_readme.py README.md --repo-root .
for f in skills/*/scripts/*.sh; do bash -n "$f"; done
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

After a behavior change to a skill, also run its eval cases (`claude plugin eval . --case '<prefix>-*' --runs 1 --ablation none`). Evals cost model usage, so they are not part of CI.
