import json
from typing import Any

from java_linter.dialects import Dialect, EmptyLineCountDialect, NamingDialect, NamingRule, SpaceDialect
from java_linter.empty_lines_liner import EmptyLineLinter
from java_linter.naming_linter import NamingLinter
from java_linter.shared import ErrorEntry
from java_linter.space_linter import SpaceLinter


class Linter:
    """Джава линтер, который ищет ошибки в поданном файле, основываясь на стиле кода, указанном в Dialect"""

    def __init__(self, dialect_filename="", dialect: Dialect | None = None):
        """При отсутствии dialect_filename использует свой базовый"""

        self._dialect = dialect if dialect else self._get_dialect(dialect_filename)

        self._naming_linter = NamingLinter(self._dialect)
        self._empty_line_linter = EmptyLineLinter(self._dialect)
        self._space_linter = SpaceLinter(self._dialect)

    def seek_for_errors(self, lines: list[str], filename: str) -> list[ErrorEntry]:
        """Использует seek_for_errors в каждом подлинтере и возвращает объединение их результатов"""
        errors = []
        errors.extend(self._naming_linter.seek_for_errors(lines, filename))
        errors.extend(self._empty_line_linter.seek_for_errors(lines, filename))
        errors.extend(self._space_linter.seek_for_errors(lines, filename))
        return errors

    def _get_dialect(self, dialect_filename: str) -> Dialect:
        """
        Возвращает экземпляр Dialect из json'а по заданному пути или из _get_default_dialect если прочтение не удалось
        """

        if not dialect_filename:
            return self._get_default_dialect()

        try:
            with open(dialect_filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            return self._json_to_dialect(data)
        except FileNotFoundError:
            print(f"Файл не найден: {dialect_filename}")
            return self._get_default_dialect()
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return self._get_default_dialect()

    def _get_default_dialect(self) -> Dialect:
        """Возвращает Dialect с базовыми значениями"""
        return Dialect(
            naming=NamingDialect(
                classes=NamingRule.CAMEL_CASE_CAPITAL,
                methods=NamingRule.CAMEL_CASE_LOWER,
                variables=NamingRule.CAMEL_CASE_LOWER,
            ),
            spaces=SpaceDialect(
                around_operators=True,
                no_around_brackets=True,
                after_comma=True,
                no_before_comma=True,
                no_around_dot=True,
                no_before_dot_comma=True,
                may_be_more_that_one_space=False,
            ),
            empty_lines=EmptyLineCountDialect(max_empty=3, after_method=1, after_class=2),
        )

    def _json_to_dialect(self, data: dict[str, Any]) -> Dialect:
        """Собирает экземпляр Dialect из полученного json'а-словаря"""

        naming_data = data["naming"]
        naming = NamingDialect(
            classes=NamingRule(naming_data["classes"]),
            methods=NamingRule(naming_data["methods"]),
            variables=NamingRule(naming_data["variables"]),
        )

        spaces_data = data["spaces"]
        spaces = SpaceDialect(
            around_operators=spaces_data["around_operators"],
            no_around_brackets=spaces_data["no_around_brackets"],
            after_comma=spaces_data["after_comma"],
            no_before_comma=spaces_data["no_before_comma"],
            no_around_dot=spaces_data["no_around_dot"],
            no_before_dot_comma=spaces_data["no_before_dot_comma"],
            may_be_more_that_one_space=bool(spaces_data["may_be_more_that_one_space"]),
        )

        empty_data = data["empty_lines"]
        empty_lines = EmptyLineCountDialect(
            max_empty=int(empty_data["max_empty"]),
            after_method=int(empty_data["after_method"]),
            after_class=int(empty_data["after_class"]),
        )

        return Dialect(naming=naming, spaces=spaces, empty_lines=empty_lines)
