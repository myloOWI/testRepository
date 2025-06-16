import unittest
from unittest.mock import patch
import requests
from pathlib import Path

import pdx_scraper


def load_sample_html():
    sample_path = Path(__file__).parent / 'sample_vehicle.html'
    return sample_path.read_text()


class MockResponse:
    def __init__(self, text):
        self.text = text
        self.status_code = 200

    def raise_for_status(self):
        pass


class MockErrorResponse:
    def __init__(self, status_code=404):
        self.text = ""
        self.status_code = status_code

    def raise_for_status(self):
        raise requests.HTTPError(f"{self.status_code} Error")


def load_inventory_html():
    path = Path(__file__).parent / 'sample_inventory.html'
    return path.read_text()


def load_inventory_page0():
    path = Path(__file__).parent / 'sample_inventory_page0.jsonp'
    return path.read_text()


def load_inventory_page1():
    path = Path(__file__).parent / 'sample_inventory_page1.jsonp'
    return path.read_text()


class PdxScraperTests(unittest.TestCase):
    def test_fetch_car_details(self):
        html = load_sample_html()
        with patch('requests.get', return_value=MockResponse(html)):
            data = pdx_scraper.fetch_car_details('https://example.com/test')

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

    def test_fetch_car_details_http_error(self):
        with patch('requests.get', return_value=MockErrorResponse()):
            data = pdx_scraper.fetch_car_details('https://example.com/missing')

        self.assertEqual(data, {})

    def test_fetch_car_details_network_error(self):
        with patch('requests.get', side_effect=requests.RequestException("boom")):
            data = pdx_scraper.fetch_car_details('https://example.com/error')

        self.assertEqual(data, {})

    def test_fetch_inventory_links(self):
        html = load_inventory_html()
        page0 = load_inventory_page0()
        page1 = load_inventory_page1()

        def mock_get(url, headers=None, timeout=10):
            if url == 'https://www.pdxmotors.com/inventory/':
                return MockResponse(html)
            elif 'pn=0' in url:
                return MockResponse(page0)
            elif 'pn=1' in url:
                return MockResponse(page1)
            raise ValueError(f'Unexpected URL {url}')

        with patch('requests.get', side_effect=mock_get):
            links = pdx_scraper.fetch_inventory_links()

        expected_links = [
            'https://www.pdxmotors.com/inventory/ford/f150/111/',
            'https://www.pdxmotors.com/inventory/tesla/model-x/222/',
            'https://www.pdxmotors.com/inventory/mercedes-benz/g-class/333/',
        ]
        self.assertEqual(links, expected_links)


if __name__ == '__main__':
    unittest.main()
