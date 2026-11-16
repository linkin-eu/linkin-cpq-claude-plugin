"""Checks the eval mocks' `plan_load` answers:

- **consistency**, always:
  - each line's packing is smallest carrier first;
  - each crate's net weight is its contents' total, and every line or item is in some crate;
  - its bands hold its packs, within the carrier's inside width and height;
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
            for content in crate["contents"]:
                key = (content.get("document"), content["item"])
                if key not in lines:
                    faults.append(f"contents names {key}, not a line")
                else:
                    pieces[key] += content["pieces"]
            below = order[:order.index(crate["carrier"])] if "bands" in crate else []
            smaller = [x["carrier"] for x in crate.get("smaller", [])]
            if smaller != below:
                faults.append(f"smaller {smaller} != carriers below {crate['carrier']} {below}")
            for x in crate.get("smaller", []):
                if x.get("height") is not None and not x["height"] > carriers[x["carrier"]]["insideHeight"]:
                    faults.append(f"smaller {x} not over the inside height {carriers[x['carrier']]['insideHeight']}")
            if "bands" in crate:
                own = carriers[crate["carrier"]]
                height = 0
                for band in crate["bands"]:
                    across, up = (band["height"], band["width"]) if band["turned"] else (band["width"], band["height"])
                    packs = sum(p["packs"] for p in band["packs"])
                    if band["across"] * across > own["insideWidth"] + 1e-9:
                        faults.append(f"band of {band['across']} across over the inside width")
                    if band["rows"] != -(-packs // band["across"]):
                        faults.append(f"band rows {band['rows']} != ceil({packs}/{band['across']})")
                    height += band["rows"] * up
                if height > own["insideHeight"] + 1e-9:
                    faults.append(f"bands {height} over the inside height {own['insideHeight']}")
                for x in crate.get("smaller", []):
                    if x.get("height") is not None and abs(x["height"] - height) > 0.01:
                        notes.append(f"smaller {x} != its own bands' {round(height, 2)}")
                for content in crate["contents"]:
                    key = (content.get("document"), content["item"])
                    packs = sum(p["packs"] for b in crate["bands"] for p in b["packs"] if (p.get("document"), p["item"]) == key)
                    if packs != content.get("packs"):
                        faults.append(f"bands' packs {packs} != contents' packs {content.get('packs')}")
    for key, count in pieces.items():
        if count == 0:
            faults.append(f"{key}: in no crate")
    crates = [c for t in plan["trucks"] for c in t["crates"]]
    gross = sum(c["netWeight"] + carriers[c["carrier"]]["emptyWeight"] for c in crates)
    if abs(gross - plan["totals"]["grossWeight"]) > 0.01:
        faults.append(f"gross {plan['totals']['grossWeight']} != the crates' {gross}")


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
        text = path.read_text(encoding="utf-8")
        plan = json.JSONDecoder().raw_decode(text, text.index("{"))[0]
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
