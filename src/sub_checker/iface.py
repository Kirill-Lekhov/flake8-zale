from src.error_message import ErrorMessage

from abc import ABC, abstractmethod
from typing import List
from tokenize import TokenInfo


class SubChecker(ABC):
	error_messages: List[ErrorMessage]

	def __init__(self, errors_messages: List[ErrorMessage]) -> None:
		self.error_messages = errors_messages

	@abstractmethod
	def check(self, tokens: List[TokenInfo]) -> None: ...
