---
name: github-community-files
description: "Drafts GitHub community health files that match how the project really works: LICENSE, CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, SUPPORT.md, issue forms, pull request template, CODEOWNERS, FUNDING.yml, CITATION.cff, and account-wide defaults in a .github repository. Make sure to use this skill whenever the user mentions any of these files, a security or vulnerability reporting policy, issue or pull request templates, a code of conduct, choosing a license, contribution guidelines, or a sponsor button. Not for README.md (use github-readme-writer)."
---

# Community files

Write the files that tell people how to use, contribute to, report problems in, and fund a project, filled with the project's real commands and contacts rather than generic boilerplate.

## When to use

- "Add a CONTRIBUTING guide", "we need a security policy", "set up issue templates", "add a code of conduct", "which license should I use"
- A `github-repo-audit` result lists area C fixes
- The user wants the same files across all their repositories (`--account-defaults`)

## Input

- **Path** to the local repository (default: the current directory).
- **Files**: specific names, or `all` for the standard set. The standard set is LICENSE (if missing), CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, issue forms with `config.yml`, and a PR template. Add SUPPORT, CODEOWNERS, FUNDING, and CITATION only when they fit (see the file guide).
- **`--account-defaults`**: write the files into the account's `.github` repository so they apply to every repository without its own copy.

## Output

- Each file written to the location in [github-facts.md](references/shared/github-facts.md#community-health-files): `.github/` by default for this skill, except LICENSE and CITATION.cff, which go at the root.
- A summary table with file, location, and source of the key facts.
- Placeholders, and any settings changes (enable private vulnerability reporting, create missing labels) as commands awaiting approval.

## Workflow

```
Community files progress:
- [ ] 1. Find existing files and defaults
- [ ] 2. Choose the file set
- [ ] 3. Learn the real workflow
- [ ] 4. Ask for what cannot be detected (one message)
- [ ] 5. Draft each file
- [ ] 6. Validate
- [ ] 7. Write files and list settings changes
```

**1. Find existing files** in `.github/`, root, and `docs/`. Note which already exist, and do not overwrite them silently. If `gh` works, also check `gh api repos/OWNER/.github/contents --jq '.[].name'`. Files there already act as defaults, and a new per-repository file overrides them. Say which applies.

**2. Choose the file set** from the request, or from the audit's area C fixes. Use [references/file-guide.md](references/file-guide.md#which-files-a-project-needs) to decide on SUPPORT, CODEOWNERS, FUNDING, and CITATION.

**3. Learn the real workflow.** Detect, never assume:
- **Setup, test, lint, and build commands.** CI workflow steps are the most reliable source, then the Makefile or justfile, then manifest scripts.
- **Default branch:** `git symbolic-ref refs/remotes/origin/HEAD`.
- **Commit convention:** follow [the detection rule in the file guide](references/file-guide.md#commit-convention).
- **Sign-off requirements:** `Signed-off-by:` trailers mean DCO. A CLA bot in workflows means a CLA.
- **Maintainers:** `gh api repos/OWNER/REPO/contributors --jq '.[0:5][].login'`, for CODEOWNERS candidates. Confirm them with the user.
- **Labels:** `gh label list` shows which labels exist for the issue forms.
- **Private vulnerability reporting:** `gh api repos/OWNER/REPO/private-vulnerability-reporting`.

**4. Ask once**, in a single message, for what cannot be detected:
- The security contact and response expectations.
- Supported versions.
- The code of conduct reporting contact.
- Funding handles.
- Citation authors and ORCID iDs.
- The license choice, if no LICENSE exists.

Offer defaults where sensible. For example, private vulnerability reporting is the default security channel for public repositories. When every open question has a safe default, do not stop: draft the files with the defaults, and list the decisions at the end so the user can change them. Stop and ask first only when a fact has no safe default, such as a private email address, the license choice, or funding handles.

**5. Draft each file** from `templates/`, following the per-file rules in [references/file-guide.md](references/file-guide.md). Two files are never written from memory:
- **LICENSE:** `gh api licenses/KEY --jq .body`. Replace `[year]` and `[fullname]`. Read the license guide in the file guide first.
- **CODE_OF_CONDUCT.md:** fetch Contributor Covenant 3.0 verbatim, as described in [the file guide](references/file-guide.md#code-of-conduct), and fill only its placeholders.

**6. Validate.**
- Each issue form parses as YAML and has `name`, `description`, and `body`. If PyYAML exists, check with `python3 -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]))" FILE`.
- Every label in a form exists, or is listed for creation.
- Every CODEOWNERS owner exists (`gh api users/NAME` or `gh api orgs/ORG/teams/TEAM`).
- FUNDING.yml uses only valid keys.
- Every command in CONTRIBUTING.md appears in CI, a Makefile, or the manifests.
- No placeholder like `[INSERT` or `[NOTE:` remains unlisted.

**7. Write the files** and print the summary. List remote changes as commands awaiting approval. For example:

```bash
gh api -X PUT repos/OWNER/REPO/private-vulnerability-reporting
gh label create "good first issue" --color 7057ff --description "Good for newcomers"
```

## Hard rules

Shared rules: [operating-rules.md](references/shared/operating-rules.md). Additional rules for this skill:

- **Legal and policy texts are fetched, not written.** LICENSE comes from GitHub's license API. The code of conduct comes from the Contributor Covenant source. Never paraphrase or "improve" either. Say plainly that license guidance is not legal advice.
- **No invented commitments.** Response times, supported versions, bounty programs, and safe-harbor language appear only if the user provides or approves them.
- **Security reports never go to public issues.** SECURITY.md must route vulnerabilities to private reporting or a private address, and every `config.yml` you write must include a `contact_links` entry that sends security reports there, even when blank issues stay enabled.
- **Do not overwrite existing files** without showing what changes. Prefer adding missing sections to an existing CONTRIBUTING.md over replacing it.
- **LICENSE cannot be an account-wide default.** In `--account-defaults` mode, skip it and say why.

## Example

Input:

> Add a contributing guide and a security policy to this repo.

Detected: CI runs `uv sync`, `uv run pytest -q`, and `uv run ruff check .`. 46 of the last 50 commit subjects match Conventional Commits. The default branch is `main`. Private vulnerability reporting is disabled.

Output (excerpt of `.github/CONTRIBUTING.md`):

````markdown
## Run the tests

```bash
uv sync
uv run pytest -q
uv run ruff check .
```

CI runs the same commands on every pull request.

## Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `type(scope): summary`, for example `fix(parser): handle empty input`. Release notes are generated from these messages.
````

Command awaiting approval: `gh api -X PUT repos/acme-labs/tinyqueue/private-vulnerability-reporting`

The complete files are in [references/examples.md](references/examples.md).

## Reference files

- [references/file-guide.md](references/file-guide.md): which files a project needs, the per-file rules, the license guide, the code of conduct procedure, commit convention detection, labels, and account-wide defaults
- [references/examples.md](references/examples.md): a complete CONTRIBUTING.md and SECURITY.md, and an account-defaults run
- `templates/`: CONTRIBUTING.md, SECURITY.md, SUPPORT.md, pull_request_template.md, CODEOWNERS, FUNDING.yml, CITATION.cff, and ISSUE_TEMPLATE/{bug_report.yml, feature_request.yml, config.yml}

## Related skills

- `github-release-writer`: owns the commit convention decision when a project has none, and the release process CONTRIBUTING.md links to
- `github-readme-writer`: the README's Contributing and Security sections link to these files
- `github-repo-family`: account-wide defaults for many repositories at once
