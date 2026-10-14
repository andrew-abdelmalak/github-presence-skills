---
name: github-profile-optimizer
description: "Audits and rewrites a GitHub personal or organization profile for a goal such as a job search: profile README, bio, links, the six pinned repositories, and the organization README in .github/profile. Diagnoses real contributions missing from the contribution graph and handles stats cards honestly. Make sure to use this skill whenever the user mentions their GitHub profile, bio, pinned repositories, profile README, contribution graph or streaks, or how their GitHub looks to recruiters, including requests to fake or backdate activity, which it refuses. Not for repository READMEs (use github-readme-writer)."
---

# Profile optimizer

Make a GitHub profile answer three questions in about 30 seconds: who is this, what do they build, and how do I reach them. Then make sure the profile shows the real work behind it.

## When to use

- "Improve my GitHub profile", "write my profile README", "what should I pin?"
- "I'm job hunting and recruiters look at my GitHub"
- "My contributions don't show up" or "my graph is empty but I commit every day"
- "Set up our organization's profile page"

## Input

- **Account** (default: the signed-in user, from `gh api user --jq .login`). Organizations are detected from the account `type`.
- **Goal**: one of `job-search`, `open-source`, `freelance`, `research`, `learning`, or `organization`. Ask if it is not stated. It changes what to emphasize (see [the checklist](references/profile-checklist.md#goal-emphasis)).
- **Context** (optional): the role they want, what they are proud of, and links to a portfolio, blog, or talks.

## Output

1. **Scorecard** against [references/profile-checklist.md](references/profile-checklist.md): Pass, Fix, or Check visually.
2. **Bio and profile fields:** current and proposed.
3. **Pinned six:** ranked, with a reason for each, and a "fix before pinning" list.
4. **Profile README draft** from [templates/profile-README.md](templates/profile-README.md), or the [organization template](templates/org-profile-README.md).
5. **Contribution graph diagnosis,** when relevant.
6. **Commands awaiting approval,** and the steps that only work in the GitHub UI.

## Workflow

```
Profile progress:
- [ ] 1. Identify the account and goal
- [ ] 2. Collect profile data
- [ ] 3. Score the checklist
- [ ] 4. Bio and fields
- [ ] 5. Choose the pinned six
- [ ] 6. Draft the profile README
- [ ] 7. Diagnose the contribution graph (if relevant)
- [ ] 8. Present, then apply after approval
```

**1. Identify the account and goal.**

```bash
gh api users/NAME --jq '{login, id, name, type, bio, company, blog, location, twitter_username, hireable, public_repos, created_at}'
```

If `type` is `Organization`, follow the organization path in [the checklist](references/profile-checklist.md#organization-profiles).

**2. Collect profile data.**

```bash
# Profile README (users: repo NAME/NAME; organizations: ORG/.github, file profile/README.md)
gh api -H "Accept: application/vnd.github.raw+json" repos/NAME/NAME/readme
# Pinned now, and everything pinnable (including repositories they contributed to)
gh api graphql -F login=NAME -f query='query($login:String!){user(login:$login){
  pinnedItems(first:6,types:[REPOSITORY,GIST]){nodes{...on Repository{nameWithOwner description stargazerCount pushedAt}...on Gist{name description}}}
  pinnableItems(first:100,types:[REPOSITORY]){nodes{...on Repository{nameWithOwner description stargazerCount pushedAt isFork isArchived primaryLanguage{name} owner{login}}}}}}'
# External merged contributions
gh search prs --author NAME --merged --limit 100 --json repository,title,url
```

For an organization, replace `user(login:)` with `organization(login:)`. Organizations have `pinnedItems` and `pinnableItems` too. Pinned items, the avatar, and the private-contributions setting are not fully visible through the API. Mark those checks **Check visually** and ask the user to confirm.

**3. Score** every item in [references/profile-checklist.md](references/profile-checklist.md), weighted by the goal.

**4. Bio and fields.** Write one bio of up to about 160 characters: role, focus, and one specific proof point or interest. No buzzword strings. Propose the name, company, blog/website, and location only if the user wants them public. Never invent employers, titles, or achievements. Ask.

**5. Choose the pinned six** with [references/pinned-repos.md](references/pinned-repos.md). Pick from `pinnableItems` only. For each pick that fails basic readiness (no description, no README, no license), list the fix and the sibling skill that makes it.

**6. Draft the profile README.** First pick one style with the user, from [the style guide](references/profile-checklist.md#profile-readme-styles). Mixing styles produces clutter. Then draft from the template. Every project line links to a real repository and states what it does. Numbers (users, stars, downloads) appear only if verified. Keep the README short enough to read in about 30 seconds. If the user has portfolio or blog content worth a site, suggest a personal GitHub Pages site at `NAME.github.io` (one per account; see [github-facts.md](../../references/github-facts.md#github-pages)).

**7. Diagnose the contribution graph** if the user mentions missing contributions, or if their local history clearly outpaces the graph. Follow [references/contributions.md](references/contributions.md). Handle stats-card requests with the policy in the same file.

**8. Present, then apply.** Show the scorecard and the drafts. Then list the changes:
- **Profile README:** if the `NAME/NAME` repository does not exist, creating it is a remote change: `gh repo create NAME --public --description "Profile README"`. Then clone it, write `README.md`, and commit and push after approval.
- **Profile fields:** `gh api -X PATCH user -f bio="..." -f blog="..."` needs the `user` token scope. If it fails with 403 or 404, tell the user to edit the fields in **Settings → Public profile**, or to run `gh auth refresh -s user` themselves.
- **Pins:** done in the UI (**Customize your pins** on the profile). List the six in order.

## Hard rules

Shared rules: [operating-rules.md](../../references/operating-rules.md). Additional rules for this skill:

- **Refuse fake activity:** backdated commits, commit or streak bots, star or follow exchanges. Explain the policy in one or two sentences ([github-facts.md](../../references/github-facts.md#platform-policy)), then offer the honest fixes in [contributions.md](references/contributions.md).
- **No invented claims:** employers, titles, years of experience, user counts, and "expert in" lists come only from the user or verifiable sources.
- **Personal data is the user's choice.** Location, email, pronouns, and hireable status are suggested, never set by default. Never guess pronouns.
- **No third-party widgets by default.** Stats cards, visitor counters, and trophies are optional, and only the honest variants in [contributions.md](references/contributions.md#stats-cards) are offered.

## Example

Input:

> Improve my GitHub profile, I'm looking for backend jobs. I'm dmitri-v.

Output (abridged):

```markdown
**Scorecard:** 5 of 11 pass. Biggest gaps: no profile README, pins show 2 forks and a course exercise, and your commits since March are not on the graph.

**Bio**
Current: "Developer"
Proposed: "Backend engineer: Go and PostgreSQL. I build reliable job and queue systems. Maintainer of pgwatch-lite."

**Pinned six:** pgwatch-lite, qrate, acme-labs/tinyqueue (3 merged PRs), shortlink, terraform-hetzner-k3s, go-retry
Fix before pinning: qrate has no README. Run `github-readme-writer`.

**Contribution graph:** your local commits use `dmitri@laptop.local`, which is not on your account and cannot be added. Set your noreply address for future commits (command below). Past commits with that address stay uncounted.
```

The complete example, including the README draft, is in [references/examples.md](references/examples.md).

## Reference files

- [references/profile-checklist.md](references/profile-checklist.md): profile checks, goal emphasis, and organization profiles
- [references/pinned-repos.md](references/pinned-repos.md): how to pick and order the six
- [references/contributions.md](references/contributions.md): missing-contribution diagnosis, stats-card policy, and what to refuse
- [references/examples.md](references/examples.md): a personal profile and an organization profile
- [templates/profile-README.md](templates/profile-README.md), [templates/org-profile-README.md](templates/org-profile-README.md)

## Related skills

- `github-repo-audit`: run it on each pinned repository
- `github-readme-writer` and `github-discoverability`: fix pinned repositories that lack a README, description, or topics
- `github-upstream-contributor`: build real outside contributions worth pinning
- `github-community-files`: the organization `.github` repository also holds default community files
