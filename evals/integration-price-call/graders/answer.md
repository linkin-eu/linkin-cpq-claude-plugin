---
type: llm
---

PASS if the reply names the operation that prices an order, `POST /customer/v1/order` (`evaluate_order`), and says from LINKIN's document what its request sends: the sales organization, the distribution channel and the items, with what each item carries. It gives no address, credential or way to sign in, and leaves access to the customer's LINKIN sales representative if it mentions access at all.
FAIL if it gives another path as the call that prices an order, invents a field or a path that LINKIN's document doesn't hold, gives an address or host for the API, a credential, a sign-in header or a way to sign in, or says the document must be asked for from the sales representative.
