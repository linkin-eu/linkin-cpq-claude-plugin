"""The plain sentences and figures the server writes into a `plan_load` answer, worked out from the
answer's own trucks and crates, so the eval mocks read as the server's do:

- each truck's `fill.space`: its crates' length × height against its lanes, length and stack
  height, in percent to one decimal, rounded down;
- `totals.toSaveATruck`: where the plan takes more than one truck and the bound, the gross weight
  above one truck fewer's payloads, and the space above one truck fewer's;
- `summary`: `head`, `reason`, `smaller`, `fills`, a sentence per truck and `closing`.

Tonnes and metres to one decimal, kilograms under a tonne, a share in whole percent rounded down,
every "at least" rounded down, and a no-break space before each unit.
"""
import json
from decimal import Decimal, ROUND_HALF_UP

NB = "\u00a0"  # a no-break space, before each unit
CLOSING = "An estimate of how much fits in a standard truck, to size the order: not a loading plan."
TERMS = {"weight": "their weight", "space": "the space they take", "longCrates": "their long crates"}


def grouped(x, decimals):
    q = Decimal(str(x)).quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_UP)
    return f"{q:,.{decimals}f}"


def mass(kg):
    whole = Decimal(str(kg)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return f"{grouped(whole, 0)}{NB}kg" if whole < 1000 else f"{grouped(kg / 1000, 1)}{NB}t"


def mass_at_least(kg):
    whole = int(kg // 1)
    return f"{whole:,}{NB}kg" if whole < 1000 else f"{(whole // 100) / 10:,.1f}{NB}t"


def metres(mm):
    return f"{grouped(mm / 1000, 1)}{NB}m"


def space(truck, narrowest):
    """A truck's space taken: as many crates across as the plan's narrowest allows."""
    sides = sum(c["length"] * c["height"] for c in truck["crates"])
    inside = truck["inside"]
    across = inside["width"] // narrowest
    return (sides * 1000 // (across * inside["length"] * inside["stackHeight"])) / 10


def reason(totals):
    """Why so many trucks, from `boundBy` and `provenLeast`; none where the bound and plan are 1."""
    if totals["bound"] <= 1:
        return f"This plan takes {totals['trucks']} trucks; fewer may be possible." if totals["trucks"] > 1 else None
    terms = totals["boundBy"]
    # The server's own reading: a term it adds later reads as the space.
    words = [TERMS.get(term, TERMS["space"]) for term in terms]
    subject = words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]
    verb = "needs" if terms in (["weight"], ["space"]) else "need"
    subject = subject[0].upper() + subject[1:]
    if totals["provenLeast"]:
        return f"{subject} {verb} {totals['bound']} trucks: no plan takes fewer."
    return f"{subject} {verb} at least {totals['bound']} trucks; this plan takes {totals['trucks']}."


def to_save(plan, narrowest):
    """What one truck fewer would at least need, where the plan takes more than one truck and the
    bound: each part only where it binds."""
    totals, trucks = plan["totals"], plan["trucks"]
    if totals["trucks"] <= 1 or totals["trucks"] != totals["bound"]:
        return None
    fewer = totals["trucks"] - 1
    inside = trucks[0]["inside"]
    area = (inside["width"] // narrowest) * inside["length"] * inside["stackHeight"]
    sides = sum(c["length"] * c["height"] for truck in trucks for c in truck["crates"])
    grams = round(totals["grossWeight"] * 1000) - trucks[0]["payload"] * 1000 * fewer
    out = {}
    if grams > 0:
        out["lighter"] = grams / 1000
    if sides - area * fewer > 0:
        share = ((sides - area * fewer) * 1000 // area) / 10
        if share > 0:
            out["smaller"] = share
    return out or None


def smaller_sentence(to_save_a_truck):
    """`summary.smaller`; a part that rounds down to nothing is left out, and with it no sentence."""
    parts = []
    if to_save_a_truck.get("lighter", 0) >= 1:
        parts.append(f"at least {mass_at_least(to_save_a_truck['lighter'])} lighter, crates included")
    if to_save_a_truck.get("smaller") is not None and int(to_save_a_truck["smaller"]) >= 1:
        parts.append(f"at least {int(to_save_a_truck['smaller'])}{NB}% of one truck's space smaller")
    if not parts:
        return None
    joined = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + ", and " + parts[-1]
    return f"One truck fewer would need an order {joined}; only a new plan shows whether that is enough."


def fill_sentence(fill, line, trucks):
    """A `summary.fills` sentence for an article the request's `fill` names."""
    name = line.get("customerMaterial") or line.get("geometry") or line["material"]
    place = f"quotation {fill['document']}, item {fill['item']}" if fill.get("document") else f"line {fill['item']}"
    article = f"{name} in {line['colour']} ({place})" if line.get("colour") else f"{name} ({place})"
    on = "the same truck" if trucks == 1 else f"{trucks} trucks"
    if fill["packs"] == 0:
        if fill["finished"]:
            return f"No plan was found with more packs of {article} on {on}."
        return f"No plan with more packs of {article} was made in time."

    def counted(n, one, many):
        return f"1 {one}" if n == 1 else f"{n:,} {many}"

    tail = "" if fill["finished"] else "; the search stopped there"
    return (f"A plan with {counted(fill['packs'], 'more pack', 'more packs')} "
            f"({counted(fill['pieces'], 'piece', 'pieces')}) of {article} still takes {on}{tail}.")


def with_fills(plan, fills):
    """The plan with `fills` after `totals`, and `summary.fills` before the trucks' sentences."""
    lines = {(None, line["item"]): line for line in plan["lines"]}
    for document in plan["documents"]:
        for item in document["items"]:
            lines[(document["number"], item["item"])] = item
    out = {}
    for key, value in plan.items():
        if key == "fills":
            continue
        out[key] = value
        if key == "totals":
            out["fills"] = fills
    summary = {}
    for key, value in plan["summary"].items():
        if key == "fills":
            continue
        if key == "trucks":
            summary["fills"] = [
                dict(({"document": f["document"]} if f.get("document") else {}), item=f["item"],
                     sentence=fill_sentence(f, lines[(f.get("document"), f["item"])], plan["totals"]["trucks"]))
                for f in fills]
        summary[key] = value
    out["summary"] = summary
    return out


def summarize(plan):
    """The plan with `fill.space`, `boundBy` (kept only above a bound of 1), `toSaveATruck` and
    `summary` written as the server writes them; `summary` comes first after `header`."""
    totals = plan["totals"]
    if totals["bound"] <= 1:
        totals.pop("boundBy", None)
    else:
        assert totals.get("boundBy"), "a bound above 1 names its terms"
    narrowest = min(c["width"] for truck in plan["trucks"] for c in truck["crates"])
    sentences = []
    for n, truck in enumerate(plan["trucks"], 1):
        truck["fill"]["space"] = space(truck, narrowest)
        k = len(truck["crates"])
        sentences.append(f"Truck {n}: {'1 crate' if k == 1 else f'{k} crates'}, {mass(truck['grossWeight'])} gross of its "
                         f"{mass(truck['payload'])} payload, {int(truck['fill']['space'])}{NB}% of its space, "
                         f"longest crate {metres(max(c['length'] for c in truck['crates']))}.")
    crates = "the one crate" if totals["crates"] == 1 else f"all {totals['crates']} crates"
    head = (f"1 truck carries {crates}, {mass(totals['grossWeight'])} gross." if totals["trucks"] == 1
            else f"{totals['trucks']} trucks carry all {totals['crates']} crates, {mass(totals['grossWeight'])} gross.")
    summary = {"head": head}
    why = reason(totals)
    if why:
        summary["reason"] = why
    saving = to_save(plan, narrowest)
    totals.pop("toSaveATruck", None)
    if saving:
        totals["toSaveATruck"] = saving
        sentence = smaller_sentence(saving)
        if sentence:
            summary["smaller"] = sentence
    previous = plan.get("summary")
    if isinstance(previous, dict) and previous.get("fills"):
        summary["fills"] = previous["fills"]
    summary.update({"trucks": sentences, "closing": CLOSING})
    out = {}
    for key, value in plan.items():
        if key == "summary":
            continue
        out[key] = value
        if key == "header":
            out["summary"] = summary
    return out


def read_mock(path):
    """A mock's text, its answer and where the answer starts and ends in it."""
    text = open(path, encoding="utf-8").read()
    start = text.index("{")
    answer, end = json.JSONDecoder().raw_decode(text, start)
    return text, answer, start, end


def write_answer(path, answer):
    text, _, start, end = read_mock(path)
    open(path, "w", encoding="utf-8").write(text[:start] + dump(answer) + text[end:])


def shortest(value):
    """A figure in its shortest digits, as the server writes it: 450 and 2, never 450.0 or 2.0."""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, dict):
        return {k: shortest(v) for k, v in value.items()}
    if isinstance(value, list):
        return [shortest(v) for v in value]
    return value


def dump(answer):
    return json.dumps(shortest(answer), ensure_ascii=False, separators=(",", ":"))
