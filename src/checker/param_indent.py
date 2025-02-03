from src.checker.iface import TokensChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode

from tokenize import INDENT, DEDENT
from typing import Final, FrozenSet


DEFINITIONS: Final[FrozenSet[str]] = frozenset(("def", "class"))
INDENT_CHARS: Final[FrozenSet[str]] = frozenset(" \t")


class ParamIndentChecker(TokensChecker):
	def check(self, tokens):
		base_indent_level = 0

		for token in tokens:
			if token.type == INDENT:
				base_indent_level += 1
			elif token.type == DEDENT:
				continue
			elif token.string in DEFINITIONS:
				break
			else:
				return

		prev_line = None

		for token in tokens:
			if token.line == prev_line:
				continue

			line_indent_level = 0
			line_indent_char = None

			for char in token.line:
				if char in INDENT_CHARS:
					line_indent_level += 1
					line_indent_char = char
				else:
					break

			if line_indent_char == " " and (line_indent_level - base_indent_level) / 4 > 1:
				self.error_messages.append(ErrorMessage(ErrorCode.INVALID_PARAM_INDENT, *token.start))

			elif line_indent_char == "\t" and line_indent_level - base_indent_level > 1:
				self.error_messages.append(ErrorMessage(ErrorCode.INVALID_PARAM_INDENT, *token.start))

			prev_line = token.line
