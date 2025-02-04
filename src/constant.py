from typing import Final, Dict, Set
from enum import Enum
from tokenize import NEWLINE, NL


class ErrorCode(Enum):
	INVALID_INDENT = 100
	INVALID_PARAM_INDENT = 101
	MISSED_COMMA = 200
	INVALID_SHORT_DOCSTRING = 300
	LINES_AROUND_DOCSTRING = 301
	INVALID_IMPORT_ORDER = 900
	MIXED_IMPORT = 901


ERROR_PREFIX: Final[str] = "EZL"
ERROR_MESSAGES: Final[Dict[ErrorCode, str]] = {
	ErrorCode.INVALID_INDENT: "Spaces are used instead of tabs",
	ErrorCode.INVALID_PARAM_INDENT: "Parameter indents should be no more than 1 level",
	ErrorCode.MISSED_COMMA: "Missing trailing comma in multiline collection",
	ErrorCode.INVALID_IMPORT_ORDER: "Invalid package import order",
	ErrorCode.MIXED_IMPORT: "Libraries from different sources are imported in one statement",
	ErrorCode.INVALID_SHORT_DOCSTRING: "Incorrect formatting of one-line docstring",
	ErrorCode.LINES_AROUND_DOCSTRING: "There should be no empty lines around docstring",
}

BRACKETS_CLOSE: Final[Set[str]] = {")", "}", "]"}

NL_TOKEN_TYPES: Final[Set[int]] = {NEWLINE, NL}

COMMA: Final[str] = ","

TAB_SIZE: Final[int] = 8
