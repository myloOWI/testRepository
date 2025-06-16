from __future__ import annotations

import json
import re
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

from playwright.sync_api import sync_playwright


def fetch_car_details(url: str, html: str | None = None) -> dict:
    """Fetch car details using Playwright.

    If *html* is provided, the browser will load that content instead of
    navigating to *url*. This is useful for testing without network access.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        if html is not None:
            page.set_content(html)
        else:
            page.goto(url)

        result: dict = {}

        title = page.locator('h1.h4.title')
        if title.count():
            result['title'] = title.inner_text().strip()

        price = page.locator('span.dws-vdp-single-field-value-vehicleprice')
        if price.count():
            result['price'] = price.inner_text().strip()

        mileage = page.locator('p.dws-forms-mileage span.dws-forms-value')
        if mileage.count():
            result['mileage'] = mileage.inner_text().strip()

        vin = page.locator('p.dws-forms-vin span.dws-forms-value')
        if vin.count():
            result['vin'] = vin.inner_text().strip()

        specs = {}
        for item in page.locator('dl.vehicle-info div.info-item').all():
            term = item.locator('dt').inner_text().strip()
            desc = item.locator('dd').inner_text().strip()
            specs[term] = desc
        if specs:
            result['specs'] = specs

        description = page.locator('meta[property="og:description"]')
        if description.count():
            content = description.get_attribute('content')
            if content:
                result['description'] = content

        browser.close()
    return result


def _slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def fetch_inventory_links(
    base_url: str = "https://www.pdxmotors.com/inventory/",
    base_html: str | None = None,
    page_html: dict[int, str] | None = None,
) -> list[str]:
    """Return a list of vehicle detail page URLs using Playwright.

    Parameters *base_html* and *page_html* allow injecting HTML content for
    the inventory page and subsequent JSONP responses. This is primarily
    intended for testing.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        if base_html is not None:
            page.set_content(base_html)
        else:
            page.goto(base_url)

        script = page.locator('script[src*="/inv-scripts-v2/inv/vehicles"]')
        if not script.count():
            browser.close()
            raise ValueError("Inventory script not found")
        src_url = urljoin(base_url, script.get_attribute('src'))
        parsed = urlparse(src_url)
        query = parse_qs(parsed.query)

        def fetch_page(pn: int) -> dict:
            if page_html and pn in page_html:
                page.set_content(page_html[pn])
                text = page.inner_text('body')
            else:
                q = query.copy()
                q['pn'] = [str(pn)]
                page_url = urlunparse(parsed._replace(query=urlencode(q, doseq=True)))
                page.goto(page_url)
                text = page.inner_text('body')
            m = re.search(r"\((\{.*\})\)", text)
            if not m:
                raise ValueError("Unexpected inventory response")
            return json.loads(m.group(1))

        first_page = fetch_page(0)
        vehicles = list(first_page.get('Vehicles', []))
        total = first_page.get('TotalRecordCount', len(vehicles))
        per_page = len(first_page.get('Vehicles', [])) or 1
        pages = (total + per_page - 1) // per_page

        for pn in range(1, pages):
            data = fetch_page(pn)
            vehicles.extend(data.get('Vehicles', []))

        browser.close()

    links = []
    for v in vehicles:
        make_slug = _slugify(v['Make'])
        model_slug = _slugify(v['Model'])
        stock = v['StockNumber']
        links.append(
            f"https://www.pdxmotors.com/inventory/{make_slug}/{model_slug}/{stock}/"
        )
    return links
