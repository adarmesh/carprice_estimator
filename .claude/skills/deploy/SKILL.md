---
name: deploy
description: Deploy the application by sourcing .env and running ./infra/deploy.sh. Use when the user asks to deploy, ship, or release the application.
disable-model-invocation: true
user-invocable: true
---

Source the `.env` file from the project root and run the deploy script:

```bash
set -a && source .env && set +a && ./infra/deploy.sh
```

Run this command exactly as written. Do not modify or skip sourcing `.env`. Report the output to the user.
