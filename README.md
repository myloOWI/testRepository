# Summary

This repository contains a small web scraper for extracting vehicle details from the PDX Motors website.

## Inventory JSON

Use `inventory_framework` to convert a list of inventory links to a JSON document.

```python
from inventory_framework import save_inventory_json

urls = [
    "https://www.pdxmotors.com/inventory/ferrari/f430/13912/",
]
save_inventory_json(urls, "inventory.json")
```

## Testing

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the test suite:

```bash
python -m pytest -q
```

## Docker

A `Dockerfile` is provided for running the scraper in a container. Build the image with:

```bash
docker build -t pdx-scraper:latest .
```

Run the tests inside the image:

```bash
docker run --rm pdx-scraper:latest
```
