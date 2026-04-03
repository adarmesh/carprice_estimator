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