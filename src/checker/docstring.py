from src.checker.iface import LinesChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode

from typing import Final, Tuple, FrozenSet, List


DEF_STATEMENTS: Final[Tuple[str, ...]] = ("def", "class")
DOCSTRING_QUOTES: Final[Tuple[str, ...]] = ("'''", '"""')
INDENT_CHARS: Final[FrozenSet[str]] = frozenset(" \t")


class LinesIterator:
	def __init__(self, lines: List[str]) -> None:
		self.lines = lines
		self.count = len(lines)
		self.ptr = 0

	def __next__(self):
		try:
			return self.lines[self.ptr]
		except IndexError:
			raise StopIteration()
		finally:
			self.ptr += 1


class DocstringChecker(LinesChecker):
	def check(self, lines):
		lines_iterator = LinesIterator(lines)

		while lines_iterator.ptr < lines_iterator.count:
			clean_line = next(lines_iterator).strip()

			if clean_line.startswith(DEF_STATEMENTS):
				clean_line = next(lines_iterator).strip()
				empty_line_before = not clean_line

				# Skip all empty lines
				while not clean_line:
					clean_line = next(lines_iterator).strip()

				if clean_line.startswith(DOCSTRING_QUOTES):
					if empty_line_before:
						self.error_messages.append(
							ErrorMessage(ErrorCode.LINES_AROUND_DOCSTRING, lines_iterator.ptr - 1, 0),
						)

					if clean_line.lstrip("'\""):
						self.error_messages.append(
							ErrorMessage(ErrorCode.INVALID_SHORT_DOCSTRING, lines_iterator.ptr, 0),
						)

						if clean_line.endswith(DOCSTRING_QUOTES):
							continue

					clean_line = next(lines_iterator).strip()

					# Skip docstring body
					while not clean_line.endswith(DOCSTRING_QUOTES):
						clean_line = next(lines_iterator).strip()

					if clean_line.rstrip("'\""):
						self.error_messages.append(
							ErrorMessage(ErrorCode.INVALID_SHORT_DOCSTRING, lines_iterator.ptr, 0),
						)

					if not next(lines_iterator).strip():
						self.error_messages.append(
							ErrorMessage(ErrorCode.LINES_AROUND_DOCSTRING, lines_iterator.ptr, 0),
						)
