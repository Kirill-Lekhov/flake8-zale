from src.checker.docstring import State, DocstringChecker
from src.constant import ErrorCode

from argparse import Namespace
from ast import Module
from typing import Optional, List


class TestState:
	def test_one_of(self):
		assert not State.AFTER_DOC.one_of(())
		assert not State.AFTER_DOC.one_of((State.NONE, State.IN_DEF, State.IN_DOC))
		assert State.AFTER_DOC.one_of((State.AFTER_DOC, ))
		assert State.AFTER_DOC.one_of((State.AFTER_DOC, State.NONE, State.IN_DEF, State.IN_DOC))


def make_checker(lines: Optional[List[str]] = None) -> DocstringChecker:
	return DocstringChecker(
		lines or [],
		False,
		Namespace(),
		Module([], []),
	)


class TestDocstringChecker:
	def test_check__without_lines(self):
		checker = make_checker([])
		assert checker.error_messages == []

	def test_check__without_errors(self):
		checker = make_checker([
			"class MyClass:\n",
			"\t'''\n",
			"\tClass docstring.\n",
			"\t'''\n",
			"\tdef __init__(self):\n",
			"\t\t'''\n",
			"\t\tThe __init__ method docstring.\n",
			"\t\t'''\n",
			"\t\tpass\n",
		])
		assert checker.error_messages == []

	def test_check__with_short_docstring_errors(self):
		checker = make_checker([
			"class MyClass:\n",
			"\t'''Class docstring.'''\n",
			"\tdef __init__(self):\n",
			"\t\t\"\"\"\n",
			"\t\tThe __init__ method docstring.\"\"\"\n",
			"\t\tpass\n",
			"\tdef method(self):\n",
			"\t\t\"\"\"The method docstring\n",
			"\t\t\"\"\"\n",
			"\t\tpass",
		])

		assert len(checker.error_messages) == 3
		assert checker.error_messages[0].error_code is ErrorCode.INVALID_SHORT_DOCSTRING
		assert checker.error_messages[0].line_number == 2
		assert checker.error_messages[0].column == 0

		assert checker.error_messages[1].error_code is ErrorCode.INVALID_SHORT_DOCSTRING
		assert checker.error_messages[1].line_number == 5
		assert checker.error_messages[1].column == 0

		assert checker.error_messages[2].error_code is ErrorCode.INVALID_SHORT_DOCSTRING
		assert checker.error_messages[2].line_number == 8
		assert checker.error_messages[2].column == 0

	def test_check__with_blank_lines_errors(self):
		checker = make_checker([
			"class MyClass:\n",
			"\t\n",
			"\t'''\n",
			"\tClass docstring.\n",
			"\t'''\n",
			"\t\n",
			"\tdef __init__(self):\n",
			"\t\t\"\"\"\n",
			"\t\tThe __init__ method docstring.",
			"\t\t\"\"\"\n",
			"\t\t\n",
			"\t\tpass\n",
			"\tdef method(self):\n",
			"\t\t\n",
			"\t\t\"\"\"\n",
			"\t\tThe method docstring\n",
			"\t\t\"\"\"\n",
			"\t\tpass",
		])

		assert len(checker.error_messages) == 4
		assert checker.error_messages[0].error_code is ErrorCode.LINES_AROUND_DOCSTRING
		assert checker.error_messages[0].line_number == 2
		assert checker.error_messages[0].column == 0

		assert checker.error_messages[1].error_code is ErrorCode.LINES_AROUND_DOCSTRING
		assert checker.error_messages[1].line_number == 6
		assert checker.error_messages[1].column == 0

		assert checker.error_messages[2].error_code is ErrorCode.LINES_AROUND_DOCSTRING
		assert checker.error_messages[2].line_number == 11
		assert checker.error_messages[2].column == 0

		assert checker.error_messages[3].error_code is ErrorCode.LINES_AROUND_DOCSTRING
		assert checker.error_messages[3].line_number == 14
		assert checker.error_messages[3].column == 0
