# Changelog format

## Contents

- [Structure](#structure)
- [Mapping changes to categories](#mapping-changes-to-categories)
- [Writing entries](#writing-entries)
- [Automation options](#automation-options)

## Structure

Follow [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/):

- The file is `CHANGELOG.md` at the repository root, written for humans.
- The newest version comes first. Keep an `## [Unreleased]` section at the top for changes not yet released.
- Each version heading has the form `## [1.4.0] - 2026-10-12`, with ISO 8601 dates.
- Within a version, use these categories, in this order, and only when non-empty: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.
- At the bottom, link each version to its comparison:

```markdown
[Unreleased]: https://github.com/OWNER/REPO/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/OWNER/REPO/compare/v1.3.2...v1.4.0
[1.3.2]: https://github.com/OWNER/REPO/releases/tag/v1.3.2
```

Release notes on GitHub can be richer (highlights, migration guides, contributor credits). The changelog stays a compact record.

## Mapping changes to categories

| Signal | Category | In user-facing notes? |
|---|---|---|
| `feat` | Added (or Changed if it alters existing behavior) | Yes |
| `fix` | Fixed | Yes |
| `perf` | Changed | Yes, if users notice it |
| `!` after the type, or a `BREAKING CHANGE:` footer | Changed or Removed, plus a breaking note | Yes, at the top |
| `deprecate` in the message, or a deprecation warning added in code | Deprecated | Yes |
| Removal of a public API, flag, option, or supported platform | Removed | Yes |
| Security fix (label `security`, an advisory link, or a CVE) | Security | Yes. Link the advisory once it is published. |
| `docs` | Usually omitted. Changed if it documents behavior users depend on. | Rarely |
| `refactor`, `test`, `ci`, `build`, `chore`, `style` | Omitted | No, but count them ("plus 7 internal changes") |
| `chore(deps)` or a Dependabot PR | Changed, only when it changes a user-facing requirement (a minimum runtime, a peer dependency) | Only then |
| PR label `enhancement` or `feature` | Added | Yes |
| PR label `bug` | Fixed | Yes |
| PR label `breaking-change` | Breaking note | Yes |

When signals conflict (for example, `fix:` on a change that adds a new option), read the diff and decide. Mark your decision for the user to check.

## Writing entries

- **One line per change,** describing the effect on users: "Jobs no longer retry after `max_attempts` is reached (#52)."
- **Use one tense throughout the file.** Match the existing changelog. For a new file, use the present tense ("Adds", "Fixes") or noun phrases.
- **Name the API, flag, or file** in backticks.
- **Link the pull request** `(#123)` and credit outside contributors: `(#123, @handle)`.
- **Group related commits** into one entry. Five commits that build one feature are one line.
- **For breaking changes,** say what to do, not only what changed.

## Automation options

Name these, then help the user choose. Install nothing without approval.

| Approach | Needs | Best for |
|---|---|---|
| GitHub generated notes + `.github/release.yml` | Labeled pull requests. No commit convention needed. | Teams that already label PRs. The simplest option. |
| [release-drafter](https://github.com/release-drafter/release-drafter) | Labeled pull requests, and an Actions workflow | A draft release that updates as each pull request merges, so the notes are ready when you tag |
| [git-cliff](https://github.com/orhun/git-cliff) | Conventional Commits, or regex rules in `cliff.toml` | Generating CHANGELOG.md from commits, locally or in CI |
| [release-please](https://github.com/googleapis/release-please) | Conventional Commits | A release PR that bumps versions and the changelog. You merge it to release. |
| [semantic-release](https://github.com/semantic-release/semantic-release) | Conventional Commits, CI with publish credentials | Fully automated version, changelog, tag, and package publish on every merge |
| [commitlint](https://github.com/conventional-changelog/commitlint) | Node.js in CI or a commit hook | Enforcing Conventional Commits once adopted |

Decision guide:
- **PRs are labeled:** use generated notes and `release.yml`. No new tooling.
- **The changelog should come from commits, with a human in the loop:** use git-cliff or release-please.
- **Every merge to main should publish:** use semantic-release. Confirm the team wants that level of automation.
- **The history is mixed:** adopt Conventional Commits for new work, and draft notes manually with this skill until the history is consistent.
