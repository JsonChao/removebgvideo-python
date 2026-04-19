import unittest
from unittest.mock import patch, Mock

from removebgvideo import RemoveBGVideoClient
from removebgvideo.exceptions import ApiError


class TestRemoveBGVideoClient(unittest.TestCase):
    def setUp(self):
        self.client = RemoveBGVideoClient(api_key="test_key", base_url="https://api.example.com")

    @patch("removebgvideo.client.requests.post")
    def test_create_job_success(self, mock_post):
        resp = Mock()
        resp.status_code = 200
        resp.json.return_value = {"id": "job_1", "status": "pending"}
        mock_post.return_value = resp

        data = self.client.create_job(video_url="https://cdn.example.com/in.mp4")
        self.assertEqual(data["id"], "job_1")

    @patch("removebgvideo.client.requests.get")
    def test_get_job_error(self, mock_get):
        resp = Mock()
        resp.status_code = 401
        resp.json.return_value = {
            "error": {"code": "invalid_api_key", "message": "Invalid API key", "request_id": "req_1"}
        }
        mock_get.return_value = resp

        with self.assertRaises(ApiError) as ctx:
            self.client.get_job("job_1")

        self.assertEqual(ctx.exception.code, "invalid_api_key")
        self.assertEqual(ctx.exception.request_id, "req_1")


if __name__ == "__main__":
    unittest.main()
