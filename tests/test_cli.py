from unittest.mock import MagicMock, patch
import unittest

from mywhoosh.cli import main
from mywhoosh.models import WorkoutTask


class TestCLI(unittest.TestCase):
	def test_cli_missing_credentials(self) -> None:
		with patch.dict("os.environ", {}, clear=True):
			with patch("mywhoosh.cli.load_env_file"):
				with patch("builtins.input", return_value=""):
					with patch("getpass.getpass", return_value=""):
						with patch("sys.stderr"):
							code = main([])
							self.assertEqual(code, 1)

	@patch("mywhoosh.cli.MyWhooshClient")
	def test_cli_success(self, mock_client_cls: MagicMock) -> None:
		mock_instance = MagicMock()
		mock_instance.get_tasks.return_value = [
			WorkoutTask(
				task_id="1",
				date="2026-10-25",
				name="Test Workout",
				description="Desc",
				tss=50,
				raw={},
			)
		]
		mock_client_cls.return_value = mock_instance

		with patch.dict(
			"os.environ",
			{"MYWHOOSH_USERNAME": "test@user.com", "MYWHOOSH_PASSWORD": "password"},
			clear=True,
		):
			with patch("mywhoosh.cli.load_env_file"):
				with patch("sys.stdout"):
					code = main(["--start-date", "2026-10-25", "--end-date", "2026-10-26"])
					self.assertEqual(code, 0)
					mock_instance.get_tasks.assert_called_once()



if __name__ == "__main__":
	unittest.main()
