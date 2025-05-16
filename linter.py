import json
from fileinput import filename

from dialects import Dialect, NamingDialect, NamingRule, SpaceDialect, Preference, EmptyLineCountDialect
from naming_linter import NamingLinter


class Linter:

    def __init__(self, dialect_filename: str):
        self.dialect = self._get_dialect(dialect_filename)
        self.naming_linter = NamingLinter(self.dialect)

    def do(self, lines: str, filename: str):
        return self.naming_linter.get_errors(lines, filename)

    def _get_dialect(self, dialect_filename: str):
        try:
            with open(dialect_filename, 'r', encoding='utf-8') as file:
                data = json.load(file)

            return self._json_to_dialect(data)
        except FileNotFoundError:
            print(f"Файл не найден: {dialect_filename}")
            return self._get_default_dialect()
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return self._get_default_dialect()

    def _get_default_dialect(self):
        return Dialect(
            naming=NamingDialect(
                classes=NamingRule.CAMEL_CASE_CAPITAL,
                methods=NamingRule.CAMEL_CASE_LOWER,
                variables=NamingRule.CAMEL_CASE_LOWER
            ),
            spaces=SpaceDialect(
                around_operators=Preference.SHOULD_BE,
                around_brackets=Preference.SHOULD_BE,
                after_comma=Preference.SHOULD_BE,
                before_comma=Preference.SHOULD_BE,
                may_be_more_that_one_space=False
            ),
            empty_lines=EmptyLineCountDialect(
                max_empty=2,
                after_method=2,
                after_class=3
            )
        )

    def _json_to_dialect(self, json_str: dict) -> Dialect:
        data = json_str

        naming_data = data["naming"]
        naming = NamingDialect(
            classes=NamingRule(naming_data["classes"]),
            methods=NamingRule(naming_data["methods"]),
            variables=NamingRule(naming_data["variables"])
        )

        spaces_data = data["spaces"]
        spaces = SpaceDialect(
            around_operators=Preference(spaces_data["around_operators"]),
            around_brackets=Preference(spaces_data["around_brackets"]),
            after_comma=Preference(spaces_data["after_comma"]),
            before_comma=Preference(spaces_data["before_comma"]),
            may_be_more_that_one_space=bool(spaces_data["may_be_more_that_one_space"])
        )

        empty_data = data["empty_lines"]
        empty_lines = EmptyLineCountDialect(
            max_empty=int(empty_data["max_empty"]),
            after_method=int(empty_data["after_method"]),
            after_class=int(empty_data["after_class"])
        )

        return Dialect(
            naming=naming,
            spaces=spaces,
            empty_lines=empty_lines
        )