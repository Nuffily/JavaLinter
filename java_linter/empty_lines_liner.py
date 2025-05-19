import re

from java_linter.dialects import Dialect
from java_linter.shared import ErrorEntry, JavaPatterns


class EmptyLineLinter:
    """Класс, ищущий синтаксические ошибки в .java файлах, связанные с количеством пустых строк подряд"""

    def __init__(self, dialect: Dialect):
        self._after_class = dialect.empty_lines.after_class
        self._after_method = dialect.empty_lines.after_method
        self._max_empty = dialect.empty_lines.max_empty

    def seek_for_errors(self, lines: list[str], filename: str) -> list[ErrorEntry]:
        """Ищет ошибки в java файле и выдает их в виде списка ErrorEntry"""
        errors = []

        if self._max_empty:
            errors.extend(self._check_consecutive_empty_lines(lines, filename))

        if self._after_class:
            errors.extend(self._check_empty_lines_after_class(lines, filename))

        if self._after_method:
            errors.extend(self._check_empty_lines_after_method(lines, filename))

        return errors

    def _check_consecutive_empty_lines(self, lines: list[str], filename: str) -> list[ErrorEntry]:
        """Проверяет, есть ли в поданных строках подряд идущие более чем n пустые строки."""
        errors = []

        count = 0

        for i, line in enumerate(lines):
            if line.strip() == "":
                count += 1
            else:
                if count > self._max_empty:
                    errors.append(
                        ErrorEntry(
                            file_name=filename,
                            line=i,
                            column=1,
                            message=f"Обнаружено {count} последовательных пустых строк, "
                            f"а должно быть не больше {self._max_empty}",
                        )
                    )
                count = 0

        if count > self._max_empty:
            errors.append(
                ErrorEntry(
                    file_name=filename,
                    line=len(lines),
                    column=1,
                    message=f"Обнаружено {count} последовательных пустых строк, "
                    f"а должно быть не больше {self._max_empty}",
                )
            )

        return errors

    def _check_empty_lines_after_class(self, lines: list[str], filename: str) -> list[ErrorEntry]:
        """Проверяет, стоит ли после каждого класса нужное кол-во пустых строк"""

        errors = []

        count = 0

        for i, line in enumerate(lines):

            if JavaPatterns.CLASS_PATTERN.match(line):

                end = self._look_for_end(lines, i)

                if not end:
                    continue

                for j, line_2 in enumerate(lines[end + 1 :], start=end + 1):

                    if line_2.strip() == "":
                        count += 1
                    else:
                        if count != self._after_class:
                            errors.append(
                                ErrorEntry(
                                    file_name=filename,
                                    line=end + 2,
                                    column=1,
                                    message=f"Обнаружено {count} пустых строк после класса, "
                                    f"а должно быть {self._after_class}",
                                )
                            )

                        break

        return errors

    def _check_empty_lines_after_method(self, lines: list[str], filename: str) -> list[ErrorEntry]:
        """Проверяет, стоит ли после каждого метода нужное кол-во пустых строк"""
        errors = []

        for i, line in enumerate(lines):

            if JavaPatterns.METHOD_PATTERN.match(line) and not re.match(r"^\s*return", line):

                if "{" in line and "}" in line:
                    end = i

                elif "{" in line:
                    end = self._look_for_end(lines, i)

                    if not end:
                        continue

                elif ";" in line:
                    end = i

                else:
                    end = i + 1

                count = 0

                for j, line_2 in enumerate(lines[end + 1 :], start=end + 1):

                    if line_2.strip() == "":
                        count += 1
                    else:
                        if count != self._after_method:
                            errors.append(
                                ErrorEntry(
                                    file_name=filename,
                                    line=end + 2,
                                    column=1,
                                    message=f"Обнаружено {count} пустых строк после метода, "
                                    f"а должно быть {self._after_method}",
                                )
                            )

                        break

        return errors

    def _look_for_end(self, lines: list[str], index: int) -> int:
        """Ищет конец класса/метода начиная с index, находя следующую неоткрытую '}'"""

        open_brackets_count = 1

        for i, line in enumerate(lines[index + 1 :], start=index + 1):
            open_brackets_count += line.count("{")
            open_brackets_count -= line.count("}")

            if open_brackets_count < 1:
                return i

        return 0
