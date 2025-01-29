from src.error_message import ErrorMessage, ErrorCode

from typing import Iterable, Iterator, Tuple, List
from importlib.metadata import version
from tokenize import TokenInfo


class Checker:
	name: str = 'flake8-zale'
	version: str = version('flake8-zale')

	error_messages: List[ErrorMessage]

	def __init__(
		self,
		logical_line: str,
		line_number: int,
		noqa: bool,
		previous_indent_level: int,
		tokens: Iterable[TokenInfo],
		filename: str,
	) -> None:
		self.error_messages: List[ErrorMessage] = []

		if noqa:
			return

		self.check_indents(tokens)

	def __iter__(self) -> Iterator[Tuple[Tuple[int, int], str]]:
		return (i.as_tuple() for i in self.error_messages)

	def check_indents(self, tokens: Iterable[TokenInfo]) -> None:
		prev_line = ("", 0)

		for token in tokens:
			if prev_line == (token.line, token.start[0]):
				continue

			for index, char in enumerate(token.line):
				if not char.isspace():
					break
				elif char == ' ':
					self.error_messages.append(ErrorMessage(ErrorCode.INVALID_INDENT, token.start[0], index))
					break

			prev_line = (token.line, token.start[0])
