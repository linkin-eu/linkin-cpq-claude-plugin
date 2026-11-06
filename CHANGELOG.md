# Changelog

The notable changes to the LINKIN CPQ plugin for Claude. Versions follow
[Semantic Versioning](https://semver.org/).

## 4.0.0

One plugin replaces the earlier LINKIN CPQ plugins, 3.0.0 from `linkin-claude` and 2.0.0 from
`claude-skills`, for Claude Desktop, claude.ai, Cowork and Claude Code.

### Added

- Two skills take over the connector's five prompts. `quoting-profiles` quotes a request, orders
  again, explains an issued price and compares a per-kg offer. `inquiring-new-profiles` prices an
  inquiry from a drawing.
- Price per kg in every price table.
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
