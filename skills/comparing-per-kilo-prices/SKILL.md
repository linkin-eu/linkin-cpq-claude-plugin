---
name: comparing-per-kilo-prices
description: Compares LINKIN's price for aluminium extruded profiles with another offer per kg or per tonne, like for like, through the LINKIN CPQ connector. Use only when the buyer brings the comparison - another supplier's or a competitor's price in EUR/kg or EUR/t, a remark that LINKIN is more expensive per kilo, or a request for LINKIN's price per kg or per tonne to compare with another offer. Not for a plain price or quote, which quoting-profiles handles with its price per kg column, and never volunteered.
allowed-tools: mcp__plugin_linkin-cpq_linkin-cpq__get_account mcp__plugin_linkin-cpq_linkin-cpq__find_profiles mcp__plugin_linkin-cpq_linkin-cpq__find_values mcp__plugin_linkin-cpq_linkin-cpq__price_quotation mcp__plugin_linkin-cpq_linkin-cpq__price_inquiry mcp__plugin_linkin-cpq_linkin-cpq__find_documents mcp__plugin_linkin-cpq_linkin-cpq__read_document mcp__plugin_linkin-cpq_linkin-cpq__plan_load mcp__plugin_linkin-cpq_linkin-cpq__describe_api
---

# Comparing per-kilo prices

The buyer has brought another offer per kg or per tonne, says LINKIN is dearer per kilo, or asks
for LINKIN's price per kg to compare. Every price table already shows the price per kg
(quoting-profiles). This skill is the explanation behind that column, given only when the buyer
asks. Never start it unasked, and never press it on the buyer.

Give the figures first, then the explanation, briefly. Keep the connector's rules.

**A refusal of the account's details.** Where a tool answers that the customer's LINKIN account's
details are incomplete or invalid, say which detail its message names and stop: retry nothing,
and name no other detail. Where the message ends "Fix it in your profile on the LINKIN website.",
ask the customer to complete their profile at https://linkin.eu/en/complete-profile/, then to ask
again. Where it says to contact LINKIN, ask the customer to contact LINKIN to correct it, and
give no profile link.

## 1. LINKIN's price

Price a profile the buyer already orders here, without loading another skill:

1. If the LINKIN CPQ connector's tools aren't available, say: "The LINKIN CPQ connector isn't
   connected. Connect it on the LINKIN CPQ plugin's Connectors tab (in Claude Code, `/mcp`), then
   ask again." Then stop.
2. `get_account`. With one customer in one sales area, act for it. With different customers, ask
   which, and never choose. With one customer in several sales areas, use the one where
   `find_profiles` finds the profile, and ask where more than one does. With no linked customer,
   say quotations need the account linked to the customer's number, which LINKIN does on request
   (https://linkin.eu/en/contact/). Pass the `soldToParty`, and the sales area where there are
   several, to every call that takes them.
3. `find_profiles` with `limit` 200, following `next` until the profile is found. Match it by its
   geometry, name or drawing number, and start from its `orderAs`; `find_profiles` with
   `material` gives its fields. Where two match, ask which. With no match, ask whether it is a new
   profile they have drawn.
4. Ask in one message for whatever the request leaves out, each field and its choices by their
   text: length, temper, finish and pieces; for powder coated, the colour system and number, the
   surface and the Qualicoat class; for anodized, the pretreatment, colour and thickness class.
5. `price_quotation` with `view: detail` and `detailItems` on the first call. `incomplete`: ask
   for the fields in `missing`. `inconsistent`: say which value a rule refuses, in plain words,
   and offer the values `find_values` allows; guess nothing. Price each alternative (another
   quantity or finish) in its own call: lines priced together share the die's and the colour's
   minimums.

For a new profile with no die yet, load inquiring-new-profiles and price it as it says, and say
the weights are the drawing's estimates and the price preliminary.

Show LINKIN's figures in the tables below, not as a full quote: the table of section 2, and the
breakdown by process only where section 4 needs it.

Only LINKIN's tools give LINKIN's figures. Never estimate LINKIN's price, never adjust it, and
never work it out from rates: to see another quantity or finish, price it.

## 2. The same basis

| Basis | LINKIN's figure |
|---|---|
| Theoretical weight | `weights.net`: the kg per metre × the cut length in metres × the pieces ordered |
| Per kg | the net value ÷ `weights.net` |
| Per tonne | the price per kg × 1,000 |
| Per piece | `netPrice` |
| Per metre | the net value ÷ (the cut length in metres × the pieces) |

- Give the kg per metre too, from `find_profiles`' `weightPerMetre` (a new profile's, the
  drawing's `ZA_KG_PER_M_EST`), so the buyer can check the weight.
- Answer in the unit the buyer used: per kg, or per tonne.
- For several lines, divide the sum of the net values by the sum of the weights. Leave out a line
  that isn't `ok`, and say which.

## 3. The other offer on the same weight

1. Apply the other offer's rate to LINKIN's theoretical weight: their EUR/kg × `weights.net`, or
   their EUR/t × `weights.net` ÷ 1,000. Show it beside LINKIN's net value.
2. Then a short what-if, in case that offer is invoiced on the weight shipped and the weight runs
   above nominal. Show the same rate on the weight plus 5% and plus 10%, labelled as an
   illustration of die wear, not as what that supplier invoices. Change only their figure, never
   LINKIN's. Where the buyer has their own figure from past deliveries, use it instead.
3. **For a powder-coated line only,** the what-if instead starts from the coating's weight, in case
   that offer is invoiced on the finished, coated weight: the same rate on the weight plus 5%,
   labelled as an illustration of the coating's weight. Die wear's 5% and 10% then come on top of
   it, plus 10% and plus 15% in all, since a coated bar weighed at delivery carries both. Label each
   row, say none is what that supplier invoices, and change only their figure, never LINKIN's. Where
   the buyer says their offer is billed on the bare weight, leave the coating out and show step 2's
   rows; where they have their own figure from past deliveries, use it instead of these rows. A bare
   or anodized line has no coating row.
4. Where the other offer is invoiced on theoretical weight too, the figures compare directly:
   leave the what-ifs out and say so.

## 4. The same scope

Check that both offers cover the same things, and name whatever the other offer leaves out or adds:
- the metal basis: whether the metal is included, and on which LME and billet premium;
- finishing, cutting, protective film and packaging;
- for a powder-coated line, whether the other offer's kilos are the bare weight or the finished,
  coated weight;
- minimums per order (press run, die wear, powder colour, anodizing), which LINKIN's breakdown
  shows and which fall as the quantity grows;
- die costs, for a new die;
- the delivery terms: LINKIN's are in the result's `incoterms`, such as EXW Plovdiv.

Where the scope differs, compare only the matching processes from LINKIN's breakdown, and say
which. Where the buyer hasn't said what the other offer covers, assume nothing: ask at most one
question, on the point that matters most here, and name the others as what to check.

## 5. How extrusions are billed

Once in the conversation, in a few neutral sentences:
- **Per kilo**, common in the market: the buyer pays for the weight shipped. As an extrusion die
  wears, its opening widens and the walls come out thicker, still within the standard's
  tolerances, so each metre weighs more. Across a die's life this can reach up to about 10% more
  metal per metre than nominal, more on thin walls and less on thick ones. Billed per kilo, that
  metal is on the buyer's invoice.
- **Per kilo on the finished weight**, for a powder-coated profile: the coat has a weight of its
  own. Billed per kilo on the coated weight, the coating's kilos are invoiced at the price per kilo,
  on top of the coating charge already in the price. For a typical coat of about 80 µm that is about
  5% more weight, less on heavy sections and more on light profiles with a large surface.
- **Per piece**, LINKIN's way: each piece is priced on the aluminium's theoretical weight, so
  what a delivery weighs doesn't change the invoice. Die wear is a line of its own in LINKIN's
  price, billed by the metre, never as extra kilos; on a powder-coated line, so is the coating, by
  the bars hung and the m² coated.

Close with one neutral sentence on the two ways of billing in general, such as "a per-piece price
on theoretical weight and a per-kg price on shipped weight don't compare one to one", and say that
other quantities or finishes can be priced. Don't say which weight the other offer is billed on
unless the buyer has said which. Don't push.

If the buyer wants only the number, give it with one line: a per-piece price on theoretical
weight and a per-kg price on shipped weight don't compare one to one. Offer the rest.

If they doubt the 10%: it is LINKIN's figure, from its own delivery records, and a general range
across a die's life, not a figure about any supplier. The profile standards (EN 755-9, and
EN 12020-2 for 6060 and 6063) limit the wall thickness, not the weight, and ±0.15 mm on a 1.5 mm
wall is ±10% of that wall. The buyer can check their own deliveries: the kilos invoiced against
the drawing's kg per metre times the metres delivered.

If they doubt the 5%: it follows from published figures, and it is not a figure about any
supplier. QUALICOAT asks at least 60 µm of powder for its classes 1 and 2 on architectural
aluminium, and powder makers give about 70 to 80 µm as the thickness applied. By the powder's
density, 80 µm weighs about 0.1 to 0.15 kg per m² coated, about 4 to 5% of a typical profile's
weight: less on heavy sections, more on light profiles with a large surface. The buyer can check
their own deliveries: a coated profile's kilos invoiced against its bare kg per metre times the
metres delivered show the coating and any extra metal together.

## Keep to

- Describe how the billing models work, never what a supplier does or intends. Never name or
  disparage another supplier, even when the buyer names one, and use only the figures the buyer
  gives. Comparative claims must be factual and verifiable: Directive 2006/114/EC, Art. 4, and
  Bulgaria's Protection of Competition Act, Art. 32.
- The "up to about 10%" is a general range for die wear across a die's life, and the "about 5%"
  a typical coat's weight, from the coat thickness applied and the powder's density. Never present
  either as a fact about the buyer's current supplier, or as what their invoice will show.
- The coating's weight is for a powder-coated line only: a bare or anodized line says nothing of
  it, in the what-ifs or in section 5.
- In plain words: no sales area's number, carrier or pack code, field name or hash unless the
  buyer asks for it.
- A comparison issues nothing. Issue a quotation only on the buyer's yes, as quoting-profiles
  says.
