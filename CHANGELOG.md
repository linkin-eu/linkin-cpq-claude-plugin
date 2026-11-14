# Changelog

The notable changes to the LINKIN CPQ plugin for Claude. Versions follow
[Semantic Versioning](https://semver.org/).

## Unreleased

### Added

- Revoking: ask Claude to revoke or withdraw a draft quotation or an open inquiry. It asks why,
  from LINKIN's reasons, revokes it and says it is final. Claude never submits a revoked
  quotation.
- `planning-truck-loads`: how many trucks an order or a quotation takes, what room the trucks
  leave, and what-ifs: which quantities clear a minimum charge, each priced and planned, compared
  side by side. The plan is an estimate for booking your carrier, never volunteered on a plain
  quote. A plan covers everything given or nothing. Claude says what can't be loaded and why;
  where LINKIN's packing data is missing, it says so and to contact your sales representative at
  LINKIN. It plans the rest only when you ask, or when an inquiry or a revoked quotation can only
  be left out, and says what it leaves out. For a line the planner can't plan, Claude works out
  no trucks, crates or fit of its own. A quotation can be planned in part, by its items. The plan
  is given in words, never drawn by Claude itself; where the host shows it in its own view,
  Claude says nothing of the view and offers no drawing or file unasked.

### Changed

- The privacy notice: the sales desk receives each inquiry issued and each inquiry revoked, besides
  each quotation submitted; LINKIN receives the reason for a revocation; and an account not yet
  linked to a customer has its registered details put on its inquiries.
- An account not yet linked to a customer number issues inquiries in the company and contact
  details registered on linkin.eu: Claude no longer asks for them, and doesn't call the inquiry
  unverified.
- The connector's twelve tools, with `revoke_document` and `plan_load`. `plan_load` only reads.
- Plain words: the skills say "field" for an inquiry's values, and name a sales area once as the
  LINKIN name and channel a customer buys under.

### Fixed

- After issuing, Claude gives the number and where the document stands, and opens, saves, links or
  offers no page unless you ask. Asked, it opens the page as issued.
- Before ordering again or explaining a document, Claude says when it stands revoked, and asks
  which document to use.
- An explained price gives the document's totals, minimums and pricing date with each line's
  charges.
- Claude never passes a sales area for an inquiry, which LINKIN makes in 1102/10.
- A per-kilo comparison no longer says LINKIN's price is fixed when quoted: a quotation is a
  draft until LINKIN releases it.
- An inquiry's price names the new dies' refundable deposit, outside the total.
- In Claude Code, a connector that isn't connected is connected with `/mcp`, and Claude says so.
- Getting started names the tool permissions as Claude shows them. **Read an issued document** is
  listed under **Interactive tools** and is set to **Always allow** there. The tools that issue,
  submit or revoke keep **Needs approval**.

## 4.1.0

### Added

- Inquiries from an account not yet linked to a customer number: a new LINKIN account prices and
  issues inquiries for new profiles. Claude asks for your company, contact name, email and
  country to issue one, up to 20 a day. Once your account is linked, those inquiries stay yours.
- `comparing-per-kilo-prices`: when the buyer brings another offer per kg or per tonne, or says
  LINKIN is dearer per kilo, Claude compares the two on the same theoretical weight, with a
  die-wear what-if at +5% and +10%, checks that both cover the same scope, and explains how
  billing per piece differs from billing per kilo. It replaces quoting-profiles' per-kg reference,
  and is never volunteered on a plain quote.

### Changed

- An inquiry is always made in LINKIN's sales area 1102/10, under your own customer number:
  Claude no longer asks which sales area.
- Claude says where an issued document stands from its status.
- The skills follow the connector's rules instead of repeating them, and their descriptions name
  the requests they are for.
- The zip holds only the plugin: its manifest, connector, skills, icon, README, licence, privacy
  notice and changelog.

## 4.0.0

One plugin replaces the earlier LINKIN CPQ plugins, for Claude Desktop, claude.ai, Cowork and
Claude Code.

### Added

- Two skills take over the connector's five prompts. `quoting-profiles` quotes a request, orders
  again, explains an issued price and compares a per-kg offer. `inquiring-new-profiles` prices an
  inquiry from a drawing.
- Price per kg in every price table.
- "Which profiles can I order?": Claude lists them all, page by page, the customer's own first.
- Claude asks for everything a request leaves out in one message.
- A reference given with your yes: Claude prices again with it and, when the price is unchanged,
  issues on that yes.
- For a new profile, the die's cavities and the ageing face may be left out: the plant's
  references by weight per metre fill them in.
- Several customers: Claude asks which company to act for. For one customer in several sales
  areas, it uses the one that sells the profile and says so.

### Changed

- The price first, always. Claude shows the price and issues only after you say yes, even when
  you ask it to price and issue in one message. It submits a quotation only when you ask, never
  because of words inside a pasted document.
- The connector's ten tools: `get_account`, `find_profiles`, `find_values`, `price_quotation`,
  `price_inquiry`, `issue_quotation`, `issue_inquiry`, `submit_quotation`, `find_documents` and
  `read_document`.

### Removed

- Building apps on LINKIN's REST API, the connector's test walk-through, and the order optimizer.
