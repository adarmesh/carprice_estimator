## Testing Standards (CI Context)

- Use factory functions from test/factories/ for data creation
- Integration tests use the test database via test/setup/db.ts
- Do not test private implementation details
- Coverage target: 80% branch coverage for new code
- Available fixtures: test/fixtures/users.json, test/fixtures/orders.json
