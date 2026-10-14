# Profile optimizer examples

Both accounts are fictional: the user `dmitri-v` and the organization `acme-labs`.

## Contents

- [Example 1: personal profile, job search](#example-1-personal-profile-job-search)
- [Example 2: organization profile](#example-2-organization-profile)

## Example 1: personal profile, job search

**Input**

> Improve my GitHub profile, I'm looking for backend jobs. I'm dmitri-v. I mostly do Go and Postgres. Remote, EU time zones.

**Data collected**

| Item | Value |
|---|---|
| `bio` / `name` / `blog` | "Developer" / "Dmitri V." / empty |
| Profile repository `dmitri-v/dmitri-v` | Does not exist |
| Pinned now | Nothing pinned, so GitHub shows "Popular repositories": `awesome-go` (fork, no own commits), `dotfiles`, `cs50-pset` (course exercises), `pgwatch-lite`, `shortlink`, `go-retry` |
| Pinnable highlights | `pgwatch-lite` (Go, 140 stars, README, MIT), `shortlink` (Go and PostgreSQL, README, MIT), `qrate` (Go rate limiter, no README, no license), `terraform-hetzner-k3s` (HCL, README), `go-retry` (small library, README, MIT), `acme-labs/tinyqueue` (3 merged PRs) |
| Merged outside PRs | `acme-labs/tinyqueue` #31, #36, #52 |
| Account emails | `dmitri.v@example.com` (primary), noreply `48151623+dmitri-v@users.noreply.github.com` |
| Local commit email | `dmitri@laptop.local` in `git config --global user.email`. 212 commits since March use it. |

**Output**

````markdown
**Scorecard (goal: job-search):** 5 of 11 pass.
| ID | Check | Verdict |
|---|---|---|
| P1 | Profile README | Fix: repository `dmitri-v/dmitri-v` does not exist |
| P5 | Bio | Fix: "Developer" says nothing about backend or Go |
| P7 | Avatar | Check visually |
| P8 | Links | Fix: no website or contact link for recruiters |
| P9 | Pins chosen | Fix: automatic "Popular repositories" show a fork and a course exercise |
| P10 | Pins ready | Fix: `qrate` has no README and no license |
| P11 | Graph reflects work | Fix: 212 commits since March use an email that is not on your account |
| P2, P3, P4, P6, P12, P13 | | Pass or user's choice |

**Bio** (113 characters)
Current: "Developer"
Proposed: "Backend engineer: Go and PostgreSQL. I build reliable job queues and monitoring tools. Remote, EU time zones."

**Pinned six** (order matters; set them with **Customize your pins** on your profile)
| # | Repository | Why |
|---|---|---|
| 1 | pgwatch-lite | Flagship: Go plus PostgreSQL, used by others (140 stars), documented |
| 2 | shortlink | Shows end-to-end backend work: HTTP API, PostgreSQL schema, Docker |
| 3 | acme-labs/tinyqueue | 3 merged PRs to someone else's project: proof you work well in a team codebase |
| 4 | qrate | Rate limiting, a classic backend interview topic. Needs a README first. |
| 5 | terraform-hetzner-k3s | Variety: infrastructure as code |
| 6 | go-retry | A small, clean, tested Go library |
Dropped: `awesome-go` (a fork with no commits of yours), `cs50-pset` (a course exercise), `dotfiles`.

**Fix before pinning**
- qrate: no README, no license. Run `github-readme-writer`, then `github-community-files` (LICENSE).

**Contribution graph**
Your global git config uses `dmitri@laptop.local`. GitHub cannot link generic `.local` addresses, so 212 commits since March are not counted. Those past commits will stay uncounted, because rewriting published history is not worth it. Future commits can count:

```bash
git config --global user.email "48151623+dmitri-v@users.noreply.github.com"
```

This uses your noreply address, so your personal email stays out of public commit history.

**Profile README draft** (for `dmitri-v/dmitri-v/README.md`)

# Hi, I'm Dmitri

Backend engineer working on job queues and monitoring tools in Go and PostgreSQL.

Looking for backend roles, remote, in EU time zones.

## Selected projects

| Project | What it does |
|---|---|
| [pgwatch-lite](https://github.com/dmitri-v/pgwatch-lite) | Lightweight PostgreSQL monitoring: slow queries, locks, and replication lag in one binary |
| [shortlink](https://github.com/dmitri-v/shortlink) | URL shortener with a REST API, PostgreSQL storage, and Docker deployment |
| [qrate](https://github.com/dmitri-v/qrate) | Token-bucket rate limiter for Go HTTP services |

## Open source contributions

- [acme-labs/tinyqueue](https://github.com/acme-labs/tinyqueue/pulls?q=is%3Apr+author%3Admitri-v+is%3Amerged): retry backoff, SQLite locking fixes, and docs (3 merged PRs)

## Get in touch

<!-- TODO: which contact links do you want public? For example, LinkedIn or a website. -->

**Placeholders to fill:** public contact links. Optional: your current or previous employer, if you want it shown.

**Commands awaiting approval**
```bash
gh repo create dmitri-v --public --description "Profile README"
git config --global user.email "48151623+dmitri-v@users.noreply.github.com"
gh api -X PATCH user -f bio="Backend engineer: Go and PostgreSQL. I build reliable job queues and monitoring tools. Remote, EU time zones."
```
If the last command fails with 403, your token lacks the `user` scope. Paste the bio in **Settings → Public profile** instead.

**In the GitHub UI (no API):** set the six pins in the order above, upload a profile photo if you have not, and decide whether to turn on **Private contributions**.
````

Note what the skill did not do:
- No stats card, because the user did not ask for one.
- No claimed years of experience or employer.
- The pinned repositories' descriptions in the README draft come from the repositories' own descriptions and READMEs.

## Example 2: organization profile

**Input**

> Set up the profile page for our org, acme-labs.

**Data collected**
- `gh api orgs/acme-labs`: description empty, blog `https://acme-labs.example`.
- `acme-labs/.github` exists (it was created for default community files) and has no `profile/` folder.
- Public repositories: `tinyqueue` (library), `logslice` (CLI), `fluxboard` (app), and 11 smaller ones. Five open `good first issue` issues across the organization.
- Discussions are enabled on `tinyqueue` only.

**Output**

````markdown
**Proposed `acme-labs/.github/profile/README.md`**

# Acme Labs

Small, dependable open source tools for running background jobs and reading logs.

## Projects

| Project | What it is |
|---|---|
| [tinyqueue](https://github.com/acme-labs/tinyqueue) | Dependency-free job queue for Python scripts, backed by SQLite |
| [logslice](https://github.com/acme-labs/logslice) | CLI that cuts large log files to a time window or request ID |
| [fluxboard](https://github.com/acme-labs/fluxboard) | Self-hosted dashboard for monitoring webhook deliveries |

## Get involved

- Read the [contributing guide](https://github.com/acme-labs/.github/blob/main/CONTRIBUTING.md) before opening a pull request.
- Find a starter task: [good first issues across Acme Labs](https://github.com/search?q=org%3Aacme-labs+label%3A%22good+first+issue%22+state%3Aopen&type=issues).
- Ask questions in [tinyqueue Discussions](https://github.com/acme-labs/tinyqueue/discussions).

## Security

Report vulnerabilities privately, as described in each project's security policy. Never report them in public issues.

**Organization pins (public view):** tinyqueue, logslice, fluxboard.

**Commands awaiting approval**
```bash
git clone https://github.com/acme-labs/.github.git /tmp/acme-labs-dotgithub
# write profile/README.md, then:
git -C /tmp/acme-labs-dotgithub add profile/README.md
git -C /tmp/acme-labs-dotgithub commit -m "Add organization profile README"
git -C /tmp/acme-labs-dotgithub push
gh api -X PATCH orgs/acme-labs -f description="Small, dependable open source tools for background jobs and logs"
```
The last command needs organization admin rights and the `admin:org` scope.
````
