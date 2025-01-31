from src.sub_checker.iface import SubChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode, BRACKETS_CLOSE, NL_TOKEN_TYPES, COMMA


class MissedCommasSubChecker(SubChecker):
	def check(self, tokens):
		is_block = False
		is_multiline_block = False
		comma_exists = False

		for token in reversed(tokens):
			if is_block:
				if token.type in NL_TOKEN_TYPES:
					is_multiline_block = True
					continue
				elif token.string == COMMA:
					comma_exists = True
					continue
				elif is_multiline_block and not comma_exists:
					self.error_messages.append(ErrorMessage(ErrorCode.MISSED_COMMA, *token.end))

				is_block = False
				is_multiline_block = False
				comma_exists = False

			if token.string in BRACKETS_CLOSE:
				is_block = True
