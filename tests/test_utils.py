from datetime import datetime, timezone
import os
from pathlib import Path
import tempfile
import unittest

from mywhoosh.utils import get_upcoming_date_range, load_env_file, parse_timestamp


class TestUtils(unittest.TestCase):
	def test_parse_timestamp_from_int(self) -> None:
		self.assertEqual(parse_timestamp(1700000000), 1700000000)

	def test_parse_timestamp_from_numeric_str(self) -> None:
		self.assertEqual(parse_timestamp("1700000000"), 1700000000)

	def test_parse_timestamp_from_iso_date(self) -> None:
		ts = parse_timestamp("2026-10-25")
		dt = datetime.fromtimestamp(ts, tz=timezone.utc)
		self.assertEqual(dt.year, 2026)
		self.assertEqual(dt.month, 10)
		self.assertEqual(dt.day, 25)

	def test_get_upcoming_date_range(self) -> None:
		start, end = get_upcoming_date_range(days=7)
		self.assertIsInstance(start, int)
		self.assertIsInstance(end, int)
		self.assertGreater(end, start)
		start_dt = datetime.fromtimestamp(start, tz=timezone.utc)
		self.assertEqual(start_dt.hour, 0)
		self.assertEqual(start_dt.minute, 0)
		self.assertEqual(start_dt.second, 0)
		end_dt = datetime.fromtimestamp(end, tz=timezone.utc)
		self.assertEqual(end_dt.hour, 23)
		self.assertEqual(end_dt.minute, 59)
		self.assertEqual(end_dt.second, 59)

	def test_load_env_file(self) -> None:
		with tempfile.TemporaryDirectory() as tmpdir:
			env_file = Path(tmpdir) / ".env"
			env_file.write_text(
				"# Comment\nTEST_MYWHOOSH_KEY=secret_value\n\nEMPTY_LINE=\n",
				encoding="utf-8",
			)
			load_env_file(env_file)
			self.assertEqual(os.environ.get("TEST_MYWHOOSH_KEY"), "secret_value")
			if "TEST_MYWHOOSH_KEY" in os.environ:
				del os.environ["TEST_MYWHOOSH_KEY"]


if __name__ == "__main__":
	unittest.main()
