# Audit checklist

Every check the audit scores. **Severity** is the default; adjust it with the goal rules at the end. **Verify with** names the field from `collect_repo_facts.sh` (`repo.*`, `community.*`, ...) or the local check. **Fix with** names the skill that writes the fix.

## Contents

- [A. Front door](#a-front-door)
- [B. README](#b-readme)
- [C. Community health](#c-community-health)
- [D. Releases](#d-releases)
- [E. Trust signals](#e-trust-signals)
- [F. Layout](#f-layout)
- [G. Before going public](#g-before-going-public-pre-public-mode)
- [Adjusting severity to the goal](#adjusting-severity-to-the-goal)

Severity levels:
- **Critical**: a first-time visitor cannot tell what the project is or legally use it, or something is leaking.
- **Important**: visitors can use the project, but contributors or careful adopters will hesitate.
- **Nice**: polish.

## A. Front door

| ID | Check | Severity | Verify with | Fix with |
|---|---|---|---|---|
| A1 | The description is set and says what the project is, in one specific sentence (not just the repository name restated) | Critical | `repo.description` | `github-discoverability` |
| A2 | 5 to 20 topics are set, covering language, domain, and project type | Important | `repo.repositoryTopics` | `github-discoverability` |
| A3 | The website field points to docs, a demo, or a package page when one exists | Nice | `repo.homepageUrl`; look for a docs site or published package | `github-discoverability` |
| A4 | A custom social preview image is set | Nice (Important before a public launch) | `repo.usesCustomOpenGraphImage` | `github-discoverability` |
| A5 | The name is readable and searchable: lowercase, hyphen-separated, and free of words like `test`, `final`, or `new` | Nice | `repo.name` | `github-discoverability` (warn about rename side effects) |

## B. README

| ID | Check | Severity | Verify with | Fix with |
|---|---|---|---|---|
| B1 | A README exists in `.github/`, root, or `docs/` | Critical | Local Glob, or `community.files.readme` | `github-readme-writer` |
| B2 | The first paragraph says what the project does and who it is for | Critical | Read the first 20 lines | `github-readme-writer` |
| B3 | Install or setup steps exist, and their commands match the manifests and scripts | Critical | Compare the README commands with `package.json`, `pyproject.toml`, `Cargo.toml`, `Makefile`, and similar files | `github-readme-writer` |
| B4 | At least one runnable usage example | Important | Code block after the install steps | `github-readme-writer` |
| B5 | Relative links and images resolve | Important | Glob each relative path | `github-readme-writer` |
| B6 | Badges, if any, are backed by real services and number six or fewer per row | Nice | Compare with [badges.md](../../../references/badges.md) | `github-readme-writer` |
| B7 | The license statement matches the LICENSE file | Nice | README text against `repo.licenseInfo` | `github-readme-writer` |
| B8 | Size and scope: well under 500 KiB, and long reference material is moved to `docs/` or a docs site | Nice | File size, heading count | `github-readme-writer` |

## C. Community health

| ID | Check | Severity | Verify with | Fix with |
|---|---|---|---|---|
| C1 | A LICENSE file that GitHub detects | Critical | `repo.licenseInfo` not null, or a root `LICENSE*` | `github-community-files` |
| C2 | `CONTRIBUTING.md` with real setup, test, and pull request steps | Important | `community.files.contributing`, local file | `github-community-files` |
| C3 | `SECURITY.md` and private vulnerability reporting enabled | Important | `repo.isSecurityPolicyEnabled`, `private_vulnerability_reporting.enabled` | `github-community-files` |
| C4 | `CODE_OF_CONDUCT.md` with a working reporting contact | Important | `community.files.code_of_conduct`, then look for an unfilled placeholder such as `[INSERT CONTACT METHOD]` or `[NOTE:` | `github-community-files` |
| C5 | Issue forms, with `config.yml` routing questions elsewhere | Important | `issue_template_dir` (YAML forms and Markdown templates), or local `.github/ISSUE_TEMPLATE/`. `repo.issueTemplates` and `community.files.issue_template` miss YAML issue forms, so use them only to confirm presence, never absence | `github-community-files` |
| C6 | Pull request template | Nice | `repo.pullRequestTemplates` | `github-community-files` |
| C7 | `SUPPORT.md`, or support channels listed in `config.yml` `contact_links` | Nice | Local files | `github-community-files` |
| C8 | `CODEOWNERS` when two or more maintainers own different areas | Nice | Local file | `github-community-files` |
| C9 | `CITATION.cff` for research software and datasets | Nice (N/A otherwise) | Local file | `github-community-files` |
| C10 | `good first issue` label exists, with open issues, when contributors are wanted | Nice | `labels`, `good_first_issues_open` | `github-community-files` (labels guidance) |

## D. Releases

| ID | Check | Severity | Verify with | Fix with |
|---|---|---|---|---|
| D1 | Version tags have published GitHub Releases, not only tags | Important | `tags` against `releases` | `github-release-writer` |
| D2 | Release notes or `CHANGELOG.md` describe user-facing changes, not only commit lists | Important | Release bodies, local `CHANGELOG.md` | `github-release-writer` |
| D3 | Version numbers follow one scheme (SemVer or CalVer) consistently | Nice | Tag names | `github-release-writer` |
| D4 | The latest release is not far behind the default branch for a project that ships to users | Nice | `releases[0].published_at` against `repo.pushedAt` | `github-release-writer` |

N/A for projects that do not ship versions, such as personal sites, notes, and course work.

## E. Trust signals

| ID | Check | Severity | Verify with | Fix with |
|---|---|---|---|---|
| E1 | A CI workflow runs tests or builds on pull requests | Important | `workflows`, local `.github/workflows/*.yml` | Out of scope. Point to the project's CI tooling. |
| E2 | Dependency updates are automated (`.github/dependabot.yml` or a Renovate config) | Nice | `github_dir`, root files | `github-repo-hardening` |
| E3 | The default branch has a ruleset or classic protection | Nice (Important when accepting contributions) | `branch_rules`. `null` means Unknown (requires permissions). | `github-repo-hardening` |
| E4 | No tracked secrets: `.env`, private keys, `*.pem`, cloud credential files | Critical | `git ls-files` pattern match. Report paths only. | Out of scope. Rotate the secret, then remove it from history. |
| E5 | Maintenance status is stated when the project is unmaintained or archived | Important | `repo.isArchived`; last push more than a year ago without a status note | `github-readme-writer` |
| E6 | Workflows pin third-party actions to commit SHAs, set least-privilege `permissions`, and never check out pull request code under `pull_request_target` | Important (Critical if `pull_request_target` checks out PR code) | Local `.github/workflows/*.yml` | `github-repo-hardening` |
| E7 | Security features on: secret scanning with push protection, Dependabot alerts, private vulnerability reporting (public repositories) | Nice | `github-repo-hardening` collector, or `private_vulnerability_reporting` | `github-repo-hardening` |

## F. Layout

| ID | Check | Severity | Verify with | Fix with |
|---|---|---|---|---|
| F1 | The root holds entry-point files only (README, LICENSE, manifests, config). Stray scripts, notes, and data live in folders. | Nice | `root_files` | Describe the moves. Do not perform them. |
| F2 | Build output and dependencies are not tracked (`node_modules/`, `dist/`, `.venv/`, `target/`, `__pycache__/`) and are listed in `.gitignore` | Important | `git ls-files`, `.gitignore` | Describe the fix |
| F3 | No tracked file above 50 MiB. GitHub blocks files above 100 MiB. | Important | `git ls-files -z \| xargs -0 du -k` or similar, sorted | Suggest Git LFS or release assets |
| F4 | `.github/` holds workflows and templates, not unrelated files | Nice | `github_dir` | Describe the moves |
| F5 | Long documentation lives in `docs/` or a docs site, not in a 1,500-line README | Nice | README length, `docs/` | `github-readme-writer` |

## G. Before going public (pre-public mode)

Any finding here **blocks** publishing until resolved. Report the file and line and the kind of finding, never the secret value.

| ID | Check | How |
|---|---|---|
| G1 | No secrets in tracked files | Search tracked files for high-signal patterns: `-----BEGIN .*PRIVATE KEY-----`, `AKIA[0-9A-Z]{16}`, `ghp_[A-Za-z0-9]{36}`, `github_pat_`, `xox[baprs]-`, `sk-[A-Za-z0-9]{20,}`, `AIza[0-9A-Za-z_-]{35}`, and assignments to names containing `password`, `secret`, or `token`. If `gitleaks` is installed, offer `gitleaks detect --source . --redact`. |
| G2 | No secrets in history | Secrets deleted from the current tree remain in history. Offer `gitleaks detect --source . --log-opts="--all" --redact` if installed. Otherwise sample with `git log -p --all -G '<pattern>' --format='%h %an %ad'` for the patterns above. Any hit means: rotate the secret first, then rewrite history or start a fresh repository. |
| G3 | Author emails the owner is comfortable publishing | `git log --all --format='%ae' \| sort -u`. Flag personal or work emails, and suggest the GitHub `noreply` address for future commits. |
| G4 | No internal references | Search for internal hostnames, `localhost` with ports in docs, absolute home paths (`/home/`, `/Users/`, `C:\Users\`), private IP ranges, and internal ticket IDs |
| G5 | License chosen and present | C1 must pass before publishing |
| G6 | Settings decided | Issues on or off, Discussions on or off, and wiki on or off, matching what the README promises |

## Adjusting severity to the goal

| Goal | Raise to Critical | Lower to Nice |
|---|---|---|
| Library or tool for other developers | B3, B4, D1 | A4 |
| Seeking contributors | C2, C5, C10 | D3 |
| Portfolio or job search | A1, B2, A4 | C8, C10 |
| Research software or dataset | C9, D1 | C6 |
| Personal or experimental | none | C2 to C10 (mark N/A when the user says contributions are not wanted) |
