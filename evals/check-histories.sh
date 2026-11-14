#!/bin/sh
# Fails if a recorded history's line doesn't point at the line before it (parentUuid). An eval that
# resumes a broken chain drops every message above the break, the skill's text among them, and
# still scores the reply.
set -eu
status=0
for f in "$(dirname "$0")"/*/history.jsonl; do
  jq -e -s '[foreach .[] as $m ({prev: null}; {prev: $m.uuid, ok: ($m.parentUuid == .prev)}; .ok)] | all' "$f" >/dev/null ||
    { echo "$f: a line's parentUuid is not the line before it" >&2; status=1; }
done
exit $status
