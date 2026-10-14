# Contributing to github-presence-skills

Bug reports, fixes to skill behavior, better examples, and corrections to GitHub facts are welcome. For a new skill or a large change, open an issue first, so we can check that it fits the package and does not overlap an existing skill.

## Before you start

- Search [existing issues](https://github.com/andrew-abdelmalak/github-presence-skills/issues).
- By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Set up

Requirements: Claude Code, Python 3.10 or later with PyYAML (`pip install pyyaml`), and the GitHub CLI for testing skills that call `gh`.

```bash
git clone https://github.com/andrew-abdelmalak/github-presence-skills.git
cd github-presence-skills
python3 scripts/check_skills.py
```

To try your changes, start Claude Code in a test repository with the plugin loaded from your clone:

```bash
claude --plugin-dir /path/to/github-presence-skills
```

## Conventions

Read [.claude/CLAUDE.md](.claude/CLAUDE.md). It is the full list, and it is what Claude Code reads when it works on this repository. The most important rules:

- **Frontmatter:** `name` matches the directory. `description` is written in the third person, says what the skill does and when to use it, ends with a "Not for X (use Y)" sentence, stays under 1,024 characters, and contains no em dashes.
- **SKILL.md** stays under 500 lines. Detail goes in `references/`, linked one level deep.
- **Facts about GitHub** go in [references/github-facts.md](references/github-facts.md), with a source link. Update the "Last verified" date when you re-check a fact.
- **Every skill has three or more eval cases** in `evals/<skill>/`.
- **Writing** follows [references/writing-style.md](references/writing-style.md).

## Run the checks

```bash
python3 scripts/check_skills.py --self-test
python3 scripts/check_skills.py
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

CI runs the same checks. Evals call the model, so they are not part of CI. Run the cases for the skill you changed before opening a pull request:

```bash
claude plugin eval . --case '<skill-prefix>-*' --runs 1 --ablation none
```

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), for example `fix(readme-writer): keep existing anchors when renaming headings`. Scopes are skill names without the `github-` prefix.

## Open a pull request

1. Branch from `main`.
2. Fill in the pull request template, and link the issue (`Fixes #12`).
3. Add an entry under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE). Contributions to `skills/*/templates/` are also dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), so people can use the templates without attribution.
