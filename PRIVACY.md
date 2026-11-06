# Privacy notice: LINKIN CPQ plugin for Claude

*Version 1, 6 November 2026.*

This notice explains how LINKIN processes personal data when you use the LINKIN CPQ plugin for
Claude and the LINKIN CPQ connector it uses, `https://mcp.linkin.eu/mcp`. It adds to
[LINKIN's privacy policy](https://linkin.eu/en/privacy-policy/), which covers your LINKIN account
and everything else LINKIN does. Where this notice says nothing, that policy applies.

## Who is responsible

LINKIN Ltd. (ЛИНКИН ООД), UIC 115840214, 55 Nestor Abadjiev str., Plovdiv, Bulgaria, is the
controller of the personal data LINKIN's services receive through the connector. Contact:
marketing@linkin.eu.

## The plugin

The plugin holds instructions for Claude (its skills), the connector's address and sign-in
settings, and an icon. It contains no code. It collects nothing and sends nothing itself.

## Signing in

You sign in to the connector with your LINKIN account, through LINKIN's sign-in page (Amazon
Cognito, in the eu-central-1 region of Amazon Web Services). Claude stores the tokens the sign-in
issues and uses them to call the connector for you. LINKIN receives your account's identifier and
the customers your account may act for. LINKIN links your account to those customers in its own
customer records.

## What reaches LINKIN

Only the requests Claude makes through the connector, which are the inputs to its tools: the
profiles, quantities, finishes, lengths and references you ask Claude to price, issue or look up,
the figures from a drawing, and the customer you choose. LINKIN does not receive your
conversation with Claude, your files or your other chats.

## What LINKIN keeps, and for how long

| Record | Kept |
|---|---|
| Each quotation and inquiry issued, with the account that issued it and the time | As long as LINKIN's privacy policy keeps contract records |
| A sandbox account's sample documents | Erased after 30 days |
| A submitted quotation | As above. It is also emailed to LINKIN's sales desk and kept in the sales desk's mailbox |
| Records that stop a repeated request from issuing a second document | One day |
| The connector's log: for each request, your account's identifier, the Claude app, the tool's name, the result and how long it took | 30 days |
| The pricing service's logs: each request's route, status and timing, a correlation id and the ids of documents issued | 90 days |
| The customer registry's logs, and request traces without their contents | 30 days |
| Your LINKIN account | As LINKIN's privacy policy says: 1 year after the account is deactivated |

So LINKIN logs which account called which tool, when, with what result and how long it took. A
request's contents reach only the documents issued, and the ids of those documents in the
pricing service's logs. The logs above keep no request's contents, email address, IP address or
sign-in token.

## Why, and on what legal basis

- **Pricing, issuing, submitting and reading documents at your request**, including emailing a
  submitted quotation to LINKIN's sales desk. Where you are LINKIN's customer yourself, as a sole
  trader, the basis is performance of a contract with you, or steps you ask for before entering
  into one (GDPR Art. 6(1)(b)). Where you act for a company or another organisation, it is
  LINKIN's legitimate interest in serving its customers through the people who act for them
  (GDPR Art. 6(1)(f)).
- **Keeping issued documents:** a legal obligation, where tax or accounting law requires LINKIN
  to keep them (GDPR Art. 6(1)(c)), and LINKIN's legitimate interest in establishing, exercising
  or defending legal claims (GDPR Art. 6(1)(f)).
- **Service logs**, for security, preventing misuse and troubleshooting: LINKIN's legitimate
  interests (GDPR Art. 6(1)(f)).

You need a LINKIN account, linked to the customer you act for, to use the connector. Without one,
Claude can't price or issue anything through it. The connector prices what you ask; it makes no
decision about you that is based solely on automated processing and has legal or similarly
significant effects on you.

## Who else processes it

LINKIN's service providers process the data on LINKIN's behalf, under data processing terms:

- **Amazon Web Services** hosts the connector and LINKIN's services in its eu-central-1 region
  (Frankfurt, Germany), runs the sign-in (Amazon Cognito), and sends email (Amazon Simple Email
  Service) from the same region.
- **Google** hosts LINKIN's mailboxes, including the sales desk's, on Google Workspace.

Amazon Web Services keeps the data in the European Union. Google may process mailbox data in the
United States. That transfer relies on the European Commission's adequacy decision for the
EU–U.S. Data Privacy Framework, under which Google LLC is certified, and on the Commission's
standard contractual clauses in Google's data processing terms. Ask marketing@linkin.eu for a
copy of these safeguards.

## Claude

Anthropic processes your conversations with Claude under the terms you or your organisation
agreed with Anthropic. Anthropic is not LINKIN's processor, LINKIN is not a party to those terms,
and LINKIN receives only the requests described above.

## Your rights

You may ask LINKIN for access to your personal data, and to correct or erase it, to restrict its
processing, or to receive it in a portable form. Write to marketing@linkin.eu, or as LINKIN's
privacy policy says.

**Your right to object.** Where LINKIN relies on its legitimate interests (GDPR Art. 6(1)(f)),
you may object at any time, on grounds relating to your particular situation. LINKIN then stops,
unless it shows compelling legitimate grounds that override your interests, or needs the data to
establish, exercise or defend legal claims.

You may also complain to Bulgaria's Commission for Personal Data Protection (CPDP,
https://www.cpdp.bg), or to the data protection authority where you live, work or where the
infringement took place.

## Changes

LINKIN publishes a new version of this notice when the plugin or the connector changes how
personal data is processed. Each version is dated and numbered at its top.
