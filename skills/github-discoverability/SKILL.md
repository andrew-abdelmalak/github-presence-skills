---
name: github-discoverability
description: "Improves how a repository is found and understood in GitHub search, topic pages, and link previews: the About description, up to 20 topics checked against GitHub's topic data, the website link, repository names and renames, and a 1280x640 social preview brief with an SVG starter. Applies changes with gh repo edit only after approval. Make sure to use this skill whenever the user mentions topics, the repository description or About section, discoverability, people not finding a repository, link previews or social preview images, or renaming a repository. Not for README content (use github-readme-writer)."
---

# Discoverability

Get a repository's short metadata right: the description, topics, website, name, and social preview. Search results, topic pages, and shared links show these fields before anyone opens the README.

## When to use

- "Add topics", "write a better description", "nobody finds my repo", "make my repo show up in search"
- "Make a social preview image", "my links look bad on social media"
- "Should I rename this repo?"
- A `github-repo-audit` result lists area A fixes

## Input

- **Target**: a local path or `owner/repo`. Applying changes requires `gh` with admin or maintain permission on the repository.
- **Audience and keywords** (optional): the words the target users would type into search.

## Output

1. **Current and proposed** metadata, side by side: description, topics, website, and the name if relevant.
2. **Topic evidence**: for each proposed topic, whether GitHub curates it and how many repositories use it.
3. **Social preview brief**, and an SVG starter written to `.github/social-preview.svg` if the user wants one.
4. **Commands awaiting approval**: one `gh repo edit` command.

## Workflow

```
Discoverability progress:
- [ ] 1. Read current metadata
- [ ] 2. Understand the project
- [ ] 3. Write the description
- [ ] 4. Choose topics with evidence
- [ ] 5. Website and name
- [ ] 6. Social preview
- [ ] 7. Present and apply after approval
```

**1. Read current metadata:**

```bash
gh repo view OWNER/REPO --json name,description,homepageUrl,repositoryTopics,usesCustomOpenGraphImage,openGraphImageUrl,primaryLanguage,isTemplate
```

**2. Understand the project** from the README's first section, the manifest (`keywords`, `classifiers`, `categories`), the primary language, and the main dependencies. Write down 5 to 10 words a user would search for.

**3. Write the description** with the formula in [references/topics-and-description.md](references/topics-and-description.md#description). Offer two variants at most. It should match the README's one-line description. If they differ, propose the same text for both.

**4. Choose topics.** Draft 10 to 20 candidates across the categories in [the topic guide](references/topics-and-description.md#topics). Check each one:

```bash
gh api "search/topics?q=CANDIDATE" --jq '.items[0:3][] | {name, curated, featured}'
gh api -X GET search/repositories -f q="topic:CANDIDATE" --jq .total_count
```

- Prefer an existing spelling that people already use (for example, `machine-learning`) over a new variant.
- Keep `curated` topics when they fit.
- Drop candidates with almost no use unless the term is genuinely the project's niche.
- Search is rate-limited, so check at most 20 candidates per run.

**5. Website and name.**
- **Website:** set it to the docs site, the package registry page, or a live demo, in that order. Never the repository's own URL. If a GitHub Pages site exists or `github-readme-writer` recommended one, use its URL once it is deployed.
- **Name:** suggest a rename only when the name is misleading or unsearchable, and the project is young. Always list the side effects in [github-facts.md](../../references/github-facts.md#repository-metadata): Pages project URLs change, and `uses:` references to actions break.

**6. Social preview.** Write the brief from [references/social-preview.md](references/social-preview.md). If the user wants a starter image, fill [templates/social-preview.svg](templates/social-preview.svg) with the real name, description, and colors. Write it to `.github/social-preview.svg`, and give the export command. Upload happens in the Settings UI, so say so.

**7. Present and apply.** Show the current and proposed table, then the single command:

```bash
gh repo edit OWNER/REPO --description "..." --homepage "..." --add-topic a,b,c --remove-topic x,y
```

Run it only after an explicit yes. Then confirm by re-running the `gh repo view` command from step 1.

## Hard rules

Shared rules: [operating-rules.md](../../references/operating-rules.md). Additional rules for this skill:

- **Topic format is strict:** at most 20 topics, each 50 characters or less, lowercase letters, numbers, and hyphens only. Validate before proposing.
- **No keyword stuffing.** The description is one sentence for humans. Topics describe the project; they are not a list of every technology it touches.
- **No misleading topics.** Do not add `awesome` unless the repository is an awesome list, or event topics such as `hacktoberfest` unless the project takes part.
- **No promises about ranking.** GitHub does not publish its search ranking. Say "helps people find it through topic pages and search", not "will rank higher".

## Example

Input:

> Nobody finds my repo acme-labs/logslice. Fix the description and topics.

Output (abridged):

````markdown
| Field | Current | Proposed |
|---|---|---|
| Description | "my log tool" | "CLI that cuts large log files to a time window or request ID without loading them into memory" |
| Topics | (none) | `cli`, `logging`, `log-analysis`, `python`, `command-line-tool`, `devops`, `observability`, `json`, `sre` |
| Website | (none) | (none: no docs site or PyPI page yet) |

Topic evidence: `cli`, `logging`, `python`, `devops`, `json`, and `sre` are curated. `logging` (13,327 repositories) beats the uncurated `logs` (2,808).

**Command awaiting approval**
```bash
gh repo edit acme-labs/logslice --description "CLI that cuts large log files to a time window or request ID without loading them into memory" --add-topic cli,logging,log-analysis,python,command-line-tool,devops,observability,json,sre
```
````

The full example, with real lookups and the social preview brief, is in [references/examples.md](references/examples.md).

## Reference files

- [references/topics-and-description.md](references/topics-and-description.md): the description formula, topic categories, and what to avoid
- [references/social-preview.md](references/social-preview.md): design brief, layout rules, export, and upload
- [references/examples.md](references/examples.md): a complete run
- [templates/social-preview.svg](templates/social-preview.svg): a 1280×640 starter to fill in

## Related skills

- `github-readme-writer`: the README's first line should match the description
- `github-repo-family`: a shared topic and description pattern across sibling repositories
- `github-repo-audit`: re-run it afterwards to confirm area A passes
