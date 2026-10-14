# Upstream contributor example

The repositories, issues, and user are fictional.

## Input

> I know Python, have about 3 hours a week, and want my first open source contribution. My GitHub is dmitri-v.

## Step 2: candidates

The search returned 30 `good first issue` results updated in the last 90 days. After filtering out archived repositories and long debates, three remained for vetting.

## Step 3: vetting

| Check | acme-labs/logslice #77 | acme-labs/tinyqueue #58 | example-org/parsely #210 |
|---|---|---|---|
| Recent merges | 6 in the last 2 months, 2 from outside contributors | 4 in the last month | Last merge 5 months ago |
| Maintainer response | Replied on #77 two days ago | Replies within a week | 3 unanswered PRs |
| License | Apache-2.0 | MIT | MIT |
| CONTRIBUTING | Yes. It asks for a comment before starting. | Yes | No |
| AI policy | "AI-assisted contributions are welcome; you must understand and test every change." | None found | None found |
| Assigned / linked PR | No / none | No / none | No / none |
| Clarity | Expected behavior stated by a maintainer | Clear | Clear, with a failing CSV attached |

````markdown
| # | Issue | Why it fits | Flags |
|---|---|---|---|
| 1 | acme-labs/logslice#77 "Support reading from stdin with -" | Python, a small CLI change, clear expected behavior, an active maintainer | None |
| 2 | acme-labs/tinyqueue#58 "Docs: example for scheduled jobs" | Docs plus a small example, a gentle way into the codebase | Lower impact |
| 3 | example-org/parsely#210 "Handle BOM in CSV header" | A real bug, with a reproduction attached | Slow reviews likely (last merge 5 months ago) |

**Recommended: #1.** The project's AI policy allows assisted work if you understand and test every change, so I'll explain each line as we go.
````

## Step 4: rules found in logslice's CONTRIBUTING

- Comment on the issue before starting.
- Branch from `main`. Conventional Commits.
- Run `pytest -q` and `ruff check .`.
- A PR template exists (`.github/pull_request_template.md`), with "Summary", "Fixes", and "Testing" sections.

## Step 5: plan and comment

**Plan**
1. In `logslice/cli.py`, when the path argument is `-`, read `sys.stdin` (text mode) instead of calling `open()`.
2. Add `tests/test_cli_stdin.py`, which pipes a three-line JSON log into `main()` and checks the filtered output.
3. Update the README usage example that already promises this behavior.

**Comment draft**

```markdown
Hi! I'd like to work on this. My plan: treat `-` as stdin in `cli.py` (reading text mode, so `--format auto` detection still sees the first lines), add a test that pipes a small JSON log in, and update the README example. I expect to open a PR within a week.
```

## Step 7: pull request description (filled into their template)

```markdown
## Summary

`logslice -` now reads the log from standard input, so compressed logs can be piped in (`zcat app.log.gz | logslice - --from ...`).

Fixes #77

## Testing

- `pytest -q`: 48 passed, including the new `tests/test_cli_stdin.py`
- `ruff check .`: clean
- Manual: `zcat sample.log.gz | logslice - --request-id 7f3c2a91` printed the 4 matching lines
```

## Step 8: commands awaiting approval

````markdown
```bash
gh issue comment 77 --repo acme-labs/logslice --body-file comment.md
gh repo fork acme-labs/logslice --remote --remote-name fork
git push -u fork feat/stdin-dash
gh pr create --repo acme-labs/logslice --head dmitri-v:feat/stdin-dash \
  --title "feat(cli): read from stdin when path is -" --body-file PR_BODY.md
```
Post the comment first, and wait for a maintainer's go-ahead before running the rest.
````

## A refusal, for contrast

**Input**

> Find 20 repos with typos in their READMEs and open PRs fixing them so my graph fills up.

**Output**

```markdown
I won't do that one. Mass typo PRs opened to collect contributions are what GitHub's policies call meaningless pull requests, and maintainers often close them, or flag the account. They also don't show employers anything.

What works instead: one real issue, like the candidates above, gets a merged PR that you can pin and talk about in interviews. Want me to find a few in your languages?
```
