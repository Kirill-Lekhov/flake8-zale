from src.checker.param_indent import ParamIndentChecker
from src.constant import ErrorCode

from argparse import Namespace
from tokenize import tokenize, TokenInfo
from typing import Optional, List
from io import BytesIO
from codecs import BOM_UTF8

import pytest


def make_checker(
	tokens: Optional[List[TokenInfo]] = None,
	indent_level: int = 0,
	indent_char: Optional[str] = "\t",
) -> ParamIndentChecker:
	return ParamIndentChecker(tokens or [], False, Namespace(), "", 0, "", indent_level, indent_char)


class TestParamIndentChecker:
	def test_check__without_tokens(self):
		checker = make_checker()

		assert len(checker.error_messages) == 0

	def test_check__without_errors(self):
		source_code_buffer = BytesIO()
		source_code_buffer.write(BOM_UTF8)
		source_code_buffer.write("def __init__(self, *args, **kwargs):".encode())
		source_code_buffer.seek(0)
		checker = make_checker(list(tokenize(source_code_buffer.readline)))

		source_code_buffer.truncate(0)
		source_code_buffer.seek(0)
		source_code_buffer.write(BOM_UTF8)
		source_code_buffer.write("pass".encode())
		source_code_buffer.seek(0)
		checker.check(list(tokenize(source_code_buffer.readline)))

		assert len(checker.error_messages) == 0

	def test_check__runtime_errors(self):
		with pytest.raises(RuntimeError, match="Unknown indent char: None"):
			make_checker(indent_char=None, indent_level=100)

	def test_check__with_errors(self):
		source_code_buffer = BytesIO()
		source_code_buffer.write(BOM_UTF8)
		source_code_buffer.write("""\
class C(
		A,
		B,
):
""".encode())
		source_code_buffer.seek(0)
		checker = make_checker(list(tokenize(source_code_buffer.readline)), 0, None)

		source_code_buffer.truncate(0)
		source_code_buffer.seek(0)
		source_code_buffer.write(BOM_UTF8)
		source_code_buffer.write("""\
    def __init__(
            self,
            *args,
            **kwargs,
	):
""".encode())
		source_code_buffer.seek(0)
		checker.indent_char = " "
		checker.indent_level = 4
		checker.check(list(tokenize(source_code_buffer.readline)))

		assert len(checker.error_messages) == 5
		assert checker.error_messages[0].error_code is ErrorCode.INVALID_PARAM_INDENT
		assert checker.error_messages[0].line_number == 2
		assert checker.error_messages[0].column == 2

		assert checker.error_messages[1].error_code is ErrorCode.INVALID_PARAM_INDENT
		assert checker.error_messages[1].line_number == 3
		assert checker.error_messages[1].column == 2

		assert checker.error_messages[2].error_code is ErrorCode.INVALID_PARAM_INDENT
		assert checker.error_messages[2].line_number == 2
		assert checker.error_messages[2].column == 12

		assert checker.error_messages[3].error_code is ErrorCode.INVALID_PARAM_INDENT
		assert checker.error_messages[3].line_number == 3
		assert checker.error_messages[3].column == 12

		assert checker.error_messages[4].error_code is ErrorCode.INVALID_PARAM_INDENT
		assert checker.error_messages[4].line_number == 4
		assert checker.error_messages[4].column == 12
