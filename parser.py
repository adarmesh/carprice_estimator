# parser.py — parsers for different domains that hold avg price of a car

import re
import requests


_KOLESA_BASE_URL = "https://kolesa.kz/cars"


def build_kolesa_url(make: str, model: str, year: str) -> str:
    """Build a kolesa.kz search URL for the given make/model/year."""
    make_slug = make.lower().replace(" ", "-")
    model_slug = model.lower().replace(" ", "-")
    return f"{_KOLESA_BASE_URL}/{make_slug}/{model_slug}/?year[from]={year}&year[to]={year}"


def parser_kolesa_kz(url: str) -> int | None:
    response = requests.get(url)
    response.raise_for_status()
    match = re.search(r'"avgPrice":(\d+)', response.text)
    return int(match.group(1)) if match else None