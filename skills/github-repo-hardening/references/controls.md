# Hardening controls

Each control states what it stops, how to check it, how to apply it, and its limits. API shapes were checked against GitHub's REST OpenAPI description on 2026-10-12.

## Contents

- [Plan limits](#plan-limits)
- [Default-branch ruleset](#default-branch-ruleset)
- [Secret scanning and push protection](#secret-scanning-and-push-protection)
- [Dependabot](#dependabot)
- [Private vulnerability reporting](#private-vulnerability-reporting)
- [CodeQL code scanning](#codeql-code-scanning)
- [GitHub Actions hardening](#github-actions-hardening)
- [OpenSSF Scorecard](#openssf-scorecard)

## Plan limits

| Control | Public repository | Private repository |
|---|---|---|
| Rulesets | Free | GitHub Pro, Team, or Enterprise Cloud |
| Secret scanning | Runs automatically for free | Organization repositories need GitHub Secret Protection |
| Code scanning (CodeQL) | Free | Organization repositories need GitHub Code Security |
| Dependabot alerts and updates | Free | Free |
| Private vulnerability reporting | Free | Not offered |

Source: GitHub Docs feature-availability notes (see [github-facts.md](shared/github-facts.md#security-reporting)). When an API call returns a plan or availability error, report it and the plan that unlocks the control. Do not retry.

## Default-branch ruleset

**Stops:** direct pushes, force pushes, and deletion of the default branch, and merges that skip CI.

**Why rulesets over classic branch protection:** rulesets apply to admins unless they are listed as bypass actors, several rulesets combine, and `evaluate` mode previews the effect before enforcing (plan permitting).

**Check:**

```bash
gh ruleset list --repo OWNER/REPO
gh ruleset check DEFAULT_BRANCH --repo OWNER/REPO
```

**Apply:** fill [../templates/ruleset-default-branch.json](../templates/ruleset-default-branch.json), then:

```bash
gh api -X POST repos/OWNER/REPO/rulesets --input ruleset.json
```

Choices to make with the user:

| Setting | Solo maintainer | Team |
|---|---|---|
| `required_approving_review_count` | `0`: the pull request is still required, so CI runs, but nobody else must approve | `1` or more |
| `require_code_owner_review` | `false` | `true`, only if CODEOWNERS exists and covers `/.github/` |
| `required_status_checks` | The job names CI reports, for example `validate` | Same. Use one aggregator job for matrix builds. |
| `bypass_actors` | Optional: repository admin role, for emergencies | Avoid, or keep to one role |

The pull request rule requires these five parameters (from the OpenAPI schema): `required_approving_review_count`, `dismiss_stale_reviews_on_push`, `require_code_owner_review`, `require_last_push_approval`, and `required_review_thread_resolution`. The status-check rule requires `required_status_checks` and `strict_required_status_checks_policy`.

**Limits:**
- A required check that has never run blocks every pull request. Run CI once before requiring its check.
- `~DEFAULT_BRANCH` keeps targeting the default branch even after it is renamed.

## Secret scanning and push protection

**Stops:** known credential formats from landing in the repository (push protection) and leaked ones going unnoticed (alerts).

**Check:** `gh api repos/OWNER/REPO --jq '.security_and_analysis'`. This needs admin rights; otherwise the field is missing, which means Unknown.

**Apply:**

```bash
gh api -X PATCH repos/OWNER/REPO \
  -f "security_and_analysis[secret_scanning][status]=enabled" \
  -f "security_and_analysis[secret_scanning_push_protection][status]=enabled"
```

**Limits:** detection covers known token patterns, not every secret. A secret found in history must be rotated. Deleting it is not enough.

## Dependabot

**Stops:** known-vulnerable dependencies lingering, and freshly published malicious versions being adopted on day one (cooldown).

**Check:**
```bash
gh api repos/OWNER/REPO/vulnerability-alerts --silent && echo enabled     # 204 enabled, 404 disabled
gh api repos/OWNER/REPO/automated-security-fixes --jq .enabled
```
Also look for `.github/dependabot.yml`.

**Apply:**
```bash
gh api -X PUT repos/OWNER/REPO/vulnerability-alerts
gh api -X PUT repos/OWNER/REPO/automated-security-fixes
```
Then add `.github/dependabot.yml` from [../templates/dependabot.yml](../templates/dependabot.yml), with one entry per ecosystem actually present (`github-actions` almost always, plus `npm`, `pip`, `cargo`, `gomod`, and so on, from the manifests).

Configuration choices:
- **Weekly schedule with grouping:** fewer, larger pull requests.
- **`cooldown`:** waits a number of days after a version is published before proposing it. `default-days` applies to all updates; `semver-major-days`, `semver-minor-days`, and `semver-patch-days` refine it where the ecosystem supports SemVer. Security updates are not delayed by the cooldown.

**Limits:** no auto-merge without the same CI and review a human change gets.

## Private vulnerability reporting

**Check and apply:** see [github-facts.md](shared/github-facts.md#security-reporting). `gh api -X PUT repos/OWNER/REPO/private-vulnerability-reporting` enables it. SECURITY.md should link to `https://github.com/OWNER/REPO/security/advisories/new` (see `github-community-files`).

## CodeQL code scanning

**Stops:** common vulnerability patterns merging unnoticed, for languages CodeQL supports.

**Check:** `gh api repos/OWNER/REPO/code-scanning/default-setup --jq .state`

**Apply:** `gh api -X PATCH repos/OWNER/REPO/code-scanning/default-setup -f state=configured`

**Limits:** it is only useful when the repository's main languages are supported. Say so for repositories that are mostly Markdown or shell.

## GitHub Actions hardening

These are file changes, so they go through the normal file workflow, then a pull request or commit after approval.

| Practice | Why | How to check |
|---|---|---|
| Pin third-party actions to a full commit SHA, with the version in a comment: `uses: owner/action@<40-hex-sha> # v1.2.3` | A moved tag cannot change what runs | `grep -nE 'uses: [^@]+@' .github/workflows/*.yml \| grep -vE '@[0-9a-f]{40}'` |
| Set `permissions: contents: read` at the top of each workflow, and raise it only per job | Limits what a compromised step can do with `GITHUB_TOKEN` | Workflows with no top-level `permissions:` key |
| Do not check out pull request code under `pull_request_target` | That trigger runs with secrets and write access | `grep -n pull_request_target .github/workflows/*.yml` |
| Lint workflows with [actionlint](https://github.com/rhysd/actionlint), and audit them with [zizmor](https://github.com/zizmorcore/zizmor) | Catches syntax errors and dangerous patterns | Suggest it. Install nothing without approval. |

To find a SHA for a tag: `gh api repos/OWNER/ACTION/git/ref/tags/vX.Y.Z --jq .object`. If `type` is `tag`, resolve it once more with `gh api repos/OWNER/ACTION/git/tags/SHA --jq .object.sha`. Pinned SHAs are kept current by Dependabot's `github-actions` ecosystem.

## OpenSSF Scorecard

[OpenSSF Scorecard](https://github.com/ossf/scorecard) scores a repository on checks such as Branch-Protection, Code-Review, Dangerous-Workflow, Dependency-Update-Tool, Pinned-Dependencies, Security-Policy, Signed-Releases, and Token-Permissions.

- **Look up existing results** (read-only, works for any repository Scorecard has scanned): `curl -s https://api.scorecard.dev/projects/github.com/OWNER/REPO | jq '{score, date, checks: [.checks[] | {name, score}]}'`
- **Publish results and a badge:** add [../templates/scorecard.yml](../templates/scorecard.yml). It needs `publish_results: true` and `id-token: write` on the job. The badge is then `[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/OWNER/REPO/badge)](https://scorecard.dev/viewer/?uri=github.com/OWNER/REPO)`.
- Use the per-check results to choose the next fixes. Do not chase the number itself.
