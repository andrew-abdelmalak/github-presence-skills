# Vetting and etiquette

## Contents

- [Vetting checklist](#vetting-checklist)
- [AI contribution policy](#ai-contribution-policy)
- [Communication](#communication)
- [During review](#during-review)

## Vetting checklist

The thresholds are heuristics for a good first experience, not rules about project quality.

| Check | Command | Healthy sign | Red flag |
|---|---|---|---|
| Recent merges | `gh pr list -R OWNER/REPO --state merged --limit 10 --json mergedAt,author` | Merges in the last ~3 months, including from outside contributors | Nothing merged in 6+ months, or only maintainers' own PRs |
| Maintainer response | `gh issue list -R OWNER/REPO --state all --limit 10 --json number,comments,createdAt`, then sample 2 or 3 issues with `gh issue view N -R OWNER/REPO --comments` | A maintainer replies within about 2 weeks | Stale questions from contributors, PRs left unreviewed for months |
| Archived | `gh repo view OWNER/REPO --json isArchived` | `false` | `true`: skip |
| License | `gh repo view OWNER/REPO --json licenseInfo` | An OSI license | None: contributions have unclear terms. Skip. |
| Contribution guide | `gh api -H "Accept: application/vnd.github.raw+json" repos/OWNER/REPO/contents/CONTRIBUTING.md`, or `.github/CONTRIBUTING.md` | Exists, with setup and test steps | Missing. Workable, but read the recent PRs to learn the norms. |
| CLA / DCO | CONTRIBUTING, PR checks (`gh pr checks` on a recent PR), `Signed-off-by` in `git log` | Clearly stated | A CLA the user cannot sign, such as an employer conflict |
| Issue assigned | `gh issue view N -R OWNER/REPO --json assignees` | Empty | Assigned to someone else |
| Linked PR | The timeline query in SKILL.md step 3 | None open | An open PR: someone is on it |
| Recent claims | `gh issue view N -R OWNER/REPO --comments` | No "I'll take this" in the last ~2 weeks | A recent claim: ask before starting, or pick another issue |
| Clarity | Read the issue | Expected behavior is stated, and a maintainer confirmed it | Open design debate with no maintainer decision |

## AI contribution policy

Many projects now state a policy on AI-assisted contributions. Check before writing any code:

```bash
for f in CONTRIBUTING.md .github/CONTRIBUTING.md docs/CONTRIBUTING.md AI_POLICY.md README.md .github/pull_request_template.md; do
  gh api -H "Accept: application/vnd.github.raw+json" "repos/OWNER/REPO/contents/$f" 2>/dev/null \
    | grep -n -i -E "\bAI\b|LLM|large language|copilot|chatgpt|claude|generated" && echo "  ^ in $f"
done
```

| Policy found | Action |
|---|---|
| Prohibits AI-generated or AI-assisted contributions | Stop. Tell the user that the project does not accept this kind of contribution. Do not write the change, and do not help disguise it. |
| Allows it with disclosure | Proceed, and add the required disclosure to the PR description, in the project's wording |
| Requires the contributor to fully understand the change | Proceed, and explain every change so the user can defend it in review |
| No policy | Proceed. The user remains responsible for the change. Suggest a brief, honest note if the user wants one. |

## Communication

**Before starting** (when CONTRIBUTING asks for it, or the change is non-trivial):

```markdown
Hi! I'd like to work on this. My plan: {{ONE_OR_TWO_SENTENCE_APPROACH}}. {{QUESTION_IF_ANY}} I expect to open a PR within {{TIMEFRAME}}.
```

Keep it short. Ask a real question only if the issue leaves something open.

**Releasing an issue** you will not finish:

```markdown
I won't be able to finish this after all. Unassigning myself so someone else can pick it up. {{OPTIONAL_NOTES_ON_WHAT_YOU_LEARNED}}
```

**Following up** on a pull request with no review: wait at least a week, then post one polite comment. Never tag individual maintainers repeatedly.

## During review

- Reply to every review comment, either by changing the code or by explaining why not.
- Push follow-up commits instead of force-pushing during review, unless the project asks for a rebased history.
- Keep the PR scoped. New ideas become new issues.
- If the maintainers decline the change, thank them and close the PR. A respectful exchange still counts for something.
- After merge, the contribution appears on the user's graph (see [github-facts.md](../../../references/github-facts.md#contribution-graph)), and the repository becomes pinnable on their profile.
