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
- Ask the model to identify as many car characteristics as possible: make, model, build year.

### Output

A JSON object:

```json
{
  "make": "Toyota",
  "model": "RAV4",
  "build_year": "2007"
}
```

### Error cases

- Image does not contain a car → return an error response
- Car is visible but if any of make/model/build_year cannot be determined → return an error response with field that couldn't be determined.

## Step 2: Price Lookup

The `make`, `model`, `build_year` fields from Step 1 are used to build a request to an external pricing API.

### Building the API URL

- Base URL: `https://kolesa.kz/cars`
- URI parameters: `make`, `model`, `build_year`
- Example: `https://kolesa.kz/cars/toyota/rav4/?year[from]=2007&year[to]=2007`

### Output

A HTML output will list ads with car images and prices. We're only interested in finding average price under

### Error cases

- Pricing API is unavailable → return an error response
- No pricing data found for the given make/model/year → return `null` for price fields

## Distribution Channel: Telegram Bot

The application will be exposed to end users via a Telegram bot.

### User flow

1. User sends a car photo to the bot
2. Bot passes the image to the car identification service (Step 1)
3. Bot receives identified make/model/build_year (or an error message)
4. Bot builds GET request for another service to get average price.
5. Bot replies with average price and built GET request in nicely human-readable format.

### Hosting requirement

The bot must run as a persistent process on a server (not a local script) to receive messages from Telegram in real time.
