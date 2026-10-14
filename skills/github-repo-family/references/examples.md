# Repository family example

Fictional organization `acme-labs`.

## Input

> Link my tinyqueue repos together and make them consistent. Owner acme-labs, everything starting with tinyqueue.

## Step 1: select and confirm

```bash
gh repo list acme-labs --source --no-archived --limit 200 \
  --json name,description,repositoryTopics,licenseInfo,isPrivate --jq '.[] | select(.name | startswith("tinyqueue"))'
```

Found 5. `tinyqueue-internal-bench` is private, so it is excluded from public links.

> Family (4 public): tinyqueue, tinyqueue-redis, tinyqueue-dashboard, tinyqueue-examples. `tinyqueue-internal-bench` is private and will not be linked. Confirm?

User: "Yes."

## Steps 2 and 3: consistency matrix

| Repository | Description | Topic `tinyqueue` | License | Badge row | Related block | CONTRIBUTING | SECURITY |
|---|---|---|---|---|---|---|---|
| tinyqueue | "Dependency-free job queue for Python scripts, backed by SQLite" ✓ | ✗ | MIT | tests, license ✓ | ✗ | own `.github/` | own `.github/` |
| tinyqueue-redis | "redis thing" ✗ | ✗ | MIT | none ✗ | ✗ | none | none |
| tinyqueue-dashboard | "Web dashboard for tinyqueue workers" ✓ | ✗ | Apache-2.0 ⚠ | 9 badges ✗ | ✗ | none | none |
| tinyqueue-examples | (empty) ✗ | ✗ | none ✗ | none | ✗ | none | none |

Family topic check: `topic:tinyqueue` is used by 0 repositories outside `acme-labs`, so it is safe to claim.

## Step 4: family spec

````markdown
| Convention | Spec |
|---|---|
| Names | Keep: all follow `tinyqueue` plus `tinyqueue-PART` |
| Descriptions | "[What it is] for tinyqueue". Proposed: tinyqueue-redis "Redis storage backend for tinyqueue", tinyqueue-examples "Runnable examples for tinyqueue: retries, timeouts, and scheduled jobs" |
| Topics | Add `tinyqueue` to all four. Keep each repository's own topics. |
| Badge row | tests, then release, then license (dashboard: trim from 9 to these 3) |
| Related projects | The block below, in all four READMEs |
| Community files | Move tinyqueue's CONTRIBUTING, SECURITY, and code of conduct to `acme-labs/.github` as account-wide defaults (via `github-community-files --account-defaults`). tinyqueue keeps its own CONTRIBUTING, because its test commands are specific. |
| License | ⚠ tinyqueue-dashboard is Apache-2.0 while the others are MIT, and tinyqueue-examples has none. Decide: is the difference on purpose? For the examples, MIT matches the rest. |
````

## Step 5: README block (copy for tinyqueue-redis)

```markdown
<!-- related-projects:start -->
## Related projects

tinyqueue is a family of 4 projects for running background jobs from Python scripts:

| Project | What it is |
|---|---|
| [tinyqueue](https://github.com/acme-labs/tinyqueue) | Dependency-free job queue for Python scripts, backed by SQLite |
| **tinyqueue-redis** (this repository) | Redis storage backend for tinyqueue |
| [tinyqueue-dashboard](https://github.com/acme-labs/tinyqueue-dashboard) | Web dashboard for tinyqueue workers |
| [tinyqueue-examples](https://github.com/acme-labs/tinyqueue-examples) | Runnable examples for tinyqueue: retries, timeouts, and scheduled jobs |

See all of them under the [`tinyqueue`](https://github.com/topics/tinyqueue) topic.
<!-- related-projects:end -->
```

No README has markers yet, so each block goes just before the License section. tinyqueue-examples has no License section, so its block goes at the end.

## Step 6: commands awaiting approval

````markdown
**Metadata (one approval)**
```bash
gh repo edit acme-labs/tinyqueue --add-topic tinyqueue
gh repo edit acme-labs/tinyqueue-redis --description "Redis storage backend for tinyqueue" --add-topic tinyqueue
gh repo edit acme-labs/tinyqueue-dashboard --add-topic tinyqueue
gh repo edit acme-labs/tinyqueue-examples --description "Runnable examples for tinyqueue: retries, timeouts, and scheduled jobs" --add-topic tinyqueue
```

**README pull requests (one per repository, same steps; shown for tinyqueue-redis)**
```bash
gh repo clone acme-labs/tinyqueue-redis /tmp/family/tinyqueue-redis -- --depth 1
git -C /tmp/family/tinyqueue-redis switch -c docs/related-projects
# insert the block into README.md
git -C /tmp/family/tinyqueue-redis commit -am "docs: add related projects section"
git -C /tmp/family/tinyqueue-redis push -u origin docs/related-projects
gh pr create --repo acme-labs/tinyqueue-redis --head docs/related-projects \
  --title "docs: add related projects section" \
  --body "Adds the shared related-projects block for the tinyqueue family."
```

**Waiting on your decision:** the license for tinyqueue-examples, and whether the Apache-2.0 license on tinyqueue-dashboard is intentional.

**Next step:** run `github-community-files --account-defaults` for the shared CONTRIBUTING, SECURITY, and code of conduct.
````

## Step 7: verify

After the pull requests merge, re-running steps 2 and 3 shows ✓ in the description, topic, badge row, and related-block columns for all four repositories. The license column still shows the open decision until the user makes it.
