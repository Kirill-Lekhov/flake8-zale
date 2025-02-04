from src.checker.tab_indentation import TabIndentationChecker
from src.constant import ErrorCode

from typing import Optional, List
from tokenize import TokenInfo, tokenize
from argparse import Namespace
from io import BytesIO
from codecs import BOM_UTF8


def make_checker(tokens: Optional[List[TokenInfo]] = None) -> TabIndentationChecker:
	return TabIndentationChecker(tokens or [], False, Namespace(), "", 0, "", 0, "\t")


class TestTabIndentationChecker:
	def test_check__without_tokens(self):
		checker = make_checker()
		assert len(checker.error_messages) == 0

	def test_check__without_errors(self):
		source_code_buffer = BytesIO(BOM_UTF8)
		source_code_buffer.write("""\
class Console:
	def say_hello():
		print("Hello World")
""".encode())
		source_code_buffer.seek(0)

		checker = make_checker(list(tokenize(source_code_buffer.readline)))
		assert len(checker.error_messages) == 0

	def test_check__with_errors(self):
		source_code_buffer = BytesIO(BOM_UTF8)
		source_code_buffer.write("""\
class Console:
    def say_hello():
        print("Hello World")
""".encode())
		source_code_buffer.seek(0)

		checker = make_checker(list(tokenize(source_code_buffer.readline)))
		assert len(checker.error_messages) == 2
		assert checker.error_messages[0].error_code is ErrorCode.INVALID_INDENT
		assert checker.error_messages[0].line_number == 2
		assert checker.error_messages[0].column == 0

		assert checker.error_messages[1].error_code is ErrorCode.INVALID_INDENT
		assert checker.error_messages[1].line_number == 3
		assert checker.error_messages[1].column == 0
