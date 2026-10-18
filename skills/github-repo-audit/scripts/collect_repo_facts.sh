#!/usr/bin/env bash
# Collect read-only facts about one GitHub repository and print them as a
# single JSON object on stdout. Every call is a GET; nothing is changed.
#
# Usage:   collect_repo_facts.sh OWNER/REPO
# Exit:    0 success (individual fields may be null)
#          2 bad usage
#          3 gh CLI missing or not signed in
#          4 repository not found or not visible
#
# A null field means that call failed: not found, no permission (branch
# rules need admin on some repos), or rate limited. Treat null as Unknown.
set -uo pipefail

repo="${1:-}"
if [[ ! "$repo" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  echo "usage: $(basename "$0") OWNER/REPO" >&2
  exit 2
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found; audit local files only" >&2
  exit 3
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not signed in; the user can run 'gh auth login', or audit local files only" >&2
  exit 3
fi

gh repo view "$repo" --json name >/dev/null 2>&1 || { echo "repository not found or not visible to this gh account: $repo" >&2; exit 4; }

# Print the output of a gh command if it succeeded and is non-empty, else null.
fetch() {
  local out
  if out=$("$@" 2>/dev/null) && [[ -n "$out" ]]; then
    printf '%s' "$out"
  else
    printf 'null'
  fi
}

fields="name,nameWithOwner,description,homepageUrl,repositoryTopics,licenseInfo"
fields+=",latestRelease,usesCustomOpenGraphImage,isFork,isArchived,isTemplate"
fields+=",visibility,defaultBranchRef,hasIssuesEnabled,hasDiscussionsEnabled"
fields+=",hasWikiEnabled,isSecurityPolicyEnabled,codeOfConduct,fundingLinks"
fields+=",issueTemplates,pullRequestTemplates,stargazerCount,forkCount,pushedAt"
fields+=",primaryLanguage"

branch=$(gh repo view "$repo" --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null)
gfi_query="repo:${repo} label:\"good first issue\" state:open is:issue"

printf '{'
printf '"repo":%s,' "$(fetch gh repo view "$repo" --json "$fields")"
printf '"community":%s,' "$(fetch gh api "repos/${repo}/community/profile" \
  --jq '{health_percentage, files: (.files | with_entries(.value |= (. != null)))}')"
printf '"private_vulnerability_reporting":%s,' "$(fetch gh api "repos/${repo}/private-vulnerability-reporting")"
printf '"releases":%s,' "$(fetch gh api "repos/${repo}/releases?per_page=10" \
  --jq '[.[] | {tag_name, name, draft, prerelease, published_at, body_chars: (.body // "" | length)}]')"
printf '"tags":%s,' "$(fetch gh api "repos/${repo}/tags?per_page=20" --jq '[.[].name]')"
printf '"workflows":%s,' "$(fetch gh api "repos/${repo}/actions/workflows" \
  --jq '[.workflows[] | {name, path, state}]')"
printf '"root_files":%s,' "$(fetch gh api "repos/${repo}/contents/" --jq '[.[] | {name, type, size}]')"
printf '"github_dir":%s,' "$(fetch gh api "repos/${repo}/contents/.github" --jq '[.[] | {name, type}]')"
printf '"issue_template_dir":%s,' "$(fetch gh api "repos/${repo}/contents/.github/ISSUE_TEMPLATE" --jq '[.[] | .name]')"
printf '"labels":%s,' "$(fetch gh api "repos/${repo}/labels?per_page=100" --jq '[.[].name]')"
printf '"good_first_issues_open":%s,' "$(fetch gh api -X GET search/issues -f q="$gfi_query" --jq '.total_count')"
if [[ -n "$branch" ]]; then
  printf '"branch_rules":%s' "$(fetch gh api "repos/${repo}/rules/branches/${branch}" --jq '[.[].type]')"
else
  printf '"branch_rules":null'
fi
printf '}\n'
