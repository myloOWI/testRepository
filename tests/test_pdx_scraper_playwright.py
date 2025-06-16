import unittest
from pathlib import Path

from pdx_scraper_playwright import fetch_car_details, fetch_inventory_links


def load_sample_html():
    sample_path = Path(__file__).parent / 'sample_vehicle.html'
    return sample_path.read_text()


def load_inventory_html():
    path = Path(__file__).parent / 'sample_inventory.html'
    return path.read_text()


def load_inventory_page0():
    path = Path(__file__).parent / 'sample_inventory_page0.jsonp'
    return path.read_text()


def load_inventory_page1():
    path = Path(__file__).parent / 'sample_inventory_page1.jsonp'
    return path.read_text()


class PlaywrightScraperTests(unittest.TestCase):
    def test_fetch_car_details(self):
        html = load_sample_html()
        data = fetch_car_details('https://example.com/test', html=html)
        expected = {
            'title': '2008 Ferrari F430',
            'price': '$172,500',
            'mileage': '23456',
            'vin': 'ZFFEW58A580160000',
            'specs': {
                'Exterior': 'Red',
                'Interior': 'Tan',
            },
            'description': 'This Ferrari is awesome',
        }
        self.assertEqual(data, expected)

    def test_fetch_inventory_links(self):
        html = load_inventory_html()
        page0 = load_inventory_page0()
        page1 = load_inventory_page1()
        pages = {0: page0, 1: page1}
        links = fetch_inventory_links(base_html=html, page_html=pages)
        expected_links = [
            'https://www.pdxmotors.com/inventory/ford/f150/111/',
            'https://www.pdxmotors.com/inventory/tesla/model-x/222/',
            'https://www.pdxmotors.com/inventory/mercedes-benz/g-class/333/',
        ]
        self.assertEqual(links, expected_links)


if __name__ == '__main__':
    unittest.main()
