import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import uuid

from mywhoosh.exceptions import ApiError, AuthenticationError
from mywhoosh.models import WorkoutTask
from mywhoosh.utils import get_upcoming_date_range, load_env_file, parse_timestamp


LOGIN_URL = "https://services.mywhoosh.com/http-service/api/login"
TASK_LIST_URL = "https://service14.mywhoosh.com/v1/task/date-range-task-list"


class MyWhooshClient:
	"""Client for authenticating and interacting with MyWhoosh APIs."""

	def __init__(
		self,
		username: str | None = None,
		password: str | None = None,
		token: str | None = None,
		timeout: float = 30.0,
	) -> None:
		self.username = username
		self.password = password
		self.token = token
		self.timeout = timeout

	@classmethod
	def from_env(cls, env_path: str = ".env") -> "MyWhooshClient":
		"""Create a MyWhooshClient using credentials found in the environment or .env file."""
		load_env_file(env_path)
		return cls(
			username=os.getenv("MYWHOOSH_USERNAME"),
			password=os.getenv("MYWHOOSH_PASSWORD"),
		)

	def authenticate(
		self, username: str | None = None, password: str | None = None
	) -> str:
		"""Authenticate with MyWhoosh and store/return the access token."""
		user = username or self.username
		pwd = password or self.password

		if not user or not pwd:
			raise AuthenticationError(
				"Username and password are required for MyWhoosh authentication."
			)

		payload = {
			"Username": user,
			"Password": pwd,
			"Platform": "Android",
			"Action": 1001,
			"CorrelationId": str(uuid.uuid4()),
			"DeviceId": str(uuid.uuid4()),
			"Authorization": "",
		}
		request = Request(
			LOGIN_URL,
			data=json.dumps(payload).encode("utf-8"),
			headers={"Accept": "application/json", "Content-Type": "application/json"},
			method="POST",
		)

		try:
			with urlopen(request, timeout=self.timeout) as response:
				result: Any = json.loads(response.read().decode("utf-8"))
		except HTTPError as error:
			raise AuthenticationError(f"Login failed with HTTP {error.code}.") from None
		except URLError as error:
			raise AuthenticationError(f"Could not reach MyWhoosh: {error.reason}") from None
		except (UnicodeDecodeError, json.JSONDecodeError) as error:
			raise AuthenticationError("MyWhoosh returned an invalid JSON response during login.") from error

		if not isinstance(result, dict):
			raise AuthenticationError("MyWhoosh returned an unexpected response during login.")

		token = result.get("AccessToken")
		if not result.get("Success") or not isinstance(token, str) or not token:
			message = result.get("Message", "No access token was returned.")
			raise AuthenticationError(f"MyWhoosh login was unsuccessful: {message}")

		self.token = token
		return token

	def ensure_authenticated(self) -> str:
		"""Return the current token or perform authentication if not authenticated yet."""
		if self.token:
			return self.token
		return self.authenticate()

	def get_raw_task_list(
		self, start_date: int | str, end_date: int | str
	) -> dict[str, Any]:
		"""Query the /task/date-range-task-list endpoint and return the raw response."""
		token = self.ensure_authenticated()
		start_ts = parse_timestamp(start_date)
		end_ts = parse_timestamp(end_date)

		query_params = urlencode({"startDate": start_ts, "endDate": end_ts})
		url = f"{TASK_LIST_URL}?{query_params}"
		request = Request(
			url,
			headers={
				"Accept": "application/json",
				"Authorization": f"Bearer {token}",
			},
			method="GET",
		)

		try:
			with urlopen(request, timeout=self.timeout) as response:
				result: Any = json.loads(response.read().decode("utf-8"))
		except HTTPError as error:
			raise ApiError(
				f"Task query failed with HTTP {error.code}.", status_code=error.code
			) from None
		except URLError as error:
			raise ApiError(f"Could not reach MyWhoosh task service: {error.reason}") from None
		except (UnicodeDecodeError, json.JSONDecodeError) as error:
			raise ApiError("MyWhoosh task service returned an invalid JSON response.") from error

		if not isinstance(result, dict):
			raise ApiError("MyWhoosh returned an unexpected response format.")

		if result.get("status") is False:
			message = result.get("message") or result.get("errors") or "Task query was unsuccessful."
			raise ApiError(f"MyWhoosh task query failed: {message}", response=result)

		return result

	def get_tasks(
		self, start_date: int | str, end_date: int | str
	) -> list[WorkoutTask]:
		"""Query tasks within a date range and return a list of WorkoutTask instances."""
		raw_result = self.get_raw_task_list(start_date, end_date)
		task_list_data = raw_result.get("data", {}).get("taskList", [])
		if not isinstance(task_list_data, list):
			return []
		return [
			WorkoutTask.from_api_dict(item)
			for item in task_list_data
			if isinstance(item, dict)
		]

	def get_upcoming_tasks(self, days: int = 7) -> list[WorkoutTask]:
		"""Retrieve tasks for the upcoming N days starting today."""
		start_ts, end_ts = get_upcoming_date_range(days=days)
		return self.get_tasks(start_ts, end_ts)
