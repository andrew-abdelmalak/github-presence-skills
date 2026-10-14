#!/usr/bin/env bash
# Collect a repository's security posture as one JSON object. Read-only: every
# call is a GET. Many settings need admin rights; a null field means the call
# failed or was not permitted, and must be reported as Unknown.
#
# Usage:   collect_posture.sh OWNER/REPO
# Exit:    0 success, 2 bad usage, 3 gh CLI missing or not signed in
set -uo pipefail

repo="${1:-}"
if [[ ! "$repo" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  echo "usage: $(basename "$0") OWNER/REPO" >&2
  exit 2
fi
command -v gh >/dev/null 2>&1 || { echo "gh CLI not found" >&2; exit 3; }
gh auth status >/dev/null 2>&1 || { echo "gh is not signed in" >&2; exit 3; }

fetch() {
  local out
  if out=$("$@" 2>/dev/null) && [[ -n "$out" ]]; then printf '%s' "$out"; else printf 'null'; fi
}

# 204 means enabled, 404 disabled. Non-admins also get 404, so without admin
# rights the answer is unknown.
status_204() {
  local code
  [[ "$admin" == "true" ]] || { printf 'null'; return; }
  code=$(gh api "repos/${repo}/$1" --silent -i 2>/dev/null | head -1 | awk '{print $2}')
  case "$code" in
    204) printf 'true' ;;
    404) printf 'false' ;;
    *) printf 'null' ;;
  esac
}

info=$(fetch gh api "repos/${repo}" --jq '{private, archived, fork, default_branch, permissions: .permissions.admin, security_and_analysis}')
branch=$(gh api "repos/${repo}" --jq .default_branch 2>/dev/null)
admin=$(gh api "repos/${repo}" --jq .permissions.admin 2>/dev/null)

# Workflow files: flag unpinned actions, missing top-level permissions, pull_request_target.
workflows='[]'
names=$(gh api "repos/${repo}/contents/.github/workflows" --jq '.[] | select(.type=="file") | .name' 2>/dev/null)
if [[ -n "$names" ]]; then
  items=()
  while IFS= read -r name; do
    body=$(gh api -H "Accept: application/vnd.github.raw+json" "repos/${repo}/contents/.github/workflows/${name}" 2>/dev/null) || continue
    unpinned=$(printf '%s\n' "$body" | grep -E '^\s*-?\s*uses:\s*[^./][^@]*@' | grep -vcE '@[0-9a-f]{40}')
    top_perms=$(printf '%s\n' "$body" | grep -qE '^permissions:' && echo true || echo false)
    prt=$(printf '%s\n' "$body" | grep -q 'pull_request_target' && echo true || echo false)
    items+=("{\"file\":\"${name}\",\"unpinned_uses\":${unpinned:-0},\"top_level_permissions\":${top_perms},\"pull_request_target\":${prt}}")
  done <<< "$names"
  workflows="[$(IFS=,; echo "${items[*]}")]"
fi

printf '{'
printf '"repo":%s,' "$info"
printf '"rulesets":%s,' "$(fetch gh api "repos/${repo}/rulesets" --jq '[.[] | {name, target, enforcement}]')"
if [[ -n "$branch" ]]; then
  printf '"rules_on_default_branch":%s,' "$(fetch gh api "repos/${repo}/rules/branches/${branch}" --jq '[.[].type] | unique')"
  printf '"classic_protection":%s,' "$(fetch gh api "repos/${repo}/branches/${branch}/protection" --jq '{enforce_admins: .enforce_admins.enabled, reviews: (.required_pull_request_reviews != null), checks: (.required_status_checks != null)}')"
else
  printf '"rules_on_default_branch":null,"classic_protection":null,'
fi
printf '"dependabot_alerts":%s,' "$(status_204 vulnerability-alerts)"
printf '"dependabot_security_updates":%s,' "$(fetch gh api "repos/${repo}/automated-security-fixes" --jq .enabled)"
printf '"dependabot_config":%s,' "$(fetch gh api "repos/${repo}/contents/.github/dependabot.yml" --jq '.name != null')"
printf '"private_vulnerability_reporting":%s,' "$(fetch gh api "repos/${repo}/private-vulnerability-reporting" --jq .enabled)"
printf '"codeql_default_setup":%s,' "$(fetch gh api "repos/${repo}/code-scanning/default-setup" --jq '.state | @json')"
printf '"workflows":%s,' "$workflows"
printf '"scorecard":%s' "$(fetch curl -sf --max-time 20 "https://api.scorecard.dev/projects/github.com/${repo}")"
printf '}\n'
