import unittest

from mywhoosh.models import WorkoutTask


class TestModels(unittest.TestCase):
	def test_workout_task_from_api_dict(self) -> None:
		raw = {
			"TaskId": "12345",
			"TaskStartedTimeEpoc": 1792368000,
			"TaskName": "Threshold Intervals",
			"TaskDescription": "Hard interval session",
			"TSS": 65,
		}
		task = WorkoutTask.from_api_dict(raw)
		self.assertEqual(task.task_id, "12345")
		self.assertEqual(task.name, "Threshold Intervals")
		self.assertEqual(task.description, "Hard interval session")
		self.assertEqual(task.tss, 65)
		self.assertTrue(task.date.startswith("2026-"))
		self.assertEqual(task.raw, raw)

	def test_workout_task_to_dict(self) -> None:
		raw = {
			"TaskId": "999",
			"TaskStartedTimeEpoc": 1792368000,
			"TaskName": "Recovery Spin",
			"TaskDescription": "Easy ride",
			"TSS": 20,
		}
		task = WorkoutTask.from_api_dict(raw)
		trimmed = task.to_dict()
		self.assertEqual(
			trimmed,
			{
				"TaskStartedTimeEpoc": task.date,
				"TaskName": "Recovery Spin",
				"TaskDescription": "Easy ride",
				"TSS": 20,
			},
		)

	def test_workout_task_defaults(self) -> None:
		task = WorkoutTask.from_api_dict({})
		self.assertEqual(task.task_id, "")
		self.assertEqual(task.name, "")
		self.assertEqual(task.description, "")
		self.assertEqual(task.tss, 0)
		self.assertEqual(task.date, "")


if __name__ == "__main__":
	unittest.main()
