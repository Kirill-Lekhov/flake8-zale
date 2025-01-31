from src.error_message import ErrorMessage
from src.checker import Checker
from src.constant import ErrorCode
from tests.cmp import cmp_error_messages

from tokenize import tokenize
from io import BytesIO
from codecs import BOM_UTF8

import pytest


class TestChecker:
	@pytest.mark.parametrize(
		"line_number, noqa, source_code, expected_errors",
		[
			(1, False, "", []),
			(1, False, "import math", []),
			(1, False, "\t\t\tvalue = 10", []),
			(7, False, "\t     \tvalue = 10", [ErrorMessage(ErrorCode.INVALID_INDENT, 1, 1)]),
			(15, False, "     # Comment line", [ErrorMessage(ErrorCode.INVALID_INDENT, 1, 0)]),
			(15, True, "     # noqa", []),
			(
				2,
				False,
				"a = [    1, 2, 3,\n    4, 5, 6\n]\n",
				[
					ErrorMessage(ErrorCode.INVALID_INDENT, 2, 0),
					ErrorMessage(ErrorCode.MISSED_COMMA, 2, 7),
				],
			),
			(
				2,
				False,
				"class Test:\n    attribute1 = 1\n    attribute2 = 2\n",
				[
					ErrorMessage(ErrorCode.INVALID_INDENT, 2, 0),
					ErrorMessage(ErrorCode.INVALID_INDENT, 3, 0),
				],
			),
		],
	)
	def test___init__(self, line_number, noqa, source_code, expected_errors):
		source_code_buffer = BytesIO()
		source_code_buffer.write(BOM_UTF8)
		source_code_buffer.write(source_code.encode())
		source_code_buffer.seek(0)
		tokens = list(tokenize(source_code_buffer.readline))[1:]
		checker = Checker('', line_number, noqa, 0, tokens, 'test')

		assert len(checker.error_messages) == len(expected_errors)

		for checker_error, expected_error in zip(checker.error_messages, expected_errors):
			cmp_error_messages(checker_error, expected_error)

	@pytest.mark.parametrize(
		"error_messages, expected_result",
		[
			([], []),
			(
				[ErrorMessage(ErrorCode.INVALID_INDENT, 1, 1), ErrorMessage(ErrorCode.INVALID_INDENT, 2, 2)],
				[
					((1, 1), f"EZL100 - Spaces are used instead of tabs"),
					((2, 2), f"EZL100 - Spaces are used instead of tabs"),
				],
			),
		],
	)
	def test___iter__(self, error_messages, expected_result):
		checker = Checker("0", 0, False, 0, [], "")
		checker.error_messages.extend(error_messages)
		assert list(checker) == expected_result
