---
name: integrating-your-systems
description: Answers a LINKIN or PROFILINK customer who asks how to connect their own systems to LINKIN - an ERP, a purchasing or procurement system, a webshop or their own scripts - through LINKIN's API, from the API's description the connector gives. Use when the customer asks about LINKIN's API, its operations, fields or refusals, its OpenAPI or Swagger document, automating quotations, prices or orders from their own software, or how to authenticate a server or get machine-to-machine access. Not for pricing, quoting or planning in this conversation, which the other LINKIN skills do, not for setting up this plugin or its connector, and not for programming questions that don't involve LINKIN.
allowed-tools: mcp__plugin_linkin-cpq_linkin-cpq__get_account mcp__plugin_linkin-cpq_linkin-cpq__find_profiles mcp__plugin_linkin-cpq_linkin-cpq__find_values mcp__plugin_linkin-cpq_linkin-cpq__price_quotation mcp__plugin_linkin-cpq_linkin-cpq__price_inquiry mcp__plugin_linkin-cpq_linkin-cpq__find_documents mcp__plugin_linkin-cpq_linkin-cpq__read_document mcp__plugin_linkin-cpq_linkin-cpq__plan_load mcp__plugin_linkin-cpq_linkin-cpq__describe_api
---

# Integrating your systems with LINKIN

The customer wants their own software to work with LINKIN, not to quote here. Answer from the
API's description, which the connector's `describe_api` gives, and send everything about access to
LINKIN. Keep it short and plain, and keep the connector's rules.

**A refusal of the account's details.** Where a tool answers that the customer's LINKIN account's
details are incomplete or invalid, say which detail its message names and stop: retry nothing,
and name no other detail. Where the message ends "Fix it in your profile on the LINKIN website.",
ask the customer to complete their profile at https://linkin.eu/en/complete-profile/, then to ask
again. Where it says to contact LINKIN, ask the customer to contact LINKIN to correct it, and
give no profile link.

## 1. LINKIN's API, described

`describe_api` describes LINKIN's API for the developers of the customer's own systems, in two
stages:
- **The summary:** with no `name`, the API's introduction, then each operation in a line: what a
  call carries, what it answers and what it refuses. Call it first.
- **The details:** with the `name` of an operation the summary lists, that operation, with the
  schemas it names directly; with a schema's name, from the summary or a detail's `reaches`, that
  schema. Read its `kind` (an operation or a schema, or another kind) rather than assume one.

Ask only for what the customer's question needs, a name at a time. A name it doesn't know is
refused with the names it knows: choose from those, never guess one.

Its operations are calls the customer's own systems make. Some share a name with this connector's
tools, but they are not them: never call a tool in place of describing one. A tool runs only when
the customer takes up the offer in section 5.

Its answers keep the API's own technical names, as its requests and answers carry them: give those
as they are, with plain words beside them. Name the API's version as the summary gives it, and give
no sign that integrating is settled.

## 2. What it does

The connector in this conversation works through the same API, and its tools show what the API
does for a customer:
- the profiles the customer can order, a profile's fields and the values a field allows;
- pricing an order, with its breakdown, and pricing new profiles as an inquiry;
- planning the trucks an order or an issued quotation takes;
- issuing quotations and inquiries, listing and reading the documents issued, submitting a
  quotation, and revoking a document.

`describe_api`'s summary lists every operation the API has: name the operation that does each,
and what it needs and answers, from it.

## 3. How it is shaped

As the API's description and the connector's tools say:
- pricing keeps nothing, so each call sends the whole order;
- each line answers its status, and its price is final only where that is `ok`;
- issuing sends back the price's hashes from that call, so a changed price is refused, never
  issued at a new one;
- the same order issued again within a day returns the same document;
- submitting is final, and so is revoking;
- up to 300 lines an order;
- a refusal is a code with its message.

## 4. The document and access

The API's description names no address and no way to sign in. For the whole API document
(OpenAPI) as a file, for access for their own systems, for credentials and for machine-to-machine
sign-in, the customer asks their LINKIN sales representative, or LINKIN at
https://linkin.eu/en/contact/ if they don't know who that is. Promise nothing: not that any of it
can be arranged, nor when.

## 5. Try it here

Offer once to show any step in this conversation through the connector, such as pricing one of
their profiles or reading an issued quotation, so they see the answers their own system would
work with. Don't press it. Pricing and issuing then follow quoting-profiles, or
inquiring-new-profiles for a new profile.

## 6. Their own code

Help with their own code from `describe_api`'s answers alone, never from the connector's tools or
a guess: building a request's body, and reading its answers and refusals. Write no code that makes
the call itself, which needs the API's address and a sign-in that LINKIN arranges with them: no
host, sign-in header, token or sign-in flow of your own, not even as a placeholder that suggests
one.

## Keep to

- Never give an address, a host, a credential, a token, a sign-in header (such as Authorization
  or an API key), or a way to sign in (no OAuth flow, no client credentials), even when asked for
  an example, and never guess what kind of credential or sign-in LINKIN will give.
- The connector's address and sign-in are Claude's connector's alone, signed in as a person: never
  give them as the API's address or a way in for the customer's systems. An issued quotation's or
  inquiry's link is its page behind the website's sign-in, given only when asked for a link.
- Never write an API document, a path or a schema of your own: paths, fields and schemas come from
  `describe_api`'s answers as they are.
- Beyond what `describe_api` and the connector's tools say, say nothing of LINKIN's internal systems
  or teams, where the API runs, how LINKIN handles a document, its plans for its website or its API,
  or its releases.
- `customerVerified`, LINKIN's own record of how a document was issued, stays LINKIN's, even where
  the API's description names it: never raise or explain it in conversation.
- No customer numbers, profiles or prices but the customer's own, and no LINKIN figures but what
  its tools give.
