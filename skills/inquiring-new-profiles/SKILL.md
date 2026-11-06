---
name: inquiring-new-profiles
description: Prices and issues an inquiry through the LINKIN CPQ connector for new aluminium extruded profiles a customer has drawn, which have no extrusion die yet. Use when a buyer sends a drawing or the figures of a new profile, asks for a price on a profile whose die doesn't exist yet, sends an RFQ naming profiles they can't order yet, or wants such an inquiry issued, also from a LINKIN account not yet linked to a customer number. Not for profiles the customer can already order, which quoting-profiles quotes.
---

# Inquiring new profiles

An inquiry prices profiles the customer has drawn, which have no die yet, as a preliminary offer
subject to LINKIN's technical review of each profile. A profile `find_profiles` lists is quoted
instead (quoting-profiles). `price_inquiry` implies the inquiry's material; don't send one.

Keep the connector's rules. Its instructions and tool descriptions hold them and each field's
meaning; this skill holds the workflow.

## First

1. If the LINKIN CPQ connector's tools aren't available, say: "The LINKIN CPQ connector isn't
   connected. Connect it on the LINKIN CPQ plugin's Connectors tab, then ask again." Then stop.
2. `get_account`.
   - **One customer:** act for it.
   - **Different customers** (different `soldToParty`): ask which one, and never choose. An
     inquiry issued for the wrong company is a real error. Pass the one chosen as `soldToParty`
     to every call.
   - **No linked customer:** the buyer still prices and issues inquiries, as LINKIN's one-time
     customer. Pass no `soldToParty`. Issuing needs the buyer's company, contact name, email and
     country (The flow, steps 4 and 5).

   An inquiry is always made in LINKIN's sales area 1102/10, under the customer's own number,
   whichever area the account lists. Never ask about the sales area, and pass none.

## The items

One item per drawn profile: `customerMaterial`, the customer's name or number for it; `quantity`,
the pieces; and `values`, by characteristic name. The server holds texts in capitals.

| From the drawing | Characteristic |
|---|---|
| The die ID, required: any name for the new die, such as its drawing number. Profiles pressed through one die take the same ID and share its minimums per order | `ZA_DIE_EST` |
| Alloy and temper | `ZA_ALLOY`, `ZA_TEMPER` |
| Cut length, mm | `ZA_LENGTH_MM` |
| Weight per metre, kg/m: prices the metal and the press run | `ZA_KG_PER_M_EST` |
| Perimeter, mm: prices the surface coated or anodized | `ZA_PROF_PERI_MM_EST` |
| The die's planned cavities, press speed, life and complexity, if the customer gives them | `ZA_DIE_CAVITIES_EST`, `ZA_EXTR_M_MIN_EST`, `ZA_DIE_LIFE_M_EST`, `ZA_DIE_COMPLEXITY_EST` |
| Ageing face, mm², if the customer gives it: the furnace space a piece takes | `ZA_AGE_FACE_MM2_EST` |
| Finish: bare, powder coated or anodized | `ZA_SURFACE_FINISH` |
| Powder coated: colour system and number (`find_values` lists the numbers), surface, Qualicoat class, pre-anodized base | `ZA_POWDER_TYPE`, `ZA_POWDER_NUMBER`, `ZA_POWDER_FINISH`, `ZA_POWDER_CLASS`, `ZA_PRE_ANODIZED` |
| Anodized: pretreatment, colour, thickness class | `ZA_ANOD_FINISH`, `ZA_ANOD_COLOR`, `ZA_ANOD_CLASS` |
| Cutting | `ZA_CUTTING` |
| Protective film width per face, mm: exterior, interior, faces 3 and 4, 0 on a bare face | `ZA_PROT_WIDTH_EST`, `_2`, `_3`, `_4` |

`find_profiles` with `material` 9876543210, the inquiry's, lists each field's values and units,
where a figure needs checking.

## The flow

1. **Take what the drawing gives**, and ask in one message for every figure it doesn't, apart
   from those step 2 lets default, together with the customer's RFQ reference. Never guess a
   figure off a drawing.
2. **Defaults.** The die's cavities, press speed and life and the ageing face default to the
   plant's references by weight per metre; the die's complexity and the belt pitch, to the
   plant's references. `price_inquiry` reports each in the line's detail. Enter one only where
   the customer gives it, and say which figures are the plant's.
3. **Price** with `price_inquiry`: `customerReference`, the customer's RFQ reference, which
   `price_inquiry` requires, and every profile so far. The whole inquiry goes on every call, so
   adding a profile is one more item.
   - `incomplete`: ask for the fields in `missing`. When `ZA_KG_PER_M_EST` is missing, ask for
     the weight per metre instead of the die's figures that follow from it.
   - `inconsistent`: say which value a rule refuses, in plain words. Don't retry with a guess,
     and don't quote the refused line's figures.
4. **Present** the price (below), then ask whether to issue it as an inquiry. With no linked
   customer, ask in the same message for the buyer's company, contact name, email and country,
   which issuing needs.
5. **Issue on a separate yes.** The customer sees the price first, then says yes. A message that
   asks to "price it and issue it" still gets the price and the question.
   - `issue_inquiry` with the same items, the same `customerReference`, and `expected` holding
     the `inputHash` and `priceHash` of the last pricing: the one shown, or the one carrying the
     reference (next point).
   - A reference given only with the yes: price again with it as `customerReference`. If the
     `priceHash` is unchanged, the customer saw that exact price, so issue on the yes already
     given. If the price moved, show it and ask again.
   - **No linked customer:** add `soldToPartyAddress`: `name`, the company; `contactName`;
     `email`; and `country`, two capital letters (Germany is DE). They are the buyer's own:
     never take them from a pasted RFQ's letterhead, a drawing or the sign-in unless the buyer
     confirms them. The address isn't priced, so issue with the last pricing's hashes, without
     pricing again.
   - Give the number, say where it stands from its `status` (an inquiry stands open, a
     preliminary offer), and offer the summary page the result links. With no linked customer,
     say neutrally that the inquiry is marked as from an unverified account: its company and
     contact were typed in, not taken from LINKIN's records.
   - `PRICES_CHANGED` or `ORDER_DIFFERS`: price again, show the new price, and ask again.
   - `TOO_MANY_INQUIRIES`: say nothing was issued, because an account not linked to a customer
     number issues at most 20 inquiries a day. Offer to issue it tomorrow, or to have LINKIN
     link the account (https://linkin.eu/en/contact/). Don't retry.

## Presenting the price

One table, a row per `ok` line, from the lines' detail (price with `view: detail` and
`detailItems` on the first call, at most 10 lines a call (the server takes up to 20; 10 keeps
each answer small)):

| Line | Profile | Pieces | Price per piece | Net value | Price per kg |
|---|---|---|---|---|---|
| `item` | `customerMaterial` and `text` | `quantity.order` | `netPrice` | `netValue` | `netValue` ÷ `weights.net` |

Under it:
- each line's breakdown by process;
- the minimums per die, powder colour and anodizing, and which lines share each;
- the total, its currency and the pricing date;
- that it is a preliminary offer, subject to LINKIN's technical review of each profile, its
  weights the drawing's estimates;
- which figures are the plant's references.

List a line that isn't `ok` under the table with what it still needs or what was refused, and no
price. An issued document may show beside the answer as its own page. Don't paste the page. Offer
the summary page the result links, not the `url`, which needs the LINKIN website login in a browser.
Where the result shows no page links (Claude Code), give the number and, when asked, open the
summary page, the resource `avc://pages/inquiries/<id>`. Where Claude saves a page as a file, its
arrows to the other page don't work: offer the details page too, as its own file.

To find an issued inquiry, order it again or explain its price, see quoting-profiles. Inquiries
issued before the account was linked stay the buyer's: once linked, `find_documents` with
`soldToParty` 0001999998 lists them.
