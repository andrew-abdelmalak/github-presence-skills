---
name: github-readme-writer
description: "Writes or improves a repository README.md from the project's real files: summary, badges, install, quick start, usage, configuration, feature and troubleshooting tables, contributing, license. Detects the project type and decides when docs belong on a GitHub Pages site instead. Make sure to use this skill whenever the user wants a README written, rewritten, improved, or reviewed, asks how to document a project, or asks whether reference docs belong in the README, even if they only paste a README and ask for feedback. Not for profile READMEs (use github-profile-optimizer) or CONTRIBUTING.md (use github-community-files)."
argument-hint: "[path] [new | improve]"
---

# README writer

Produce a README that tells a first-time visitor what the project is, gets them to a working result in minutes, and points everyone else to the right place. Every command and fact in it comes from the repository.

## When to use

- "Write a README", "my README is bad", "document this project", "make this repo look professional"
- A `github-repo-audit` result lists area B fixes
- A project is about to be published, released, or shared

## Input

- **Path** (default: the current directory) to a local clone. A remote-only repository can be read through `gh`, but local files give better results.
- **Mode**: `new` writes from scratch. `improve` keeps accurate content and fixes the rest. Default to `improve` when a README exists, unless the user asks for a rewrite.
- **Audience** (optional): end users, developers integrating a library, contributors, researchers, or hiring managers. If it is unclear and changes the outcome, ask once.

## Output

1. The README content, written to `README.md` at the repository root (or to its existing location).
2. In `improve` mode, a short change summary before the file: what was kept, changed, added, and removed.
3. The placeholder list, and a docs-site recommendation if the content outgrows one page.

## Workflow

```
README progress:
- [ ] 1. Inventory the repository
- [ ] 2. Classify the project type
- [ ] 3. Build the fact sheet
- [ ] 4. Plan the outline
- [ ] 5. Draft
- [ ] 6. Verify
- [ ] 7. Decide on a docs site
- [ ] 8. Write the file
```

**1. Inventory.** Read whatever of these exists:
- **Existing docs:** README, `docs/`, CHANGELOG
- **Manifests:** `package.json`, `pyproject.toml`, `setup.cfg`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle*`, `Gemfile`, `*.gemspec`, `composer.json`, `*.csproj`, `Dockerfile`, `docker-compose.yml`, `Makefile`, `justfile`
- **Entry points:** `bin` and `scripts` fields, `[project.scripts]`, `cmd/`, `src/main.*`
- **Code and tests:** `examples/`, test files
- **Project files:** `.github/workflows/`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`

Run `git remote get-url origin` for the owner and name. Run `gh repo view --json description,homepageUrl,repositoryTopics,latestRelease` if `gh` is available.

**2. Classify** the project with [references/project-types.md](references/project-types.md). The type decides which sections appear and in what order.

**3. Build a fact sheet** before writing prose. List: name, one-line purpose, audience, prerequisites (runtime and version), install command per channel, the shortest working example, main commands or API entry points, configuration options, license, CI workflow file names, docs URL, and support channel. Record where each fact came from. A fact with no source becomes a `TODO` placeholder.

- **Published packages:** use a registry install command only after confirming the package is published. Evidence is a publish step in CI, a registry link in the docs, or a read-only lookup such as `npm view <name> version`, `pip index versions <name>`, or `cargo search <name> --limit 1`. Otherwise give the from-source install and a `TODO` for the registry command.

**4. Plan the outline** from [references/section-guide.md](references/section-guide.md). In `improve` mode, compare the existing README section by section and mark each **keep**, **fix**, **add**, or **remove**. Accurate content in the author's voice stays.

**5. Draft** from [templates/README.template.md](templates/README.template.md). Follow [writing-style.md](../../references/writing-style.md) and [badges.md](../../references/badges.md).

**6. Verify.** First run the bundled linter, which catches mechanical problems (headings, fences, alt text, unfilled tokens, missing files, hype words):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/lint_readme.py" README.md --repo-root .
```

Fix every error, and fix or justify every warning. Then check the judgment items, and repeat until every item passes:
- Every shell command appears in a manifest, script, Makefile, or CI file, or is a standard command for that ecosystem.
- Every relative link and image path exists (check with Glob).
- Every badge maps to a real workflow, release, registry page, or license.
- The quick start runs top to bottom with no step missing, including environment variables and required services.
- If a heading was renamed, `grep -rn "#old-anchor"` finds no inbound links left broken.
- The [writing-style self-check](../../references/writing-style.md#self-check) passes.

**7. Decide on a docs site.** Apply the rule in [references/section-guide.md](references/section-guide.md#when-to-move-docs-to-a-site). If the content needs a site, keep the README short, link to `docs/`, and include the site recommendation in the response. Do not scaffold the site unless the user asks.

**8. Write the file.** In `improve` mode, show the change summary first. Write `README.md`, any image assets the user supplied, and, if the summary moves reference material out of the README, the `docs/` files that receive it. Other files stay untouched, and missing ones such as CONTRIBUTING.md are mentioned as next steps.

## Hard rules

Shared rules: [operating-rules.md](../../references/operating-rules.md). Additional rules for this skill:

- **No invented commands, versions, or outputs.** If you cannot confirm a command, mark it `TODO`. Show sample output only if you ran the command or the repository documents that output.
- **Keep what is true.** In `improve` mode, never drop accurate technical content just to fit the template. Move it, or recommend moving it to `docs/`.
- **No hand-written table of contents** unless the README has more than about eight H2 sections. GitHub renders an outline automatically.
- **Images:** use only images that exist in the repository or that the user provides, always with alt text. Suggest a screenshot or demo GIF as a `TODO` when the project has a UI or terminal output worth showing.
- **The first lines carry the weight:** the H1, the one-line description, and at most one badge row. No banner image that pushes the description below the fold.

## Example

Input:

> Write a README for this repo.

The repository is a Python CLI. `pyproject.toml` declares `logslice = "logslice.cli:main"`, requires Python 3.10 or later, and has no runtime dependencies. There is a `tests.yml` workflow, an Apache-2.0 LICENSE, and no README.

Output (opening lines):

````markdown
# logslice

Cut large log files down to a time window or a request ID, without loading them into memory.

[![tests](https://github.com/acme-labs/logslice/actions/workflows/tests.yml/badge.svg)](https://github.com/acme-labs/logslice/actions/workflows/tests.yml)
[![License](https://img.shields.io/github/license/acme-labs/logslice)](LICENSE)

## Install

Requires Python 3.10 or later.

<!-- TODO: confirm logslice is published on PyPI; until then the from-source install below is the only verified one -->
```bash
pipx install git+https://github.com/acme-labs/logslice
```
````

The full input and output, and an `improve`-mode example, are in [references/examples.md](references/examples.md).

## Reference files

- [references/section-guide.md](references/section-guide.md): what each section is for, its rules, and when to move docs to a GitHub Pages site
- [references/project-types.md](references/project-types.md): detection signals, section sets per type, and install commands per ecosystem
- [references/examples.md](references/examples.md): a complete new README and an `improve`-mode change summary
- [templates/README.template.md](templates/README.template.md): the skeleton to fill
- `scripts/lint_readme.py`: the deterministic README checker. Run it; do not read it into context. It needs only the Python standard library.

## Related skills

- `github-discoverability`: make the repository description match the README's first line, and set topics
- `github-community-files`: CONTRIBUTING, SECURITY, and other files the README links to
- `github-release-writer`: release badges show "no releases" until a release is published
- `github-repo-family`: the "Related projects" block shared across sibling repositories
