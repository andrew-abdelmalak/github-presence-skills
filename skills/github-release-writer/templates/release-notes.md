<!--
Release notes template for github-release-writer. Delete empty sections and these comments.
The GitHub release title is the version tag. Do not repeat it as a heading here.
-->

{{ONE_OR_TWO_SENTENCE_SUMMARY_OF_WHAT_THIS_RELEASE_MEANS_FOR_USERS}}

## Breaking changes

- {{WHAT_CHANGED}} (#{{PR}}). {{HOW_TO_MIGRATE}}

## New

- {{FEATURE_AND_HOW_TO_USE_IT}} (#{{PR}}, @{{AUTHOR}})

## Fixed

- {{BUG_EFFECT_THAT_IS_NOW_GONE}} (#{{PR}})

## Other changes

<details>
<summary>{{N}} internal changes (CI, refactors, dependencies)</summary>

- {{INTERNAL_CHANGE}} (#{{PR}})

</details>

## Upgrade

```{{SHELL_LANGUAGE}}
{{UPGRADE_COMMAND}}
```

## Contributors

Thanks to {{@HANDLES}}. Welcome to our first-time contributors: {{@NEW_HANDLES}}.

**Full changelog:** https://github.com/{{OWNER}}/{{REPO}}/compare/{{PREVIOUS_TAG}}...{{NEW_TAG}}
