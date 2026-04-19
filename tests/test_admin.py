import unittest
from unittest.mock import patch, Mock

from removebgvideo.admin import RemoveBGVideoAdminClient


class TestRemoveBGVideoAdminClient(unittest.TestCase):
    def setUp(self):
        self.client = RemoveBGVideoAdminClient(admin_token="admin_token", base_url="https://api.example.com")

    @patch("removebgvideo.admin.requests.get")
    def test_list_keys(self, mock_get):
        resp = Mock()
        resp.status_code = 200
        resp.json.return_value = {"items": [{"client_id": "acme-prod"}]}
        mock_get.return_value = resp

        data = self.client.list_keys()
        self.assertEqual(data["items"][0]["client_id"], "acme-prod")


if __name__ == "__main__":
    unittest.main()
