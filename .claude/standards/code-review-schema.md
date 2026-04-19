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
