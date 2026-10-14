---
name: github-repo-audit
description: "Checks a repository before it is shared or made public, then audits how it presents itself and returns a scored checklist with ranked fixes: README, license, community health files, description, topics, social preview, releases, CI and security signals, and root layout, plus a pre-public secrets and history check. Read-only. Make sure to use this skill whenever the user asks what is missing from a repository, wants a repo reviewed or audited, asks whether a project is ready to share, launch, open source, or make public (including a private repository about to go public, where it checks for leaked secrets first), or asks how to improve a repository without naming one specific file. Not for writing the fixes: each fix names the skill that writes it."
argument-hint: "[path | owner/repo] [pre-public]"
---

# GitHub repository audit

Score a repository against what visitors, contributors, and GitHub itself look for, then hand back a short, ranked list of fixes. Each fix points to the skill in this package that writes it. This skill never changes anything.

## When to use

- "Audit my repo", "review this repository", "what is missing from my GitHub project"
- "Is this ready to make public?" or "I am about to open source this" (use `pre-public` mode)
- Before a launch, a release announcement, or a job application that links the repository
- As the first step when the user asks to "improve" a repository without saying what to improve

## Input

- **Target** (`$ARGUMENTS` or ask): a local path (default: the current directory) or `owner/repo`.
- **Mode**: `standard` (default) or `pre-public`. Use `pre-public` when the user mentions going public or open sourcing, even if they did not name the mode.
- **Goal** (optional): who the repository is for, such as users of a library, contributors, employers, or researchers. It changes which checks are critical.

## Output

1. A summary line: `N of M applicable checks pass. Critical: X open.` If GitHub reports a community health percentage, show it too, labeled as GitHub's number.
2. A results table grouped by area, with **Pass**, **Fix**, or **N/A**, and the evidence for each verdict.
3. **Top fixes**, ranked: at most seven, critical first. Each names its sibling skill and the exact first action.
4. In `pre-public` mode: a separate **Before going public** block with blocking findings.

Use the format in [references/examples.md](references/examples.md).

## Workflow

Copy this checklist into your response and tick items off as you go:

```
Audit progress:
- [ ] 1. Resolve the target and data tier
- [ ] 2. Collect remote facts
- [ ] 3. Scan local files
- [ ] 4. Score every check
- [ ] 5. Rank the fixes
- [ ] 6. Pre-public checks (pre-public mode only)
- [ ] 7. Report
```

**1. Resolve the target.** For a local path, read `git remote get-url origin` to find `owner/repo`. If there is no remote, audit local files only and mark remote-only checks **N/A (no remote)**. Check `gh auth status` once and pick the data tier from [operating-rules.md](../../references/operating-rules.md#data-sources).

**2. Collect remote facts.** Run the bundled script. It makes read-only `gh` calls and prints one JSON object:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/collect_repo_facts.sh" OWNER/REPO
```

A `null` field means the call failed or needs more permission (branch rules, for example). Report it as **Unknown**, never as **Fix**. If the script exits with code 3, `gh` is unavailable. Continue with local files and say which checks you could not run.

**3. Scan local files.** Use Glob and Read on the working tree. Look for the README in `.github/`, root, and `docs/`, community files in their supported locations, `.github/workflows/`, manifests, `.gitignore`, and large or generated files. Run `git ls-files | head -200` to see what is tracked. Read only the parts of large files you need.

**4. Score every check** in [references/checklist.md](references/checklist.md). For each check, record the verdict and one line of evidence: a path, a field value, or a command result. Mark a check **N/A** when it does not fit the project type. For example, `CITATION.cff` applies only to research software and datasets. Adjust severity to the stated goal as the checklist describes.

**5. Rank the fixes.** Order by severity, then by impact on a first-time visitor, then by effort, smallest first. Merge fixes one skill handles in one pass. For example, a missing CONTRIBUTING and a missing SECURITY become one `github-community-files` item.

**6. Pre-public checks.** In `pre-public` mode, run the "Before going public" checks in the checklist. Anything that could leak a secret or personal data blocks publishing until it is resolved. When `gitleaks` or `trufflehog` is installed, suggest running it and show the command. Do not install either tool.

**7. Report** in the output shape from [operating-rules.md](../../references/operating-rules.md#output-shape). This skill has no commands awaiting approval.

## Hard rules

Shared rules: [operating-rules.md](../../references/operating-rules.md). Additional rules for this skill:

- **Read-only.** Do not create, edit, or delete files, and do not run any remote change, even if a fix is one line. Offer the sibling skill instead.
- **Evidence or Unknown.** Every verdict cites what you saw. If you could not see it, the verdict is **Unknown**, not **Fix**. A pasted file list or summary is not proof that something is absent unless the user says it is complete, or explicitly says the thing is missing.
- **No invented scores.** Report counts of checks, not made-up percentages or grades. GitHub's `health_percentage` may be quoted as GitHub's figure.
- **Never print secret values.** If a secret seems to be tracked, report the file path and the kind of secret only.

## Example

Input: `/github-repo-audit acme-labs/tinyqueue`

Output (abridged):

```markdown
**tinyqueue audit:** 16 of 30 applicable checks pass. Critical: 4 open (A1, B3, B4, D1). (GitHub community health: 57%.)

| Area | Check | Verdict | Evidence |
|---|---|---|---|
| Front door | A1 Description | Fix | Empty `description` |
| README | B3 Install steps | Fix (Critical) | README has no install command; `pyproject.toml` defines package `tinyqueue` |
| Community | C1 License | Pass | `LICENSE` detected as MIT |
| Releases | D1 Published releases | Fix (Critical) | 4 tags (`v0.1.0` to `v0.4.0`), 0 releases |

**Top fixes**
1. Critical: add install and quick-start sections. Run `github-readme-writer` (improve mode).
2. Critical: publish GitHub Releases for the existing tags. Run `github-release-writer`.
3. Critical: write a description and 8 to 12 topics. Run `github-discoverability`.
```

The complete example, including pre-public mode, is in [references/examples.md](references/examples.md).

## Reference files

- [references/checklist.md](references/checklist.md): every check, with its severity, how to verify it, and the skill that fixes it
- [references/examples.md](references/examples.md): two complete audits, a standard one and a pre-public one
- `scripts/collect_repo_facts.sh`: the read-only `gh` collector. Run it; do not read it into context.
- [../../references/github-facts.md](../../references/github-facts.md): platform limits cited in verdicts

## Related skills

- `github-readme-writer`: README fixes (area B)
- `github-discoverability`: description, topics, homepage, social preview (area A)
- `github-community-files`: LICENSE, CONTRIBUTING, SECURITY, templates (area C)
- `github-release-writer`: releases and changelog (area D)
- `github-repo-hardening`: rulesets, security features, and Actions hardening (area E)
- `github-repo-family`: when the same fixes repeat across many repositories, use account-wide defaults instead
