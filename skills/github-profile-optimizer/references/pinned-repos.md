# Choosing the pinned six

Pins are the most-viewed part of a profile after the README. They should show the person's best and most relevant work for their goal, not their most recent or most starred repositories.

## Candidate pool

Take candidates from `pinnableItems` (see SKILL.md step 2). It includes the user's own repositories and repositories owned by others that they contributed to. Exclude:
- Archived repositories, unless they are a notable finished project.
- Forks with no commits of the user's own. Pin the upstream repository they contributed to instead, if it is pinnable.
- Course exercises, tutorial clones, and empty or "hello world" repositories, unless the goal is `learning` and nothing better exists.
- Private repositories. Pins are public.

## Scoring

Score each candidate from 0 to 3 on each criterion. Weights depend on the goal.

| Criterion | 0 | 3 | Weight: job-search | open-source | freelance | research | learning |
|---|---|---|---|---|---|---|---|
| **Goal fit**: shows the skills the goal needs | Unrelated | Exactly the target role or domain | 3 | 2 | 3 | 3 | 2 |
| **Readiness**: description, README, license, recent activity | None | All present | 2 | 2 | 2 | 2 | 2 |
| **Substance**: real problem, non-trivial code, tests | Toy | Production-grade or widely used | 2 | 3 | 2 | 2 | 1 |
| **Evidence of use**: stars, dependents, downloads, merged upstream | None | Clearly used by others | 1 | 3 | 1 | 1 | 0 |
| **Ownership**: the user's own role in it | Minor | Author or core maintainer | 2 | 2 | 2 | 2 | 2 |

Pick the top six, then adjust for **variety**: if four picks show the same skill, swap the weakest for the best project that shows a different one (a frontend app, a library, infrastructure, writing, research).

## Ordering

The first two pins get the most attention:
1. The flagship: the best overall score.
2. The strongest proof of the target skill, if it differs from the flagship.
3. To 6. Variety, then outside contributions, then supporting tools.

## Readiness fixes

For every pick, run quick checks:

```bash
gh repo view OWNER/REPO --json description,licenseInfo,repositoryTopics,pushedAt --jq '{description, license: .licenseInfo.key, topics: (.repositoryTopics|length), pushedAt}'
```

| Missing | Fix with |
|---|---|
| Description or topics | `github-discoverability` |
| README, or a README without install or usage | `github-readme-writer` |
| License | `github-community-files` |
| Signs of abandonment (no push in years) while the project is still shown as active | `github-readme-writer`: add a status note, or pick a different repository |

## Gists

Gists can be pinned too. Use one when a gist is a well-known snippet or guide. Most profiles are better served by six repositories.
