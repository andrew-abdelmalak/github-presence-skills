# Topics and description

## Contents

- [Where these fields appear](#where-these-fields-appear)
- [Description](#description)
- [Topics](#topics)
- [Names](#names)

## Where these fields appear

- The **description** shows under the repository name in search results, on profiles and pinned cards, in topic listings, and in the default link preview text.
- **Topics** link the repository into topic pages (`github.com/topics/NAME`), and they can be searched with `topic:NAME`.
- Repository search can also match the name, the description, and the README (`in:name`, `in:description`, `in:topics`, `in:readme` qualifiers).

GitHub does not publish how it ranks results. Write for people first.

## Description

**Formula:** `[What it is] that/for [what it does or who it serves] [key differentiator]`.

| Weak | Why | Strong |
|---|---|---|
| "my log tool" | Says nothing | "CLI that cuts large log files to a time window or request ID without loading them into memory" |
| "A blazing fast, modern, powerful queue" | Hype, no information | "Dependency-free job queue for Python scripts, backed by SQLite" |
| "Fluxboard" | Restates the name | "Self-hosted dashboard for monitoring webhook deliveries and retries" |
| "React + Node + Mongo + Docker app" | A stack, not a purpose | "Recipe planner that builds a weekly shopping list (React, Node, MongoDB)" |

Rules:
- One sentence. Aim for about 60 to 160 characters. This range is a heuristic: long descriptions get cut off in cards and previews.
- Put the main search term early: the words a user would type, such as "CLI", "Python library", or "dashboard".
- No trailing hashtags or emoji strings. One leading emoji is acceptable if the owner wants it.
- Use the same sentence as the README's one-line description, or a close variant.

## Topics

Aim for 8 to 15 topics. GitHub allows 20, but each one should earn its place. Cover these categories:

| Category | Examples | Notes |
|---|---|---|
| Language / runtime | `python`, `typescript`, `rust`, `nodejs` | Match the primary language |
| Framework / platform | `django`, `react`, `kubernetes`, `claude-code` | Only frameworks the project is built on or for |
| Project type | `cli`, `library`, `api`, `template`, `dataset`, `github-action`, `vscode-extension` | Helps people filter |
| Domain / problem | `log-analysis`, `job-queue`, `static-site-generator` | The most valuable category. Use the words users search for. |
| Audience / field | `devops`, `bioinformatics`, `education` | When the audience is specific |
| Ecosystem / distribution | `pypi`, `npm-package`, `homebrew` | Only when published there |

Check candidates with the commands in SKILL.md step 4:
- **`curated: true`** means GitHub maintains a topic page with a description, a strong signal that the spelling is the accepted one.
- **Usage count** (`search/repositories?q=topic:NAME`): among synonyms, the most-used spelling is the one people browse. A topic used by only a handful of repositories helps only if it is truly the project's niche term.

Avoid:
- **Synonym splitting:** `ml`, `machinelearning`, and `machine-learning` together. Pick the established one.
- **Owner or brand names,** unless the project belongs to an ecosystem users browse by that name.
- **Meaningless topics:** `project`, `code`, `github`, `open-source` (on its own), `2026`.
- **Event topics** (`hacktoberfest`) unless participating, and `awesome` unless the repository is an awesome list.

Topic format: lowercase letters, numbers, and hyphens, 50 characters or less, at most 20 (see [github-facts.md](shared/github-facts.md#repository-metadata)).

## Beyond GitHub

Some audiences find projects through curated lists and registries rather than GitHub search. Recommend a listing only when the project meets the list's published inclusion criteria.

| Channel | When it fits | How |
|---|---|---|
| Curated "awesome" lists for the project's topic | The project is useful, documented, and maintained, and the list's criteria (stars, age, license) are met | One pull request per list, following its CONTRIBUTING. This is a remote change, drafted with `github-upstream-contributor` etiquette. |
| The ecosystem's package registry (npm, PyPI, crates.io, and so on) | The project is installable | Set the registry page as the repository website once published |
| Ecosystem directories, such as plugin and skill marketplaces | The project is a plugin, extension, or skill | Follow each directory's submission process |
| GitHub topic pages | Always | Covered by topics above |

Rules:
- Never submit to lists the project does not qualify for, and never open near-identical pull requests across many lists at once. Both count as spam to maintainers.
- Prefer two or three well-matched lists over a broad blast.
- Re-check each list's current submission rules before drafting. They change.

## Names

A good repository name is lowercase, hyphen-separated, pronounceable, and matches the package or command name when one exists. Avoid:
- Generic names (`utils`, `tool`, `app`).
- Version or status words (`-v2`, `-final`, `-new`, `-test`).
- Names that imply an affiliation the project lacks, such as using a company's trademark as the first word.

Renaming has costs (see [github-facts.md](shared/github-facts.md#repository-metadata)): GitHub Pages project URLs change, and other repositories' `uses:` references to actions in this repository break. Recommend a rename only for young or misleadingly named projects, and list these costs with the recommendation. Renaming is a remote change that needs approval:

```bash
gh repo rename NEW-NAME --repo OWNER/OLD-NAME
```
