from typing import Iterable, Iterator, Tuple, Final, Dict
from importlib.metadata import version


class ErrorMessage:
    ERRORS: Final[Dict[int, str]] = {
        100: "Spaces are used instead of tabs",
    }

    line_number: int
    column: int

    def __init__(self, line_number, column):
        self.line_number = line_number
        self.column = column

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, self.__class__)
            and self.line_number == __value.line_number
            and self.column == __value.column
        )

    def as_tuple(self) -> Tuple[Tuple[int, int], str]:
        return (self.line_number, self.column), self.make_error(100)

    @classmethod
    def make_error(cls, code: int) -> str:
        return f"EZL{code} - {cls.ERRORS[code]}"


class Checker:
    name: str = 'flake8-zale'
    version: str = version('flake8-zale')

    errors: Iterable[Tuple[int, str]]

    def __init__(
        self,
        logical_line: str,
        line_number: int,
        noqa: bool,
        previous_indent_level: int,
        tokens: Iterable,
        filename: str,
    ) -> None:
        self.errors = []

        if noqa or not tokens:
            return

        for index, char in enumerate(tokens[0].line):
            if not char.isspace():
                break
            elif char == ' ':
                self.errors.append(ErrorMessage(line_number, index))
                break

    def __iter__(self) -> Iterator[Tuple[Tuple[int, int], str]]:
        return (i.as_tuple() for i in self.errors)
