from src.checker.iface import Checker, TokensChecker, LinesChecker, TreeChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode

from argparse import Namespace
from ast import Module


class TestChecker:
	def test___init__(self):
		class FakeChecker(Checker):
			def check(self, tokens_or_tree):
				pass

			def __iter__(self):
				return iter([])

		ns = Namespace()
		checker = FakeChecker(ns)
		assert checker.options is ns
		assert checker.error_messages == []


class TestTokensChecker:
	def test___init__(self):
		last_checked_tokens = None


		class FakeTokensChecker(TokensChecker):
			def check(self, tokens):
				nonlocal last_checked_tokens
				last_checked_tokens = tokens


		ns = Namespace()
		checker = FakeTokensChecker(
			[6, 2, 3],		# type: ignore - for testing purposes
			False,
			ns,
			"LOGICAL_LINE",
			15,
			"FILENAME",
		)
		assert checker.options is ns
		assert last_checked_tokens == [6, 2, 3]

		checker = FakeTokensChecker(
			[7, 1, 7],		# type: ignore - for testing purposes
			True,
			ns,
			"LOGICAL_LINE",
			15,
			"FILENAME",
		)
		assert last_checked_tokens == [6, 2, 3]

	def test___iter__(self):
		class FakeTokensChecker(TokensChecker):
			def check(self, tokens):
				pass


		ns = Namespace()
		checker = FakeTokensChecker(
			[6, 2, 3],		# type: ignore - for testing purposes
			False,
			ns,
			"LOGICAL_LINE",
			15,
			"FILENAME",
		)
		checker.error_messages = [
			ErrorMessage(ErrorCode.INVALID_INDENT, 15, 16),
			ErrorMessage(ErrorCode.INVALID_PARAM_INDENT, 11, 9),
			ErrorMessage(ErrorCode.INVALID_IMPORT_ORDER, 17, 1),
			ErrorMessage(ErrorCode.INVALID_SHORT_DOCSTRING, 19, 10),
		]
		assert list(checker) == [
			((15, 16), str(checker.error_messages[0])),
			((11, 9), str(checker.error_messages[1])),
			((17, 1), str(checker.error_messages[2])),
			((19, 10), str(checker.error_messages[3])),
		]


class TestLinesChecker:
	def test___init__(self):
		last_checked_lines = None


		class FakeLinesChecker(LinesChecker):
			def check(self, lines):
				nonlocal last_checked_lines
				last_checked_lines = lines


		ns = Namespace()
		checker = FakeLinesChecker(
			["LINE1", "LINE2", "LINE3"],
			False,
			ns,
			Module([], []),
		)
		assert checker.options is ns
		assert last_checked_lines == ["LINE1", "LINE2", "LINE3"]

		checker = FakeLinesChecker(
			["LINE4", "LINE5", "LINE6"],
			True,
			ns,
			Module([], []),
		)
		assert last_checked_lines == ["LINE1", "LINE2", "LINE3"]

	def test___iter__(self):
		class FakeLiesChecker(LinesChecker):
			def check(self, lines):
				pass


		ns = Namespace()
		checker = FakeLiesChecker([], False, ns, Module([], []))
		checker.error_messages = [
			ErrorMessage(ErrorCode.INVALID_INDENT, 15, 16),
			ErrorMessage(ErrorCode.INVALID_PARAM_INDENT, 11, 9),
			ErrorMessage(ErrorCode.INVALID_IMPORT_ORDER, 17, 1),
			ErrorMessage(ErrorCode.INVALID_SHORT_DOCSTRING, 19, 10),
		]
		assert list(checker) == [
			(15, 16, str(checker.error_messages[0]), None),
			(11, 9, str(checker.error_messages[1]), None),
			(17, 1, str(checker.error_messages[2]), None),
			(19, 10, str(checker.error_messages[3]), None),
		]


class TestTreeChecker:
	def test___init__(self):
		last_checked_tree = None


		class FakeTreeChecker(TreeChecker):
			def check(self, tree):
				nonlocal last_checked_tree
				last_checked_tree = tree


		ns = Namespace()
		tree = Module([], [])
		checker = FakeTreeChecker(tree, False, ns)
		assert checker.options is ns
		assert last_checked_tree is tree

		checker = FakeTreeChecker(Module([], []), True, ns)
		assert last_checked_tree is tree

	def test___iter__(self):
		class FakeTreeChecker(TreeChecker):
			def check(self, tree):
				pass


		ns = Namespace()
		checker = FakeTreeChecker(Module([], []), False, ns)
		checker.error_messages = [
			ErrorMessage(ErrorCode.INVALID_INDENT, 15, 16),
			ErrorMessage(ErrorCode.INVALID_PARAM_INDENT, 11, 9),
			ErrorMessage(ErrorCode.INVALID_IMPORT_ORDER, 17, 1),
			ErrorMessage(ErrorCode.INVALID_SHORT_DOCSTRING, 19, 10),
		]
		assert list(checker) == [
			(15, 16, str(checker.error_messages[0]), None),
			(11, 9, str(checker.error_messages[1]), None),
			(17, 1, str(checker.error_messages[2]), None),
			(19, 10, str(checker.error_messages[3]), None),
		]
