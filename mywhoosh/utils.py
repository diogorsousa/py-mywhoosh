from datetime import datetime, timedelta, timezone
import os
from pathlib import Path


def load_env_file(env_path: Path | str = ".env") -> None:
	"""Load key-value pairs from a .env file into os.environ if not already set."""
	path = Path(env_path)
	if not path.is_file():
		return
	try:
		with path.open("r", encoding="utf-8") as f:
			for line in f:
				line = line.strip()
				if not line or line.startswith("#") or "=" not in line:
					continue
				key, _, val = line.partition("=")
				key = key.strip()
				val = val.strip().strip("'\"")
				if key and key not in os.environ:
					os.environ[key] = val
	except OSError:
		pass


def get_upcoming_date_range(days: int = 7) -> tuple[int, int]:
	"""Return Unix timestamps for start (today 00:00:00 UTC) and end (days ahead 23:59:59 UTC)."""
	now = datetime.now(timezone.utc)
	start = now.replace(hour=0, minute=0, second=0, microsecond=0)
	end = (start + timedelta(days=days)).replace(
		hour=23, minute=59, second=59, microsecond=0
	)
	return int(start.timestamp()), int(end.timestamp())


def parse_timestamp(value: str | int) -> int:
	"""Parse an integer timestamp or ISO date string into a Unix timestamp."""
	if isinstance(value, int):
		return value
	try:
		return int(value)
	except ValueError:
		dt = datetime.fromisoformat(value)
		if dt.tzinfo is None:
			dt = dt.replace(tzinfo=timezone.utc)
		return int(dt.timestamp())
