---
name: comparing-per-kilo-prices
description: Compares LINKIN's price for aluminium extruded profiles with another offer per kg or per tonne, like for like, through the LINKIN CPQ connector. Use only when the buyer brings the comparison - another supplier's or a competitor's price in EUR/kg or EUR/t, a remark that LINKIN is more expensive per kilo, or a request for LINKIN's price per kg or per tonne to compare with another offer. Not for a plain price or quote, which quoting-profiles handles with its price per kg column, and never volunteered.
---

# Comparing per-kilo prices

The buyer has brought another offer per kg or per tonne, says LINKIN is dearer per kilo, or asks
for LINKIN's price per kg to compare. Every price table already shows the price per kg
(quoting-profiles). This skill is the explanation behind that column, given only when the buyer
asks. Never start it unasked, and never press it on the buyer.

Give the figures first, then the explanation, briefly. Keep the connector's rules.

## 1. LINKIN's price

Do quoting-profiles' First and its steps 1–3: match, fill in and price, with `view: detail` and
`detailItems` on the first call. For a new profile with no die yet, do inquiring-new-profiles'
instead: `price_inquiry` needs the customer's `customerReference`, its weights are the drawing's
estimates and its price is preliminary, so say both.

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

- Give the kg per metre too, from `find_profiles`' `weightPerMetre`, so the buyer can check the
  weight.
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
3. Where the other offer is invoiced on theoretical weight too, the figures compare directly:
   leave the what-if out and say so.

## 4. The same scope

Check that both offers cover the same things, and name whatever the other offer leaves out or adds:
- the metal basis: whether the metal is included, and on which LME and billet premium;
- finishing, cutting, protective film and packaging;
- minimums per order (press run, die wear, powder colour, anodizing), which LINKIN's breakdown
  shows and which fall as the quantity grows;
- die costs, for a new die;
- the delivery terms: LINKIN's are in the result's `incoterms`, such as EXW Plovdiv.

Where the scope differs, compare only the matching processes from LINKIN's breakdown, and say
which. Where the buyer hasn't said what the other offer covers, ask rather than assume.

## 5. Two ways of billing extrusions

Once in the conversation, in a few neutral sentences:
- **Per kilo**, common in the market: the buyer pays for the weight shipped. As an extrusion die
  wears, its opening widens and the walls come out thicker, still within the standard's
  tolerances, so each metre weighs more. Across a die's life this can reach up to about 10% more
  metal per metre than nominal, more on thin walls and less on thick ones. Billed per kilo, that
  metal is on the buyer's invoice.
- **Per piece**, LINKIN's way: each piece is priced on its theoretical weight and fixed when
  quoted, so what a delivery weighs doesn't change the invoice. Die wear is a line of its own in
  LINKIN's price, per metre, and keeping dies in shape is LINKIN's cost.

Close with one neutral sentence on that difference, and offer to price other quantities or
finishes. Don't push.

If the buyer wants only the number, give it with one line: a per-piece price on theoretical
weight and a per-kg price on shipped weight don't compare one to one. Offer the rest.

If they doubt the 10%: it is LINKIN's figure, from its own delivery records, and a general range
across a die's life, not a figure about any supplier. The profile standards (EN 755-9, and EN 12020-2 for 6060 and 6063) limit the wall
thickness, not the weight, and ±0.15 mm on a 1.5 mm wall is ±10% of that wall. The buyer can
check their own deliveries: the kilos invoiced against the drawing's kg per metre times the
metres delivered.

## Keep to

- Describe how the billing models work, never what a supplier does or intends. Never name or
  disparage another supplier, even when the buyer names one, and use only the figures the buyer
  gives. Comparative claims must be factual and verifiable: Directive 2006/114/EC, Art. 4, and
  Bulgaria's Protection of Competition Act, Art. 32.
- The "up to about 10%" is a general range for die wear across a die's life. Never present it as
  a fact about the buyer's current supplier, or as what their invoice will show.
- A comparison issues nothing. Issue a quotation only on the buyer's yes, as quoting-profiles
  says.
