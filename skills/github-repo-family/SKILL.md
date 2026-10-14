---
name: github-repo-family
description: "Makes a set of related repositories read as one family: a consistency matrix across descriptions, topics, licenses, badges, and README sections, a shared family topic, a Related projects block kept in sync between marker comments in every README, and account-wide default community files. Changes go through pull requests or approved commands. Make sure to use this skill whenever the user wants several repositories cross-linked, made consistent, standardized, or given shared files, or mentions a related projects section. Not for a single repository (use github-repo-audit)."
---

# Repository family

Treat several related repositories (a core library and its plugins, a set of tools from one team, a project and its docs and examples) as a family. A visitor who lands on any one of them should find the others and see the same standards everywhere.

## When to use

- "Cross-link my repositories", "add a related projects section to all of them"
- "Make my repos consistent", "standardize descriptions and topics across our org"
- "Same CONTRIBUTING and code of conduct for all repos"
- The same `github-repo-audit` fixes repeat across many repositories

## Input

- **Owner:** a user or organization.
- **Family selector:** a topic (`--topic tinyqueue`), a name prefix (`tinyqueue-`), or an explicit list. Ask if it is not given. Never assume every repository of the owner is one family.
- **Family name and tagline** (optional): otherwise proposed from the main repository.

## Output

1. **Consistency matrix:** one row per repository, with one column per convention, showing what differs.
2. **Family spec:** the conventions to apply (naming, description pattern, shared topic, badge row, README blocks, community files).
3. **Per-repository change list,** and the files or patches.
4. **Commands awaiting approval:** metadata edits and pull requests, grouped.

## Workflow

```
Family progress:
- [ ] 1. Select the family
- [ ] 2. Inventory each repository
- [ ] 3. Build the consistency matrix
- [ ] 4. Propose the family spec
- [ ] 5. Generate per-repository changes
- [ ] 6. Apply after approval
- [ ] 7. Verify
```

**1. Select the family.**

```bash
gh repo list OWNER --source --no-archived --limit 200 --topic TOPIC \
  --json name,description,repositoryTopics,licenseInfo,defaultBranchRef,url,isPrivate,pushedAt
```

Or list without `--topic` and filter by name prefix. Show the selected list and confirm it before doing anything else.

**2. Inventory each repository.** For each one: description, topics, license key, the first about 40 lines of the README (`gh api -H "Accept: application/vnd.github.raw+json" repos/OWNER/REPO/readme | head -40`), the badges present, whether the `related-projects` markers exist, and which community files it has or inherits from `OWNER/.github`.

**3. Build the consistency matrix.** Columns: description pattern, family topic, license, badge row, README sections (install, usage, contributing, license), related block, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT. Mark each cell ✓, ✗, or the differing value.

**4. Propose the family spec.** Each convention follows the reference skill that owns it:

| Convention | Rule | Owned by |
|---|---|---|
| Names | One pattern, such as `CORE` plus `CORE-PLUGIN` (`tinyqueue`, `tinyqueue-redis`). Rename only with the user's agreement and the rename warnings. | `github-discoverability` |
| Descriptions | A shared shape: `[What this one is] for/in [family]`. Each description still stands alone. | `github-discoverability` |
| Topics | Every member gets one shared family topic, plus its own topics. Check that the family topic is not already used by unrelated repositories: `gh api -X GET search/repositories -f q="topic:NAME" --jq .total_count`. | `github-discoverability` |
| Badge row | Same order and style in every README | [badges.md](../../references/badges.md) |
| Related projects | The same block in every README, between markers, with the current repository marked | [templates/related-projects.md](templates/related-projects.md) |
| Community files | Shared files in `OWNER/.github` (account-wide defaults). Per-repository files only where commands differ. | `github-community-files` |
| License | Usually the same across the family. Flag differences; do not change a license without the user deciding. | `github-community-files` |

**5. Generate per-repository changes.**
- **Related block:** fill the template. If the markers `<!-- related-projects:start -->` and `<!-- related-projects:end -->` exist, replace only what is between them. Otherwise insert the block just before the License section, or at the end. Running the skill again updates the block in place and never duplicates it.
- **Metadata:** one `gh repo edit` per repository (description, `--add-topic` for the family topic).
- **Community defaults:** hand off to `github-community-files --account-defaults`, and list the per-repository files that will keep overriding the defaults. A member with any file in its own `.github/ISSUE_TEMPLATE/` ignores all default issue templates, so list those members separately.
- **Protections:** organizations on GitHub Team or Enterprise can target many repositories with one organization ruleset. Hand that to `github-repo-hardening` instead of repeating per-repository rulesets.

**6. Apply after approval.**
- **Local clones the user names:** edit the files directly.
- **Repositories only on GitHub:** prefer one pull request per repository. Show the commands, and run them after an explicit yes:

  ```bash
  gh repo clone OWNER/REPO /tmp/family/REPO -- --depth 1
  git -C /tmp/family/REPO switch -c docs/related-projects
  # edit README.md
  git -C /tmp/family/REPO commit -am "docs: add related projects section"
  git -C /tmp/family/REPO push -u origin docs/related-projects
  gh pr create --repo OWNER/REPO --head docs/related-projects --title "docs: add related projects section" --body "Adds the shared related-projects block for the FAMILY family."
  ```

- **Metadata:** batch every `gh repo edit` command in one block for a single approval.

**7. Verify.** Re-run step 2 and show the matrix again. Every cell should now be ✓, or carry a reason it differs on purpose.

## Hard rules

Shared rules: [operating-rules.md](../../references/operating-rules.md). Additional rules for this skill:

- **Confirm the family list** before any change. A wrong selector multiplies every mistake.
- **Edit only inside the markers** in READMEs. Content outside them belongs to each repository.
- **Pull requests over direct pushes** for repositories with other maintainers or branch protection. Never push to a default branch the user did not explicitly approve.
- **Private members:** do not link a private repository from a public README. Leave it out of the public block, and say so.

## Example

Input:

> Link my tinyqueue repos together and make them consistent. Owner acme-labs, everything starting with tinyqueue.

Output (abridged):

```markdown
**Family (4):** tinyqueue, tinyqueue-redis, tinyqueue-dashboard, tinyqueue-examples. Confirm?

| Repository | Description pattern | Topic `tinyqueue` | License | Related block | CONTRIBUTING |
|---|---|---|---|---|---|
| tinyqueue | ✓ | ✗ | MIT | ✗ | own |
| tinyqueue-redis | ✗ "redis thing" | ✗ | MIT | ✗ | none |
| tinyqueue-dashboard | ✓ | ✗ | Apache-2.0 | ✗ | none |
| tinyqueue-examples | ✗ (empty) | ✗ | none | ✗ | none |
```

The complete example, with the spec, the README block, and the commands, is in [references/examples.md](references/examples.md).

## Reference files

- [templates/related-projects.md](templates/related-projects.md): the marker block to insert or update
- [references/examples.md](references/examples.md): a complete family run

## Related skills

- `github-discoverability`: names, descriptions, and topics for each member
- `github-community-files`: account-wide defaults in `OWNER/.github`
- `github-readme-writer`: members whose README needs more than the shared block
- `github-repo-audit`: check each member afterwards
