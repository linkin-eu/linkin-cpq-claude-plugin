"""Cuts an eval run's session transcript down to a recorded history, as the cases' `history.jsonl`
files are: the user and assistant messages only, assistant entries that hold only thinking left
out, each line chained to the one before it, under a fixed session id and the working folder
`/eval`. A skill's "Base directory for this skill" line is rewritten to `/plugin/skills/<name>`.

Record on the case whose session the history continues, keeping its temporary folder:

    claude plugin eval . --case <case> --runs 1 --ablation none --model opus --judge-model opus \\
      --max-cost-usd <n> -j 1 --keep-temp --no-publish

Run it from a checkout with no other copy of the plugin under it (CONTRIBUTING): the cut rewrites
the skill's path, so the history can't show which copy was loaded. The eval prints the folder it
kept; the transcript is the session's `.jsonl` file under its `config/projects/`.

Usage, from the plugin's root:
    python3 evals/tools/cut_history.py <transcript.jsonl> evals/<case>/history.jsonl [<n>]

<n> numbers the fixed session id in its last twelve digits, as in
00000000-0000-4000-8000-000000000001 for 1: keep the number the history has (default 1). Then run
evals/check-histories.sh.
"""
import json
import sys

ASSISTANT_KEYS = ("model", "type", "role", "content", "stop_reason", "stop_sequence", "diagnostics")
SKILL_BASE = "Base directory for this skill: "


def cut(lines, session_id):
    kept, prev = [], None
    for line in lines:
        entry = json.loads(line)
        if entry.get("type") not in ("user", "assistant"):
            continue
        msg = entry["message"]
        if entry["type"] == "assistant":
            if all(c.get("type") == "thinking" for c in msg["content"]):
                continue
            msg = {k: msg[k] for k in ASSISTANT_KEYS if k in msg}
        else:
            msg = {"role": msg["role"], "content": msg["content"]}
            if isinstance(msg["content"], list):
                for c in msg["content"]:
                    if c.get("type") == "text" and c["text"].startswith(SKILL_BASE):
                        head, body = c["text"].split("\n", 1)
                        c["text"] = SKILL_BASE + "/plugin/skills/" + head.rsplit("/", 1)[1] + "\n" + body
        kept.append({
            "type": entry["type"], "uuid": entry["uuid"], "parentUuid": prev, "isSidechain": False,
            "sessionId": session_id, "timestamp": entry["timestamp"], "cwd": "/eval",
            "version": entry["version"], "userType": entry["userType"], "message": msg,
        })
        prev = entry["uuid"]
    return kept


def main():
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) == 4 else 1
    with open(src, encoding="utf-8") as f:
        kept = cut(f, f"00000000-0000-4000-8000-{n:012d}")
    with open(out, "w", encoding="utf-8") as f:
        for entry in kept:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(len(kept), "lines")


if __name__ == "__main__":
    main()
