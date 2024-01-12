from tokenize import tokenize
from io import BytesIO
from codecs import BOM_UTF8

import pytest

from src.checker import ErrorMessage, Checker


class TestErrorMessage:
    def test___init__(self):
        msg = ErrorMessage(1, 11)
        assert msg.line_number == 1 and msg.column == 11

    def test_as_tuple(self):
        msg = ErrorMessage(1, 11)
        assert msg.as_tuple() == ((1, 11), "EZL100 - Spaces are used instead of tabs")

    def test_make_error(self):
        assert ErrorMessage.make_error(100) == "EZL100 - Spaces are used instead of tabs"

        with pytest.raises(KeyError):
            assert ErrorMessage.make_error(0)


class TestChecker:
    @pytest.mark.parametrize(
        "line_number, noqa, source_code, expected_errors",
        [
            (1, False, "", []),
            (1, False, "import math", []),
            (1, False, "\t\t\tvalue = 10", []),
            (7, False, "\t     \tvalue = 10", [ErrorMessage(1, 1)]),
            (15, False, "     # Comment line", [ErrorMessage(1, 0)]),
            (15, True, "     # noqa", []),
            (2, False, "a = [    1, 2, 3,\n    4, 5, 6\n]\n", [ErrorMessage(2, 0)]),
            (2, False, "class Test:\n    attribute1 = 1\n    attribute2 = 2\n", [ErrorMessage(2, 0), ErrorMessage(3, 0)]),
        ],
    )
    def test___init__(self, line_number, noqa, source_code, expected_errors):
        source_code_buffer = BytesIO()
        source_code_buffer.write(BOM_UTF8)
        source_code_buffer.write(source_code.encode())
        source_code_buffer.seek(0)
        tokens = tuple(tokenize(source_code_buffer.readline))[1:]
        checker = Checker('', line_number, noqa, 0, tokens, 'test')
        assert checker.errors == expected_errors

    @pytest.mark.parametrize(
        "error_messages, expected_result",
        [
            ([], []),
            (
                [ErrorMessage(1, 1), ErrorMessage(2, 2)],
                [
                    ((1, 1), ErrorMessage.make_error(100)),
                    ((2, 2), ErrorMessage.make_error(100)),
                ],
            ),
        ],
    )
    def test___iter__(self, error_messages, expected_result):
        checker = Checker(0, 0, False, 0, [], "")
        checker.errors.extend(error_messages)
        assert list(checker) == expected_result
