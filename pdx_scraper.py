import requests
from bs4 import BeautifulSoup


def fetch_car_details(url: str) -> dict:
    """Fetches car details from a PDX Motors inventory page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
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


def main():
    url = 'https://www.pdxmotors.com/inventory/ferrari/f430/13912/'
    details = fetch_car_details(url)
    for k, v in details.items():
        print(f"{k}: {v}")


if __name__ == '__main__':
    main()
