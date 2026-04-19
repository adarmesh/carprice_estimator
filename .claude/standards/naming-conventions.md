## Naming Conventions

### Python
- Functions and variables: `snake_case`
- Module-level constants: `UPPER_SNAKE_CASE`; prefix with `_` if private to the module (e.g. `_MAX_IMAGE_BYTES`, `_KOLESA_BASE_URL`)
- Private helpers (not part of public API): prefix with `_` (e.g. `_load_image_bytes`)
- Module files: `snake_case.py`

### Tests
- Test functions: `test_<function_under_test>_<scenario>` (e.g. `test_parser_kolesa_kz_returns_avg_price`)
- Private test helpers: prefix with `_` (e.g. `_mock_get`)
- Fixture files: `<make>_<model>_<year>.<ext>` for car-specific fixtures (e.g. `toyota_rav4_2007.html`)
