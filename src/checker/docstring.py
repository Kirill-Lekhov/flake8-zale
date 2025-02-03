from src.checker.iface import LinesChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode

from typing import Final, Tuple, Collection
from enum import IntEnum


DEF_STATEMENTS: Final[Tuple[str, ...]] = ("def", "class")
DOCSTRING_QUOTES: Final[Tuple[str, ...]] = ("'''", '"""')


class State(IntEnum):
	NONE = 0
	IN_DEF = 1
	IN_DOC = 2
	AFTER_DOC = 3

	def one_of(self, states: Collection["State"]) -> bool:
		return any(map(lambda x: self is x, states))


class DocstringChecker(LinesChecker):
	def check(self, lines):
		state = State.NONE
		last_state = State.NONE
		nl_before_doc = False

		for line_num, line_text in enumerate(lines, 1):
			clean_line = line_text.strip()
			last_state = state

			if state.one_of((State.NONE, State.AFTER_DOC, State.IN_DEF)) and clean_line.startswith(DEF_STATEMENTS):
				state = State.IN_DEF
				nl_before_doc = False

			if state is State.IN_DEF and not clean_line:
				nl_before_doc = True

			if state is State.IN_DEF and clean_line.startswith(DOCSTRING_QUOTES):
				state = State.IN_DOC

				if nl_before_doc:
					self.error_messages.append(ErrorMessage(ErrorCode.LINES_AROUND_DOCSTRING, line_num - 1, 0))

				if clean_line.lstrip("'\""):
					self.error_messages.append(ErrorMessage(ErrorCode.INVALID_SHORT_DOCSTRING, line_num, 0))

				if clean_line.endswith(DOCSTRING_QUOTES) and clean_line.rstrip("'\""):		# one line case
					state = State.AFTER_DOC

				continue

			if state is State.IN_DOC and clean_line.endswith(DOCSTRING_QUOTES):
				state = State.AFTER_DOC

				if clean_line.rstrip("'\"") and last_state is not State.IN_DEF:
					self.error_messages.append(ErrorMessage(ErrorCode.INVALID_SHORT_DOCSTRING, line_num, 0))

			if state is State.AFTER_DOC:
				if not clean_line:
					self.error_messages.append(ErrorMessage(ErrorCode.LINES_AROUND_DOCSTRING, line_num, 0))
