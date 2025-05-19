import re
from typing import Any

from java_linter.dialects import Dialect
from java_linter.shared import ErrorEntry


class SpaceLinter:

    def __init__(self, dialect: Dialect):
        self._after_comma = dialect.spaces.after_comma
        self._no_before_comma = dialect.spaces.no_before_comma
        self._no_around_brackets = dialect.spaces.no_around_brackets
        self._around_operators = dialect.spaces.around_operators
        self._may_be_more_that_one_space = dialect.spaces.may_be_more_that_one_space

        self._no_before_dot_comma = dialect.spaces.no_before_dot_comma
        self._no_around_dot = dialect.spaces.no_around_dot

    def seek_for_errors(self, lines: list[str], filename: str) -> list[Any]:
        errors = []

        if self._after_comma:
            errors.extend(self._check_spaces_after_comma(lines, filename))

        if self._no_before_comma:
            errors.extend(self._check_no_spaces_before_comma(lines, filename))

        if self._no_around_brackets:
            errors.extend(self._check_no_spaces_around_brackets(lines, filename))

        if self._around_operators:
            errors.extend(self._check_no_spaces_around_operators(lines, filename))

        if self._no_before_dot_comma:
            errors.extend(self._check_no_spaces_before_dot_comma(lines, filename))

        if self._no_around_dot:
            errors.extend(self._check_no_spaces_around_dot(lines, filename))

        if not self._may_be_more_that_one_space:
            errors.extend(self.check_no_spaces_more_that_one(lines, filename))

        return errors

    def _check_spaces_after_comma(self, lines: list[str], filename: str) -> list[Any]:

        errors = []

        for i, line in enumerate(lines):

            if "," in line:
                for match in re.finditer(r",\S", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start() + 1,
                            message="После запятой должен быть пробел",
                        )
                    )

        return errors

    def check_no_spaces_more_that_one(self, lines: list[str], filename: str) -> list[Any]:

        errors = []

        spaces_match = re.compile(r".*\S\s\s+.*")

        for i, line in enumerate(lines):

            if spaces_match.match(line):

                for match in re.finditer(r"\S\s\s+", line):

                    if line[match.end()] != "/":
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=match.start() + 1,
                                message="Не должно быть более одного пробела подряд внутри строки",
                            )
                        )

        return errors

    def _check_no_spaces_before_comma(self, lines: list[str], filename: str) -> list[Any]:

        errors = []

        for i, line in enumerate(lines):

            if "," in line:
                for match in re.finditer(r"\s,", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start() + 1,
                            message="Не должно быть пробелов перед запятой",
                        )
                    )

        return errors

    def _check_no_spaces_around_dot(self, lines: list[str], filename: str) -> list[Any]:

        errors = []

        for i, line in enumerate(lines):

            if "." in line:
                for match in re.finditer(r"\s\.", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start() + 1,
                            message="Не должно быть пробелов перед точкой",
                        )
                    )
                for match in re.finditer(r"\.\s", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start() + 1,
                            message="После точки не должен быть пробел",
                        )
                    )

        return errors

    def _check_no_spaces_before_dot_comma(self, lines: list[str], filename: str) -> list[Any]:

        errors = []

        for i, line in enumerate(lines):

            if ";" in line:
                for match in re.finditer(r"\s;", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start() + 1,
                            message="Не должно быть пробелов перед точкой с запятой",
                        )
                    )

        return errors

    def _check_no_spaces_around_brackets(self, lines: list[str], filename: str) -> list[Any]:

        errors = []

        for i, line in enumerate(lines):

            if "(" in line:
                for match in re.finditer(r"(\w+)\s+(\()", line):
                    if match.group(1) not in ("while", "for", "do", "if", "case", "switch", "catch"):
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=match.start(2),
                                message="Перед открывающейся скобкой не должно быть пробела",
                            )
                        )

                for match in re.finditer(r"(\(\s)", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start(1) + 2,
                            message="После открывающейся скобкой не должно быть пробела",
                        )
                    )

            if ")" in line:
                for match in re.finditer(r"\S\s+(\))", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start(1),
                            message="Перед закрывающейся скобкой не должно быть пробела",
                        )
                    )

                for match in re.finditer(r"(\))\w", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start(1),
                            message="После закрывающейся скобки должен быть пробел",
                        )
                    )

            if "{" in line:
                for match in re.finditer(r"\S{", line):
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i + 1,
                            column=match.start() + 1,
                            message="Перед открывающей фигурной скобкой должен быть пробел",
                        )
                    )

        return errors

    def _check_no_spaces_around_operators(self, lines: list[str], filename: str) -> list[Any]:

        errors = []

        operator_pattern = r"==|->|\+|-|\*|/(?:/)|="

        for i, line in enumerate(lines):

            if re.search(operator_pattern, line):
                match = re.search(operator_pattern, line)

                if match:
                    start = match.start()
                    end = match.end()

                    if not (line[start - 1].isspace() and line[end].isspace()):
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=start + 1,
                                message="Операторы должны быть окружены пробелами",
                            )
                        )

        return errors
