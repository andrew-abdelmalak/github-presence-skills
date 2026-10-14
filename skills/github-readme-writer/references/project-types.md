# Project types

Detect the type first. It decides which sections the README needs and what "quick start" means.

## Contents

- [Detection signals](#detection-signals)
- [Sections per type](#sections-per-type)
- [Install commands per ecosystem](#install-commands-per-ecosystem)

## Detection signals

| Type | Signals |
|---|---|
| **Library / package** | Package manifest with no executable entry point. Code under `src/` or the package directory. Imports in examples. |
| **CLI tool** | `bin` in `package.json`, `[project.scripts]` in `pyproject.toml`, `[[bin]]` or `src/main.rs` in `Cargo.toml`, `cmd/<name>/main.go`, an argument parser in the entry file |
| **Web app / service** | Web framework dependency (Next.js, Django, Rails, Express, FastAPI, Spring), `Dockerfile` or `docker-compose.yml`, `.env.example`, routes or pages directories |
| **Desktop / mobile app** | Electron, Tauri, Flutter, React Native, Xcode, or Android Gradle project files |
| **Framework plugin / extension** | Manifest naming a host (VS Code `engines.vscode`, `.claude-plugin/plugin.json`, a browser extension `manifest.json`, `gh-` CLI extension) |
| **Template / starter** | `isTemplate: true` from `gh repo view`, or a "use this template" intent. Placeholder names in config. |
| **Dataset** | Data files (`.csv`, `.parquet`, `.jsonl`) form most of the repository. Data dictionary or schema files. |
| **Research code** | Paper references, `CITATION.cff`, notebooks, experiment configs, `results/` |
| **Collection / list** | Mostly Markdown, one large list, "awesome" naming |
| **Configuration / dotfiles** | Shell, editor, or system config files. An install script that creates symlinks. |

A repository can match two types (for example, a library that also ships a CLI). Use the primary type's section set, and add the secondary type's install and usage subsections.

## Sections per type

Section numbers refer to [section-guide.md](section-guide.md#section-reference). **R** = required, **O** = optional, **-** = omit.

| Section | Library | CLI | Web app | Desktop / mobile | Plugin | Template | Dataset | Research | Collection | Dotfiles |
|---|---|---|---|---|---|---|---|---|---|---|
| 1-3 Title, description, badges | R | R | R | R | R | R | R | R | R | R |
| 4 Visual | O | R | R | R | O | O | O | O | - | O |
| 5 Introduction | R | R | R | R | R | R | R | R | R | O |
| 6 Features | O | O | R | R | O | R | - | - | - | O |
| 7 Requirements | R | R | R | R | R | R | O | R | - | R |
| 8 Install | R | R | O (deploy instead) | R (download links) | R | "Use this template" steps | Download or load steps | R | - | R |
| 9 Quick start | R | R | R (run locally) | O | R | R (first customization) | R (load and inspect) | R (reproduce one result) | - | O |
| 10 Usage | R | R | O | O | R | O | Data dictionary | R | Contribution format | O |
| 11 Configuration | O | O | R (env vars) | O | O | R (what to rename) | - | O | - | O |
| 12 Documentation | O | O | O | O | O | - | R (schema) | R (paper link) | - | - |
| 13 Troubleshooting | O | O | O | O | O | - | - | O | - | O |
| 15 Contributing | R | R | R | R | R | O | O | O | R | - |
| 17 License | R | R | R | R | R | R | R (data license) | R | R | R |
| Citation block | - | - | - | - | - | - | R | R | - | - |

Type-specific notes:

- **Web app:** document required environment variables in a table, and point to `.env.example`. Never write real values. Give a one-command local run (`docker compose up`, `npm run dev`) when one exists.
- **Template:** the quick start is "click Use this template, then rename X, Y, Z". Include the list of placeholders the user must change.
- **Dataset:** state the source, collection date, license (often different from the code license), size, and a column-level data dictionary. Mention personal data handling if any personal data is present.
- **Research code:** link to the paper, show how to reproduce one headline result, and include a BibTeX block that matches `CITATION.cff`.
- **Collection:** the README is the product. Add a short contribution rule (format, inclusion criteria) near the top. A Contents list is justified here.
- **Plugin:** state the host and its minimum version, and give the host's own install command.

## Install commands per ecosystem

Use only the commands that apply, with the real package name from the manifest. A library and a CLI install differently in several ecosystems.

| Ecosystem | Library | CLI tool | Verify published with (read-only) |
|---|---|---|---|
| npm | `npm install NAME` | `npm install --global NAME`, or `npx NAME` for one-off runs | `npm view NAME version` |
| Python | `pip install NAME` | `pipx install NAME` or `uv tool install NAME` | `pip index versions NAME` |
| Rust | `cargo add NAME` | `cargo install NAME` | `cargo search NAME --limit 1` |
| Go | `go get MODULE` | `go install MODULE/cmd/NAME@latest` | `go list -m MODULE@latest` |
| Ruby | `bundle add NAME` | `gem install NAME` | `gem search -e NAME --remote` |
| PHP | `composer require VENDOR/NAME` | `composer global require VENDOR/NAME` | `composer show VENDOR/NAME --available` |
| .NET | `dotnet add package NAME` | `dotnet tool install --global NAME` | `dotnet package search NAME` |
| Java (Maven / Gradle) | Dependency snippet with group, artifact, and version | Download from Releases | Search Maven Central |
| From source | `git clone` + the build command from the manifest | Same | Always valid if the build works |
| Homebrew | - | `brew install NAME` (only if a formula or tap exists) | `brew info NAME` |
| Container | - | `docker run IMAGE` (only if an image is published) | Check the registry page |

If verifying needs network access you do not have, use the from-source install and a `TODO` for the registry command.
