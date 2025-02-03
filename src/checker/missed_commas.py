from src.checker.iface import TokensChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode, BRACKETS_CLOSE, NL_TOKEN_TYPES, COMMA


class MissedCommasChecker(TokensChecker):
	def check(self, tokens):
		is_block = False
		is_multiline_block = False
		comma_exists = False
		error_messages = []

		for token in reversed(tokens):
			if is_block:
				if token.type in NL_TOKEN_TYPES:
					is_multiline_block = True
					continue
				elif token.string == COMMA:
					comma_exists = True
					continue
				elif is_multiline_block and not comma_exists:
					error_messages.append(ErrorMessage(ErrorCode.MISSED_COMMA, *token.end))

				is_block = False
				is_multiline_block = False
				comma_exists = False

			if token.string in BRACKETS_CLOSE:
				is_block = True

		self.error_messages.extend(reversed(error_messages))
