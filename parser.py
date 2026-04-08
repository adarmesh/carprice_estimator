# parser.py — parsers for different domains that hold avg price of a car

import re
import requests


def parser_kolesa_kz(url: str) -> int | None:
    response = requests.get(url)
    response.raise_for_status()
    match = re.search(r'"avgPrice":(\d+)', response.text)
    return int(match.group(1)) if match else None