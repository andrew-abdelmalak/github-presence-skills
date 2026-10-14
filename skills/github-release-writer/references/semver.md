# Versioning

## Contents

- [Semantic Versioning in brief](#semantic-versioning-in-brief)
- [What counts as the public API](#what-counts-as-the-public-api)
- [Breaking-change signals](#breaking-change-signals)
- [Choosing the next version](#choosing-the-next-version)
- [Other schemes](#other-schemes)

## Semantic Versioning in brief

From [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html):

- A version is `MAJOR.MINOR.PATCH`.
- Increment **MAJOR** for incompatible changes to the public API, **MINOR** for backward-compatible new functionality, and **PATCH** for backward-compatible bug fixes.
- Version `0.y.z` is initial development: anything may change at any time, and the public API is not considered stable.
- Pre-release versions add a hyphen suffix: `1.0.0-rc.1`, `2.3.0-beta.2`.
- Once released, a version's contents must not change. Release a new version instead.

Git tags conventionally add a `v` prefix (`v1.4.0`). Follow the repository's existing tag style.

## What counts as the public API

A change breaks users if it breaks what they depend on, and that differs by project type:

| Project type | Public API includes |
|---|---|
| Library | Exported functions, classes, types, and their signatures; default behavior; supported runtime versions; raised errors that callers catch |
| CLI | Command and flag names, positional arguments, exit codes, output format that scripts parse, config file format, environment variables |
| Web service / API | Endpoints, request and response schemas, authentication, status codes, rate limits |
| App | Data and file formats, configuration, user-visible workflows, supported platforms |
| GitHub Action / plugin | Inputs, outputs, required permissions, host version support |

## Breaking-change signals

Treat each of these as a possible breaking change, and confirm by reading the diff:

- A `!` after the commit type, or a `BREAKING CHANGE:` footer
- A PR label such as `breaking-change` or `breaking`
- Removed or renamed exports, commands, flags, endpoints, or config keys
- Changed defaults
- Changed parameter order or types
- A raised minimum runtime, OS, or peer dependency version
- Changed output formats, or exit codes that scripts parse
- Database or file format migrations without backward reading support

## Choosing the next version

Start from the latest released version, and use the first matching row:

| Changes since last release | Version is 1.0.0 or later | Version is 0.y.z |
|---|---|---|
| Any breaking change | MAJOR (`2.0.0`) | MINOR (`0.5.0`) by common convention |
| New backward-compatible functionality | MINOR (`1.5.0`) | PATCH or MINOR. Follow the project's history, defaulting to PATCH. |
| Only fixes | PATCH (`1.4.1`) | PATCH |
| Only internal changes (CI, refactors, docs) | No release needed. If releasing anyway, PATCH. | Same |

Notes:
- The 0.x convention (breaking changes bump MINOR) is widespread, and package managers such as Cargo treat it that way, but it is not part of the SemVer spec. Say so when you recommend it.
- Recommend `1.0.0` when the user says the API is stable or the project is used in production. Do not push it on them.
- For a release candidate, propose `X.Y.Z-rc.1`, and publish it with `--prerelease`.

## Other schemes

- **CalVer** (`2026.10.0`, `26.10`): suits apps and services released on a schedule. Keep it if the project already uses it.
- **No versions** (rolling main branch): fine for sites and personal tools. The audit marks area D as N/A.
- Do not switch a project's scheme without the user asking.
