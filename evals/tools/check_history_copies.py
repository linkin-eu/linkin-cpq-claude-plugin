"""Checks that each recorded history still holds what the plugin now holds.

- A skill's text in a history, after its "Base directory for this skill" line, must be that
  skill's SKILL.md as it stands.
- A tool's answer in a history must equal the case's own mock or the shared one; the check cannot
  tell which answered the recording, since a case's own mock may answer only what follows its
  history. Where either is a mock that answers from a fixture by input, it is not compared.

A history whose copies differ was recorded against older files: update its copies, or record it
again.

Usage, from the plugin's root: python3 evals/tools/check_history_copies.py
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
EVALS = ROOT / "evals"
SKILL_HEADER = "Base directory for this skill: "


def body(path):
    """A skill's or a mock's text after its front matter."""
    text = path.read_text()
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    return text.strip()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def main():
    skills = {p.parent.name: body(p) for p in (ROOT / "skills").glob("*/SKILL.md")}
    faults = []
    for history in sorted(EVALS.glob("*/history.jsonl")):
        case = history.parent
        uses = {}
        for number, line in enumerate(history.read_text().splitlines(), 1):
            message = json.loads(line)["message"]
            for text in strings(message):
                if not text.startswith(SKILL_HEADER):
                    continue
                head, _, copy = text.partition("\n")
                name = head.rsplit("/", 1)[-1]
                if name not in skills:
                    faults.append(f"{history}:{number}: {name} is no skill of the plugin")
                elif copy.strip() != skills[name]:
                    faults.append(f"{history}:{number}: {name}'s text differs from its SKILL.md")
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if part.get("type") == "tool_use":
                    uses[part["id"]] = part["name"].split("__")[-1]
                if part.get("type") != "tool_result":
                    continue
                tool = uses.get(part["tool_use_id"], "")
                answer = part["content"]
                if not isinstance(answer, str):
                    answer = "".join(p.get("text", "") for p in answer if isinstance(p, dict))
                mocks = [body(m) for m in (case / "mocks/linkin-cpq" / f"{tool}.md",
                                           EVALS / "mocks/linkin-cpq" / f"{tool}.md") if m.exists()]
                if not mocks or any("{{" in m for m in mocks):
                    continue
                if answer.strip() not in mocks:
                    faults.append(f"{history}:{number}: {tool}'s answer is neither mock's")
    for fault in faults:
        print(fault, file=sys.stderr)
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
