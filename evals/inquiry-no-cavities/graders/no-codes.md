---
# Plain words: no sales area's number, carrier code, field name or hash the customer didn't ask for.
type: regex
pattern: 'price ?hash|input ?hash|\b[hp]1:[0-9a-f]{8}|\bZA_[A-Z]|\b1[01]02 ?/ ?10\b|\bAW1\b'
flags: i
match: not_contains
---
