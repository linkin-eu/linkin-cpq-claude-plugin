---
name: planning-truck-loads
description: Plans how a LINKIN order loads onto trucks through the LINKIN CPQ connector, and tries what-ifs on it. Use when the buyer asks how many trucks an order or a quotation takes, what room a truck leaves, whether quotations share a truck, how to fill a truck, or how many pieces to order so a line clears a minimum charge (the metal's weight, a die's press run, a powder colour) with the load in mind. Not for a plain price, which quoting-profiles gives, and never volunteered on one. Not for new profiles with no die yet, which have no packing to plan.
---

# Planning truck loads

`plan_load` estimates how the customer's profiles load onto standard trailers, for booking the
customer's own carrier, since prices are ex works. It plans lines being priced, as
`price_quotation` takes them, and issued quotations by number, together. Keep the connector's
rules: its tool descriptions hold each field's meaning. Quoting, issuing and submitting stay
quoting-profiles'.

## First

1. If the LINKIN CPQ connector's tools aren't available, say: "The LINKIN CPQ connector isn't
   connected. Connect it on the LINKIN CPQ plugin's Connectors tab (in Claude Code, `/mcp`), then
   ask again." Then stop.
2. `get_account`, and the customer and sales area as quoting-profiles takes them. A sign-in
   linked to no customer plans nothing: its documents are inquiries, whose profiles have no die
   yet.

## Plan an order

1. **The lines.** From the conversation, priced first with `price_quotation` (`view: detail`),
   since only `ok` lines are planned; or an issued quotation, found with `find_documents` and
   planned by its number.
2. **Plan** with `plan_load`, `drawings: false`: the lines as priced, the quotations as
   `documents`.
3. **Present:**
   - the trucks (`totals.trucks`), and per truck its net weight against the payload, its fill
     (floor, volume, weight) and what it leaves `free` (the payload less the net weight, and each
     lane's unused length);
   - each line or quotation not planned, and why, from its messages, never estimated;
   - that it is an estimate: theoretical weights, the crates' own weight not yet counted, the
     axles not checked, and no promise of how the plant loads.
4. **The drawing**, only when asked, for the plan chosen: `plan_load` again with
   `drawings: true`. Where the host shows no SVG, as Claude Code doesn't, save each truck's
   `drawing` as a `.svg` file and give its path.

## What-ifs: the minimums and the load

For "how do I fill the truck without falling under the minimum", or what more or fewer pieces
change:

1. **Find what binds**, in the priced detail:
   - **the metal:** a line whose metal charges have `minimum: true` is billed a weight above its
     `weights.net`, and that weight is its minimum;
   - **a die's press run and wear, a powder colour, the anodizing:** the order's `groups` with an
     `uplift`, each with the lines that share it.

   No tool gives the price list, so a minimum that doesn't bind can't be read. Say so, and price
   fewer pieces to see where one starts.
2. **Estimate the pieces that clear it**, from the answer's own figures, never from rates:
   - the metal: the billed weight ÷ (the weight per metre × the length in metres), rounded up;
   - a group: its `basis` × `minimum` ÷ `value` is the basis that reaches it, shared by its lines;
   - then up to the finish's packs in `find_profiles`: at least the smallest `minimum`, in steps
     of its `rounding`.
3. **Price and plan each option**, in calls of its own, `drawings: false`: `price_quotation`
   with every line of the option, then `plan_load`. The price comes only from the tool: never
   work one out.
4. **Compare** the options in one table: the pieces per line, the net value, the price per kg,
   the minimums still paid, the trucks, and what the last truck leaves free. The free payload and
   free lane lengths don't say a crate fits, since a crate needs a lane of its own length and its
   own weight. To see whether more fits, plan it.
5. **The customer chooses.** Issue only as quoting-profiles issues: price, show, ask, and issue
   on a separate yes.

## Limits

- A plan takes at most 300 lines, 10 quotations and 600 crates. Past them, plan fewer at once.
- New profiles with no die yet are never planned, neither an inquiry's line nor an issued
  inquiry.
- A coated pack the plant hasn't measured yet is left out and named, never estimated.
