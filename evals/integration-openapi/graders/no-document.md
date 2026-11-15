---
type: regex
pattern: 'openapi:\s*3|"openapi"\s*:|swagger:\s*[''"]?2|^\s*paths:|^\s*(GET|POST|PUT|PATCH|DELETE)\s+/'
flags: im
match: not_contains
---
