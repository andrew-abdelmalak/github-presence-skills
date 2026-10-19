# Community file guide

## Contents

- [Which files a project needs](#which-files-a-project-needs)
- [Per-file rules](#per-file-rules)
- [License guide](#license-guide)
- [Code of conduct](#code-of-conduct)
- [Commit convention](#commit-convention)
- [Labels](#labels)
- [Account-wide defaults](#account-wide-defaults)

## Which files a project needs

| File | Add when | Skip when |
|---|---|---|
| LICENSE | Always, for public code others may use | Never skip for a public project. Without a license, others have no right to use the code. |
| CONTRIBUTING.md | The project accepts outside contributions | The README says contributions are not accepted |
| SECURITY.md | The code runs anywhere other than the author's own machine | Pure notes or collections |
| CODE_OF_CONDUCT.md | People interact in issues, discussions, or chat | Single-author archives |
| Issue forms + config.yml | Issues are enabled | Issues are disabled |
| pull_request_template.md | The project accepts pull requests | Same as CONTRIBUTING |
| SUPPORT.md | Questions arrive as issues, or there is a forum, chat, or commercial support | `config.yml` `contact_links` already covers it |
| CODEOWNERS | Two or more maintainers own different areas, or reviews must be automatic | Single maintainer |
| FUNDING.yml | The maintainer has a sponsorship or donation account | No account exists. Never create placeholder handles. |
| CITATION.cff | Research software, datasets, or anything people cite in papers | Other projects |

## Per-file rules

**CONTRIBUTING.md** ([template](../templates/CONTRIBUTING.md))
- Start with one sentence on what kinds of contributions are welcome. Do not open with a long thank-you.
- Setup, test, and lint commands must match CI exactly. When they differ, CI is the truth. Flag the drift.
- State the branch to target, the commit convention, sign-off rules (DCO or CLA), and what review looks like.
- Include a section on AI-assisted contributions only if the maintainer chooses a policy. Ask; do not decide for them.
- Inbound license: one line saying contributions are licensed under the project license, unless a CLA says otherwise.

**SECURITY.md** ([template](../templates/SECURITY.md))
- Supported versions come from the user or the release policy. If unknown, write "Only the latest release receives security fixes" and ask the user to confirm.
- The reporting channel for public repositories is private vulnerability reporting (`https://github.com/OWNER/REPO/security/advisories/new`) once it is enabled, with an email fallback if the user gives one.
- State what a good report contains (affected version, reproduction, impact) and what happens next. Include timelines only if the maintainer commits to them.

**CODE_OF_CONDUCT.md**: see [Code of conduct](#code-of-conduct).

**SUPPORT.md** ([template](../templates/SUPPORT.md)): where to ask questions, what the maintainers do not support, and paid support if it exists.

**Issue forms** ([bug](../templates/ISSUE_TEMPLATE/bug_report.yml), [feature](../templates/ISSUE_TEMPLATE/feature_request.yml), [config](../templates/ISSUE_TEMPLATE/config.yml))
- Required top-level keys are `name`, `description`, and `body`. Labels must already exist.
- Ask only for what maintainers need to act. Every required field costs reporters effort.
- Version fields should list real versions, or be free text if versions change often.
- `config.yml` sets `blank_issues_enabled: false` only when the forms cover every case. Route questions to Discussions or SUPPORT.md, and security reports to private reporting, through `contact_links`.

**pull_request_template.md** ([template](../templates/pull_request_template.md)): a summary, the linked issue, how it was tested, and a short checklist. Keep the checklist to items reviewers actually check.

**CODEOWNERS** ([template](../templates/CODEOWNERS))
- The last matching pattern wins, so put the catch-all `*` line first.
- Owners must have write access, or reviews are not requested.
- Team owners use `@org/team`.

**FUNDING.yml** ([template](../templates/FUNDING.yml)): only the keys listed in [github-facts.md](shared/github-facts.md#community-health-files), with real handles from the user.

**CITATION.cff** ([template](../templates/CITATION.cff))
- Use `cff-version: 1.2.0`.
- Authors need `family-names` and `given-names`. Add `orcid` when the user provides it.
- `version` and `date-released` must match a real release.
- If `cffconvert` is installed, validate with `cffconvert --validate`.

## License guide

This is orientation, not legal advice. For anything with commercial or employer implications, the user should check with their organization or a lawyer.

| Goal | Common choice | GitHub API key |
|---|---|---|
| Maximum reuse, short and simple | MIT | `mit` |
| Permissive, with an explicit patent grant | Apache License 2.0 | `apache-2.0` |
| Changes to these files must stay open, but they can be combined with closed code | Mozilla Public License 2.0 | `mpl-2.0` |
| Every distributed derivative must stay open | GNU GPL v3 | `gpl-3.0` |
| Same as GPL, and also covers network use (SaaS) | GNU AGPL v3 | `agpl-3.0` |
| Public domain dedication | CC0 1.0 or The Unlicense | `cc0-1.0`, `unlicense` |

Procedure:
1. Check for license constraints: an employer's policy, licenses of copied code, and dependency licenses. GPL dependencies matter most for permissive projects that distribute bundled builds.
2. Fetch the text: `gh api licenses/KEY --jq .body > LICENSE`.
3. Replace `[year]` with the current year and `[fullname]` with the copyright holder (a person or organization the user confirms).
4. For documentation or data with no code, Creative Commons licenses such as CC BY 4.0 are common. GitHub's license API offers only `cc0-1.0` from that family, so take any other CC text from creativecommons.org.

## Code of conduct

Use Contributor Covenant 3.0, the current version, unless the project already uses another code.

```bash
gh api -H "Accept: application/vnd.github.raw+json" \
  "repos/EthicalSource/contributor_covenant/contents/content/version/3/0/code_of_conduct.md?ref=release" \
  | awk 'BEGIN{n=0} /^\+\+\+$/{n++; next} n>=2' > CODE_OF_CONDUCT.md
```

Then:
1. Replace `[NOTE: describe your means of reporting here.]` with the contact the user provides: an email address or a form. A GitHub username alone is not a private channel.
2. The enforcement section starts with a `[NOTE: ...]` paragraph. Ask whether the maintainers accept the suggested ladder. If they do, delete that note line. If they do not, insert their own process in its place.
3. Keep the Attribution section unchanged. The text is licensed CC BY-SA 4.0.
4. Never paraphrase the covenant's body.

Fallback if that fetch fails: `gh api codes_of_conduct/contributor_covenant --jq .body` returns version 2.0. Replace `[INSERT CONTACT METHOD]` with the contact, and tell the user it is the older version.

## Commit convention

Detect the existing convention:

```bash
git log -50 --no-merges --format=%s
```

Count the subjects that match `^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?: `.

| Match rate | Action |
|---|---|
| 70% or more | Document Conventional Commits in CONTRIBUTING.md, and link the [spec](https://www.conventionalcommits.org/en/v1.0.0/) |
| 20% to 70% | Mention the mix and ask whether to standardize. If yes, document it, and hand off to `github-release-writer` for tooling. |
| Under 20% | Document what the history shows (for example, "imperative summary under 72 characters"). Suggest Conventional Commits only if the user wants generated changelogs. |

Do not add commit-lint tooling from this skill. That decision belongs to `github-release-writer`.

## Labels

- New GitHub repositories include `good first issue` and `help wanted` among their default labels. Older or imported repositories may not, so check with `gh label list`.
- Issue forms reference `bug` and `enhancement`. Create missing labels only with approval.
- A `good first issue` label only helps when open issues carry it and each one says where to start.

## Account-wide defaults

Write files into the **public** `.github` repository of the user or organization (see [github-facts.md](shared/github-facts.md#community-health-files)).

1. Check that it exists: `gh repo view OWNER/.github`. If it does not, creating it is a remote change and needs approval: `gh repo create OWNER/.github --public --description "Default community health files"`.
2. Write CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, SUPPORT.md, FUNDING.yml, and `ISSUE_TEMPLATE/`. Keep the text generic across repositories. Commands that differ by repository belong in each repository's own CONTRIBUTING.md.
3. LICENSE cannot be a default. Each repository needs its own.
4. In organizations, the same repository can also hold `profile/README.md` (see `github-profile-optimizer`).
5. A repository's own file always wins, so tell the user which repositories will keep their own copies.
6. **Issue templates are all-or-nothing.** If a repository has any valid issue template or `config.yml` in its own `.github/ISSUE_TEMPLATE/`, none of the default templates apply to it (GitHub Docs). To use the shared forms, delete that repository's own folder. To keep one local form, copy every shared form into it.
7. **CODEOWNERS needs a ruleset to bite.** A CODEOWNERS file only requests reviews. Merges are blocked only when a ruleset requires code-owner review (see `github-repo-hardening`). Cover `/.github/` in CODEOWNERS so changes to workflows get the right reviewers.
