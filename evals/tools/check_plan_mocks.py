"""Checks the eval mocks' `plan_load` answers:

- **consistency**, always:
  - each line's packing is smallest carrier first;
  - each crate's net weight is its contents' total, and every line or item is in some crate;
  - a crate is as long as its longest bars' cut length, at least, and holds them longest first;
  - its packs' `positions`, laid out run by run, lie within the carrier's inside, none overlapping,
    as many as its contents' packs, and `standing` is the top of the highest;
  - its `smaller` names exactly the carriers below its own, each height over that carrier's inside;
  - each stack is one width, a shorter crate only on a longer one, with no gaps, under `stackHeight`;
  - the gross weight is the crates' net weight plus their empty weight;
- **shape**, given the server's OpenAPI document (`--openapi <path>`): every key the `LoadPlan`
  schema requires, no key it lacks, and the types.

Usage, from the plugin's root: python3 evals/tools/check_plan_mocks.py [--openapi <path>] [mock...]
With no mocks named, it checks every plan answer under evals/. It exits non-zero on a fault.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from plan_summary import read_mock  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]


def resolve(schemas, schema):
    while "$ref" in schema:
        schema = schemas[schema["$ref"].split("/")[-1]]
    if "allOf" in schema and len(schema["allOf"]) == 1:
        return resolve(schemas, schema["allOf"][0])
    return schema


def check_shape(schemas, value, schema, path, faults):
    schema = resolve(schemas, schema)
    alternatives = schema.get("oneOf") or schema.get("anyOf")
    if alternatives:
        alternatives = [a for a in alternatives if resolve(schemas, a).get("type") != "null"]
        if value is None:
            return
        if len(alternatives) == 1:
            return check_shape(schemas, value, alternatives[0], path, faults)
    kind = schema.get("type")
    if isinstance(kind, list):
        kind = [k for k in kind if k != "null"][0] if value is not None else "null"
    if kind == "object" or "properties" in schema:
        if not isinstance(value, dict):
            faults.append(f"{path}: not an object")
            return
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                faults.append(f"{path}: missing {key}")
        for key, item in value.items():
            if key not in properties:
                faults.append(f"{path}: unknown {key}")
            else:
                check_shape(schemas, item, properties[key], f"{path}.{key}", faults)
    elif kind == "array":
        if not isinstance(value, list):
            faults.append(f"{path}: not an array")
            return
        for i, item in enumerate(value):
            check_shape(schemas, item, schema["items"], f"{path}[{i}]", faults)
    elif kind == "string" and not isinstance(value, str):
        faults.append(f"{path}: not a string")
    elif kind == "integer" and not (isinstance(value, int) and not isinstance(value, bool)):
        faults.append(f"{path}: not an integer")
    elif kind == "number" and not (isinstance(value, (int, float)) and not isinstance(value, bool)):
        faults.append(f"{path}: not a number")
    elif kind == "boolean" and not isinstance(value, bool):
        faults.append(f"{path}: not a boolean")


def check_consistency(plan, faults, notes):
    carriers = {c["carrier"]: c for c in plan["carriers"]}
    order = [c["carrier"] for c in plan["carriers"]]
    lines = {(None, line["item"]): line for line in plan["lines"]}
    for document in plan["documents"]:
        for item in document["items"]:
            lines[(document["number"], item["item"])] = item
    for key, line in lines.items():
        packing = [p["carrier"] for p in line["packing"]]
        if packing != [c for c in order if c in packing]:
            faults.append(f"{key}: packing not smallest first")
    pieces = {key: 0 for key in lines}
    for truck in plan["trucks"]:
        stacks = {}
        for crate in truck["crates"]:
            stacks.setdefault((crate["x"], crate["y"]), []).append(crate)
        for where, stack in stacks.items():
            stack.sort(key=lambda c: c["z"])
            if len({c["width"] for c in stack}) > 1:
                faults.append(f"stack {where}: widths differ")
            if any(a["length"] < b["length"] for a, b in zip(stack, stack[1:])):
                faults.append(f"stack {where}: a longer crate on a shorter one")
            if any(a["z"] + a["height"] != b["z"] for a, b in zip(stack, stack[1:])):
                faults.append(f"stack {where}: a gap or overlap")
            if stack[-1]["z"] + stack[-1]["height"] > truck["inside"]["stackHeight"]:
                faults.append(f"stack {where}: over the stack height")
        for crate in truck["crates"]:
            if abs(sum(x["netWeight"] for x in crate["contents"]) - crate["netWeight"]) > 0.01:
                faults.append("crate net weight != contents")
            cuts = [lines[(x.get("document"), x["item"])].get("cutLength") for x in crate["contents"]
                    if (x.get("document"), x["item"]) in lines]
            if cuts and None not in cuts:
                if crate["length"] < max(cuts):
                    faults.append(f"crate length {crate['length']} under its longest bars' {max(cuts)}")
                if cuts != sorted(cuts, reverse=True):
                    faults.append(f"crate holds cut lengths {cuts}, not longest first")
            for content in crate["contents"]:
                key = (content.get("document"), content["item"])
                if key not in lines:
                    faults.append(f"contents names {key}, not a line")
                else:
                    pieces[key] += content["pieces"]
            below = order[:order.index(crate["carrier"])] if "positions" in crate else []
            smaller = [x["carrier"] for x in crate.get("smaller", [])]
            if smaller != below:
                faults.append(f"smaller {smaller} != carriers below {crate['carrier']} {below}")
            for x in crate.get("smaller", []):
                if x.get("height") is not None and not x["height"] > carriers[x["carrier"]]["insideHeight"]:
                    faults.append(f"smaller {x} not over the inside height {carriers[x['carrier']]['insideHeight']}")
            if "positions" in crate:
                placement(crate, carriers[crate["carrier"]], faults, notes)
            elif "standing" in crate or any(k in c for c in crate["contents"] for k in ("packs", "width", "height")):
                faults.append("a crate that is its pack carries standing, packs or a pack face")
    for key, count in pieces.items():
        if count == 0:
            faults.append(f"{key}: in no crate")
    crates = [c for t in plan["trucks"] for c in t["crates"]]
    gross = sum(c["netWeight"] + carriers[c["carrier"]]["emptyWeight"] for c in crates)
    if abs(gross - plan["totals"]["grossWeight"]) > 0.01:
        faults.append(f"gross {plan['totals']['grossWeight']} != the crates' {gross}")


EPS = 1e-6


def placement(crate, own, faults, notes):
    """A crate's packs laid out as its `positions` say: each run's packs left to right from its
    first pack, each touching the last, and where the next would pass the inside's right wall, back
    to the left wall one row up, the row as high as the pack lies (its width where turned). Its
    faults and notes are added to those given."""
    packs, laid = [0] * len(crate["contents"]), []
    for run in crate["positions"]:
        if run["count"] < 1:
            faults.append(f"a run of {run['count']} packs")
        if not 0 <= run["content"] < len(crate["contents"]):
            faults.append(f"a run's content {run['content']} is not in its contents")
            continue
        content = crate["contents"][run["content"]]
        if "width" not in content or "height" not in content:
            faults.append(f"content {run['content']} has packs in positions but no face")
            continue
        across, up = (content["height"], content["width"]) if run["turned"] else (content["width"], content["height"])
        x, y = run["x"], run["y"]
        for at in range(run["count"]):
            if at and x + across > own["insideWidth"] + EPS:  # the first pack lies where the run says
                x, y = 0, y + up
            laid.append((x, y, x + across, y + up))
            x += across
        packs[run["content"]] += run["count"]
    for at, (x0, y0, x1, y1) in enumerate(laid):
        if x0 < -EPS or y0 < -EPS or x1 > own["insideWidth"] + EPS or y1 > own["insideHeight"] + EPS:
            faults.append(f"pack {at} at ({round(x0, 2)}, {round(y0, 2)}) lies outside the inside")
        for (a0, b0, a1, b1) in laid[:at]:
            if x0 < a1 - EPS and a0 < x1 - EPS and y0 < b1 - EPS and b0 < y1 - EPS:
                faults.append(f"pack {at} at ({round(x0, 2)}, {round(y0, 2)}) overlaps another")
                break
    top = max((y1 for _, _, _, y1 in laid), default=0)
    if abs(top - crate.get("standing", -1)) > 0.01:
        faults.append(f"standing {crate.get('standing')} != the top of the highest pack {round(top, 2)}")
    for at, content in enumerate(crate["contents"]):
        if packs[at] != content.get("packs"):
            faults.append(f"content {at}: positions' packs {packs[at]} != contents' packs {content.get('packs')}")
    for x in crate.get("smaller", []):
        if x.get("height") is not None and abs(x["height"] - top) > 0.01:
            notes.append(f"smaller {x} != its own standing {round(top, 2)}")


def plan_mocks():
    for path in sorted((ROOT / "evals").rglob("plan_load*")):
        text = path.read_text(encoding="utf-8")
        if '"trucks"' in text:
            yield path


def main(argv):
    schemas = None
    if argv[:1] == ["--openapi"]:
        schemas = json.load(open(argv[1], encoding="utf-8"))["components"]["schemas"]
        argv = argv[2:]
    paths = [pathlib.Path(p) for p in argv] or list(plan_mocks())
    bad = 0
    for path in paths:
        _, plan, _, _ = read_mock(path)
        faults, notes = [], []
        if schemas:
            check_shape(schemas, plan, schemas["LoadPlan"], "$", faults)
        if not faults:
            check_consistency(plan, faults, notes)
        shown = path.resolve().relative_to(ROOT) if path.resolve().is_relative_to(ROOT) else path
        print(("ok  " if not faults else "BAD ") + str(shown))
        for fault in faults:
            print("    ", fault)
        for note in notes:
            print("     note:", note)
        bad += bool(faults)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
