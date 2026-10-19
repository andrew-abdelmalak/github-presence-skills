# GitHub facts

Platform rules and limits that the skills in this package depend on. Skills cite this file instead of repeating numbers, so a change on GitHub's side is fixed in one place.

**Last verified:** 2026-10-12, against the source of docs.github.com (the `github/docs` repository), GitHub's site policy (`github/site-policy`), and live REST API responses. Before you rely on a fact for something irreversible, check the linked source again.

## Contents

- [Profiles and organizations](#profiles-and-organizations)
- [Repository metadata](#repository-metadata)
- [README rendering](#readme-rendering)
- [Community health files](#community-health-files)
- [Licenses and codes of conduct](#licenses-and-codes-of-conduct)
- [Security reporting](#security-reporting)
- [Releases](#releases)
- [Contribution graph](#contribution-graph)
- [GitHub Actions](#github-actions)
- [Rulesets and security features](#rulesets-and-security-features)
- [GitHub Pages](#github-pages)
- [Platform policy](#platform-policy)

## Profiles and organizations

| Fact | Source |
|---|---|
| A profile README appears when a **public** repository is named exactly like the username and has a non-empty `README.md` at its root. Repositories created before July 2020 need **Share to profile** clicked once. | [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme) |
| A user can pin **up to six** repositories and gists, combined, through **Customize your pins** on the profile. GitHub documents no API for pinning. | [Pinning items to your profile](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile) |
| The GraphQL fields `user { pinnedItems }` and `user { pinnableItems }` return what is pinned now and what can be pinned. `pinnableItems` includes repositories owned by others that the user contributed to. | GraphQL API responses, checked 2026-10-12 |
| An organization can pin up to six repositories for the public view and six for the member view. | [Customizing your organization's profile](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile) |
| Organization profile README: `profile/README.md` in a **public** repository named `.github`. Member-only README: `profile/README.md` in a **private** repository named `.github-private`. | Same as above |

## Repository metadata

| Fact | Source |
|---|---|
| Topics: at most **20** per repository, each **50 characters or less**, using lowercase letters, numbers, and hyphens. | [Classifying your repository with topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) |
| `gh api "search/topics?q=<term>"` returns matching topics with `featured` and `curated` flags. A curated topic has a topic page that GitHub maintains. | REST API response, checked 2026-10-12 |
| Social preview image: PNG, JPG, or GIF, **under 1 MB**. Recommended **1280×640** px, minimum **640×320** px. PNG transparency is supported. GitHub documents only the Settings UI for uploading it (**Settings → Social preview → Edit**). | [Customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) |
| `gh repo view --json usesCustomOpenGraphImage,openGraphImageUrl` shows whether a custom social preview is set. | `gh` CLI field list |
| Renaming a repository redirects web traffic and `git clone`/`fetch`/`push`, **except** GitHub Pages project-site URLs. Actions referenced with `uses: owner/old-name` are **not** redirected and fail with `repository not found`. Creating a new repository with the old name breaks the redirects. | [Renaming a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository) |
| `gh repo edit` accepts `--description`, `--homepage`, `--add-topic`, and `--remove-topic`. | `gh repo edit --help` |
| Pushing a file larger than **50 MiB** prints a warning. Files larger than **100 MiB** are blocked and need Git LFS. Uploads through the browser are limited to 25 MiB. | [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) |

## README rendering

| Fact | Source |
|---|---|
| GitHub shows the README from `.github/`, the repository root, or `docs/`, checked in that order. | [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) |
| Content beyond **500 KiB** is truncated. | Same as above |
| GitHub generates an outline (table of contents) from headings automatically, so a hand-written table of contents is optional. | Same as above |
| Relative links and image paths work in rendered Markdown. | Same as above |
| Alert blocks render from `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, and `> [!CAUTION]`. | [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) |
| A workflow status badge lives at `https://github.com/OWNER/REPO/actions/workflows/FILE/badge.svg`. Add `?branch=NAME` or `?event=push` to filter it. | [Adding a workflow status badge](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge) |

## Community health files

| File | Where GitHub looks | Notes |
|---|---|---|
| `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`, `ACCESSIBILITY.md` | `.github/`, then root, then `docs/` | Can be an account-wide default |
| `FUNDING.yml` | `.github/` only, default branch | Can be an account-wide default |
| Issue templates and forms | `.github/ISSUE_TEMPLATE/` | Can be an account-wide default |
| Discussion category forms | `.github/DISCUSSION_TEMPLATE/` | |
| Pull request template | `pull_request_template.md` in root, `docs/`, or `.github/`. Several templates go in `.github/PULL_REQUEST_TEMPLATE/` and are chosen with the `?template=` query parameter. | |
| `CODEOWNERS` | `.github/`, then root, then `docs/`; the first one found is used | Must be under 3 MB |
| `CITATION.cff` | Root of the default branch | Adds **Cite this repository** (APA and BibTeX) |
| `LICENSE` | Repository root | **Cannot** be an account-wide default |

Sources: [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file), [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [Creating a pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository), [About CITATION files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files).

**Account-wide defaults.** Put a file in a **public** repository named `.github` on the account. GitHub then uses it for every repository on that account that has no file of the same type. A repository's own file overrides the default.

**Community profile checklist.** For public repositories, GitHub checks for a README, `CODE_OF_CONDUCT`, `LICENSE`, `CONTRIBUTING`, issue templates, and a security policy. `gh api repos/OWNER/REPO/community/profile` returns `health_percentage` and the files it found. Markdown issue templates count only with valid `name:` and `about:` keys. ([About community profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories))

**Issue forms.** Every form must start with `name`, `description`, and `body`. The optional keys are `title`, `labels`, `assignees`, `type`, and `projects`. Labels that do not exist in the repository are not created. Forms work for issues only, not pull requests. `.github/ISSUE_TEMPLATE/config.yml` takes `blank_issues_enabled` and `contact_links`. Changes take effect once merged to the default branch. ([Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms), [Configuring issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository))

**CODEOWNERS syntax.** Patterns follow gitignore rules except that `\#` escapes, `!` negation, and `[ ]` ranges do not work. The last matching pattern takes precedence. All owners for one pattern must be on the same line.

**FUNDING.yml keys.** `github`, `patreon`, `open_collective`, `ko_fi`, `tidelift`, `community_bridge`, `liberapay`, `issuehunt`, `polar`, `buy_me_a_coffee`, `thanks_dev`, `custom`. Each external platform takes one value. `github` takes up to four usernames plus one organization, and `custom` takes up to four URLs. Quote any URL that contains `:` inside an array. ([Displaying a sponsor button](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository))

**Labels.** GitHub surfaces issues labeled `good first issue` to new contributors in search and recommendations. `help wanted` is a widespread convention, but this doc does not name it. ([Encouraging helpful contributions with labels](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/encouraging-helpful-contributions-to-your-project-with-labels))

## Licenses and codes of conduct

| Fact | Source |
|---|---|
| GitHub shows a detected license in the repository sidebar. Name the file `LICENSE` or `LICENSE.md`. | [Adding a license to a repository](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) |
| `gh api licenses --jq '.[].key'` lists the license templates GitHub serves: `agpl-3.0 apache-2.0 bsd-2-clause bsd-3-clause bsl-1.0 cc0-1.0 epl-2.0 gpl-2.0 gpl-3.0 lgpl-2.1 mit mpl-2.0 unlicense`. `gh api licenses/<key> --jq .body` returns the text with `[year]` and `[fullname]` placeholders. | REST API response, checked 2026-10-12 |
| `gh api codes_of_conduct/contributor_covenant --jq .body` returns Contributor Covenant **2.0**, with the placeholder `[INSERT CONTACT METHOD]`. | REST API response, checked 2026-10-12 |
| The current Contributor Covenant is **3.0**, licensed CC BY-SA 4.0. Its source text is at `content/version/3/0/code_of_conduct.md` on the `release` branch of `EthicalSource/contributor_covenant`, with TOML front matter between `+++` lines and two `[NOTE: ...]` placeholders (reporting method and enforcement). | [EthicalSource/contributor_covenant](https://github.com/EthicalSource/contributor_covenant) |
| GitHub looks for a code of conduct in `.github/`, then root, then `docs/`. | [Adding a code of conduct](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project) |

## Security reporting

| Fact | Source |
|---|---|
| `SECURITY.md` should state the supported versions and how to report a vulnerability. | [Adding a security policy](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy) |
| Owners and admins of a public repository can enable **private vulnerability reporting**, which adds a **Report a vulnerability** button. By default the form asks for a summary, details, proof of concept, and impact. `gh api repos/OWNER/REPO/private-vulnerability-reporting` returns `{"enabled": true|false}`. `PUT` on the same path enables it, and `DELETE` disables it. | [Configuring private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository) |

## Releases

| Fact | Source |
|---|---|
| `.github/release.yml` configures generated release notes. Top-level `changelog` holds `exclude` (`labels`, `authors`) and `categories`. Each category has a required `title` and `labels` (`"*"` catches everything else), plus optional `exclude`. | [Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) |
| `gh release create <tag>` accepts `--generate-notes`, `--notes-start-tag`, `--notes-file`, `--draft`, `--latest`, and `--verify-tag`. | `gh release create --help` |
| `POST /repos/OWNER/REPO/releases/generate-notes` (with `tag_name`, optional `previous_tag_name` and `target_commitish`) returns a generated name and body. GitHub documents that the result "is not saved anywhere". It is meant as a draft for a new release. | [GitHub REST OpenAPI description](https://github.com/github/rest-api-description) |

## Contribution graph

A commit appears on the graph only when **all** of these are true:

1. It was authored with an email address linked to the account, or with the account's GitHub-provided `noreply` address.
2. It is in a standalone repository, not a fork.
3. It is on the default branch or the `gh-pages` branch.

At least one of these must also be true: you are a collaborator or organization member, you have forked the repository, or you have opened an issue or pull request in it.

Other facts:

- Creating a repository and forking one always count. Issues, pull requests, reviews, and discussions count when they are opened in a standalone repository, not a fork.
- Updates can take up to 24 hours.
- Adding a previously used email address to the account rebuilds past contributions. Generic addresses such as `jane@computer.local` can't be added.
- Adding `.patch` to a commit URL shows the author email that was used.
- The profile places commits by their **author date**.
- Private contributions can be shown as anonymous daily counts.

Sources: [Profile contributions reference](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference), [Troubleshooting missing contributions](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions).

## GitHub Actions

| Fact | Source |
|---|---|
| In a public repository, scheduled workflows are disabled automatically after 60 days with no repository activity. When a public repository is forked, scheduled workflows are disabled by default. | [Disabling and enabling a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows) |
| The OpenSSF Scorecard action needs `publish_results: true` and job permission `id-token: write` to publish results to `api.scorecard.dev` and enable the badge. | [ossf/scorecard-action](https://github.com/ossf/scorecard-action) |

## Rulesets and security features

| Fact | Source |
|---|---|
| Rulesets are available in public repositories on GitHub Free, and in public and private repositories on GitHub Pro, Team, and Enterprise Cloud. | [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) |
| Secret scanning runs automatically for free on public repositories. Private and internal organization repositories need GitHub Secret Protection. | GitHub Docs feature availability for secret scanning |
| Code scanning is available for public repositories, and for organization-owned private repositories with GitHub Code Security. | GitHub Docs feature availability for code scanning |
| `POST /repos/OWNER/REPO/rulesets` creates a ruleset. The `pull_request` rule requires `required_approving_review_count`, `dismiss_stale_reviews_on_push`, `require_code_owner_review`, `require_last_push_approval`, and `required_review_thread_resolution`. `PUT .../vulnerability-alerts`, `PUT .../automated-security-fixes`, and `PATCH .../code-scanning/default-setup` exist. | GitHub REST OpenAPI description |
| Dependabot's `cooldown` option takes `default-days`, plus `semver-major-days`, `semver-minor-days`, and `semver-patch-days` where the ecosystem supports SemVer. | [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) |
| If a repository has any valid issue template or `config.yml` in its own `.github/ISSUE_TEMPLATE`, none of the account-default issue templates are used for it. | [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) |

## GitHub Pages

| Fact | Source |
|---|---|
| One user or organization site per account, published from a repository named `<owner>.github.io`. | [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) |
| Published sites can be at most 1 GB, and the recommended source repository limit is 1 GB. Deployments time out after 10 minutes. Soft limits: 100 GB of bandwidth per month, and 10 builds per hour unless you deploy with a custom Actions workflow. | Same as above |
| Pages is not for running an online business, e-commerce, or SaaS. | Same as above |
| Verifying a custom domain stops other users from taking it over, which can happen when a site is deleted while its DNS records stay. Verification covers immediate subdomains. | [Verifying your custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages) |

## Platform policy

- GitHub's Acceptable Use Policies (section 4, "Spam and Inauthentic Activity") prohibit inauthentic interactions such as fake accounts and automated inauthentic activity, and **rank abuse such as automated starring or following**. ([Acceptable Use Policies](https://github.com/github/site-policy/blob/main/Policies/acceptable-use-policies/github-acceptable-use-policies.md))
- The policy on disrupting other users lists opening empty or meaningless issues or pull requests, and starring or following in large volume within a short period. ([Disrupting the experience of other users](https://github.com/github/site-policy/blob/main/Policies/acceptable-use-policies/github-disrupting-the-experience-of-other-users.md))
