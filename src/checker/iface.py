from src.error_message import ErrorMessage

from abc import ABC, abstractmethod
from typing import List, Final, Union, Iterable, Tuple, Any
from argparse import Namespace
from tokenize import TokenInfo
from ast import Module
from importlib.metadata import version


class Checker(ABC):
	name: str = "flake8-zale"
	version: str = version("flake8-zale")

	error_messages: List[ErrorMessage]
	options: Final[Namespace]

	def __init__(self, options: Namespace) -> None:
		self.error_messages = []
		self.options = options

	@abstractmethod
	def check(self, tokens_or_tree: Union[List[TokenInfo], Module]) -> None: ...
	@abstractmethod
	def __iter__(self) -> Iterable[Tuple[Any, ...]]: ...


class TokensChecker(Checker):
	def __init__(
		self,
		tokens: List[TokenInfo],
		noqa: bool,
		options: Namespace,
		# Useless, but required by flake8 plugin manager
		logical_line: str,
		line_number: int,
		previous_indent_level: int,
		filename: str,
	) -> None:
		super().__init__(options)

		if not noqa:
			self.check(tokens)

	@abstractmethod
	def check(self, tokens: List[TokenInfo]) -> None: ...

	def __iter__(self) -> Iterable[Tuple[Tuple[int, int], str]]:
		return (((i.line_number, i.column), str(i)) for i in self.error_messages)


class TreeChecker(Checker):
	def __init__(self, tree: Module, noqa: bool, options: Namespace) -> None:
		super().__init__(options)

		if not noqa:
			self.check(tree)

	@abstractmethod
	def check(self, tree: Module) -> None: ...

	def __iter__(self) -> Iterable[Tuple[int, int, str, None]]:
		return ((i.line_number, i.column, str(i), None) for i in self.error_messages)
