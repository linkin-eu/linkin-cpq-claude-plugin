---
# customerVerified, LINKIN's own record of how a document was issued, stays LINKIN's
# (integrating-your-systems), and so does the API's line that LINKIN hasn't verified a new
# customer's details.
type: regex
pattern: 'customerVerified|unverified|not verified'
flags: i
match: not_contains
---
