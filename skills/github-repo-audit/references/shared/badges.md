# Badges

Badges are small status images at the top of a README or profile. Used well, they answer "does it build, what version is it, what license is it" at a glance. Used badly, they are a wall of noise or a set of claims nobody can check.

## Rules

1. **Every badge must be backed by something real.** No CI badge without a CI workflow. No coverage badge without a coverage service that receives reports. No package-version badge for a package that is not published. Check each one before adding it.
2. **Show at most six badges in one row.** Pick by reader value, in this order:
   1. Build status
   2. Latest release or package version
   3. License
   4. Supported runtime versions (for libraries)
   5. Coverage (only when tracked)
   6. Downloads or community links
3. **Prefer native URLs.** For GitHub Actions status, use GitHub's own badge endpoint, not a third-party proxy.
4. **Link each badge to its evidence:** the workflow runs, the release page, the license file, the package page.
5. **Give every badge alt text** that reads as a sentence fragment: `alt="CI status"`, not `alt="badge"`.
6. **Keep one style per row.** Do not mix `flat` and `for-the-badge`.
7. **Avoid vanity badges** (stars, followers, profile views, "made with love"). They measure popularity, not quality, and they look desperate on small projects. Include them only when the user asks.

## URL patterns

Replace `OWNER`, `REPO`, `WORKFLOW.yml`, and `PKG` with real values found in the project.

| Badge | Markdown | Requires |
|---|---|---|
| GitHub Actions status | `[![CI](https://github.com/OWNER/REPO/actions/workflows/WORKFLOW.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/WORKFLOW.yml)` | The file `.github/workflows/WORKFLOW.yml` exists |
| Latest GitHub release | `[![Release](https://img.shields.io/github/v/release/OWNER/REPO)](https://github.com/OWNER/REPO/releases/latest)` | At least one published release, not only a tag |
| License | `[![License](https://img.shields.io/github/license/OWNER/REPO)](LICENSE)` | A license GitHub can detect |
| npm version | `[![npm](https://img.shields.io/npm/v/PKG)](https://www.npmjs.com/package/PKG)` | Published on npm |
| PyPI version | `[![PyPI](https://img.shields.io/pypi/v/PKG)](https://pypi.org/project/PKG/)` | Published on PyPI |
| Python versions | `[![Python](https://img.shields.io/pypi/pyversions/PKG)](https://pypi.org/project/PKG/)` | Classifiers declared in package metadata |
| crates.io version | `[![crates.io](https://img.shields.io/crates/v/PKG)](https://crates.io/crates/PKG)` | Published on crates.io |
| Go reference | `[![Go Reference](https://pkg.go.dev/badge/MODULE.svg)](https://pkg.go.dev/MODULE)` | A public Go module |
| Codecov | `[![codecov](https://img.shields.io/codecov/c/github/OWNER/REPO)](https://codecov.io/gh/OWNER/REPO)` | Coverage uploaded to Codecov |
| Static label | `![Label](https://img.shields.io/badge/LABEL-MESSAGE-COLOR)` | Nothing. Use only for facts that do not change, such as "Claude Code skill". |

Notes:
- A GitHub tag without a published release makes the release badge show "no releases". Publishing a release fixes it (see `github-release-writer`).
- In static badges, escape `-` as `--` and `_` as `__`, and write spaces as `_` or `%20`.
- To filter the Actions badge by branch or event, append `?branch=main` or `?event=push` (see [github-facts.md](github-facts.md#readme-rendering)).

## Placement

- **Repository README:** one row directly under the H1, or under the one-line description. Never between install steps.
- **Profile README:** prefer a short line of plain links (blog, email, Mastodon) over technology logo badges. A row of 30 language logos tells a reader nothing about what you can build.
