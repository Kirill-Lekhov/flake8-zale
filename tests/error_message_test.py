from src.error_message import ErrorMessage, ErrorCode


class TestErrorMessage:
	def test___init__(self):
		msg = ErrorMessage(ErrorCode.INVALID_INDENT, 1, 11)
		assert msg.line_number == 1 and msg.column == 11

	def test_as_tuple(self):
		msg = ErrorMessage(ErrorCode.INVALID_INDENT, 1, 11)
		assert msg.as_tuple() == ((1, 11), "EZL100 - Spaces are used instead of tabs")
