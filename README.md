# Car Price Estimator

Identifies a car's make and model from a photo using Claude vision.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

```bash
python main.py <image_path>
```

Supported formats: JPEG, PNG, HEIC.

### Examples

```bash
python main.py car.jpg
python main.py photo.heic
```

### Output

On success:
```json
{
  "make": "Toyota",
  "model": "Camry"
}
```

If the car's make or model cannot be determined:
```json
{
  "make": "Toyota",
  "model": null
}
```

If no car is detected in the image:
```json
{
  "error": "No car detected in image"
}
```
