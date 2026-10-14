---
name: github-release-writer
description: "Drafts GitHub release notes and CHANGELOG.md entries from commits, merged pull requests, and tags, recommends the next semantic version with evidence, writes migration notes for breaking changes, and sets up .github/release.yml and a commit convention. Publishes with gh release create only after approval. Make sure to use this skill whenever the user mentions release notes, a changelog, the next version number, semantic versioning, tagging, or cutting or publishing a release. Not for writing individual commit messages."
argument-hint: "[path] [notes | changelog | setup | publish] [version]"
---

# Release writer

Turn a range of history into release notes people can act on: what changed for them, what breaks, and how to upgrade. Recommend a version number with evidence, and set the project up so the next release is easier.

## When to use

- "Write release notes", "update the CHANGELOG", "what changed since v1.2?", "what should the next version be?"
- "Cut a release" or "publish v2.0.0" (publishing requires approval)
- "Set up automatic release notes" or "should we use Conventional Commits?"
- A `github-repo-audit` result lists area D fixes, such as tags without releases

## Input

- **Path** to the local repository (default: the current directory), with tags fetched.
- **Mode**: `notes` (default), `changelog`, `setup`, or `publish`. Modes combine: "cut a release" means notes, changelog, then publish.
- **Version** (optional): the target tag. If absent, the skill recommends one.
- **Range** (optional): defaults to the last release tag through `HEAD`.

## Output

- **Version recommendation:** the proposed version, the rule that decided it, and the commits that triggered it.
- **Release notes** in the [template](templates/release-notes.md) shape.
- **CHANGELOG.md entry** in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format, written to the file in `changelog` mode.
- **In `setup` mode:** a `.github/release.yml` and the commit convention decision.
- **Commands awaiting approval** for tagging and publishing.

## Workflow

```
Release progress:
- [ ] 1. Find the range
- [ ] 2. Collect changes
- [ ] 3. Classify each change
- [ ] 4. Detect breaking changes
- [ ] 5. Recommend the version
- [ ] 6. Draft notes and changelog entry
- [ ] 7. Publish (after approval) or hand off
```

**1. Find the range.**

```bash
git fetch --tags --quiet
git tag --sort=-v:refname | head -10
gh release list --limit 10
```

The previous release is the newest tag that has a published release. If tags exist without releases, say so: the audit calls this D1. Offer to backfill notes for the newest tag.

**2. Collect changes.**

```bash
git log PREV_TAG..HEAD --no-merges --format='%h%x09%s%x09%an'
gh pr list --state merged --base DEFAULT_BRANCH --search "merged:>=PREV_TAG_DATE" \
  --json number,title,labels,author,body --limit 200
```

Optionally, ask GitHub for its generated draft as a cross-check. It needs write access and saves nothing:

```bash
gh api -X POST repos/OWNER/REPO/releases/generate-notes -f tag_name=NEW_TAG -f previous_tag_name=PREV_TAG --jq .body
```

**3. Classify each change** into Added, Changed, Deprecated, Removed, Fixed, or Security, using the mapping in [references/changelog-format.md](references/changelog-format.md#mapping-changes-to-categories). Sources in order: Conventional Commit type, then PR labels, then reading the PR body or diff. Mark low-confidence items for the user to check. Leave internal-only changes (CI, refactors, test-only) out of the user-facing notes, but count them.

**4. Detect breaking changes** with the signals in [references/semver.md](references/semver.md#breaking-change-signals). Every breaking change gets a migration note: what to change, before and after. If you cannot tell whether something breaks users, ask. Do not guess.

**5. Recommend the version** with the decision table in [references/semver.md](references/semver.md#choosing-the-next-version). Show the rule and the evidence: "MINOR: 2 features (#41, #44), no breaking changes".

**6. Draft** the notes from [templates/release-notes.md](templates/release-notes.md), and the changelog entry. Credit contributors by `@handle` from PR authors, and name first-time contributors. In `changelog` mode, insert the entry under `## [Unreleased]` or as a new version section. Update the compare links at the bottom. If no CHANGELOG.md exists, start one from [templates/CHANGELOG.md](templates/CHANGELOG.md).

**7. Publish or hand off.** In `publish` mode, show the commands and wait for an explicit yes:

```bash
gh release create vX.Y.Z --target DEFAULT_BRANCH --title "vX.Y.Z" --notes-file RELEASE_NOTES.md --draft
```

Recommend `--draft` first, so the user can review the release on GitHub and publish it there. Use `--verify-tag` instead of `--target` when the tag already exists. Use `--prerelease` for versions with a pre-release suffix.

**Setup mode.** Write `.github/release.yml` from [templates/release.yml](templates/release.yml), mapping its categories to labels that exist (`gh label list`). Decide the commit convention with the user using [references/changelog-format.md](references/changelog-format.md#automation-options). Name the tools, but do not install them.

## Hard rules

Shared rules: [operating-rules.md](../../references/operating-rules.md). Additional rules for this skill:

- **Never move, delete, or re-point an existing tag,** and never publish without explicit approval of the exact command.
- **Breaking claims need evidence.** Do not call a release "non-breaking" or "fully backwards compatible" unless the evidence supports it. Say what was checked.
- **Security fixes:** if a fix relates to an unpublished security advisory, do not describe the vulnerability in the notes. Ask the user to link the advisory once it is published.
- **Write for users, not for the commit log.** "Jobs no longer retry after `max_attempts`" beats "fix: off-by-one in retry loop". Keep commit hashes out of the notes body. PR links are enough.
- **No hype** in notes ("massive release!", "huge improvements"). The changes speak for themselves.

## Example

Input:

> Write release notes for the next tinyqueue release.

Facts: last release `v0.4.0`. Since then:
- `feat(worker): add per-job timeout (#41)`
- `fix(sqlite): close connections on shutdown (#43)`
- `feat!: rename Queue.put to Queue.enqueue (#45)`
- 3 `ci`/`chore` commits

Output (abridged):

````markdown
**Recommended version: v0.5.0.** One breaking change (#45). The project is below 1.0, so by the 0.x convention a breaking change bumps MINOR. At 1.0 or later, it would be v1.0.0.

## Breaking changes
- `Queue.put()` is renamed to `Queue.enqueue()` (#45). Update calls:
  ```python
  queue.put(job)      # before
  queue.enqueue(job)  # after
  ```

## New
- Per-job timeouts: `queue.enqueue(job, timeout=30)` stops a job after 30 seconds (#41, @dana-k).

## Fixed
- SQLite connections are now closed on shutdown, so the database file is no longer left locked (#43).
````

The complete example, with the changelog entry and publish commands, is in [references/examples.md](references/examples.md).

## Reference files

- [references/changelog-format.md](references/changelog-format.md): Keep a Changelog structure, the category mapping, entry style, and automation options
- [references/semver.md](references/semver.md): version rules, what counts as public API per project type, breaking-change signals, and the decision table
- [references/examples.md](references/examples.md): a full release, and a setup-mode run
- [templates/](templates/): `CHANGELOG.md`, `release.yml`, `release-notes.md`

## Related skills

- `github-community-files`: CONTRIBUTING.md documents the commit convention chosen here
- `github-readme-writer`: the release badge starts working after the first published release
- `github-repo-audit`: checks D1 to D4 afterwards
