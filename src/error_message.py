from src.constant import ERROR_PREFIX, ERROR_MESSAGES, ErrorCode

from typing import Tuple


class ErrorMessage:
	line_number: int
	column: int
	error_code: ErrorCode

	def __init__(self, error_code: ErrorCode, line_number: int, column: int):
		self.error_code = error_code
		self.line_number = line_number
		self.column = column

	def as_tuple(self) -> Tuple[Tuple[int, int], str]:
		return (
			(self.line_number, self.column),
			f"{ERROR_PREFIX}{self.error_code.value} - {ERROR_MESSAGES.get(self.error_code)}"
		)
