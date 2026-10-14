# Audit examples

Both examples use a fictional repository, `acme-labs/tinyqueue`: a small Python job-queue library. The facts shown are what the collector script and local scan would return for it.

## Contents

- [Example 1: standard audit](#example-1-standard-audit)
- [Example 2: pre-public audit](#example-2-pre-public-audit)

## Example 1: standard audit

**Input**

> Audit acme-labs/tinyqueue. It's a library, I want people to use it.

**Facts collected (abridged)**

```json
{
  "repo": {
    "description": "",
    "homepageUrl": "",
    "repositoryTopics": [],
    "licenseInfo": {"key": "mit", "name": "MIT License"},
    "usesCustomOpenGraphImage": false,
    "isSecurityPolicyEnabled": false,
    "issueTemplates": [],
    "pullRequestTemplates": []
  },
  "community": {"health_percentage": 57, "files": {"readme": true, "license": true, "contributing": true, "code_of_conduct": false, "issue_template": false, "pull_request_template": false}},
  "private_vulnerability_reporting": {"enabled": false},
  "releases": [],
  "tags": ["v0.4.0", "v0.3.0", "v0.2.0", "v0.1.0"],
  "workflows": [{"name": "tests", "path": ".github/workflows/tests.yml", "state": "active"}],
  "github_dir": [{"name": "workflows", "type": "dir"}],
  "branch_rules": null
}
```

Local scan: `README.md` (41 lines, no install section). `pyproject.toml` declares `name = "tinyqueue"` and `requires-python = ">=3.10"`. `CONTRIBUTING.md` exists. `tinyqueue.egg-info/` is tracked.

**Output**

```markdown
**tinyqueue audit:** 16 of 30 applicable checks pass. Critical: 4 open (A1, B3, B4, D1). (GitHub community health: 57%.)
Goal: library for other developers, so B3, B4, and D1 are raised to Critical.
Omitted from this table for brevity: C7 (Fix, Nice: no SUPPORT.md); C8, C10, D4 (N/A); E5, F1, F3, F4, F5 (Pass).

| Area | Check | Verdict | Evidence |
|---|---|---|---|
| Front door | A1 Description | Fix | `description` is empty |
| Front door | A2 Topics | Fix | 0 topics |
| Front door | A3 Website | N/A | No docs site or published package page found |
| Front door | A4 Social preview | Fix | `usesCustomOpenGraphImage: false` |
| Front door | A5 Name | Pass | `tinyqueue`: lowercase, searchable |
| README | B1 Exists | Pass | `README.md` at root |
| README | B2 What and who | Pass | Line 3: "A minimal, dependency-free job queue for Python scripts" |
| README | B3 Install steps | Fix (Critical) | No install section; `pyproject.toml` defines package `tinyqueue` |
| README | B4 Usage example | Fix (Critical) | No code block shows enqueueing or running a job |
| README | B5 Links resolve | Pass | 2 relative links, both resolve |
| README | B6 Badges | N/A | No badges |
| README | B7 License statement | Pass | "MIT", matches LICENSE |
| README | B8 Size | Pass | 41 lines |
| Community | C1 License | Pass | MIT detected |
| Community | C2 CONTRIBUTING | Pass | Setup, test command `pytest`, and PR steps present |
| Community | C3 Security policy | Fix | No SECURITY.md; private vulnerability reporting disabled |
| Community | C4 Code of conduct | Fix | Not found |
| Community | C5 Issue forms | Fix | No `.github/ISSUE_TEMPLATE/` |
| Community | C6 PR template | Fix | None |
| Community | C9 Citation | N/A | Not research software |
| Releases | D1 Published releases | Fix (Critical) | 4 tags, 0 releases |
| Releases | D2 Change notes | Fix | No CHANGELOG.md, no release bodies |
| Releases | D3 Version scheme | Pass | Tags follow SemVer |
| Trust | E1 CI | Pass | `tests.yml` active |
| Trust | E2 Dependency updates | Fix | No `dependabot.yml` or Renovate config |
| Trust | E3 Branch rules | Unknown | Rules endpoint returned no data (needs admin) |
| Trust | E4 No tracked secrets | Pass | No matches in tracked files |
| Layout | F2 Build output untracked | Fix | `tinyqueue.egg-info/` is tracked |

**Top fixes**
1. Critical: add install (`pip install tinyqueue`, once confirmed published) and a quick-start example. Run `github-readme-writer` in improve mode.
2. Critical: publish GitHub Releases for the existing tags, starting with `v0.4.0`. Run `github-release-writer`.
3. Critical: write a description and 8 to 12 topics. Run `github-discoverability`.
4. Important: add SECURITY.md, a code of conduct, and issue forms, and enable private vulnerability reporting. Run `github-community-files`.
5. Important: stop tracking `tinyqueue.egg-info/`: add it to `.gitignore`, then run `git rm -r --cached tinyqueue.egg-info`.
6. Nice: add `.github/dependabot.yml` for `pip` and `github-actions`.
7. Nice: design a social preview. `github-discoverability` writes the brief and an SVG you can export.

**Next step:** start with fix 1 by running `github-readme-writer`.
```

## Example 2: pre-public audit

**Input**

> /github-repo-audit . pre-public

**Situation**

A private repository with no remote yet, about to be published. The local scan finds:
- `config/dev.env` is tracked and contains a line matching `password=`.
- `git log -p --all -G 'AKIA[0-9A-Z]{16}'` finds one commit that added and later removed a matching string in `deploy/aws.sh`.
- Author emails in history: `jane@acme-internal.example` and `jane.doe@users.noreply.github.com`.
- `docs/setup.md` mentions `http://build01.corp.acme.example:8080`.
- No LICENSE.

**Output**

```markdown
**Before going public: 4 blocking findings.** Do not publish until each one is resolved.

| ID | Finding | Location | Action |
|---|---|---|---|
| G1 | Tracked file contains a credential assignment (`password=`) | `config/dev.env` line 3 | Rotate the credential. Delete the file, add `*.env` to `.gitignore`, and commit `config/dev.env.example` with placeholder values. |
| G2 | An AWS access key ID pattern exists in history | commit `4f2a9c1`, `deploy/aws.sh` | Deactivate the key in AWS first. Then either rewrite history with `git filter-repo`, or publish a fresh repository without the old history. Deleting the line in a new commit is not enough. |
| G4 | Internal hostname in documentation | `docs/setup.md` line 12 | Replace it with a placeholder such as `http://localhost:8080` |
| G5 | No license | repository root | Choose a license. Run `github-community-files` (LICENSE). |

**Also review (not blocking)**
- G3: history contains the work address `jane@acme-internal.example`. If you do not want it public, rewrite author emails before publishing. Use your `noreply` address for future commits.
- G6: decide whether Issues and Discussions should be on. The README currently says "open an issue".

After these are resolved, run the standard audit for the remaining presentation fixes.
```
