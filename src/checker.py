from src.error_message import ErrorMessage
from src.sub_checker.indent_type import IndentTypeSubChecker
from src.sub_checker.missed_commas import MissedCommasSubChecker

from typing import List, Iterator, Tuple, List
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
		tokens: List[TokenInfo],
		filename: str,
	) -> None:
		self.error_messages: List[ErrorMessage] = []

		if noqa:
			return

		IndentTypeSubChecker(self.error_messages).check(tokens)
		MissedCommasSubChecker(self.error_messages).check(tokens)

	def __iter__(self) -> Iterator[Tuple[Tuple[int, int], str]]:
		return (i.as_tuple() for i in self.error_messages)
