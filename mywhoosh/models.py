from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class WorkoutTask:
	task_id: str
	date: str
	name: str
	description: str
	tss: int | float
	raw: dict[str, Any]

	@classmethod
	def from_api_dict(cls, data: dict[str, Any]) -> "WorkoutTask":
		epoch = data.get("TaskStartedTimeEpoc")
		date_str = ""
		if isinstance(epoch, (int, float)):
			date_str = datetime.fromtimestamp(epoch).strftime("%Y-%m-%d")
		elif epoch is not None:
			try:
				date_str = datetime.fromtimestamp(float(epoch)).strftime("%Y-%m-%d")
			except (ValueError, OSError):
				date_str = str(epoch)

		return cls(
			task_id=str(data.get("TaskId") or ""),
			date=date_str,
			name=str(data.get("TaskName") or ""),
			description=str(data.get("TaskDescription") or ""),
			tss=data.get("TSS") or 0,
			raw=data,
		)

	def to_dict(self) -> dict[str, Any]:
		"""Return dictionary formatted with essential workout fields."""
		return {
			"TaskStartedTimeEpoc": self.date,
			"TaskName": self.name,
			"TaskDescription": self.description,
			"TSS": self.tss,
		}
