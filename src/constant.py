from typing import Final, Dict
from enum import Enum


class ErrorCode(Enum):
	INVALID_INDENT = 100


ERROR_PREFIX: Final[str] = "EZL"
ERROR_MESSAGES: Final[Dict[ErrorCode, str]] = {
	ErrorCode.INVALID_INDENT: "Spaces are used instead of tabs",
}
