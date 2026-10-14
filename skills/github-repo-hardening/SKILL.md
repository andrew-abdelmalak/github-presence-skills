---
name: github-repo-hardening
description: "Audits and applies the security settings that make a repository trustworthy to adopters and contributors: a ruleset on the default branch, secret scanning and push protection, Dependabot alerts and grouped updates with a cooldown, private vulnerability reporting, CodeQL code scanning, pinned and least-privilege GitHub Actions, and an OpenSSF Scorecard. Every setting change waits for approval. Make sure to use this skill whenever the user mentions branch protection, rulesets, protecting main, secret scanning, Dependabot, CodeQL, Scorecard, pinning actions, workflow permissions, hardening or securing a repository, or asks whether a GitHub Actions workflow is safe, or which security features their plan allows on a private repository. Not for writing SECURITY.md (use github-community-files) or fixing vulnerable code."
---

# Repository hardening

Turn on the server-side protections that adopters look for and that stop the most common supply-chain and review failures. Good intentions and local hooks can't replace them. Plan limits are stated up front, and every change is shown before it runs.

## When to use

- "Protect main", "require pull requests", "set up branch protection or rulesets"
- "Enable secret scanning", "set up Dependabot", "add CodeQL", "add an OpenSSF Scorecard badge"
- "Harden my GitHub Actions", "pin actions", "workflow permissions"
- A `github-repo-audit` result lists area E fixes

## Input

- **Target**: a local path or `owner/repo`. Reading most settings, and applying any, needs admin rights on the repository.
- **Mode**: `audit` (default, read-only) or `apply`.
- **Team shape**: solo maintainer or several reviewers. It changes the ruleset (see [references/controls.md](references/controls.md#default-branch-ruleset)).

## Output

1. **Posture table:** each control with Active, Missing, Not available on this plan, or Unknown (no permission), and the evidence.
2. **Plan:** the missing controls in priority order, each with its exact command or file.
3. **Commands awaiting approval**, then a re-audit after they run.

## Workflow

```
Hardening progress:
- [ ] 1. Confirm the target is long-lived
- [ ] 2. Collect the current posture
- [ ] 3. Check plan limits
- [ ] 4. Build the plan
- [ ] 5. Apply after approval
- [ ] 6. Re-audit
```

**1. Confirm the target is long-lived.** Do not harden forks, throwaway experiments, or archived repositories. Ask if unsure.

**2. Collect the posture** with the read-only script. It prints one JSON object, and `null` means the call failed or lacked permission (report **Unknown**):

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/collect_posture.sh" OWNER/REPO
```

In a local clone, also read `.github/workflows/*.yml` and `.github/dependabot.yml` directly. The script only samples remote workflow files.

**3. Check plan limits** in [github-facts.md](../../references/github-facts.md#security-reporting) and [references/controls.md](references/controls.md#plan-limits). Rulesets on private repositories need GitHub Pro, Team, or Enterprise Cloud. Code scanning and secret scanning on private repositories need GitHub Code Security or Secret Protection. Report these as **Not available on this plan**, with what unlocks them, rather than as failures.

**4. Build the plan** in this order. Each recipe is in [references/controls.md](references/controls.md):

1. A ruleset on the default branch, from [templates/ruleset-default-branch.json](templates/ruleset-default-branch.json)
2. Secret scanning and push protection
3. Dependabot alerts and security updates, plus `.github/dependabot.yml` from [templates/dependabot.yml](templates/dependabot.yml) for the ecosystems actually in the repository
4. Private vulnerability reporting (public repositories)
5. CodeQL default setup (public repositories, or private ones with Code Security)
6. GitHub Actions hardening: SHA-pinned actions, top-level `permissions: contents: read`, and no untrusted checkout under `pull_request_target`
7. Optionally, OpenSSF Scorecard with a badge, from [templates/scorecard.yml](templates/scorecard.yml)

**5. Apply after approval.** Show every command and file in one block, and wait for an explicit yes. Create the ruleset in `evaluate` mode first when the plan supports it, then switch it to `active`.

**6. Re-audit.** Run the script again. Every applied control must show **Active**. Anything that did not change gets a reason (plan, permissions, or a check that has never run).

## Hard rules

Shared rules: [operating-rules.md](../../references/operating-rules.md). Additional rules for this skill:

- **Never lock the owner out.** For solo maintainers, use 0 required approvals (pull requests and checks are still required), or add the owner as a bypass actor. Never set required approvals at or above the number of people who can approve.
- **Required checks must match real check names** that have already run at least once. Otherwise every pull request blocks forever.
- **No blanket auto-merge for bot pull requests.** Dependabot pull requests get the same CI and review as human ones.
- **State limits honestly.** Push protection blocks known secret patterns only. A Scorecard score summarizes practices; it is not a security guarantee.
- **Do not disable** existing protections, or delete rulesets, unless the user asks for that exact change.

## Example

Input:

> Harden acme-labs/tinyqueue. I'm the only maintainer.

Output (abridged):

````markdown
| Control | Status | Evidence |
|---|---|---|
| Default-branch ruleset | Missing | `rulesets: []`, classic protection 404 |
| Secret scanning / push protection | Active / Missing | `security_and_analysis` |
| Dependabot alerts | Active | `vulnerability-alerts` 204 |
| dependabot.yml | Missing | not in `.github/` |
| Private vulnerability reporting | Missing | `enabled: false` |
| Actions pinned to SHAs | Missing | `tests.yml` uses `actions/checkout@v4` |

**Commands awaiting approval**
```bash
gh api -X POST repos/acme-labs/tinyqueue/rulesets --input ruleset.json
gh api -X PATCH repos/acme-labs/tinyqueue -f "security_and_analysis[secret_scanning_push_protection][status]=enabled"
gh api -X PUT repos/acme-labs/tinyqueue/private-vulnerability-reporting
```
````

The complete run is in [references/examples.md](references/examples.md).

## Reference files

- [references/controls.md](references/controls.md): every control, with its commands, plan limits, the solo-maintainer ruleset, Actions hardening, and Scorecard
- [references/examples.md](references/examples.md): a complete audit and apply run
- [templates/](templates/): `ruleset-default-branch.json`, `dependabot.yml`, `scorecard.yml`
- `scripts/collect_posture.sh`: the read-only posture collector. Run it; do not read it into context.

## Related skills

- `github-community-files`: SECURITY.md and CODEOWNERS. CODEOWNERS only enforces review once the ruleset requires code-owner review.
- `github-repo-audit`: area E checks, and the re-check afterwards
- `github-readme-writer`: add the Scorecard badge once results are published
