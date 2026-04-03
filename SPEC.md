# Car Price Estimator — Specification

## Overview

A service that identifies a car from a photo and returns structured data for downstream price lookup.

## Prerequisites

Install all necessary dep-cies to build an app (requirements.txt, package.json, etc.)

## Step 1: Car Identification (in scope)

### Input

- A photo of a car (JPEG, PNG, HEIC)

### Processing

- Send the image to the Anthropic API (Claude vision)
- Ask the model to identify the car's make and model

### Output

A JSON object:

```json
{
  "make": "Toyota",
  "model": "Camry"
}
```

### Error cases

- Image does not contain a car → return an error response
- Car is visible but make/model cannot be determined → return `null` for the unknown fields

## Step 2: Price Lookup (out of scope)

The `make` and `model` fields from Step 1 will be passed to external pricing APIs. Not part of this implementation.

## Distribution Channel: Telegram Bot

The application will be exposed to end users via a Telegram bot.

### User flow

1. User sends a car photo to the bot
2. Bot passes the image to the car identification service (Step 1)
3. Bot replies with the identified make/model (or an error message)

### Hosting requirement

The bot must run as a persistent process on a server (not a local script) to receive messages from Telegram in real time.

## Step 3: Image Collection (in scope)

Every car photo received via the Telegram bot is stored for future use (dataset accumulation, model validation, fine-tuning).

### Storage backend

**Azure Blob Storage** — one container for raw images.

### What to store

| Data | Where |
|---|---|
| Raw image file | Azure Blob Storage |
| Metadata (make, model, error, timestamp, telegram user hash, blob path) | Azure SQL / SQLite (TBD) |

### Flow

1. User sends photo to Telegram bot
2. Bot downloads the image from Telegram
3. Image is uploaded to Azure Blob Storage (key: `{date}/{uuid}.jpg`)
4. Identification result + blob reference saved to metadata store
5. Bot replies to user

### Notes

- Store Telegram `file_id` alongside the blob key as a cheap reference
- Hash user identifiers — do not store raw Telegram user IDs