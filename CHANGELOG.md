# Changelog

The notable changes to the LINKIN CPQ plugin for Claude. Versions follow
[Semantic Versioning](https://semver.org/).

## Unreleased

### Added

- `integrating-your-systems`: asked how to connect an ERP, a purchasing system, a webshop or your
  own software to LINKIN, Claude answers from the description of LINKIN's API that the connector
  gives: a summary of every operation, then the operation or schema you ask about, in the API's
  own names. For the whole API document, access, credentials and machine-to-machine sign-in it
  sends you to your LINKIN sales representative, promising neither that they can be arranged nor
  when. It gives no address, credential or sign-in recipe, and writes no document of its own.
- Revoking: ask Claude to revoke or withdraw a draft quotation or an open inquiry. It asks why,
  from LINKIN's reasons, revokes it and says it is final. Claude never submits a revoked
  quotation.
- `planning-truck-loads`: how many trucks an order or a quotation takes, how much of each truck it
  takes, and what-ifs: which quantities clear a minimum charge, each priced and planned, compared
  side by side.
  - The plan estimates how much of an order fits standard trucks, to size the order: it is not a
    loading plan, and is never volunteered on a plain quote.
  - Claude leads with the plan's own sentences: the trucks, why so many where there are more than
    one, what one truck fewer would at least need (a floor, never advice to cut the order), and
    each truck's gross weight against its payload and its share of its space.
  - A plan covers everything given or nothing. Claude says what can't be loaded and why; where
    LINKIN's packing data is missing, it says so and to contact your sales representative at
    LINKIN. It plans the rest only when you ask, or when an inquiry or a revoked quotation can only
    be left out, and says what it leaves out.
  - For a line or a quantity the planner didn't plan, Claude works out no trucks, crates or fit of
    its own; a quantity asked about is priced and planned.
  - A quotation can be planned in part, by its items.
  - Each truck's net and gross weight is given, the crates' empty weight LINKIN's approximation.
  - Asked where an article is, Claude names every crate and truck holding it, and says where a
    crate is shared with other articles, of any length; asked why a crate isn't a smaller one,
    it answers from the plan's own figures.
  - Asked how much more of an article would fit, it plans with that article named and gives the
    plan's own sentence: a number of packs a plan still takes on as many trucks, never the most
    that fits, nor a price.
  - The plan is given in words, and Claude draws none. Where the host shows the plan in its own
    view, Claude says nothing of the view.

### Changed

- The privacy notice, version 3, says more exactly what LINKIN receives: the numbers of the
  documents you name, your own names for profiles and lines, the reason and any note you give when
  you revoke a document, and the names of the API's operations or schemas you ask Claude to
  describe. An account not yet linked to a customer has its registered details put on its inquiries.
  The sales desk receives each inquiry issued and each inquiry revoked, besides each quotation
  submitted. Revoking, planning truck loads and describing LINKIN's API are among the purposes, and
  a revocation is kept with its reason and note. The README's privacy summary lists what the notice
  lists.
- An account not yet linked to a customer number issues inquiries in the company and contact
  details registered on linkin.eu: Claude no longer asks for them, and doesn't call the inquiry
  unverified.
- The connector's thirteen tools, with `revoke_document`, `plan_load` and `describe_api`.
  `plan_load` and `describe_api` only read.
- Plain words: the skills say "field" for an inquiry's values, and name a sales area once as the
  LINKIN name and channel a customer buys under.
- `comparing-per-kilo-prices`, for a coated profile: billed per kilo on the finished, coated
  weight, the coat's own weight is invoiced at the price per kilo, about 5% more weight for a
  typical coat. Claude explains it neutrally, asks which weight the other offer's kilos are, and
  shows it as a labelled what-if, with die wear's on top. A bare profile says nothing of it.

### Fixed

- After issuing, Claude gives the number and where the document stands, and opens, saves, links or
  offers no page unless you ask. Asked, it opens the page as issued.
- Before ordering again or explaining a document, Claude takes where it stands from the list of
  documents: one revoked, it says so, with the day and the reason, and reads it no further; to order
  again, it asks which document to use.
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
- A plan refused names the first ten lines or items that can't be planned, each as you named it
  and with its mend, and says how many more, as the connector now gives them. Claude says and
  guesses nothing of what is wrong with those more, which may differ, until these are mended.
- Claude works out no pieces from a count of packs, nor a rounding from one, since a pack may be
  part-filled: the pieces are those the price or the plan gives.

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
