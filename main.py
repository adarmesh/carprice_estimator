import argparse
import base64
import io
import json
from pathlib import Path
import anthropic
from dotenv import load_dotenv
from PIL import Image
from pillow_heif import register_heif_opener


register_heif_opener()
load_dotenv()

_IDENTIFY_CAR_TOOL = {
    "name": "identify_car",
    "description": "Report the identified car make and model, or an error if no car is present.",
    "input_schema": {
        "type": "object",
        "properties": {
            "make": {"type": ["string", "null"], "description": "Car manufacturer, e.g. Toyota"},
            "model": {"type": ["string", "null"], "description": "Car model name, e.g. Camry"},
            "error": {"type": ["string", "null"], "description": "Set if no car is detected"},
        },
        "required": ["make", "model", "error"],
    },
}


_MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB API limit
_MAX_DIMENSION = 1568  # Claude's recommended max for vision


def _load_image_bytes(path: Path) -> tuple[bytes, str]:
    """Load image from path, converting HEIC if needed. Returns (bytes, media_type)."""
    img = Image.open(path)

    # Resize if either dimension exceeds the recommended max
    if img.width > _MAX_DIMENSION or img.height > _MAX_DIMENSION:
        img.thumbnail((_MAX_DIMENSION, _MAX_DIMENSION), Image.LANCZOS)

    # Save as JPEG (best compression for photos)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=85)

    # If still too large, reduce quality until it fits
    quality = 75
    while buf.tell() > _MAX_IMAGE_BYTES and quality >= 30:
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=quality)
        quality -= 15

    return buf.getvalue(), "image/jpeg"


def identify_car(image_path: str) -> dict:
    path = Path(image_path)
    if not path.exists():
        return {"error": f"File not found: {image_path}"}

    if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".heic", ".heif"):
        return {"error": f"Unsupported file type: {path.suffix}. Only JPEG, PNG, and HEIC are supported."}

    image_bytes, media_type = _load_image_bytes(path)
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=(
            "You are a car identification expert. "
            "When given an image, determine if it contains a car. "
            "If it does not contain a car, set error to 'No car detected in image' and make/model to null. "
            "If it contains a car but you cannot determine the make or model, set those fields to null."
        ),
        tools=[_IDENTIFY_CAR_TOOL],
        tool_choice={"type": "tool", "name": "identify_car"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": "Identify the car's make and model."},
                ],
            }
        ],
    )

    tool_input = next(b.input for b in response.content if b.type == "tool_use")
    if tool_input.get("error"):
        return {"error": tool_input["error"]}
    return {"make": tool_input["make"], "model": tool_input["model"]}


def main():
    parser = argparse.ArgumentParser(description="Identify a car from a photo.")
    parser.add_argument("image", help="Path to a JPEG, PNG, or HEIC image of a car")
    args = parser.parse_args()

    try:
        result = identify_car(args.image)
    except RuntimeError as e:
        print(json.dumps({"error": str(e)}, indent=2))
        return
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()