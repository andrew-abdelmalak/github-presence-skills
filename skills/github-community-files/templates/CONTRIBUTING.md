<!--
Template for github-community-files. Fill every {{PLACEHOLDER}} from detected facts.
Delete sections that do not apply and all instruction comments before writing.
-->

# Contributing to {{PROJECT_NAME}}

{{ONE_SENTENCE_ON_WELCOME_CONTRIBUTIONS}}
<!-- Example: "Bug reports, fixes, and documentation improvements are welcome. For new features, open an issue first so we can agree on the design." -->

## Before you start

- Search [existing issues](https://github.com/{{OWNER}}/{{REPO}}/issues) to avoid duplicates.
- For anything larger than a small fix, open an issue first and describe the change you plan.
- Issues labeled [`good first issue`](https://github.com/{{OWNER}}/{{REPO}}/labels/good%20first%20issue) are scoped for newcomers.
- By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Set up your environment

Requirements: {{RUNTIME_AND_TOOLS_WITH_VERSIONS}}

```bash
git clone https://github.com/{{OWNER}}/{{REPO}}.git
cd {{REPO}}
{{SETUP_COMMANDS}}
```

## Run the checks

```bash
{{TEST_COMMAND}}
{{LINT_COMMAND}}
```

CI runs the same checks on every pull request. A pull request with failing checks will not be merged.

## Make your change

1. Create a branch from `{{DEFAULT_BRANCH}}`: `git switch -c {{BRANCH_NAME_EXAMPLE}}`.
2. Keep the change focused on one problem. Unrelated cleanups belong in their own pull request.
3. Add or update tests for behavior changes.
4. Update the documentation when behavior or options change.

## Commit messages

{{COMMIT_CONVENTION_PARAGRAPH}}
<!-- From the commit convention rule in references/file-guide.md. -->

<!-- Include only if the project uses DCO:
Sign off every commit (`git commit -s`) to certify the [Developer Certificate of Origin](https://developercertificate.org/).
-->

## Open a pull request

1. Push your branch and open a pull request against `{{DEFAULT_BRANCH}}`.
2. Fill in the pull request template, and link the issue it resolves (`Fixes #123`).
3. {{REVIEW_EXPECTATION}}
<!-- Example: "A maintainer will review within a week. Expect questions; they are part of the process." Use only what the maintainer confirms. -->

<!-- Include only if the maintainer chose a policy:
## AI-assisted contributions

{{AI_POLICY}}
-->

## Report a bug or request a feature

Use the [issue forms](https://github.com/{{OWNER}}/{{REPO}}/issues/new/choose). For security problems, follow [SECURITY.md](SECURITY.md) instead. Never report vulnerabilities in a public issue.

## License

By contributing, you agree that your contributions are licensed under the project's [{{LICENSE_NAME}}](../LICENSE).
<!-- Fix the LICENSE link for where this file lives: "LICENSE" at the root, "../LICENSE" from .github/ or docs/. -->
