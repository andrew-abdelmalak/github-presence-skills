# Community files examples

Fictional repository: `acme-labs/tinyqueue`, a Python library.

## Contents

- [Example 1: CONTRIBUTING and SECURITY](#example-1-contributing-and-security)
- [Example 2: account-wide defaults](#example-2-account-wide-defaults)

## Example 1: CONTRIBUTING and SECURITY

**Input**

> Add a contributing guide and a security policy.

**Detected facts**

| Fact | Source |
|---|---|
| Setup `uv sync`; checks `uv run pytest -q` and `uv run ruff check .` | `.github/workflows/tests.yml` steps |
| Python 3.10 or later, uv | `pyproject.toml`, workflow `setup-uv` step |
| Default branch `main` | `git symbolic-ref refs/remotes/origin/HEAD` |
| 46 of the last 50 subjects match Conventional Commits | `git log -50 --no-merges --format=%s` |
| No DCO trailers, no CLA bot | Commit trailers, workflows |
| License MIT | `LICENSE` |
| Private vulnerability reporting disabled | `gh api repos/acme-labs/tinyqueue/private-vulnerability-reporting` |
| Labels `bug`, `enhancement`, `good first issue` exist | `gh label list` |
| No CODE_OF_CONDUCT.md | Glob |

**The one question asked**

> Two things I can't detect. (1) Which versions get security fixes? Default: "only the latest release". (2) Should reports go only through GitHub's private reporting, or also to an email address? I'd enable private reporting either way.

User answer: "Latest only. Also security@acme-labs.example. We reply within a week."

**Output: `.github/CONTRIBUTING.md`**

````markdown
# Contributing to tinyqueue

Bug reports, fixes, and documentation improvements are welcome. For new features, open an issue first so we can agree on the design before you write code.

## Before you start

- Search [existing issues](https://github.com/acme-labs/tinyqueue/issues) to avoid duplicates.
- For anything larger than a small fix, open an issue first and describe the change you plan.
- Issues labeled [`good first issue`](https://github.com/acme-labs/tinyqueue/labels/good%20first%20issue) are scoped for newcomers.

## Set up your environment

Requirements: Python 3.10 or later, and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/acme-labs/tinyqueue.git
cd tinyqueue
uv sync
```

## Run the checks

```bash
uv run pytest -q
uv run ruff check .
```

CI runs the same checks on every pull request. A pull request with failing checks will not be merged.

## Make your change

1. Create a branch from `main`: `git switch -c fix/retry-backoff`.
2. Keep the change focused on one problem. Unrelated cleanups belong in their own pull request.
3. Add or update tests for behavior changes.
4. Update the documentation when behavior or options change.

## Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `type(scope): summary`, for example `fix(worker): stop retrying after max_attempts`. Use `feat` for new features and `fix` for bug fixes, and add `!` after the type for breaking changes. Release notes are generated from these messages.

## Open a pull request

1. Push your branch and open a pull request against `main`.
2. Fill in the pull request template, and link the issue it resolves (`Fixes #123`).
3. A maintainer will review it. Expect questions; they are part of the process.

## Report a bug or request a feature

Use the [issue forms](https://github.com/acme-labs/tinyqueue/issues/new/choose). For security problems, follow [SECURITY.md](SECURITY.md) instead. Never report vulnerabilities in a public issue.

## License

By contributing, you agree that your contributions are licensed under the project's [MIT License](../LICENSE).
````

Note what was left out: the code of conduct line, because the project has no code of conduct yet, and review timelines, because the user did not commit to one for pull requests.

**Output: `.github/SECURITY.md`**

```markdown
# Security policy

## Supported versions

Only the latest release receives security fixes.

## Report a vulnerability

Do not report security problems in public issues, discussions, or pull requests.

Report them privately through [GitHub private vulnerability reporting](https://github.com/acme-labs/tinyqueue/security/advisories/new), or email security@acme-labs.example.

Include:

- The affected version or commit
- Steps to reproduce, or a proof of concept
- The impact you expect: what an attacker could do

## What happens next

You will get a reply within a week. We will keep you informed while we work on a fix, and credit you in the advisory unless you prefer otherwise.
```

**Summary and approvals**

````markdown
| File | Location | Key facts from |
|---|---|---|
| CONTRIBUTING.md | `.github/CONTRIBUTING.md` | `tests.yml`, `pyproject.toml`, git history |
| SECURITY.md | `.github/SECURITY.md` | Your answers |

**Commands awaiting approval**
```bash
gh api -X PUT repos/acme-labs/tinyqueue/private-vulnerability-reporting
```
SECURITY.md links to private reporting, so enable it before you merge.

**Next step:** add a code of conduct (Contributor Covenant 3.0) and issue forms. Ask me to continue with `github-community-files`.
````

## Example 2: account-wide defaults

**Input**

> I have 14 repos and none of them have a code of conduct or security policy. Fix all of them at once.

**Output**

````markdown
Your account has no `.github` repository yet. Files placed there apply to every repository on `acme-labs` that does not have its own copy.

**Plan**
| File | Goes to | Effect |
|---|---|---|
| CODE_OF_CONDUCT.md (Contributor Covenant 3.0) | `acme-labs/.github` | All 14 repositories |
| SECURITY.md (generic: latest release only, private reporting) | `acme-labs/.github` | 13 repositories. `tinyqueue` keeps its own. |
| SUPPORT.md | `acme-labs/.github` | All 14 |
| ISSUE_TEMPLATE/ (bug, feature, config) | `acme-labs/.github` | All 14 |
| LICENSE | Not possible | GitHub does not support a default LICENSE. Three repositories have none: `scratch`, `talk-demos`, `dotfiles`. |

The generic SECURITY.md cannot list per-repository versions, so it says "only the latest release of each project receives security fixes".

**Commands awaiting approval**
```bash
gh repo create acme-labs/.github --public --description "Default community health files for acme-labs"
git clone https://github.com/acme-labs/.github.git /tmp/acme-labs-dotgithub
```
After you approve, I will write the files into the clone and show you the commit before pushing. Private vulnerability reporting is a per-repository setting, so enabling it on all 14 repositories is a separate list of 14 commands, which I'll show next.
````
