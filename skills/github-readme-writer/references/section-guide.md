# README section guide

What each section is for, in the default order. Include a section only when the project has real content for it. [project-types.md](project-types.md) says which sections each project type needs.

## Contents

- [Section reference](#section-reference)
- [Tables that earn their place](#tables-that-earn-their-place)
- [Visuals](#visuals)
- [Length](#length)
- [When to move docs to a site](#when-to-move-docs-to-a-site)

## Section reference

| # | Section | Purpose | Rules |
|---|---|---|---|
| 1 | **Title (H1)** | Name the project | Use the project name exactly as users type or import it. A logo is fine above or beside it, if it stays small. |
| 2 | **One-line description** | Say what it is and what it does, in one sentence | 10 to 25 words. It should match the repository's About description (see `github-discoverability`). Lead with the noun: "A CLI that...", "A Python library for...". |
| 3 | **Badges** | Status at a glance | One row, six at most, all real. Follow [badges.md](shared/badges.md). |
| 4 | **Visual** (optional) | Show, don't tell | A screenshot, terminal recording, or diagram, for projects with a UI, CLI output, or architecture worth seeing. Needs alt text. |
| 5 | **Introduction** | The problem, who it is for, and what makes it different | 2 to 4 sentences. Name the alternative and the difference ("Unlike `grep`, it understands timestamps"). No history of the project. |
| 6 | **Features** (optional) | Scannable capabilities | 3 to 7 bullets, each a concrete capability. Use a comparison table only when comparing with named alternatives, and only with verifiable claims. |
| 7 | **Requirements** | What must exist first | Runtime and minimum version, OS limits, required services, accounts, or API keys |
| 8 | **Install** | Get it onto the machine | One code block per channel, the most common first. Verify that the package is published before listing a registry command. |
| 9 | **Quick start** | A first success in under five minutes | The shortest complete path to a visible result, at most about 10 lines of code. Include expected output only if it is real. |
| 10 | **Usage** | The common tasks | Task-oriented subsections ("Filter by request ID"), each with a command or code block |
| 11 | **Configuration** | Every option a user can set | A table with option, default, and description. Move it to docs when it exceeds about 15 rows. |
| 12 | **Documentation** | Where the rest lives | Link to `docs/` or the docs site, API reference, and examples directory |
| 13 | **Troubleshooting / FAQ** | Fix known problems fast | A table with symptom, cause, and fix. Use only problems from issues, docs, or code (error messages), never imagined ones. |
| 14 | **Project status / Roadmap** (optional) | Set expectations | "Experimental", "Maintained", or "Looking for a maintainer". Link to a roadmap issue or project board instead of pasting a list. Label features honestly (see [Honest status labels](#honest-status-labels)). |
| 15 | **Contributing** | Point to the process | 1 to 3 sentences linking to `CONTRIBUTING.md`. Mention `good first issue` if the label is used. |
| 15a | **Maintainers** (optional) | Say who decides and who to contact | GitHub handles of current maintainers. Useful once there are several, or when ownership changed. |
| 16 | **Security** (optional) | Point to the policy | One sentence linking to `SECURITY.md`. Never "open an issue" for vulnerabilities. |
| 17 | **License** | Legal terms in one line | `Released under the [MIT License](LICENSE).` It must match the LICENSE file. |
| 18 | **Credits / Acknowledgments** (optional) | Thank people and projects | Contributors, upstream projects, funders. Link each one. To credit non-code work (design, docs, triage) systematically, suggest the [all-contributors](https://allcontributors.org) convention. |
| 19 | **Related projects** (optional) | Cross-link sibling repositories | Maintained by `github-repo-family` between marker comments. Do not edit inside the markers by hand. |

## Honest status labels

When a README lists features or architecture, mark anything that is not fully working. Readers forgive "planned"; they don't forgive discovering it themselves.

| Label | Meaning |
|---|---|
| (no label) | Implemented and usable now |
| **Experimental** | Present, but unstable or incomplete |
| **Planned** | Not implemented yet. Link the tracking issue. |
| **Demo data** | Shown with mock or generated data, not real behavior |

If you could not find evidence that a feature works, ask before listing it.

## Tables that earn their place

A table belongs in a README when readers scan it for one row. Good uses:

- **Feature table:** capability, status, and notes. Best when features differ by platform or plan.
- **Configuration table:** option, type, default, and description.
- **Troubleshooting table:** symptom, likely cause, and fix.
- **Compatibility table:** project version against runtime or OS versions.

A two-row table is a sentence. A table with one meaningful column is a list.

## Visuals

- **Screenshots:** crop to the relevant part, keep under about 1 MB, and store in `docs/images/` or `.github/assets/`.
- **Terminal demos:** a GIF or SVG recording works. Describe what it shows in a sentence nearby, for screen readers and for readers who skip images.
- **Light and dark themes:** use a `<picture>` element with `prefers-color-scheme` sources when a diagram is unreadable on one theme.
- **Diagrams:** GitHub renders Mermaid code blocks, which stay editable and diffable. An architecture diagram should show 3 to 6 real components found in the code, label the direction of data flow, and draw planned parts dashed and labeled "planned". Never add boxes (a cache, a queue, an AI service) the repository does not contain.

## Length

- Keep a README to what a newcomer needs to evaluate, install, and start. GitHub truncates content beyond 500 KiB (see [github-facts.md](shared/github-facts.md#readme-rendering)), but a README stops being readable long before that.
- As a heuristic, consider a docs site once the README passes about 400 lines, or holds full API or configuration references.

## When to move docs to a site

Recommend a documentation site when **any** of these is true:

- Full reference material (API, CLI flags, configuration) would push the README past about 400 lines.
- Users need documentation for more than one version at a time.
- There are several separate guides (tutorials, deployment, migration) that users navigate between.
- The project needs searchable documentation.

Otherwise, a README plus a `docs/` folder of Markdown files is enough. GitHub renders those files with relative links.

When a site is warranted, recommend a generator that matches the project's ecosystem. Do not scaffold it unless asked:

| Ecosystem | Default choice | Notes |
|---|---|---|
| Python | Material for MkDocs or Zensical | Zensical is the newer generator from the Material for MkDocs team |
| JavaScript / TypeScript, React | Docusaurus | Built-in versioned docs |
| Vue / Vite | VitePress | |
| Any ecosystem, accessibility focus | Starlight (Astro) | |
| No build step wanted | Jekyll | Built into GitHub Pages |

Publishing guidance to include with the recommendation:

- Deploy with a GitHub Actions workflow that uses `actions/upload-pages-artifact` and `actions/deploy-pages`. A custom Actions workflow is also exempt from the soft limit of 10 builds per hour (see [github-facts.md](shared/github-facts.md#github-pages)).
- After the first deploy, set the repository's website field to the site URL. `github-discoverability` does this.
- If the site uses a custom domain, verify the domain in the account settings so nobody can take it over if the site is later removed.
- Pages is for project documentation and personal sites, not for running a commercial service.
