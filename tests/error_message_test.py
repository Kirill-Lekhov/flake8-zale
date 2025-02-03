from src.error_message import ErrorMessage
from src.constant import ErrorCode, ERROR_MESSAGES, ERROR_PREFIX


class TestErrorMessage:
	def test___init__(self):
		msg = ErrorMessage(ErrorCode.INVALID_INDENT, 12, 11)
		assert msg.error_code is ErrorCode.INVALID_INDENT
		assert msg.line_number == 12
		assert msg.column == 11

	def test___str__(self):
		code = ErrorCode.INVALID_INDENT
		msg = ErrorMessage(code, 12, 11)
		code_msg = ERROR_MESSAGES[code]

		assert str(msg) == f"{ERROR_PREFIX}{code.value} - {code_msg}"
