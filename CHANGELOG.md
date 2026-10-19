# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- README section "What the skills run and send", listing every command and outside service the skills use.
- OpenSSF Scorecard badge in the README.

### Changed

- CI installs its Python and npm tools from hash-locked files in `ci/`.

## [0.2.0] - 2026-10-18

### Added

- GitHub connector fallback: when `gh` is unavailable, the skills read files, issues, pull requests, releases, and repository metadata through GitHub MCP tools. Settings the connector cannot see are reported as Unknown.
- Audit reports end with a "How to check the Unknowns" list: one read-only command or settings path for each check the data source could not see.
- Eval case `audit-connector-fallback` (29 cases in total).

### Changed

- Skills create commits, pull requests, issues, and release notes under the user's identity only, with no AI co-author or "Generated with" line, unless the user asks for attribution or another project's policy requires AI disclosure.

## [0.1.0] - 2026-10-18

### Added

- Nine skills: `github-repo-audit`, `github-readme-writer`, `github-community-files`, `github-discoverability`, `github-release-writer`, `github-repo-hardening`, `github-profile-optimizer`, `github-repo-family`, and `github-upstream-contributor`.
- `github-repo-hardening`: rulesets, secret scanning and push protection, Dependabot with cooldown, private vulnerability reporting, CodeQL, Actions pinning and permissions, and OpenSSF Scorecard, with a read-only posture collector.
- Shared references: operating rules, verified GitHub facts, writing style, and badge guidance.
- `collect_repo_facts.sh`: read-only GitHub data collection for audits.
- `lint_readme.py`: a deterministic README checker used by `github-readme-writer`.
- README guidance: honest status labels, a Maintainers section, and architecture diagram rules. Profile README styles. Listing beyond GitHub. Socialify and release-drafter as options.
- `scripts/check_skills.py`: frontmatter, link, symlink, README, manifest, and eval-coverage checks, run in CI with the official `skills-ref` validator and `reuse lint`.
- Plugin evals: 28 cases, three or more per skill.
- OpenSSF Scorecard workflow for this repository.
- REUSE licensing: MIT for the package, CC0-1.0 for `skills/*/templates/`, CC-BY-SA-4.0 for `CODE_OF_CONDUCT.md`.

[Unreleased]: https://github.com/andrew-abdelmalak/github-presence-skills/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/andrew-abdelmalak/github-presence-skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/andrew-abdelmalak/github-presence-skills/releases/tag/v0.1.0
