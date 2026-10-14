# Release writer examples

Fictional repository `acme-labs/tinyqueue`.

## Contents

- [Example 1: cut a release](#example-1-cut-a-release)
- [Example 2: setup mode](#example-2-setup-mode)

## Example 1: cut a release

**Input**

> Cut the next tinyqueue release.

**Range**

```text
$ git tag --sort=-v:refname | head -3
v0.4.0
v0.3.0
v0.2.0
$ gh release list --limit 3
v0.4.0  Latest  v0.4.0  2026-08-30
```

**Changes since `v0.4.0`** (`git log v0.4.0..HEAD --no-merges`, PR data from `gh pr list`)

| Commit subject | PR | Author | Labels |
|---|---|---|---|
| `feat(worker): add per-job timeout` | #41 | @dana-k (first contribution) | enhancement |
| `fix(sqlite): close connections on shutdown` | #43 | @mtorres | bug |
| `feat!: rename Queue.put to Queue.enqueue` | #45 | @mtorres | breaking-change |
| `docs: add retry example` | #46 | @mtorres | documentation |
| `ci: test on Python 3.13` | #44 | @mtorres | |
| `chore(deps): bump pytest to 8.4` | #47 | dependabot | dependencies |

**Classification**
- Added: #41
- Fixed: #43
- Changed (breaking): #45. The diff confirms `Queue.put` is removed, not aliased.
- Omitted from the user-facing notes: #44, #47 (internal), #46 (docs, not behavior)

**Output**

````markdown
**Recommended version: v0.5.0**
Rule: one breaking change (#45). The project is below 1.0, so by the common 0.x convention a breaking change bumps MINOR. This convention is not part of the SemVer spec. If you consider the API stable, release v1.0.0 instead.

---

### RELEASE_NOTES.md

This release adds per-job timeouts and fixes a locked-database problem on shutdown. It renames `Queue.put()`, so update your calls before upgrading.

## Breaking changes

- `Queue.put()` is renamed to `Queue.enqueue()` (#45). Update every call:
  ```python
  queue.put(job)      # before
  queue.enqueue(job)  # after
  ```

## New

- Per-job timeouts: `queue.enqueue(job, timeout=30)` stops a job that runs longer than 30 seconds and marks it failed (#41, @dana-k).

## Fixed

- SQLite connections are closed on shutdown, so the database file is no longer left locked for the next process (#43).

## Other changes

<details>
<summary>3 other changes (docs, CI, dependencies)</summary>

- Added a retry example to the docs (#46)
- CI now tests Python 3.13 (#44)
- Bumped pytest to 8.4 (#47)

</details>

## Upgrade

```bash
pip install --upgrade git+https://github.com/acme-labs/tinyqueue@v0.5.0
```

## Contributors

Thanks to @mtorres and @dana-k. Welcome to our first-time contributor @dana-k.

**Full changelog:** https://github.com/acme-labs/tinyqueue/compare/v0.4.0...v0.5.0

---

### CHANGELOG.md entry (inserted above 0.4.0)

## [0.5.0] - 2026-10-12

### Added

- Per-job timeouts with `queue.enqueue(job, timeout=...)` (#41, @dana-k)

### Changed

- **Breaking:** `Queue.put()` is renamed to `Queue.enqueue()` (#45)

### Fixed

- SQLite connections are closed on shutdown (#43)

[Unreleased]: https://github.com/acme-labs/tinyqueue/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/acme-labs/tinyqueue/compare/v0.4.0...v0.5.0

---

**Commands awaiting approval**
```bash
git add CHANGELOG.md
git commit -m "docs: changelog for v0.5.0"
git push origin main
gh release create v0.5.0 --target main --title "v0.5.0" --notes-file RELEASE_NOTES.md --draft
```
The release is created as a draft. Review it on GitHub, then click **Publish release**. Publishing creates the `v0.5.0` tag at the tip of `main`.
````

## Example 2: setup mode

**Input**

> Set up automatic release notes for this repo. We label PRs but our commit messages are all over the place.

**Facts**
- `gh label list` returns: `bug`, `documentation`, `enhancement`, `good first issue`, `help wanted`, `dependencies`, `question`. There is no `breaking-change` label.
- Of the last 50 commit subjects, 9 (18%) match Conventional Commits.

**Output**

````markdown
Your PRs are labeled, so GitHub's generated notes fit without changing how you commit. I wrote `.github/release.yml`:

```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
  categories:
    - title: Breaking changes
      labels:
        - breaking-change
    - title: New features
      labels:
        - enhancement
    - title: Bug fixes
      labels:
        - bug
    - title: Documentation
      labels:
        - documentation
    - title: Dependencies
      labels:
        - dependencies
    - title: Other changes
      labels:
        - "*"
```

From now on, `gh release create vX.Y.Z --generate-notes` groups merged PRs by these labels. Label breaking PRs with `breaking-change` so they appear first.

**Commit convention:** only 18% of recent commits follow Conventional Commits. Labels already give you grouped notes, so I would not change your commit style. Adopt Conventional Commits only if you want a commit-based CHANGELOG.md (git-cliff) or release PRs (release-please).

**Commands awaiting approval**
```bash
gh label create breaking-change --color B60205 --description "Changes that require users to update their code or config"
gh label create ignore-for-release --color EDEDED --description "Leave this PR out of release notes"
```
````
