from inventory_framework import save_inventory_json
from pdx_scraper_playwright import fetch_inventory_links


def main() -> None:
    links = fetch_inventory_links()
    save_inventory_json(links, "inventory.json")


if __name__ == "__main__":
    main()
