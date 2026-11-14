---
name: planning-truck-loads
description: Plans how a LINKIN order loads onto trucks through the LINKIN CPQ connector, and tries what-ifs on it. Use when the buyer asks how many trucks an order or a quotation takes, what room a truck leaves, whether quotations share a truck, how to fill a truck, or how many pieces to order so a line clears a minimum charge (the metal's weight, a die's press run, a powder colour) with the load in mind. Not for a plain price, which quoting-profiles gives, and never volunteered on one. Not for new profiles with no die yet, which have no packing to plan.
---

# Planning truck loads

`plan_load` estimates how the customer's profiles load onto standard trailers, for booking the
customer's own carrier, since prices are ex works. It plans lines being priced, as
`price_quotation` takes them, and issued quotations by number, whole or the items named,
together, and all it is given or nothing. Trucks and crates come from it alone: of a line, item
or quotation it didn't plan, refused or was never given, draw no conclusion of your own, not that
it fits or likely fits, nor its trucks, crates, room or share of the payload, by weight, length,
volume or free space, even called an estimate. Asked, give its weight as priced or entered, never
set against the truck. Keep the connector's rules: its tool descriptions hold each field's
meaning. Quoting, issuing and submitting stay quoting-profiles'.

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
   planned by its number, with `items` where only some of its items are meant.
2. **Plan** with `plan_load`, without drawings: the lines as priced, the quotations as
   `documents`.
3. **A refusal,** `NOT_PLANNABLE`, plans nothing. Its message gives each fault a sentence of its
   own:
   - **LINKIN's data** (a pack not measured yet, a pack no carrier takes): say what is missing,
     and pass on as they are its words "this is LINKIN's data, not a mistake of yours: contact
     your sales representative at LINKIN so it can be fixed".
   - **The customer's own** (an inquiry's line, a quotation not theirs, unknown or revoked, an
     item it doesn't hold, a line not `ok`): say what it is and its mend.

   Say the mends in plain words, without the request's field names (`items[0]`,
   `documents[0].items`). Where the only mend is to leave it out (an inquiry's line, a revoked
   quotation), plan the rest and say so; where the customer must choose (another number, or
   waiting for LINKIN's data), ask. A plan without a line, item or quotation names what it leaves
   out, and is never given as the whole order.
4. **Present:**
   - what it didn't plan, and why it can't be planned yet, in plain words, saying plainly that
     the plan doesn't include it;
   - the trucks (`totals.trucks`; where `provenLeast` is false, fewer may be possible, down to
     `bound`), and per truck its net weight against the payload, its fill (floor, volume, weight)
     and what it leaves `free` (the payload less the net weight, and each lane's unused length);
   - that it is an estimate on theoretical weights, with no promise of how the plant loads; and,
     while `emptyWeightCounted` and `axlesChecked` are false, that the crates' own weight isn't
     counted and the axles aren't checked.
5. **The drawing**, only when asked, for the plan chosen: `plan_load` again with
   `drawings: true`. Offer none unasked. Where the host shows no SVG, as Claude Code doesn't, save
   each truck's `drawing` as a `.svg` file and give its path.

## What-ifs: the minimums and the load

For "how do I fill the truck without falling under the minimum", or what more or fewer pieces
change:

1. **Find what binds**, in the priced detail:
   - **a line's own minimum:** a charge with `minimum: true` and `perOrder: false` bills a
     minimum quantity for the line, such as the metal's weight above `weights.net`;
   - **a die's press run and wear, a powder colour, the anodizing:** the order's `groups` with an
     `uplift`, each with the lines that share it.

   No tool gives the price list, so a minimum that doesn't bind can't be read. Say so, and price
   fewer pieces to see where one starts.
2. **Estimate which pieces to price**, from the pricing's own figures, only to choose what to
   price:
   - the metal: the billed weight ÷ (the weight per metre × the length in metres), rounded up;
   - a group, in proportion: one line reaches it at about its `quantity.order` × `minimum` ÷
     `value`; lines sharing it, by each line's share of the `basis`;
   - where the quantity a line's own minimum lifts isn't shown, price more pieces instead.
3. **Price and plan each option**, in calls of its own, without drawings: `price_quotation`
   (`view: detail`) with every line of the option, then `plan_load`. The packs round the pieces
   up, and `quantity.order` says to what. The price comes only from the tool: never work one
   out. An option refused is compared as refused, with its fault, as in Plan an order.
4. **Compare** the options in one table: the pieces per line, the net value, the price per kg,
   the minimums still paid, the trucks, and what the last truck leaves free. The free payload and
   free lane lengths don't say a crate fits, since a crate needs a lane of its own length and its
   own weight. To see whether more fits, plan it.
5. **The customer chooses.** Issue only as quoting-profiles issues: price, show, ask, and issue
   on a separate yes.

## Limits

Past a plan's limits (`plan_load`'s description), plan fewer lines or quotations at once.
