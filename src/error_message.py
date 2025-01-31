from src.constant import ERROR_PREFIX, ERROR_MESSAGES, ErrorCode


class ErrorMessage:
	line_number: int
	column: int
	error_code: ErrorCode

	def __init__(self, error_code: ErrorCode, line_number: int, column: int):
		self.error_code = error_code
		self.line_number = line_number
		self.column = column

	def __str__(self) -> str:
		return f"{ERROR_PREFIX}{self.error_code.value} - {ERROR_MESSAGES.get(self.error_code)}"
