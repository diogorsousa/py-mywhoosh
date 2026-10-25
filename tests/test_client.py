import json
from unittest.mock import MagicMock, patch
import urllib.error
import unittest

from mywhoosh.client import MyWhooshClient
from mywhoosh.exceptions import ApiError, AuthenticationError


class TestMyWhooshClient(unittest.TestCase):
	def setUp(self) -> None:
		self.client = MyWhooshClient(username="test@example.com", password="password123")

	def test_authenticate_missing_credentials(self) -> None:
		empty_client = MyWhooshClient()
		with self.assertRaises(AuthenticationError):
			empty_client.authenticate()

	@patch("mywhoosh.client.urlopen")
	def test_authenticate_success(self, mock_urlopen: MagicMock) -> None:
		mock_response = MagicMock()
		mock_response.read.return_value = json.dumps({
			"Success": True,
			"AccessToken": "fake-jwt-token-12345",
		}).encode("utf-8")
		mock_response.__enter__.return_value = mock_response
		mock_urlopen.return_value = mock_response

		token = self.client.authenticate()
		self.assertEqual(token, "fake-jwt-token-12345")
		self.assertEqual(self.client.token, "fake-jwt-token-12345")

	@patch("mywhoosh.client.urlopen")
	def test_authenticate_api_error_response(self, mock_urlopen: MagicMock) -> None:
		mock_response = MagicMock()
		mock_response.read.return_value = json.dumps({
			"Success": False,
			"Message": "Invalid credentials",
		}).encode("utf-8")
		mock_response.__enter__.return_value = mock_response
		mock_urlopen.return_value = mock_response

		with self.assertRaises(AuthenticationError) as ctx:
			self.client.authenticate()
		self.assertIn("Invalid credentials", str(ctx.exception))

	@patch("mywhoosh.client.urlopen")
	def test_authenticate_http_error(self, mock_urlopen: MagicMock) -> None:
		mock_urlopen.side_effect = urllib.error.HTTPError(
			url="https://services.mywhoosh.com",
			code=401,
			msg="Unauthorized",
			hdrs={},  # type: ignore
			fp=None,  # type: ignore
		)
		with self.assertRaises(AuthenticationError) as ctx:
			self.client.authenticate()
		self.assertIn("401", str(ctx.exception))

	@patch("mywhoosh.client.urlopen")
	def test_get_tasks_success(self, mock_urlopen: MagicMock) -> None:
		client = MyWhooshClient(token="mock-token")
		mock_response = MagicMock()
		mock_response.read.return_value = json.dumps({
			"status": True,
			"data": {
				"taskList": [
					{
						"TaskId": "t1",
						"TaskStartedTimeEpoc": 1792368000,
						"TaskName": "Base Miles",
						"TaskDescription": "Endurance zone",
						"TSS": 45,
					}
				]
			},
		}).encode("utf-8")
		mock_response.__enter__.return_value = mock_response
		mock_urlopen.return_value = mock_response

		tasks = client.get_tasks("2026-10-25", "2026-11-01")
		self.assertEqual(len(tasks), 1)
		self.assertEqual(tasks[0].task_id, "t1")
		self.assertEqual(tasks[0].name, "Base Miles")
		self.assertEqual(tasks[0].tss, 45)

	@patch("mywhoosh.client.urlopen")
	def test_get_raw_task_list_failure(self, mock_urlopen: MagicMock) -> None:
		client = MyWhooshClient(token="mock-token")
		mock_response = MagicMock()
		mock_response.read.return_value = json.dumps({
			"status": False,
			"message": "Token expired",
		}).encode("utf-8")
		mock_response.__enter__.return_value = mock_response
		mock_urlopen.return_value = mock_response

		with self.assertRaises(ApiError) as ctx:
			client.get_tasks("2026-10-25", "2026-11-01")
		self.assertIn("Token expired", str(ctx.exception))


if __name__ == "__main__":
	unittest.main()
