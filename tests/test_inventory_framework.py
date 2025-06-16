import json
import unittest
from unittest.mock import patch

import inventory_framework


class InventoryFrameworkTests(unittest.TestCase):
    def test_inventory_to_json(self):
        links = ["http://example.com/1", "http://example.com/2"]
        details = [{"title": "Car1"}, {"title": "Car2"}]
        with patch("inventory_framework.fetch_car_details", side_effect=details):
            data = inventory_framework.inventory_to_json(links)

        self.assertEqual(json.loads(data), details)


if __name__ == "__main__":
    unittest.main()
