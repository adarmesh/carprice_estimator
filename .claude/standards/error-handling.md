## Error Handling Standards

### Return shape
- User-facing functions return `{"error": str}` on failure; never raise to the caller
- Successful returns must not include an `"error"` key
- Callers check `result.get("error")` before accessing other fields

### Exception catching
- Catch specific exception types — never bare `except Exception` or `except:`
- For Anthropic API calls, catch in order: `RateLimitError`, `AuthenticationError`, `APIConnectionError`, then `APIError` as a fallback
- For `requests` HTTP calls, catch `requests.HTTPError` (raised by `raise_for_status()`) and `requests.ConnectionError` separately
- Do not silently discard exceptions; if a value is optional on failure, log or surface the reason

### Validation before I/O
- Validate file existence and supported extensions before opening files or calling external APIs
- Return an `{"error": ...}` dict immediately on invalid input rather than letting downstream code raise

### Bot layer
- When a scraper/parser result is optional (e.g. avg price), catching failure is acceptable but must not use bare `except Exception` — catch the specific expected exceptions (`requests.HTTPError`, `requests.ConnectionError`, `requests.Timeout`)
- User-visible error messages must be human-readable, not raw exception strings
