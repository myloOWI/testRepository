import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
import json
import re


def fetch_car_details(url: str) -> dict:
    """Fetches car details from a PDX Motors inventory page.

    Returns an empty dictionary if the request fails.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to fetch {url}: {exc}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')

    result = {}

    # car title
    title = soup.find('h1', class_='h4 title')
    if title:
        result['title'] = title.get_text(strip=True)

    # price
    price = soup.find('span', class_='dws-vdp-single-field-value-vehicleprice')
    if price:
        result['price'] = price.get_text(strip=True)

    # mileage
    mileage = soup.find('p', class_='dws-forms-mileage')
    if mileage:
        value_span = mileage.find('span', class_='dws-forms-value')
        if value_span:
            result['mileage'] = value_span.get_text(strip=True)

    # VIN
    vin = soup.find('p', class_='dws-forms-vin')
    if vin:
        value_span = vin.find('span', class_='dws-forms-value')
        if value_span:
            result['vin'] = value_span.get_text(strip=True)

    # specs
    specs = {}
    spec_container = soup.find('dl', class_='vehicle-info')
    if spec_container:
        for item in spec_container.find_all('div', class_='info-item'):
            term = item.find('dt')
            description = item.find('dd')
            if term and description:
                specs[term.get_text(strip=True)] = description.get_text(strip=True)
    if specs:
        result['specs'] = specs

    # description (fallback to og:description meta tag)
    description = soup.find('meta', property='og:description')
    if description and description.get('content'):
        result['description'] = description['content']

    return result


def _slugify(value: str) -> str:
    """Converts text into a slug suitable for URLs."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def fetch_inventory_links(base_url: str = "https://www.pdxmotors.com/inventory/") -> list[str]:
    """Returns a list of vehicle detail page URLs from the inventory."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0 Safari/537.36",
    }
    response = requests.get(base_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    script = soup.find("script", src=re.compile(r"/inv-scripts-v2/inv/vehicles"))
    if not script or not script.get("src"):
        raise ValueError("Inventory script not found")

    src_url = urljoin(base_url, script["src"])
    parsed = urlparse(src_url)
    query = parse_qs(parsed.query)

    def fetch_page(page_num: int) -> dict:
        q = query.copy()
        q["pn"] = [str(page_num)]
        page_url = urlunparse(parsed._replace(query=urlencode(q, doseq=True)))
        r = requests.get(page_url, headers=headers, timeout=10)
        r.raise_for_status()
        m = re.search(r"\((\{.*\})\)", r.text)
        if not m:
            raise ValueError("Unexpected inventory response")
        return json.loads(m.group(1))

    first_page = fetch_page(0)
    vehicles = list(first_page["Vehicles"])
    total = first_page["TotalRecordCount"]
    per_page = len(first_page["Vehicles"])
    pages = (total + per_page - 1) // per_page

    for pn in range(1, pages):
        data = fetch_page(pn)
        vehicles.extend(data.get("Vehicles", []))

    links = []
    for v in vehicles:
        make_slug = _slugify(v["Make"])
        model_slug = _slugify(v["Model"])
        stock = v["StockNumber"]
        links.append(
            f"https://www.pdxmotors.com/inventory/{make_slug}/{model_slug}/{stock}/"
        )

    return links


def main():
    parser = argparse.ArgumentParser(
        description="Fetch car details from a PDX Motors inventory page"
    )
    parser.add_argument(
        "url",
        nargs="?",
        default="https://www.pdxmotors.com/inventory/ferrari/f430/13912/",
        help="Vehicle URL to scrape",
    )
    args = parser.parse_args()

    details = fetch_car_details(args.url)
    for k, v in details.items():
        print(f"{k}: {v}")


if __name__ == '__main__':
    main()
