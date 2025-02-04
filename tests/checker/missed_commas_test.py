from src.checker.missed_commas import MissedCommasChecker
from src.constant import ErrorCode

from io import BytesIO
from typing import Optional, List
from tokenize import TokenInfo, tokenize
from argparse import Namespace
from codecs import BOM_UTF8


def make_checker(tokens: Optional[List[TokenInfo]] = None):
	return MissedCommasChecker(tokens or [], False, Namespace(), "", 0, "", 0, "\t")


class TestMissedCommasChecker:
	def test_checker__without_tokens(self):
		checker = make_checker()
		assert len(checker.error_messages) == 0

	def test_checker__without_errors(self):
		source_code_buffer = BytesIO()
		source_code_buffer.write(BOM_UTF8)
		source_code_buffer.write("""\
from random import (
	choice,
	randint,
)

MATRIX = [
	(1, 2, 3),
	[4, 5, 6],
	{7, 8, 9},
	{
		"key1": "value1",
		"key2": "value2",
		"key3": "value3",
	},
]


class A:
	pass


class B:
	pass


class C(
	A,
	B,
	# D,
):
	def __init__(
		self,
		*args,
		**kwargs,
	)
		pass
""".encode())
		source_code_buffer.seek(0)
		checker = make_checker(list(tokenize(source_code_buffer.readline)))
		assert len(checker.error_messages) == 0

	def test_checker__with_errors(self):
		source_code_buffer = BytesIO()
		source_code_buffer.write(BOM_UTF8)
		source_code_buffer.write("""\
from random import (
	choice,
	randint
)

MATRIX = [
	(1, 2, 3),
	[
		4,
		5,
		6
	],
	{7, 8, 9},
	{
		"key1": "value1",
		"key2": "value2",
		"key3": "value3"
	}
]


class A:
	pass


class B:
	pass


class C(
	A,
	B
):
	def __init__(
		self,
		*args,
		**kwargs
	)
		pass
""".encode())
		source_code_buffer.seek(0)
		checker = make_checker(list(tokenize(source_code_buffer.readline)))
		assert len(checker.error_messages) == 6

		assert checker.error_messages[0].error_code == ErrorCode.MISSED_COMMA
		assert checker.error_messages[0].line_number == 3
		assert checker.error_messages[0].column == 8

		assert checker.error_messages[1].error_code == ErrorCode.MISSED_COMMA
		assert checker.error_messages[1].line_number == 11
		assert checker.error_messages[1].column == 3

		assert checker.error_messages[2].error_code == ErrorCode.MISSED_COMMA
		assert checker.error_messages[2].line_number == 17
		assert checker.error_messages[2].column == 18

		assert checker.error_messages[3].error_code == ErrorCode.MISSED_COMMA
		assert checker.error_messages[3].line_number == 18
		assert checker.error_messages[3].column == 2

		assert checker.error_messages[4].error_code == ErrorCode.MISSED_COMMA
		assert checker.error_messages[4].line_number == 32
		assert checker.error_messages[4].column == 2

		assert checker.error_messages[5].error_code == ErrorCode.MISSED_COMMA
		assert checker.error_messages[5].line_number == 37
		assert checker.error_messages[5].column == 10
