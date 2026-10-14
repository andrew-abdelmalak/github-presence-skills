# Repository hardening example

Fictional repository `acme-labs/tinyqueue`: public, one maintainer, CI workflow `tests.yml` with a job named `test`.

## Input

> Harden acme-labs/tinyqueue. I'm the only maintainer.

## Step 2: posture (abridged script output)

```json
{
  "repo": {"private": false, "default_branch": "main", "permissions": true,
           "security_and_analysis": {"secret_scanning": {"status": "enabled"},
                                     "secret_scanning_push_protection": {"status": "disabled"}}},
  "rulesets": [],
  "classic_protection": null,
  "dependabot_alerts": true,
  "dependabot_security_updates": false,
  "dependabot_config": null,
  "private_vulnerability_reporting": false,
  "codeql_default_setup": "not-configured",
  "workflows": [{"file": "tests.yml", "unpinned_uses": 2, "top_level_permissions": false, "pull_request_target": false}],
  "scorecard": null
}
```

## Output

````markdown
**Posture:** 2 of 9 controls active. Public repository, so every control is available for free.

| # | Control | Status | Evidence |
|---|---|---|---|
| 1 | Default-branch ruleset | Missing | no rulesets, no classic protection |
| 2 | Secret scanning | Active | `security_and_analysis.secret_scanning` |
| 2 | Push protection | Missing | `secret_scanning_push_protection: disabled` |
| 3 | Dependabot alerts | Active | `vulnerability-alerts` 204 |
| 3 | Dependabot security updates | Missing | `automated-security-fixes.enabled: false` |
| 3 | dependabot.yml | Missing | no `.github/dependabot.yml` |
| 4 | Private vulnerability reporting | Missing | `enabled: false` |
| 5 | CodeQL default setup | Missing | `not-configured`; Python is supported |
| 6 | Actions pinned and least-privilege | Missing | `tests.yml`: 2 unpinned `uses:`, no top-level `permissions:` |

**Plan**

1. **Ruleset (solo maintainer):** require a pull request with 0 approvals, so CI always runs and you never lock yourself out; require the `test` check; block force pushes and deletion. `ruleset.json` is filled from the template with `"context": "test"`.
2. **Push protection** on.
3. **Dependabot security updates** on, plus `.github/dependabot.yml` for `github-actions` and `pip`: weekly, grouped, `cooldown.default-days: 7`.
4. **Private vulnerability reporting** on. Your SECURITY.md already links to it.
5. **CodeQL default setup** on.
6. **`tests.yml`:** pin `actions/checkout` and `actions/setup-python` to commit SHAs with version comments, and add `permissions: contents: read` at the top. I'll show the diff.

**Commands awaiting approval**
```bash
gh api -X POST repos/acme-labs/tinyqueue/rulesets --input ruleset.json
gh api -X PATCH repos/acme-labs/tinyqueue -f "security_and_analysis[secret_scanning_push_protection][status]=enabled"
gh api -X PUT repos/acme-labs/tinyqueue/automated-security-fixes
gh api -X PUT repos/acme-labs/tinyqueue/private-vulnerability-reporting
gh api -X PATCH repos/acme-labs/tinyqueue/code-scanning/default-setup -f state=configured
```
The two file changes (`dependabot.yml`, `tests.yml`) go through a pull request, so the new ruleset applies to them too.

**Optional:** an OpenSSF Scorecard workflow with a README badge. Want it?
````

## After approval

The skill runs the commands, opens the pull request for the file changes, and runs `collect_posture.sh` again. The result is 9 of 9 active. The ruleset shows in `gh ruleset list --repo acme-labs/tinyqueue`.

## A private repository on GitHub Free, for contrast

````markdown
| Control | Status |
|---|---|
| Default-branch ruleset | Not available on this plan: private repositories need GitHub Pro, Team, or Enterprise Cloud |
| Secret scanning | Not available on this plan: user-owned private repositories need GitHub Secret Protection |
| Dependabot alerts and updates | Available. Plan below. |
| Private vulnerability reporting | Not offered for private repositories |

I'll set up what this plan supports (Dependabot and Actions hardening). When the repository goes public, rulesets, secret scanning, and CodeQL become free; run this skill again then.
````
