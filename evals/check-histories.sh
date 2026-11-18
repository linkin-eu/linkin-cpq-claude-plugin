#!/bin/sh
# Fails if a recorded history's line doesn't point at the line before it (parentUuid). An eval that
# resumes a broken chain drops every message above the break, the skill's text among them, and
# still scores the reply. Then fails if a history's copy of a skill or of a mock's answer is not
# the file as it stands (tools/check_history_copies.py), and if the skills' paragraph on a refusal
# of the account's details is missing from one or differs between them, since each skill carries
# it whole.
set -eu
status=0
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
