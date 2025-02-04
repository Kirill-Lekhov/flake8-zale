from src.checker.iface import TokensChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode, TAB_SIZE

from tokenize import INDENT, DEDENT, ENCODING
from typing import Final, FrozenSet


DEFINITIONS: Final[FrozenSet[str]] = frozenset(("def", "class"))
INDENT_CHARS: Final[FrozenSet[str]] = frozenset(" \t")
SKIPPED_TOKEN_TYPES: Final[FrozenSet[int]] = frozenset((DEDENT, ENCODING, INDENT))


class ParamIndentChecker(TokensChecker):
	def check(self, tokens):
		for token in tokens:
			if token.type in SKIPPED_TOKEN_TYPES:
				continue
			elif token.string in DEFINITIONS:
				break
			else:
				return

		if self.indent_char == " ":
			base_indent_level = self.indent_level
		elif self.indent_char == "\t":
			base_indent_level = self.indent_level // TAB_SIZE
		else:
			if self.indent_level:
				raise RuntimeError(f"Unknown indent char: {self.indent_char}")
			else:
				base_indent_level = 0

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
