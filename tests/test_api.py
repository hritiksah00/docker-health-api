import json
import unittest
from urllib.request import urlopen


class APIIntegrationTests(unittest.TestCase):
    def get_json(self, path):
        url = f"http://127.0.0.1:5000{path}"

        with urlopen(url, timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(
                response.headers.get_content_type(),
                "application/json",
            )
            return json.load(response)

    def test_health_endpoint(self):
        data = self.get_json("/health")
        self.assertEqual(data, {"status": "ok"})

    def test_home_endpoint(self):
        data = self.get_json("/")
        self.assertEqual(data["service"], "docker-health-api")


if __name__ == "__main__":
    unittest.main()