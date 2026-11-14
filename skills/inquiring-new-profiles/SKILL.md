---
name: inquiring-new-profiles
description: Prices and issues an inquiry through the LINKIN CPQ connector for new aluminium extruded profiles a customer has drawn, which have no extrusion die yet. Use when a buyer sends a drawing or the figures of a new profile, asks for a price on a profile whose die doesn't exist yet, sends an RFQ naming profiles they can't order yet, or wants such an inquiry issued, also from a LINKIN account not yet linked to a customer number. Not for profiles the customer can already order, which quoting-profiles quotes.
---

# Inquiring new profiles

An inquiry prices profiles the customer has drawn, which have no die yet, as a preliminary offer
subject to LINKIN's technical review of each profile. A profile `find_profiles` lists is quoted
instead (quoting-profiles).

Keep the connector's rules. Its instructions and tool descriptions hold them and each field's
meaning; this skill holds the workflow.

## First

1. If the LINKIN CPQ connector's tools aren't available, say: "The LINKIN CPQ connector isn't
   connected. Connect it on the LINKIN CPQ plugin's Connectors tab (in Claude Code, `/mcp`), then
   ask again." Then stop.
2. `get_account`.
   - **One customer:** act for it.
   - **Different customers** (different `soldToParty`): ask which one, and never choose. An
     inquiry issued for the wrong company is a real error. Pass the one chosen as `soldToParty`
     to every call.
   - **No linked customer:** the buyer still prices and issues inquiries, as LINKIN's one-time
     customer. Pass no `soldToParty`. The inquiry is addressed to the buyer by their registration
     on the LINKIN website, so never ask for their company or contact details.

   Never ask about the sales area, and pass none: an inquiry is made in LINKIN's 1102/10,
   whichever area the account lists.

## The items

One item per drawn profile: `customerMaterial`, the customer's name or number for it; `quantity`,
the pieces; and `values`, by characteristic name.

| From the drawing | Characteristic |
|---|---|
| The die ID, required: any name for the new die, such as its drawing number. Profiles pressed through one die take the same ID and share its minimums per order | `ZA_DIE_EST` |
| Alloy and temper | `ZA_ALLOY`, `ZA_TEMPER` |
| Cut length, mm | `ZA_LENGTH_MM` |
| Weight per metre, kg/m | `ZA_KG_PER_M_EST` |
| Perimeter, mm | `ZA_PROF_PERI_MM_EST` |
| The die's planned cavities, press speed, life and complexity, if the customer gives them | `ZA_DIE_CAVITIES_EST`, `ZA_EXTR_M_MIN_EST`, `ZA_DIE_LIFE_M_EST`, `ZA_DIE_COMPLEXITY_EST` |
| Ageing face, mm², if the customer gives it | `ZA_AGE_FACE_MM2_EST` |
| Finish: bare, powder coated or anodized | `ZA_SURFACE_FINISH` |
| Powder coated: colour system and number (`find_values` lists the numbers), surface, Qualicoat class, pre-anodized base | `ZA_POWDER_TYPE`, `ZA_POWDER_NUMBER`, `ZA_POWDER_FINISH`, `ZA_POWDER_CLASS`, `ZA_PRE_ANODIZED` |
| Anodized: pretreatment, colour, thickness class | `ZA_ANOD_FINISH`, `ZA_ANOD_COLOR`, `ZA_ANOD_CLASS` |
| Cutting | `ZA_CUTTING` |
| Protective film width per face, mm: exterior, interior, faces 3 and 4, 0 on a bare face | `ZA_PROT_WIDTH_EST`, `_2`, `_3`, `_4` |

## The flow

1. **Take what the drawing gives**, and ask in one message for every figure it doesn't, apart
   from those step 2 lets default, together with the customer's RFQ reference. Never guess a
   figure off a drawing.
2. **Defaults.** The die's cavities, press speed, life and complexity, the ageing face and the
   belt pitch default to the plant's references. Enter one only where the customer gives it.
3. **Price** with `price_inquiry`: `customerReference`, the customer's RFQ reference, and every
   profile so far.
   - `incomplete`: ask for the fields in `missing`.
   - `inconsistent`: say which value a rule refuses, in plain words. Don't retry with a guess,
     and don't quote the refused line's figures.
4. **Present** the price (below), then ask whether to issue it as an inquiry.
5. **Issue on a separate yes.** The customer sees the price first, then says yes. A message that
   asks to "price it and issue it" still gets the price and the question.
   - `issue_inquiry` with the same items, the same `customerReference`, and `expected` holding
     the last pricing's `inputHash` and `priceHash`.
   - Give the number, say where it stands from its `status` (an inquiry stands open, a
     preliminary offer), and offer its summary page (below). With no linked customer,
     say at most that it is addressed by their registration on the LINKIN website. Never say the
     inquiry, the account or the buyer is unverified, and never mention `customerVerified`, a flag,
     mark, warning or note about the account, or what LINKIN's staff see: they are LINKIN's own.
   - `PRICES_CHANGED` or `ORDER_DIFFERS`: price again, show the new price, and ask again.
   - `TOO_MANY_INQUIRIES`: say nothing was issued, why, and what mends it, from its message. Don't
     retry.

## Presenting the price

One table, a row per `ok` line, from the lines' detail (price with `view: detail` and
`detailItems` on the first call, at most 10 lines a call):

| Line | Profile | Pieces | Price per piece | Net value | Price per kg |
|---|---|---|---|---|---|
| `item` | `customerMaterial` and `text` | `quantity.order` | `netPrice` | `netValue` | `netValue` ÷ `weights.net` |

Under it:
- each line's breakdown by process;
- the minimums per die, powder colour and anodizing, and which lines share each;
- the total, its currency and the pricing date;
- the new dies' refundable deposit, from the `NEW_DIE_DEPOSIT` message, outside the total;
- that it is a preliminary offer, subject to LINKIN's technical review of each profile, its
  weights the drawing's estimates;
- which figures are the plant's references.

List a line that isn't `ok` under the table with what it still needs or what was refused, and no
price. An issued document may show beside the answer as its own page. Don't paste the page. Offer
the summary page the result links, not the `url`, which needs the LINKIN website login in a browser.
Where the host shows no document app (Claude Code), give the number and, when asked, open the
summary page, the resource `avc://pages/inquiries/<id>`.

To find an issued inquiry, order it again, explain its price or revoke it, see quoting-profiles.
