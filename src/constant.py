from typing import Final, Dict, Set
from enum import Enum
from tokenize import NEWLINE, NL


class ErrorCode(Enum):
	INVALID_INDENT = 100
	MISSED_COMMA = 200


ERROR_PREFIX: Final[str] = "EZL"
ERROR_MESSAGES: Final[Dict[ErrorCode, str]] = {
	ErrorCode.INVALID_INDENT: "Spaces are used instead of tabs",
	ErrorCode.MISSED_COMMA: "Missing trailing comma in multiline collection",
}

BRACKETS_CLOSE: Final[Set[str]] = {")", "}", "]"}

NL_TOKEN_TYPES: Final[Set[int]] = {NEWLINE, NL}

COMMA: Final[str] = ","
