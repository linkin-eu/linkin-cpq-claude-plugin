---
name: integrating-your-systems
description: Answers a LINKIN or PROFILINK customer who asks how to connect their own systems to LINKIN - an ERP, a purchasing or procurement system, a webshop or their own scripts - through LINKIN's API, from LINKIN's API document (OpenAPI), which it carries. Use when the customer asks about LINKIN's API, its OpenAPI or Swagger document, an API call's fields or refusals, automating quotations, prices or orders from their own software, or how to authenticate a server or get machine-to-machine access. Not for pricing, quoting or planning in this conversation, which the other LINKIN skills do, not for setting up this plugin or its connector, and not for programming questions that don't involve LINKIN.
---

# Integrating your systems with LINKIN

The customer wants their own software to work with LINKIN, not to quote here. Answer from LINKIN's
API document, which this skill carries, and send everything about access to LINKIN. Keep it short
and plain, and keep the connector's rules.

## 1. LINKIN's API document

This skill's `reference/` folder holds LINKIN's API document for customers, as LINKIN builds it:
- `overview.md`: each operation in a line, what it needs, answers and refuses. Read it first.
- `openapi.json`: the whole document (OpenAPI), about 380 KB. Search it for what an answer needs,
  by an operation's `operationId` or a schema's name, and read only that part: never read it
  whole.
- `stamp.json`: which build of the document it is; its `infoVersion` is the document's version.

When the customer asks about integrating, say this plugin carries LINKIN's API document, and that
access goes through LINKIN (section 4).

Asked for the document, give `openapi.json` as it is, as a file, never by writing its text out:
- where the customer can open this plugin's files, as in Claude Code, give its path;
- where they can't, as in claude.ai or Claude Desktop, copy the file with a file copy into the
  folder for files you give the user, unchanged;
- where you can do neither, say so, and that they can ask their LINKIN sales representative for it.

Never edit, shorten or rewrite it. Name its version as the stamp gives it, give no sign that it is
final or that integrating is settled, and say that access, credentials and sign-in go through
LINKIN (section 4).

## 2. What it does

The connector in this conversation works through the same API, and its tools show what the API
does for a customer:
- the customers and sales areas a sign-in orders for;
- the profiles the customer can order, a profile's fields and the values a field allows;
- pricing an order, with its breakdown, and pricing new profiles as an inquiry;
- planning the trucks an order or an issued quotation takes;
- issuing quotations and inquiries, listing and reading the documents issued, submitting a
  quotation, and revoking a document.

Which operation does each, where the document has one, and what it needs and answers, is the
document's to say: name them from it.

## 3. How it is shaped

As the document and the connector's tools say:
- pricing keeps nothing, so each call sends the whole order;
- each line answers its status, and its price is final only where that is `ok`;
- issuing sends back the price's hashes from that call, so a changed price is refused, never
  issued at a new one;
- the same order issued again within a day returns the same document;
- submitting is final, and so is revoking;
- up to 300 lines an order;
- a refusal is a code with its message.

## 4. Access

The document names no address and no sign-in. For access for their own systems, for credentials
and for machine-to-machine sign-in, the customer asks their LINKIN sales representative, or LINKIN
at https://linkin.eu/en/contact/ if they don't know who that is. Promise nothing: not that access
can be arranged, nor when.

## 5. Try it here

Offer once to show any step in this conversation through the connector, such as pricing one of
their profiles or reading an issued quotation, so they see the answers their own system would
work with. Don't press it. Pricing and issuing then follow quoting-profiles, or
inquiring-new-profiles for a new profile.

## 6. Their own code

Help with their own code from the document alone: its operations, fields and refusals, never from
the connector's tools or a guess. Leave the API's address and the sign-in to what LINKIN arranges
with them: no host, sign-in header, token or sign-in flow of your own, not even as a placeholder
that suggests one.

## Keep to

- Never give an address, a host, a credential, a token, a sign-in header (such as Authorization
  or an API key), or a way to sign in (no OAuth flow, no client credentials), even when asked for
  an example, and never guess what kind of credential or sign-in LINKIN will give.
- The connector's address and sign-in are Claude's connector's alone, signed in as a person: never
  give them as the API's address or a way in for the customer's systems. An issued quotation's or
  inquiry's link is its page behind the website's sign-in, given only when asked for a link.
- Never write an API document, a path or a schema of your own: paths, fields and schemas come from
  LINKIN's document as it is.
- Beyond what LINKIN's API document and tools say, say nothing of LINKIN's internal systems or
  teams, its staff tools, where the API runs, how LINKIN handles a document, its plans for its
  website or its API, or its releases.
- The document describes every field an answer carries. `customerVerified`, LINKIN's internal flag
  on an issued document, stays LINKIN's even so: never raise or explain it in conversation.
- No customer numbers, profiles or prices but the customer's own, and no LINKIN figures but what
  its document and tools give.
