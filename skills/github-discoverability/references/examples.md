# Discoverability example

Fictional repository `acme-labs/logslice` (a Python CLI). The topic data is real: GitHub API lookups run on 2026-10-12. The numbers change over time, so a real run always looks them up again.

## Input

> Nobody finds my repo acme-labs/logslice. Fix the description and topics, and I'd like a social preview too.

## Step 1: current metadata

```json
{
  "name": "logslice",
  "description": "my log tool",
  "homepageUrl": "",
  "repositoryTopics": [],
  "usesCustomOpenGraphImage": false,
  "primaryLanguage": {"name": "Python"}
}
```

## Step 2: project terms

From the README and `pyproject.toml`: a CLI for slicing JSON and Common Log Format files by time window or request ID, streaming, Python 3.10 or later. Likely search words: "log", "logging", "cli", "time range", "request id", "json logs".

## Step 4: topic lookups

| Candidate | Curated | Repositories using it | Decision |
|---|---|---|---|
| `cli` | yes | 139,217 | Keep: project type |
| `python` | yes (featured) | 938,735 | Keep: language |
| `logging` | yes | 13,327 | Keep: the accepted spelling for the domain |
| `logs` | no | 2,808 | Drop: synonym of `logging`, less used |
| `log-analysis` | no topic page | 2,528 | Keep: the exact problem |
| `log-parser` | no | 317 | Drop: rarely used, and the tool does not parse into fields |
| `command-line-tool` | no | 9,748 | Keep: a common browse term alongside `cli` |
| `devops` | yes | 46,695 | Keep: audience |
| `sre` | yes | 4,857 | Keep: audience |
| `observability` | no | 17,613 | Keep: domain |
| `json` | yes | 52,179 | Keep: a supported format |
| `streaming` | no | 12,530 | Drop: mostly means media streaming, which would mislead |

## Output

````markdown
| Field | Current | Proposed |
|---|---|---|
| Description | "my log tool" | "CLI that cuts large log files to a time window or request ID without loading them into memory" |
| Topics | (none) | `cli`, `logging`, `log-analysis`, `python`, `command-line-tool`, `devops`, `sre`, `observability`, `json` (9 of 20) |
| Website | (none) | Leave empty for now. Set it to the PyPI page after the first publish. |
| Name | `logslice` | Keep: short, unique, matches the command name |

The description matches the README's first line (written by `github-readme-writer`).

**Social preview brief**
| Element | Content |
|---|---|
| Name | logslice |
| Tagline | "Cut huge logs to the minutes that matter" |
| Visual | A stack of horizontal lines with one highlighted band (the time window) |
| Colors | Background #0F172A, accent #38BDF8, text #F8FAFC |
| URL line | github.com/acme-labs/logslice |

I wrote a filled-in starter to `.github/social-preview.svg`. To export it as a PNG, use the first available tool:
```bash
rsvg-convert -w 1280 -h 640 .github/social-preview.svg -o social-preview.png
```
Upload `social-preview.png` yourself in **Settings → General → Social preview → Edit**. GitHub has no API for this step.

**Command awaiting approval**
```bash
gh repo edit acme-labs/logslice \
  --description "CLI that cuts large log files to a time window or request ID without loading them into memory" \
  --add-topic cli,logging,log-analysis,python,command-line-tool,devops,sre,observability,json
```
````

## After approval

The skill runs the command, then confirms the result:

```bash
gh repo view acme-labs/logslice --json description,repositoryTopics
```

It reports the new values, and reminds the user that the social preview upload is still theirs to do.
