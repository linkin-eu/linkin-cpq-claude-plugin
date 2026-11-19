# Changelog

The notable changes to the LINKIN CPQ plugin for Claude. Versions follow
[Semantic Versioning](https://semver.org/).

## Unreleased

### Changed

- The README says when Claude asks before it issues, submits or revokes. In Claude Desktop and
  claude.ai, **Needs approval** asks each time only in **Manual** mode, and **Always ask**, where
  Claude offers it, is built to ask in every mode
  ([Get started](README.md#claude-desktop-or-claudeai), step 5). In Claude Code, add the four
  tools that issue, submit or revoke to `permissions.ask`, so that no mode runs them without
  asking you ([Claude Code](README.md#claude-code)).
- A per-kg or per-tonne comparison no longer gives a full quote first. Claude prices it within
  the comparison, shows LINKIN's figures in the comparison's tables, and asks at most one question
  about what the other offer covers.
- When quoting, pricing a new profile or planning trucks, Claude names things in plain words:
  LINKIN's sales area by its name, a crate by its kind, a figure by what it means, with no
  internal code unless you ask for one. For a new profile, it says in one sentence which die
  figures LINKIN's plant set because your drawing didn't give them, and that your own figures
  would replace them.
- A quote for a profile you already order gives each process as one total (metal, extrusion,
  finishing), as the README's example shows. Ask how the price was made for each charge's rate
  and basis.
- When Claude issues a quotation, it says it stands as a draft that you submit, when you ask,
  for LINKIN to release, and that a submission is final: you can neither change nor withdraw it.
  An issued inquiry stands open, a preliminary offer subject to LINKIN's technical review of each
  profile. When or how LINKIN answers is LINKIN's to say: if you ask, Claude points you to LINKIN.
- The README's setup follows Anthropic's help pages. On a Team plan, Code execution and Skills
  are on unless an Owner turned them off. An organization's own marketplace doesn't sync on a
  schedule, and a LINKIN release doesn't sync it: an Owner syncs it again after each release. In
  Claude Code, the one-step install needs version 2.1.292 or later, a plugin from Claude Desktop
  comes across when you sign in to Claude Code 2.1.273 or later with the same claude.ai account,
  and automatic updates are off until you turn them on.
- The README's example for a new profile also gives its name, perimeter, finish, protective film
  and your RFQ reference, and the README says a new die carries a refundable deposit, shown with
  the price but not included in it.
- The licence now says a quotation is a draft until you submit it, for LINKIN to release
  ([LICENSE](LICENSE), section 5). It said a quotation was a draft until LINKIN released it,
  which skipped your own step.
- Where LINKIN refuses because your account's profile lacks a detail, Claude still names that
  detail and sends you to complete your profile on LINKIN's website, now also when LINKIN's
  message gives the profile page's link itself. Where the message says to contact LINKIN, Claude
  still sends you to LINKIN, with no profile link.

## 5.0.3

### Changed

- In Claude Code, the tools that only read run without asking in the turn that starts a LINKIN
  skill. The tools that issue, submit or revoke still ask. To never be asked for a read, add the
  nine read-only tools to your settings ([Claude Code](README.md#claude-code)).

### Fixed

- Claude Desktop's marketplace panel no longer warns about keys in the plugin's manifest it
  doesn't recognize.

## 5.0.2

### Fixed

- Signing in from Claude Code works again. The sign-in comes back to port 47819 on your computer,
  so keep that port free. 5.0.0 said signing in no longer needed that port, which wasn't so.

## 5.0.1

### Changed

- The plugin connects at LINKIN's new address, `https://cpq.mcp.linkin.eu/mcp`. If Claude says
  after the update that the LINKIN CPQ connector isn't connected, connect it again and sign in; in
  Claude Code, run `/mcp` and sign in again. A LINKIN connector you added yourself at the old
  address keeps working ([Updating](README.md#updating)).
- The privacy notice, version 4, names the connector's new address and its earlier one.

### Fixed

- When LINKIN refuses a request because your account's profile is missing a detail, Claude sends
  you to complete it at <https://linkin.eu/en/complete-profile/>, or, for an account linked to a
  customer number, to LINKIN to correct it. It doesn't retry.

## 5.0.0

A major version: it needs version 2.0 of LINKIN's CPQ connector, which LINKIN runs for you, and
doesn't work with an earlier one.

### Added

- `integrating-your-systems`: ask how to connect your ERP, purchasing system, webshop or own
  software to LINKIN, and Claude answers from the description of LINKIN's API that the connector
  gives, in the API's own names. For the full API document (OpenAPI), and for access and sign-in
  for your own systems, it refers you to your LINKIN sales representative.
- Revoking: ask Claude to revoke or withdraw a draft quotation or an open inquiry. It asks why, from
  LINKIN's reasons, revokes it and says it is final. Claude never submits a revoked quotation.
- `planning-truck-loads`: ask how many trucks an order, a quotation or some of its items take, where
  a profile is in the load, or how much more of it fits. Claude answers in words from LINKIN's own
  estimate, which is for sizing the order, not a loading plan, and never works out a truck count of
  its own. To clear a minimum charge with the load in mind, it prices and plans each quantity and
  compares them. If some lines or items can't be planned, it names the first ten, with what mends
  each, and says how many more there are.
- Updating: the README says how to update the plugin in each Claude app.

### Changed

- You add the plugin from LINKIN's marketplace, and it updates from there. The zip is no longer
  published: if you uploaded it, delete the plugin and add it again from the marketplace.
- In Claude Code, signing in no longer needs port 47819.
- The privacy notice, version 3, says more exactly what LINKIN receives: the numbers of the
  documents you name, your own names for profiles and lines, the reason and any note you give when
  you revoke a document, and the names of the API's operations or schemas you ask Claude to
  describe. An account not yet linked to a customer has its registered details put on its inquiries.
  The sales desk receives each inquiry issued and each inquiry revoked, besides each quotation
  submitted. Revoking, planning truck loads and describing LINKIN's API are among the purposes, and
  a revocation is kept with its reason and note. The README's privacy summary lists what the notice
  lists.
- An account not yet linked to a customer number issues inquiries in the company and contact
  details registered on linkin.eu: Claude no longer asks for them.
- The icon is a navy L on white, and the plugin's description says what each of its skills does.
- Claude names a sales area as LINKIN Bulgaria (1102/10) or PROFILINK (1002/10).
- The connector has three new tools, thirteen in all: **Revoke a document** (`revoke_document`),
  **Plan the trucks** (`plan_load`) and **Describe the API** (`describe_api`). The last two only
  read.
- `comparing-per-kilo-prices`, for a powder-coated profile: where an offer is billed per kilo on
  the coated weight, the coat's own weight is invoiced at the price per kilo, about 5% more weight
  for a typical coat. Claude explains this neutrally, asks whether the other offer's kilos are bare
  or coated, and shows the coat's weight as a labelled what-if, with die wear added on top. For a
  bare or anodized profile, it doesn't mention the coat.

### Fixed

- After issuing, Claude gives the number and where the document stands, and opens, saves, links or
  offers no page unless you ask. Asked, it opens the page as issued.
- Before ordering again or explaining a document, Claude takes where it stands from the list of
  documents: one revoked, it says so, with the day and the reason, and reads it no further; to order
  again, it asks which document to use.
- An explained price gives the document's totals, minimums and pricing date with each line's
  charges.
- Claude no longer picks a sales area for an inquiry, even when your account buys under several:
  LINKIN makes every inquiry under LINKIN Bulgaria (1102/10).
- A per-kilo comparison no longer says LINKIN's price is fixed when quoted: a quotation is a
  draft until LINKIN releases it.
- A per-kilo comparison no longer says which weight the other offer is billed on unless you have
  said which.
- An inquiry's price names the new dies' refundable deposit, outside the total.
- In Claude Code, a connector that isn't connected is connected with `/mcp`, and Claude says so.
- Get started names the tool permissions as Claude shows them: set **Read-only tools** to
  **Always allow**, and under **Interactive tools** set **Read an issued document** and **Plan the
  trucks** to **Always allow** too. Leave the tools that issue, submit or revoke on **Needs
  approval**. In Claude Code, add `plan_load` and `describe_api` to the tools you allow.
- An inquiry's price says which figures the plant's defaults gave, by the weight per metre or the
  plant's references, as the connector prices them, and takes the belt pitch where you give it.
- An inquiry ordered again is priced with the new order's reference.
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
