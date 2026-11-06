# Comparing a per-kg offer

Many extruders quote and invoice per kg, so buyers ask what LINKIN's price comes to per kg or per
tonne, or how it compares with another supplier's per-kg offer. Give the figures first, then the
explanation.

## 1. LINKIN's price

`find_profiles` to match the profile. Ask for the length, finish and pieces the offer leaves out.
Price it with `price_quotation`, `view: detail` on its line, or with `price_inquiry` for a drawn
profile with no die yet. Only an `ok` line has a price.

## 2. LINKIN's price per kg

- The line's net value over its net weight, `weights.net`. That is the theoretical weight: the
  kg per metre × the cut length in metres × the pieces ordered (`quantity.order`). Times 1,000
  for a price per tonne.
- Give the kg per metre too, from `find_profiles`' `weightPerMetre`, so the buyer can check it.
- For several lines: the sum of their net values over the sum of their weights, leaving out the
  lines not priced, and say which.
- Never estimate a weight. On an inquiry the weight is the drawing's estimate and the offer is
  preliminary: say both.

## 3. Like for like

LINKIN's figure covers metal, extrusion, finishing and set-up. Where the other offer covers less
(mill finish, or conversion without the metal), compare only the matching processes from the
breakdown, and say which. On a small order LINKIN's figure carries its minimums (press run,
metal, die wear): say so, and that it falls as the quantity grows.

## 4. Their offer on this profile

Their price per kg × LINKIN's theoretical weight, beside LINKIN's matching figure. Where they
invoice on weighed weight, or the buyer doesn't know, show it again with the extra metal added:
the buyer's own figure from past deliveries if they have one, otherwise around 10%, LINKIN's
figure. Adjust only their figure, never LINKIN's. Present it as a what-if ("with around 10% extra
metal, LINKIN's figure, …"), not as what that supplier will invoice or which offer will turn out
cheaper.

## 5. Why it isn't one to one

Once in the conversation, in a few sentences:
- LINKIN's price is built from per-kg rates on the theoretical weight and fixed per piece when
  quoted. What a delivery actually weighs doesn't change the invoice.
- As an extrusion die wears, its bearings wear and the opening widens: the walls come out thicker
  and the profile heavier per metre, the more so the longer a die runs before it is replaced.
- Invoiced per kg on weighed weight, that extra metal is billed to the buyer. Per piece, it is
  LINKIN's cost: die wear is a known charge per metre in LINKIN's price.
- LINKIN's delivery records, and what customers who moved from per-kg suppliers report, put the
  extra metal at around 10%, more on thin walls, less on thick ones. On an offer invoiced on
  theoretical weight none of this applies, and the figures compare directly.

If the buyer wants the number only, give it with one line: a per-piece price on theoretical
weight doesn't compare one to one with a per-kg price invoiced on weighed weight. Offer the rest.

If they doubt the 10%: it comes from LINKIN's delivery records and from customers who switched
from per-kg suppliers. The profile standards (EN 755-9, and EN 12020-2 for 6060 and 6063) limit
wall thickness, not weight, and ±0.15 mm on a 1.5 mm wall is ±10% of that wall. The buyer can
check their own deliveries: the kilos invoiced against the drawing's kg/m times the metres
delivered.

## Keep to

Describe how the two billing models work, never what a supplier does or intends. Don't name a
supplier yourself, and use only the figures the buyer gives. Comparative advertising rules
(Directive 2006/114/EC Art. 4, and Bulgaria's Protection of Competition Act Art. 32) are why.
