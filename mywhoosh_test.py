"""Backward-compatible runner and helper functions delegating to mywhoosh.cli."""

from mywhoosh.cli import (
	authenticate,
	get_date_range_task_list,
	get_default_date_range,
	main,
	trim_task,
)

if __name__ == "__main__":
	raise SystemExit(main())

