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
pip install -r requirements.playwright.txt  # needed for Playwright
playwright install
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

Running the image will automatically download the full inventory from the PDX Motors website and save it to `inventory.json` in the working directory:

```bash
docker run --rm pdx-scraper:latest
```

### Playwright option

You can alternatively scrape using Playwright. Install the extra dependency and browsers, then run the dedicated script:

```bash
pip install -r requirements.playwright.txt
playwright install
python scrape_inventory_playwright.py
```

To containerize this approach, build and run the image defined in `Dockerfile.playwright`:

```bash
docker build -f Dockerfile.playwright -t pdx-scraper-playwright:latest .
docker run --rm pdx-scraper-playwright:latest
```
