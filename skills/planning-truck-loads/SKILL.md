---
name: planning-truck-loads
description: Estimates how much of a LINKIN order fits standard trucks, to size the order, through the LINKIN CPQ connector, and tries what-ifs on it. Use when the buyer asks how many trucks an order or a quotation takes, why so many, what room a truck leaves, how much more of an article would fit, whether quotations share a truck, where an article is in the load, how to fill a truck, or how many pieces to order so a line clears a minimum charge (the metal's weight, a die's press run, a powder colour) with the load in mind. Not for a plain price, which quoting-profiles gives, and never volunteered on one. Not for new profiles with no die yet, which have no packing to plan.
allowed-tools: mcp__plugin_linkin-cpq_linkin-cpq__get_account mcp__plugin_linkin-cpq_linkin-cpq__find_profiles mcp__plugin_linkin-cpq_linkin-cpq__find_values mcp__plugin_linkin-cpq_linkin-cpq__price_quotation mcp__plugin_linkin-cpq_linkin-cpq__price_inquiry mcp__plugin_linkin-cpq_linkin-cpq__find_documents mcp__plugin_linkin-cpq_linkin-cpq__read_document mcp__plugin_linkin-cpq_linkin-cpq__plan_load mcp__plugin_linkin-cpq_linkin-cpq__describe_api
---

# Planning truck loads

`plan_load` estimates how much of the customer's order fits standard trucks, by weight and by
size, so the customer can size the order: it is not a loading plan. It plans lines being priced, as
`price_quotation` takes them, and issued quotations by number, whole or the items named, together,
and all it is given or nothing. Quoting, issuing and submitting stay quoting-profiles'. Keep to the
rules at the end of this skill.

## First

1. If the LINKIN CPQ connector's tools aren't available, say: "The LINKIN CPQ connector isn't
   connected. Connect it on the LINKIN CPQ plugin's Connectors tab (in Claude Code, `/mcp`), then
   ask again." Then stop.
2. `get_account`, and the customer and sales area as quoting-profiles takes them. A sign-in
   linked to no customer plans nothing: its documents are inquiries, whose profiles have no die
   yet.

## Plan an order

1. **The lines.** From the conversation, priced first with `price_quotation` (`view: detail` with
   `detailItems`, as quoting-profiles prices), since only `ok` lines are planned; or an issued
   quotation, found with `find_documents` and planned by its number, with `items` where only some of
   its items are meant.
2. **Plan** with `plan_load`: the lines as priced, the quotations as `documents`.
3. **A refusal,** `NOT_PLANNABLE`, plans nothing. Its message gives each fault, up to the first
   ten, a sentence of its own, and says how many more. What is wrong with those more is not said,
   and may differ from the faults given, even where they look alike: give their count, say and
   guess nothing of their faults, and say they are named once the faults given are mended. Each
   fault given is:
   - **LINKIN's data** (a pack not measured yet, a pack no carrier takes): say what is missing,
     and pass on as they are its words "this is LINKIN's data, not a mistake of yours: contact
     your sales representative at LINKIN so it can be fixed".
   - **The customer's own** (an inquiry's line, a quotation not theirs, unknown or revoked, an
     item it doesn't hold, a line not `ok`): say what it is and its mend.

   Say the faults and mends in plain words, without the request's field names (`items[0]`,
   `documents[0].items`). Where the only mend is to leave it out (an inquiry's line, a revoked
   quotation), plan the rest and say so; where the customer must choose (another number, or
   waiting for LINKIN's data), ask. A plan without a line, item or quotation names what it leaves
   out, and is never given as the whole order.
4. **Present.** Where part of the order wasn't planned (left out after a refusal, or a profile
   with no die yet), first say what, and why it can't be planned yet, in plain words, saying
   plainly that the plan doesn't include it: the plan's "all" is all it was given. Then lead with
   `summary`'s sentences as they are, translated only where the conversation isn't in English:
   `head`, then `reason`, `smaller` and `fills` where given, a sentence per truck, and `closing`.
   Change none of their figures, and add no cause of your own to `reason`'s. Its "no plan takes
   fewer" is for crates lying along the truck under `stackHeight`, as `provenLeast` says. With
   them:
   - the net weight, the goods alone, beside the gross;
   - a truck's two shares are of its payload and of its space, as its sentence gives them; never
     its `fill.volume` or `fill.floor`, which measure otherwise;
   - that the weights are theoretical, each crate's empty weight LINKIN's approximation, and, while
     `axlesChecked` is false, that the axles aren't checked.

   Never present the plan as a loading plan, a carrier's booking or how the plant loads.

   A pack count may include a part-filled pack: never work pieces out from packs, nor a rounding
   from them. Give the pieces the answers give: a line's or an item's as priced or issued, a
   crate's in its `contents`, a fill's in its sentence.

## Asked about a plan

Only when the customer asks:

1. **Whether fewer trucks could do:** `summary.smaller` says what one truck fewer would need of the
   order, each "at least" a floor, not shown to be enough: only a new plan shows that. Without it,
   the plan gives no such figure.
2. **Where an article is** (a line, or a quotation's item): every crate on every truck whose
   `contents` name it. A line's entry is its item with no `document`; a quotation's item is its
   number and item together (a line and two quotations may each have an item 10). Its pieces, packs
   where given, and weight in a crate are that entry's, not the crate's. A crate may hold several
   articles, of any cut length and of other quotations too, the crate as long as the longest bars:
   say it is shared, and with which, each by its text and colour. Never guess a crate from its size
   or the line's `packing`. Where a crate's `positions` put its packs is the planner's estimate of
   how they fit, not how the plant packs: asked where in a crate the packs lie, say the plan gives
   the crate and its truck, not how the plant packs or loads them.
3. **Why a crate isn't a smaller one:** its `smaller` gives the height its packs would stand in each
   smaller carrier, against that carrier's inside height in `carriers`; a height absent means some
   of its packs fit no way across that carrier. Without `smaller`, the crate is its smallest carrier
   or is itself the pack, and the plan gives no other reason. Never work it out from the positions
   or the packs.
4. **How much more of an article fits:** plan with `fill` naming it (again, where the order is
   already planned), a line by its `item`, a quotation's item by its `document` and `item`: those
   the customer asks about, up to 100, every article of the order where they ask about all of them.
   Lead with its sentence in `summary.fills` as it is. It is a number of packs more with which a
   plan still takes as many trucks, as a new plan crates and loads them: never the most that could
   fit, never that every smaller amount fits, never that its room takes another article, and never
   that the plant ships so many. Where the sentence says no plan was found or made in time, or that
   the search stopped there, it says nothing of whether more fits. Where it says no plan was made in
   time, or that the search stopped there, time ran out: to search that article again, plan the same
   lines and quotations with `fill` naming it alone. It carries no price: to know one, price the
   order with that line raised (the what-ifs' step 3). Never work it out from the free payload or
   lane lengths.

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
3. **Price and plan each option**, in calls of its own: `price_quotation` with every line of the
   option (`view: detail` with `detailItems`, as quoting-profiles prices), then `plan_load`. The
   packs round the pieces up, and `quantity.order` says to what. The price comes only from the tool:
   never work one out. An option refused is compared as refused, with its fault, as in Plan an
   order.
4. **Compare** the options in one table: the pieces per line, the net value, the price per kg, the
   minimums still paid, the trucks, and the last truck's gross weight against its payload and its
   share of its space in whole percent, as its sentence gives them.
   Neither share, nor the free payload and lane lengths, says a crate fits: a crate needs a lane as
   wide as it and its own length in one piece, or a crate of its width at least as long to stand
   on under `stackHeight`, and the payload for its goods and its own empty weight. To see how much
   more of an article fits, plan with `fill` (Asked about a plan, point 4); to see what a quantity
   asked about would take, price and plan it. Never work either out from the options planned.
5. **The customer chooses.** Issue only as quoting-profiles issues: price, show, ask, and issue
   on a separate yes.

## Keep to

- Trucks and crates come from `plan_load` alone: of a line, item, quotation or quantity it didn't
  plan, refused or was never given, draw no conclusion of your own, not that it fits or likely
  fits, nor its trucks, crates, room or share of the payload, by weight, length, volume or free
  space, even called an estimate. Give its weight only when asked, as priced or entered, never set
  against the truck.
- A plan may show beside the answer in the host's view of it. Shown or not, give it in words from
  the answer alone, and say nothing of the view, neither that it shows nor how to use it.
- The plan's answer carries no drawing: draw no truck of your own (no ASCII, SVG or diagram), take
  nothing from a view as the plan's facts (where axles stand, or where bars lie along a crate), and
  offer no drawing, file or download, not even in a closing line; asked for a drawing, say you
  can't give one.
- Never turn `summary.smaller`'s floors into crates or pieces, never say that so much less would
  fit, and never advise cutting or splitting the order: to see a smaller quantity the buyer names,
  price and plan it.
- Name a crate by its text (a full crate), never by a carrier's code unless asked, in a plan, a
  what-if or an answer about where an article is.
- Keep the connector's rules: its tool descriptions hold each field's meaning.
- Past a plan's limits (`plan_load`'s description), plan fewer lines or quotations at once.

**A refusal of the account's details.** Where a tool answers that the customer's LINKIN account's
details are incomplete or invalid, say which detail its message names and stop: retry nothing,
and name no other detail. Where the message ends "Fix it in your profile on the LINKIN website.",
ask the customer to complete their profile at https://linkin.eu/en/complete-profile/, then to ask
again. Where it says to contact LINKIN, ask the customer to contact LINKIN to correct it, and
give no profile link.
