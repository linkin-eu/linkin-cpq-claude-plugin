"""Writes the eval mocks of the planning cases from made-up figures, as the server would answer them:

- `fill-truck-minimum`: the bare profile 7800001, 6 m, T5, priced and planned at each quantity the
  case may try (`fixtures/price_quotation-<n>.json`, `fixtures/plan_load-<n>.json`);
- `load-plan-inquiry-line`: the 200-bar plan;
- `load-plan-quotation` and `load-plan-app-host`: the coated quotation's plan, its trucks and crates
  as written in the mock, its sentences and figures worked out again (`plan_summary.py`);
- `load-plan-two-trucks`: a heavy bare profile on two trucks, bound by weight alone;
- `load-plan-fill`: the coated quotation's plan with more packs of its item 10.

Every figure is made up: metal 2,420 + 640 EUR/t with a 250 kg minimum a line, the press run
545 EUR/t with the die's 272.50 EUR minimum, die wear 0.16 EUR/m on two cavities, 20 kg a crate.

Run from the plugin's root: python3 evals/tools/make_plan_mocks.py
Nothing should change unless the answer's shape or these figures did: check with git diff.
"""
import copy
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from plan_summary import dump, read_mock, summarize, with_fills, write_answer  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
CASES = ROOT / "evals"

# One width, so the carriers differ only in height. Smallest first, as the answer lists them.
CARRIERS = [
    {"carrier": "AW1/3", "text": "Third crate", "insideWidth": 660, "insideHeight": 250, "emptyWeight": 20},
    {"carrier": "AW1/2", "text": "Half crate", "insideWidth": 660, "insideHeight": 370, "emptyWeight": 20},
    {"carrier": "AW1", "text": "Full crate", "insideWidth": 660, "insideHeight": 470, "emptyWeight": 20},
]
CRATES = {"AW1": (760, 560), "AW1/2": (760, 420), "AW1/3": (760, 300)}  # outside width and height, mm
INSIDE = {"length": 13600, "width": 2450, "height": 2600, "stackHeight": 2460}
HEADER = {"soldToParty": "0000900001", "salesArea": {"salesOrganization": "1102", "salesOrganizationText": "LINKIN Bulgaria", "distributionChannel": "10"}}


def r1(x):
    return float(int(x * 10 + 0.5 + 1e-9)) / 10


def r2(x):
    return round(x + 1e-9, 2)


def fmt(x, decimals=2):
    return f"{x:,.{decimals}f}"


def kg(x):
    return f"{x:,.0f}" if x == int(x) else f"{x:,.2f}".rstrip("0")


def write_json(path, answer):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump(answer) + "\n", encoding="utf-8")


def write_md(path, answer, front="expect:\n  documents: array\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{front}---\n\n" + dump(answer) + "\n", encoding="utf-8")


# ---- fill-truck-minimum: 7800001 bare, 0.6 kg/m, 6 m -------------------------------------------

KG_M, LENGTH_M, METAL_MIN, PRESS_MIN = 0.6, 6, 250, 272.5
ROUNDINGS = [("AW1", 200), ("AW1/2", 100), ("AW1/3", 50)]  # pieces a crate holds, by carrier
QUANTITIES = (50, 70, 100, 139, 140, 150, 200, 300, 400)


def order_quantity(entered):
    """As the server rounds: whole steps of the largest rounding, the rest one step of the smallest
    rounding at least as large."""
    whole, rest = divmod(max(entered, 50), 200)
    return whole * 200 + (min(r for _, r in ROUNDINGS if r >= rest) if rest else 0)


def packs_for(quantity):
    """The crates a quantity is packed in: (carrier, count, pieces)."""
    whole, rest = divmod(quantity, 200)
    out = [("AW1", whole, whole * 200)] if whole else []
    if rest:
        pieces, carrier = min((r, n) for n, r in ROUNDINGS if r >= rest)
        out.append((carrier, 1, pieces))
    return out


def digest(prefix, text):
    return prefix + hashlib.sha256(text.encode()).hexdigest()


def price(base, entered):
    """The priced order at a quantity, from the `per-tonne` case's priced line."""
    q = order_quantity(entered)
    net = r2(q * LENGTH_M * KG_M)
    billed = max(net, METAL_MIN)
    die_metres = q * LENGTH_M / 2
    m3 = q * 0.0375
    lme, billet = r2(billed * 2.42), r2(billed * 0.64)
    press = r2(net * 0.545)
    press_billed = max(press, PRESS_MIN)
    wear = r2(die_metres * 0.16)
    heat = r2(m3 * 5.2)
    metal_min, press_min = billed > net, press < PRESS_MIN
    net_value = r2(lme + billet + press_billed + wear + heat)

    o = copy.deepcopy(base)
    item = o["items"][0]
    o["inputHash"] = digest("h1:", f"7800001-{entered}")
    o["priceHash"] = digest("p1:", f"7800001-{entered}-2026-11-06")
    o["totals"]["netValue"] = net_value
    o["totals"]["lines"]["rounded"] = 1 if q != entered else 0
    packs = packs_for(q)
    packed = ", ".join(f"{count} x {carrier}" for carrier, count, _ in packs)
    item["quantity"]["entered"], item["quantity"]["order"] = entered, q
    item["packs"] = [{"bundle": carrier, "count": count, "pieces": pieces} for carrier, count, pieces in packs]
    item["bars"]["count"] = q
    item["netValue"] = net_value
    item["netPrice"]["amount"] = r2(net_value / q)
    item["weights"]["net"] = item["weights"]["gross"] = net
    if q == entered:
        message = {"severity": "info", "code": "ZSD_AVC/003", "attention": False, "text": f"Order quantity {q} PC packed as {packed}",
                   "params": [str(q), "PC", packed], "target": {"item": "10"}}
    else:
        message = {"severity": "warning", "code": "ZSD_AVC/002", "attention": False,
                   "text": f"Order quantity {entered} PC rounded up to {q} PC as {packed}",
                   "params": [str(entered), "PC", str(q), packed], "target": {"item": "10"}}
    item["messages"] = [message]

    metal, extrusion = item["breakdown"]
    metal["value"] = r2(lme + billet)
    metal["minimum"] = metal_min
    for charge, rate, value in ((metal["charges"][0], 2420, lme), (metal["charges"][1], 640, billet)):
        charge["value"] = value
        charge["quantity"]["value"] = billed
        charge["minimum"] = metal_min
        charge["basis"] = f"Metal, billed weight: {kg(billed)} kg × {fmt(rate)} EUR / 1,000 kg"
    press_run, die_wear, ageing = extrusion["charges"]
    extrusion["value"] = r2(press_billed + wear + heat)
    extrusion["minimum"] = extrusion["perOrder"] = press_min
    press_run["value"] = press_billed
    press_run["quantity"]["value"] = net
    press_run["minimum"] = press_run["perOrder"] = press_min
    press_run["basis"] = (
        f"Press output from 1,300 kg/h: 545.00 EUR per 1,000 kg × {kg(net)} kg through die 680001 is {fmt(press)}, "
        f"billed at the least the die's 272.50 EUR minimum per order; 1 item, {kg(net)} kg in the order"
        if press_min else f"Press output from 1,300 kg/h: {kg(net)} kg × 545.00 EUR / 1,000 kg")
    die_wear["value"] = wear
    die_wear["quantity"]["value"] = die_metres
    die_wear["basis"] = f"Die level 4, Die life 20,000-25,000 m: {kg(die_metres)} m × 0.16 EUR / m"
    ageing["value"] = heat
    ageing["quantity"]["value"] = m3
    ageing["basis"] = f"Temper T5, standard: {kg(m3)} m³ × 52.00 EUR / 10 m³"
    if press_min:
        uplift = r2(PRESS_MIN - press)
        o["groups"] = [{"id": "g1", "conditionType": "ZPDM", "key": "680001", "text": "Press run minimum",
                        "basis": {"value": net, "unit": "KGM", "sapUnit": "KG"}, "value": press, "minimum": PRESS_MIN, "uplift": uplift,
                        "items": [{"item": "10", "basis": net, "share": uplift}]}]
        item["uplift"] = uplift
        item["groups"] = ["g1"]
        item["shares"] = [{"group": "g1", "basis": net, "share": uplift}]
    else:
        o["groups"] = []
        item["uplift"] = 0
        item["groups"] = []
        item["shares"] = []
    return o, q, packs, net


def bare_plan(header, packs, net):
    """The plan of a bare line: each crate is its pack, one line in it, no packs or bands. Crates
    of one length and width stack, the full ones under the part one."""
    crates = []
    z = 0
    for carrier, count, pieces in packs:
        width, height = CRATES[carrier]
        per = pieces // count
        for _ in range(count):
            crate_net = r2(per * LENGTH_M * KG_M)
            crates.append({"carrier": carrier, "length": 6000, "width": width, "height": height, "x": 0, "y": 0, "z": z,
                           "netWeight": crate_net, "contents": [{"item": "10", "pieces": per, "netWeight": crate_net}]})
            z += height
    lanes = 2450 // max(c["width"] for c in crates)
    floor = sum(c["length"] * c["width"] for c in crates if c["z"] == 0) / (13600 * 2450) * 100
    volume = sum(c["length"] * c["width"] * c["height"] for c in crates) / (13600 * 2450 * 2600) * 100
    used = {carrier for carrier, _, _ in packs}  # a line's packing: the carriers its crates are of, smallest first
    line = {"item": "10", "material": "1370000305", "text": "7800001 · Example profile · T5, standard · 6000 mm · Bare",
            "geometry": "7800001", "surfaceFinish": "BARE", "cutLength": 6000,
            "packing": [{"carrier": c, "packingValue": r} for c, r in reversed(ROUNDINGS) if c in used]}
    gross = r2(net + 20 * len(crates))
    return {"header": header, "lines": [line], "documents": [], "carriers": CARRIERS,
            "totals": {"trucks": 1, "crates": len(crates), "netWeight": net, "grossWeight": gross, "bound": 1, "provenLeast": True},
            "emptyWeightCounted": True, "axlesChecked": False, "stacksFewest": True,
            "trucks": [{"vehicle": "SEMI_13_6", "text": "Curtainsider semi-trailer 13.6 m", "inside": dict(INSIDE),
                        "payload": 24000, "netWeight": net, "grossWeight": gross,
                        "fill": {"floor": r1(floor), "volume": r1(volume), "weight": r1(gross / 24000 * 100)},
                        "free": {"payloadLessGrossWeight": r2(24000 - gross), "unusedLaneLengths": [13600 - 6000] + [13600] * (lanes - 1)},
                        "crates": crates}]}


def fill_truck_minimum():
    _, base, _, _ = read_mock(CASES / "per-tonne/mocks/linkin-cpq/price_quotation.md")
    header = {k: v for k, v in base["header"].items() if k in ("soldToParty", "salesArea")}
    fixtures = CASES / "fill-truck-minimum/mocks/linkin-cpq/fixtures"
    for entered in QUANTITIES:
        priced, _, packs, net = price(base, entered)
        write_json(fixtures / f"price_quotation-{entered}.json", priced)
        write_json(fixtures / f"plan_load-{entered}.json", summarize(bare_plan(header, packs, net)))
    inquiry_line = CASES / "load-plan-inquiry-line/mocks/linkin-cpq/fixtures/plan_load-200.json"
    inquiry_line.write_text((fixtures / "plan_load-200.json").read_text(encoding="utf-8"), encoding="utf-8")


# ---- the coated quotation: its plan is written in the mock; its sentences are worked out again ----

def coated_quotation():
    for case in ("load-plan-quotation", "load-plan-app-host"):
        path = CASES / case / "mocks/linkin-cpq/plan_load.md"
        _, answer, _, _ = read_mock(path)
        write_answer(path, summarize(answer))


def fill():
    """330 more packs of the coated item 10: 22 more full crates of 15 packs, so 24 crates in the
    truck's 24 long-crate slots (two behind one another, three lanes, four high)."""
    _, answer, _, _ = read_mock(CASES / "load-plan-quotation/mocks/linkin-cpq/plan_load.md")
    answer = with_fills(answer, [{"document": "LQ26000002", "item": "10", "packs": 330, "pieces": 1320, "finished": True}])
    write_md(CASES / "load-plan-fill/mocks/linkin-cpq/plan_load.md", answer)


# ---- two trucks: quotation LQ26000004, 7800002 bare at 1.2 kg/m, 4,000 pieces in 20 full crates --

def two_trucks():
    """29.2 t gross takes two 24 t payloads; the 20 crates take under one truck's space and stand
    within its long-crate slots, so the weight alone sets the bound."""
    per, crate_net = 200, round(200 * 6 * 1.2, 3)

    def crate(x, y, z):
        return {"carrier": "AW1", "length": 6000, "width": 760, "height": 560, "x": x, "y": y, "z": z, "netWeight": crate_net,
                "contents": [{"document": "LQ26000004", "item": "10", "pieces": per, "netWeight": crate_net}]}

    def truck(crates):
        net = round(sum(c["netWeight"] for c in crates), 3)
        gross = round(net + 20 * len(crates), 3)
        lanes = INSIDE["width"] // 760
        used = [max([c["x"] + c["length"] for c in crates if c["y"] == lane * 760], default=0) for lane in range(lanes)]
        floor = sum(c["length"] * c["width"] for c in crates if c["z"] == 0) / (13600 * 2450) * 100
        volume = sum(c["length"] * c["width"] * c["height"] for c in crates) / (13600 * 2450 * 2600) * 100
        return {"vehicle": "SEMI_13_6", "text": "Curtainsider semi-trailer 13.6 m", "inside": dict(INSIDE), "payload": 24000,
                "netWeight": net, "grossWeight": gross,
                "fill": {"floor": r1(floor), "volume": r1(volume), "weight": r1(gross / 24000 * 100)},
                "free": {"payloadLessGrossWeight": round(24000 - gross, 3), "unusedLaneLengths": [13600 - u for u in used]},
                "crates": crates}

    # truck 1: two stacks behind one another in each of two lanes, four high; truck 2: one stack of four
    trucks = [truck([crate(x, y, z) for x in (0, 6000) for y in (0, 760) for z in (0, 560, 1120, 1680)]),
              truck([crate(0, 0, z) for z in (0, 560, 1120, 1680)])]
    net = round(sum(t["netWeight"] for t in trucks), 3)
    gross = round(sum(t["grossWeight"] for t in trucks), 3)
    answer = {"header": HEADER, "lines": [],
              "documents": [{"number": "LQ26000004", "items": [{"item": "10", "material": "1370000305",
                             "text": "7800002 · Example heavy profile · T5, standard · 6000 mm · Bare", "geometry": "7800002",
                             "surfaceFinish": "BARE", "cutLength": 6000, "packing": [{"carrier": "AW1", "packingValue": per}]}]}],
              "carriers": CARRIERS,
              "totals": {"trucks": 2, "crates": 20, "netWeight": net, "grossWeight": gross, "bound": 2, "provenLeast": True, "boundBy": ["weight"]},
              "emptyWeightCounted": True, "axlesChecked": False, "stacksFewest": True, "trucks": trucks}
    write_md(CASES / "load-plan-two-trucks/mocks/linkin-cpq/plan_load.md", summarize(answer))


if __name__ == "__main__":
    fill_truck_minimum()
    coated_quotation()
    fill()
    two_trucks()
