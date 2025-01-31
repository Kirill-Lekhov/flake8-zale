from src.sub_checker.iface import SubChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode


class IndentTypeSubChecker(SubChecker):
	def check(self, tokens):
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
