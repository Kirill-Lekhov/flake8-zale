from src.checker.docstring import DocstringChecker, LinesIterator
from src.constant import ErrorCode

from argparse import Namespace
from ast import Module
from typing import Optional, List

import pytest


def make_checker(lines: Optional[List[str]] = None) -> DocstringChecker:
	return DocstringChecker(
		lines or [],
		False,
		Namespace(),
		Module([], []),
	)


class TestLinesIterator:
	def test___init__(self):
		iterator = LinesIterator([])
		assert iterator.lines == []
		assert iterator.count == 0
		assert iterator.ptr == 0

		iterator = LinesIterator(["1", "2", "3"])
		assert iterator.lines == ["1", "2", "3"]
		assert iterator.count == 3
		assert iterator.ptr == 0

	def test___next__(self):
		iterator = LinesIterator(["1"])
		assert next(iterator) == "1"
		assert iterator.ptr == 1

		with pytest.raises(StopIteration):
			next(iterator)

		assert iterator.ptr == 2


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
			"\n",
			"\n",
			"def main():\n",
			"\tpass\n",
			"\n",
			"\n",
			"'''\n",
			"Not docstring, just multiline comment\n",
			"'''\n",
			"def test(): ...\n",
		])
		assert checker.error_messages == []

		checker = make_checker([
			"class MyClass:\n",
			"\tdef __init__(self):\n",
			"\t\tpass\n",
			"\n",
			"\n",
			"def main():\n",
			"\tpass\n",
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
