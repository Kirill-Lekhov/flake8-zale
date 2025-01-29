from src.error_message import ErrorMessage


def cmp_error_messages(a: ErrorMessage, b: ErrorMessage) -> bool:
	return (
		isinstance(a, ErrorMessage) and
		isinstance(b, ErrorMessage) and
		a.error_code is b.error_code and
		a.line_number == b.line_number and
		a.column == b.column
	)
