# README writer examples

Both examples use fictional repositories under `acme-labs`.

## Contents

- [Example 1: new README for a CLI](#example-1-new-readme-for-a-cli)
- [Example 2: improve mode](#example-2-improve-mode)

## Example 1: new README for a CLI

**Input**

> Write a README for this repo. It's going public next week.

**What the inventory found**

| Fact | Source |
|---|---|
| Name `logslice`, version `0.3.0` | `pyproject.toml` `[project]` |
| Requires Python 3.10 or later, no runtime dependencies | `requires-python = ">=3.10"`, empty `dependencies` |
| CLI entry point `logslice = "logslice.cli:main"` | `[project.scripts]` |
| Flags `--from`, `--to`, `--request-id`, `--format {auto,json,clf}`, `-o/--output` | `argparse` setup in `logslice/cli.py` |
| Error `could not detect timestamp format; pass --format` | `logslice/detect.py` line 58 |
| Tests on Python 3.10 to 3.13 | `.github/workflows/tests.yml` matrix |
| Apache-2.0 | `LICENSE` |
| Not on PyPI | `pip index versions logslice` returned no match; no publish job in CI |
| Remote `acme-labs/logslice` | `git remote get-url origin` |
| `CONTRIBUTING.md` absent | Glob |

Type: **CLI tool**. Sections from the CLI column of [project-types.md](project-types.md#sections-per-type).

**Output: README.md**

````markdown
# logslice

Cut large log files down to a time window or a request ID, without loading them into memory.

[![tests](https://github.com/acme-labs/logslice/actions/workflows/tests.yml/badge.svg)](https://github.com/acme-labs/logslice/actions/workflows/tests.yml)
[![License](https://img.shields.io/github/license/acme-labs/logslice)](LICENSE)

<!-- TODO: add a short terminal recording of the quick start, for example docs/images/demo.gif -->

`logslice` streams a log file line by line and keeps only the lines inside a time range or tied to one request. It reads JSON logs and Common Log Format, detects which one it is given, and never holds the whole file in memory, so multi-gigabyte files work on a laptop. Use it when `grep` is not enough because you need time ranges, not text matches.

## Requirements

- Python 3.10 or later
- No other dependencies

## Install

```bash
pipx install git+https://github.com/acme-labs/logslice
```

<!-- TODO: add `pipx install logslice` once the package is published on PyPI -->

## Quick start

Keep the five minutes around an incident from a JSON log:

```bash
logslice app.log --from "2026-03-14T09:55:00Z" --to "2026-03-14T10:00:00Z" -o incident.log
```

## Usage

### Follow one request

```bash
logslice app.log --request-id 7f3c2a91
```

### Read from standard input

```bash
zcat app.log.gz | logslice - --from "2026-03-14T09:55:00Z"
```

<!-- TODO: confirm that "-" reads standard input; cli.py passes the path to open(), so this example needs checking before release -->

### Force the log format

`--format` accepts `auto` (default), `json`, or `clf`.

```bash
logslice access.log --format clf --from "14/Mar/2026:09:55:00 +0000"
```

## Options

| Option | Default | Description |
|---|---|---|
| `--from TIME` | start of file | Keep lines at or after this time |
| `--to TIME` | end of file | Keep lines before this time |
| `--request-id ID` | none | Keep only lines with this request ID |
| `--format {auto,json,clf}` | `auto` | Log format. `auto` inspects the first lines. |
| `-o, --output PATH` | standard output | Write matching lines to a file |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `could not detect timestamp format; pass --format` | The first lines match neither JSON nor Common Log Format | Pass `--format json` or `--format clf` explicitly |

## Contributing

Issues and pull requests are welcome. Run the test suite with `pytest` before opening a pull request.

<!-- TODO: add CONTRIBUTING.md (run github-community-files) and link it here -->

## License

Released under the [Apache License 2.0](LICENSE).
````

**Placeholders to fill**
- A demo GIF of the quick start (optional, but it helps a CLI).
- The PyPI install line, once the package is published.
- Confirm that `-` reads standard input. The code passes the path straight to `open()`, so the example may be wrong. Fix the code or drop the example.
- A CONTRIBUTING.md to link from the Contributing section.

**Next step:** run `github-discoverability` to set the description to the README's first line and add topics.

Note how the skill handled facts:
- **Unconfirmed behavior:** the standard-input example was kept with a `TODO`, because reading the code raised doubt. It was not presented as working.
- **Unverified channel:** there is no PyPI badge or `pip install logslice`, because publication could not be verified.
- **Troubleshooting:** the only row comes from a real error message in the code.

## Example 2: improve mode

**Input**

> My README is a mess, can you improve it? Keep my intro, I like it.

**Existing README, by section**

| Existing section | Lines | Finding |
|---|---|---|
| Logo banner, 1,600 px wide | 1-3 | Pushes the description below the fold |
| "Welcome to Fluxboard!!!" | 5 | Filler opening |
| Intro paragraph | 7-10 | Accurate and in the author's voice. Keep it. |
| 14 badges, including "made with love", visitor count, and 6 language logos | 12-26 | Over the limit. The `build` badge points to a Travis CI config that no longer exists. |
| "Installation": `npm i fluxboard` | 28-31 | `package.json` has `"private": true`. Not published. |
| "API" with 60 functions | 33-410 | Reference material that belongs in docs |
| No license section | | `LICENSE` is MIT |

**Output: change summary, shown before writing**

```markdown
**Kept:** your intro paragraph (lines 7 to 10), unchanged.

**Changed**
- Banner reduced to a 120 px logo beside the title, so the description shows first.
- "Welcome to Fluxboard!!!" replaced by the one-line description: "A self-hosted dashboard for monitoring webhook deliveries."
- Install: replaced `npm i fluxboard` (the package is private, so that command fails) with clone, `npm ci`, and `npm run dev`, all taken from `package.json` scripts.

**Removed**
- 11 badges: 6 language logos, visitor count, "made with love", the stale Travis build badge, stars, and forks. Kept: GitHub Actions `ci.yml` status and License.

**Moved**
- The 60-function API reference moves to `docs/api.md`, linked from a new Documentation section. The README goes from 410 to about 120 lines.

**Added**
- Quick start (`docker compose up`, from `docker-compose.yml`)
- Configuration table built from `.env.example` (8 variables)
- License section (MIT)

Write README.md and docs/api.md now?
```

The skill then writes the files, after the user agrees, through Claude Code's normal permission prompt.
