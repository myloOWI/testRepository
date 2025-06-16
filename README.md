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
python3 -m unittest discover -s tests -v
```
