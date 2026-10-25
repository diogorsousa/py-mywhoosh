import argparse
import getpass
import json
import os
import sys
from typing import Any

from mywhoosh.client import MyWhooshClient
from mywhoosh.exceptions import MyWhooshError
from mywhoosh.models import WorkoutTask
from mywhoosh.utils import get_upcoming_date_range, load_env_file, parse_timestamp


def authenticate(username: str, password: str) -> str:
	"""Authenticate with MyWhoosh and return access token."""
	return MyWhooshClient(username=username, password=password).authenticate()


def get_date_range_task_list(
	token: str, start_date: int | str, end_date: int | str
) -> dict[str, Any]:
	"""Query the raw date-range-task-list response using an access token."""
	client = MyWhooshClient(token=token)
	return client.get_raw_task_list(start_date, end_date)


def trim_task(task: dict[str, Any]) -> dict[str, Any]:
	"""Convert a raw task dictionary into essential trimmed format."""
	return WorkoutTask.from_api_dict(task).to_dict()


def get_default_date_range() -> tuple[int, int]:
	"""Return Unix timestamps for start (today 00:00:00) and end (7 days ahead 23:59:59) in UTC."""
	return get_upcoming_date_range(days=7)


def main(argv: list[str] | None = None) -> int:
	load_env_file()
	default_start, default_end = get_default_date_range()
	env_start = os.getenv("MYWHOOSH_START_DATE")
	env_end = os.getenv("MYWHOOSH_END_DATE")

	initial_start = parse_timestamp(env_start) if env_start else default_start
	initial_end = parse_timestamp(env_end) if env_end else default_end

	parser = argparse.ArgumentParser(
		prog="mywhoosh",
		description="Authenticate with MyWhoosh and query the date-range task list.",
	)
	parser.add_argument(
		"--start-date",
		type=parse_timestamp,
		default=initial_start,
		help="Start date Unix timestamp or ISO string (defaults to today 00:00:00 UTC)",
	)
	parser.add_argument(
		"--end-date",
		type=parse_timestamp,
		default=initial_end,
		help="End date Unix timestamp or ISO string (defaults to 7 days ahead 23:59:59 UTC)",
	)
	args = parser.parse_args(argv)

	username = os.getenv("MYWHOOSH_USERNAME") or input("MyWhoosh email: ").strip()
	password = os.getenv("MYWHOOSH_PASSWORD") or getpass.getpass("MyWhoosh password: ")

	if not username or not password:
		print("Email and password are required.", file=sys.stderr)
		return 1

	try:
		client = MyWhooshClient(username=username, password=password)
		tasks = client.get_tasks(args.start_date, args.end_date)
		print(json.dumps([task.to_dict() for task in tasks], indent=2))
	except MyWhooshError as error:
		print(error, file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
