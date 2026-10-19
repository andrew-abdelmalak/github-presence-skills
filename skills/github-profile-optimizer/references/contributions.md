# Contribution graph, stats, and what to refuse

## Contents

- [Diagnose missing contributions](#diagnose-missing-contributions)
- [Fixes](#fixes)
- [Stats cards](#stats-cards)
- [What to refuse](#what-to-refuse)

The counting rules are in [github-facts.md](shared/github-facts.md#contribution-graph). In short, a commit counts only when its author email is linked to the account and it lands on the default or `gh-pages` branch of a repository that is not a fork.

## Diagnose missing contributions

Run these in order and stop at the first cause found. A user can have several causes, though, so finish the list before reporting.

**1. Which emails does the account have?**

```bash
gh api user --jq '{login, id}'
gh api user/emails --jq '.[] | {email, verified, primary}'
```

The second call needs the `user:email` scope. If it fails, ask the user to read **Settings → Emails**, or to run `gh auth refresh -s user:email` themselves. The account's noreply address is `ID+USERNAME@users.noreply.github.com` for accounts created after July 18, 2017. Older accounts that turned on email privacy before that date use `USERNAME@users.noreply.github.com`.

**2. Which emails do the commits use?** In each repository the user cares about:

```bash
git config user.email
git config --global user.email
git log --all --format='%ae' | sort | uniq -c | sort -rn | head
```

For a commit already on GitHub, adding `.patch` to the commit URL shows the author email.

**3. Compare.** Any author email that is not on the account is a cause. Classify each one:
- **A real address the user owns:** it can be added to the account, and past commits then count.
- **A generic address** (`*.local`, `localhost`, `user@hostname`, `(none)`): it can't be added, so past commits stay uncounted.

**4. Check the other rules** for the repositories in question:
- **Forks:** `gh repo view OWNER/REPO --json isFork,parent`. Work in a fork counts only once it is merged upstream.
- **Branches:** commits only on feature branches count after they are merged to the default branch.
- **Timing:** commits made in the last 24 hours may not show yet.
- **Private repositories:** they show only if **Private contributions** is turned on (profile → **Contribution settings**), and then only as counts.

## Fixes

| Cause | Fix | Kind |
|---|---|---|
| A real email not on the account | **Settings → Emails → Add email address**, then verify it. GitHub rebuilds the graph, including past commits, within about 24 hours. | The user does it in the UI |
| A generic email in local config | `git config --global user.email "ID+USERNAME@users.noreply.github.com"` | Persistent config change: show it and wait for a yes |
| Generic-email commits already pushed | They stay uncounted. Rewriting published history to change authors is disruptive and rarely worth it. Say so plainly. | None recommended |
| Work in a fork | Open a pull request upstream (see `github-upstream-contributor`) | |
| Work on unmerged branches | Merge it through a pull request, if it is ready | |
| Private work hidden | Turn on **Private contributions**, if the user wants the counts shown | The user does it in the UI |

To keep a personal email out of future commits, suggest turning on **Keep my email address private** in **Settings → Emails**, and committing with the noreply address.

## Stats cards

Default: **do not add stats cards.** Offer them only when the user asks. They measure activity volume, not quality, and they can fail visibly.

If the user wants them:

| Option | How it works | Caveats |
|---|---|---|
| [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) through its GitHub Actions workflow or a self-hosted instance | Generates SVG cards | The project's README says the public instance is best-effort and can be unreliable under rate limits and traffic, and it recommends self-hosting or the Actions workflow. Do not use the public instance URL. |
| [lowlighter/metrics](https://github.com/lowlighter/metrics) | An Actions workflow that commits a generated SVG to the profile repository | Needs a token secret in the profile repository. Many plugins: pick one or two. |
| [Platane/snk](https://github.com/Platane/snk) | An Actions workflow that generates a contribution-graph "snake" animation | Decorative only |
| [github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats) | Streak card | Rewards daily activity rather than meaningful work. Recommend against it for `job-search`. |

Rules when adding one:
- **Prefer Actions-generated images committed to the profile repository.** They never show a broken image when a third-party service is down.
- **Tokens go in Actions secrets.** A personal access token used for private stats belongs in a repository secret, never in the README or a workflow file. Use the smallest scope the tool documents.
- **At most one card,** placed after the projects section, never above it.
- **Freshness:** a scheduled workflow that regenerates the card stops after 60 days with no activity in the repository (see [github-facts.md](shared/github-facts.md#github-actions)). The card then silently shows old numbers. Tell the user, and suggest re-enabling the workflow from the Actions tab when that happens.

## What to refuse

Refuse these, explain in one or two sentences, and offer the honest alternative:

| Request | Why not | Honest alternative |
|---|---|---|
| Fill the graph with backdated commits, or draw text or patterns in it | Deceptive. The graph places commits by author date, which is trivially faked, and GitHub's Acceptable Use Policies prohibit automated inauthentic activity. | Fix uncounted real work with the diagnosis above |
| A bot or Action that commits daily to keep a streak | Same as above, and it misleads anyone reading the graph | Turn on private contributions if the real work happens in private repositories |
| Star-for-star or follow-for-follow, or scripts that star or follow in bulk | Explicitly prohibited as rank abuse. It also risks account restrictions. | Improve discoverability (`github-discoverability`), and share the work where its audience is |
| Trivial pull requests to other projects to "get contributions" | Prohibited as disruptive ("empty or meaningless" PRs), and it burns maintainer goodwill | `github-upstream-contributor` finds real issues to work on |
