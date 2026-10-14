# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Eight skills: `github-repo-audit`, `github-readme-writer`, `github-community-files`, `github-discoverability`, `github-release-writer`, `github-profile-optimizer`, `github-repo-family`, and `github-upstream-contributor`.
- Shared references: operating rules, verified GitHub facts, writing style, and badge guidance.
- `collect_repo_facts.sh`: read-only GitHub data collection for audits.
- `scripts/check_skills.py`: frontmatter, link, symlink, README, manifest, and eval-coverage checks, run in CI.
- Plugin evals: three or more cases per skill.
- `github-repo-hardening`: rulesets, secret scanning and push protection, Dependabot with cooldown, private vulnerability reporting, CodeQL, Actions pinning and permissions, and OpenSSF Scorecard, with a read-only posture collector.
- `lint_readme.py`: a deterministic README checker used by `github-readme-writer`.
- README guidance: honest status labels, a Maintainers section, and architecture diagram rules. Profile README styles. Listing beyond GitHub. Socialify and release-drafter as options.
- REUSE licensing: MIT for the package, CC0-1.0 for `skills/*/templates/`.

[Unreleased]: https://github.com/andrew-abdelmalak/github-presence-skills/commits/main
