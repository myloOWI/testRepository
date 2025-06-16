import unittest
from unittest.mock import patch
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


if __name__ == '__main__':
    unittest.main()
