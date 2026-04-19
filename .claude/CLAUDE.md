# CLAUDE.md

## Testing Standards (CI Context)

- Use factory functions from test/factories/ for data creation
- Integration tests use the test database via test/setup/db.ts
- Do not test private implementation details
- Coverage target: 80% branch coverage for new code
- Available fixtures: test/fixtures/users.json, test/fixtures/orders.json

## Review Criteria

- Critical: security issues, data loss risk, authentication bypass
- Major: missing error handling, uncovered edge cases
- Minor: naming conventions, style inconsistencies

## Code review schema

Output findings as rdjson (Reviewdog Diagnostic JSON):

```json
{
  "diagnostics": [
    {
      "message": "string",
      "location": {
        "path": "string",
        "range": {
          "start": {
            "line": 1
          }
        }
      },
      "severity": "ERROR | WARNING | INFO"
    }
  ]
}
```

Severity mapping: high → `ERROR`, medium → `WARNING`, low → `INFO`.
