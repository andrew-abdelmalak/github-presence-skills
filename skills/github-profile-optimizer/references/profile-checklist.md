# Profile checklist

## Contents

- [Personal profile checks](#personal-profile-checks)
- [Goal emphasis](#goal-emphasis)
- [Organization profiles](#organization-profiles)

## Personal profile checks

| ID | Check | How to verify | Fix |
|---|---|---|---|
| P1 | A profile README is shown | The public repository `NAME/NAME` exists with a non-empty `README.md`. Pre-July-2020 repositories need **Share to profile**. | Create it (see SKILL.md step 8) |
| P2 | The README's first two lines say who you are and what you build | Read them | Rewrite from the template |
| P3 | The README is scannable in about 30 seconds: short sections, no wall of badges | Rendered length, badge count | Trim. Follow [badges.md](shared/badges.md#placement). |
| P4 | No broken images or dead third-party widgets | Each image URL loads. No public stats instances that often fail. | Remove, or switch to Actions-generated images ([contributions.md](contributions.md#stats-cards)) |
| P5 | The bio states role and focus, specifically | `bio` field | Propose a new bio |
| P6 | The display name is set | `name` field | Ask the user what name they want public |
| P7 | The avatar is a real photo or a deliberate logo, not the default pattern | Check visually | The user uploads one in Settings |
| P8 | Website or blog and contact links are set when the goal needs them | `blog`, `twitter_username`, social accounts (check visually) | Propose links the user owns |
| P9 | Six pins chosen deliberately, not the automatic "Popular repositories" | `pinnedItems` count and contents | [pinned-repos.md](pinned-repos.md) |
| P10 | Each pinned repository has a description, a README, and a license | `gh repo view` on each pin | Route to `github-discoverability`, `github-readme-writer`, or `github-community-files` |
| P11 | The contribution graph reflects real work | Compare local history with the graph ([contributions.md](contributions.md)) | Fix the email or branch causes |
| P12 | Private contributions shown or hidden on purpose | Check visually (**Contribution settings** on the profile) | User's choice |
| P13 | Hireable status and contact email match the goal | `hireable`, public email (check visually) | User's choice |

## Goal emphasis

| Goal | Most important | Less important |
|---|---|---|
| `job-search` | P2, P5, P9, P10 (pins look finished), P11, and a clear "how to reach me" | Stats cards, follower counts |
| `open-source` | Pins of maintained projects, links to docs, P10, and a sponsor link if one exists | Hireable status |
| `freelance` | P2 states the services and the client type, P8 has a site and contact, pins show client-like work | Stats |
| `research` | Links to papers, a scholar profile, or ORCID; pins with `CITATION.cff` | Streaks, stats |
| `learning` | An honest "currently learning" line, pins of the best projects with clear READMEs | Claims of expertise |

## Profile README styles

Pick one primary style for the goal. All of them follow the same honesty rules.

| Style | Leads with | Upkeep | Best for |
|---|---|---|---|
| **Plain prose** | Two or three honest sentences, then links | None | Experienced developers, and anyone who wants signal over decoration. The template's default. |
| **Project showcase** | A table of selected projects with outcomes | Low: update when projects change | Job seekers and freelancers whose work is public |
| **Résumé** | Role, experience, talks, and writing | Low | Candidates with credentials that are not visible in code |
| **Visual** | One banner, screenshot, or diagram, then prose | Low | Designers and front-end developers. Needs alt text and a small file. |
| **Self-updating** | Recent posts, releases, or activity, injected by a scheduled Action | Ongoing | People who publish often. Scheduled workflows in public repositories stop after 60 days without repository activity, so the content can silently freeze (see [github-facts.md](shared/github-facts.md#github-actions)). |

Avoid walls of technology logo badges and multiple stats cards in any style. They crowd out the information a visitor came for.

## Organization profiles

GitHub details are in [github-facts.md](shared/github-facts.md#profiles-and-organizations).

| ID | Check | How to verify |
|---|---|---|
| O1 | A public `.github` repository with `profile/README.md` | `gh api repos/ORG/.github/contents/profile/README.md` |
| O2 | The README says what the organization builds and for whom, in its first lines | Read it |
| O3 | It routes visitors: key repositories, how to contribute, where to ask, how to report security issues | Read it |
| O4 | Public pins (up to six) show flagship projects | `organization { pinnedItems }` |
| O5 | A member-only README in a private `.github-private` repository, if members need internal links | Ask. It is optional. |
| O6 | The description, website, and avatar are set | `gh api orgs/ORG --jq '{description, blog, email}'` |
| O7 | Default community files exist in `.github` | See `github-community-files` account-wide defaults |

Organization fields can be updated with `gh api -X PATCH orgs/ORG -f description="..." -f blog="..."`. This needs organization admin rights and the `admin:org` token scope, so it is a remote change that needs approval.
