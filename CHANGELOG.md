# Changelog

The notable changes to the LINKIN CPQ plugin for Claude. Versions follow
[Semantic Versioning](https://semver.org/).

## 4.2.0

### Changed

- To issue an inquiry from an account not yet linked to a customer number, you also give a phone
  number, street and city, and a house number, postal code and phone extension where you have
  them. LINKIN checks that the phone number is a valid one in your country.
- Where Claude shows apps, Claude asks only whether to issue, and you give your details in
  LINKIN's form under its answer. In Claude Code, Claude asks for them with the price. Where
  LINKIN refuses a detail, Claude asks once for what it names.

## 4.1.1

### Changed

- After issuing an inquiry from an account not yet linked to a customer number, Claude no longer
  tells the buyer that it is marked as from an unverified account. The buyer's own view of the
  inquiry no longer shows that mark either; LINKIN still sees it.

### Fixed

- Getting started names the tool permissions as Claude shows them. **Read an issued document** is
  listed under **Interactive tools** and is set to **Always allow** there. The three tools that
  issue or submit keep **Needs approval**.

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
