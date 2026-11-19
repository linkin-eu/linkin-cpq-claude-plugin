#!/bin/sh
# Fails if a recorded history's line doesn't point at the line before it (parentUuid). An eval that
# resumes a broken chain drops every message above the break, the skill's text among them, and
# still scores the reply. Then fails if a history's copy of a skill or of a mock's answer is not
# the file as it stands (tools/check_history_copies.py), and if the skills' paragraph on a refusal
# of the account's details is missing from one or differs between them, since each skill carries
# it whole. Also fails if a skill's allowed-tools is not exactly the connector's nine read-only
# tools, by full name, which Claude Code then runs without asking: never a tool that issues,
# submits or revokes, and never a wildcard. The nine must also be exactly the tools the server's
# tool list (mocks/linkin-cpq/_tools.json) marks readOnlyHint, so a tool that comes to write, or a
# new read tool, fails here when the list is replaced. And if .claude-plugin/plugin.json holds a
# top-level key beyond the nine it has now: Claude Desktop's marketplace strips the directory
# listing fields (icon, supportUrl, privacyPolicyUrl and their kin) with a warning, though
# `claude plugin validate --strict` passes them. The marketplace entry's name must also be
# plugin.json's: it is the name customers install by, and the validator lets the two differ.
set -eu
status=0
prefix=mcp__plugin_linkin-cpq_linkin-cpq__
reads="${prefix}get_account ${prefix}find_profiles ${prefix}find_values ${prefix}price_quotation ${prefix}price_inquiry ${prefix}find_documents ${prefix}read_document ${prefix}plan_load ${prefix}describe_api"
reads_sorted=$(printf '%s\n' $reads | sort)
for f in "$(dirname "$0")"/../skills/*/SKILL.md; do
  listed=$(awk 'NR == 1 && $0 == "---" { fm = 1; next } fm && $0 == "---" { exit } fm && sub(/^allowed-tools:[ \t]*/, "") { print }' "$f")
  if [ "$(printf '%s\n' $listed | sort)" != "$reads_sorted" ]; then
    echo "$f: allowed-tools is not exactly the connector's nine read-only tools" >&2; status=1
  fi
done
marked=$(jq -r --arg p "$prefix" '.tools[] | select(.annotations.readOnlyHint == true) | $p + .name' "$(dirname "$0")/mocks/linkin-cpq/_tools.json" | sort)
if [ "$marked" != "$reads_sorted" ]; then
  echo "evals/mocks/linkin-cpq/_tools.json: the tools marked readOnlyHint are not the nine the skills pre-approve" >&2; status=1
fi
plugin=$(jq -r .name "$(dirname "$0")/../.claude-plugin/plugin.json")
entries=$(jq -r '.plugins[].name' "$(dirname "$0")/../.claude-plugin/marketplace.json")
if [ "$entries" != "$plugin" ]; then
  echo ".claude-plugin/marketplace.json: its entry's name is not plugin.json's, $plugin" >&2; status=1
fi
keys=$(jq -r 'keys_unsorted[] | select(. as $k | ["name", "displayName", "description", "version", "author", "homepage", "repository", "license", "keywords"] | index($k) | not)' "$(dirname "$0")/../.claude-plugin/plugin.json")
if [ -n "$keys" ]; then
  echo ".claude-plugin/plugin.json: keys beyond the nine it may hold: $(echo $keys)" >&2; status=1
fi
marker="**A refusal of the account's details.**"
first=""
for f in "$(dirname "$0")"/../skills/*/SKILL.md; do
  para=$(awk -v m="$marker" 'index($0, m) == 1 { p = 1 } p && $0 == "" { exit } p' "$f")
  if [ -z "$para" ]; then
    echo "$f: no paragraph on a refusal of the account's details" >&2; status=1
  elif [ -z "$first" ]; then
    first=$para
  elif [ "$para" != "$first" ]; then
    echo "$f: its paragraph on a refusal of the account's details differs from the others" >&2; status=1
  fi
done
for f in "$(dirname "$0")"/*/history.jsonl; do
  jq -e -s '[foreach .[] as $m ({prev: null}; {prev: $m.uuid, ok: ($m.parentUuid == .prev)}; .ok)] | all' "$f" >/dev/null ||
    { echo "$f: a line's parentUuid is not the line before it" >&2; status=1; }
done
python3 "$(dirname "$0")/tools/check_history_copies.py" || status=1
exit $status
