"""Utility for processing multiple inventory links and exporting data as JSON."""

import json
from typing import Iterable, List

from pdx_scraper import fetch_car_details


def inventory_to_json(links: Iterable[str]) -> str:
    """Fetch details for all inventory links and return JSON string."""
    data: List[dict] = []
    for url in links:
        details = fetch_car_details(url)
        data.append(details)
    return json.dumps(data, indent=2)


def save_inventory_json(links: Iterable[str], filename: str) -> None:
    """Fetch details for all links and save them to *filename* in JSON format."""
    json_data = inventory_to_json(links)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json_data)
