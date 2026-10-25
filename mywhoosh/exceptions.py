class MyWhooshError(Exception):
	"""Base exception for all MyWhoosh errors."""
	pass


class AuthenticationError(MyWhooshError):
	"""Raised when authentication with MyWhoosh fails."""
	pass


class ApiError(MyWhooshError):
	"""Raised when an API request to MyWhoosh fails."""

	def __init__(
		self,
		message: str,
		status_code: int | None = None,
		response: dict | None = None,
	) -> None:
		super().__init__(message)
		self.status_code = status_code
		self.response = response
