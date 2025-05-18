import re
from typing import Any

from java_linter.dialects import Dialect, NamingRule
from java_linter.shared import JavaPatterns, ErrorEntry


class NamingLinter:

    def __init__(self, dialect: Dialect):
        self._class_dialect = dialect.naming.classes
        self._method_dialect = dialect.naming.methods
        self._var_dialect = dialect.naming.variables

    def seek_for_errors(self, lines: list[str], filename: str) -> list[Any]:
        errors: list[ErrorEntry] = []
        errors.extend(self._check_class_names(lines, filename))
        errors.extend(self._check_method_names(lines, filename))
        errors.extend(self._check_var_names(lines, filename))
        return errors

    def _check_class_names(self, lines: list[str], filename: str) -> list[Any]:
        errors: list[ErrorEntry] = []

        for i, line in enumerate(lines):
            class_name_match = JavaPatterns.CLASS_PATTERN.search(line)

            if class_name_match:
                class_name = class_name_match.group(1)

                if self._class_dialect == NamingRule.SNAKE_CASE:
                    if not self._check_is_snake_case(class_name):
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=class_name_match.start(1) + 1,
                                message="Имена классов должны быть в snake_case",
                            )
                        )

                else:
                    if "_" in class_name:
                        print(class_name)
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=class_name_match.start(1) + 1,
                                message="Имена классов не должны быть в snake_case"
                            )
                        )

                if self._class_dialect == NamingRule.CAMEL_CASE_CAPITAL:
                    if not class_name[0].isupper():
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=class_name_match.start(1) + 1,
                                message="Имена классов должны начинаться с заглавной буквы"
                            )
                        )

                elif self._class_dialect == NamingRule.CAMEL_CASE_LOWER:
                    if not class_name[0].islower():
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=class_name_match.start(1) + 1,
                                message="Имена классов должны начинаться со строчной буквы"
                            )
                        )

        return errors

    def _check_method_names(self, lines: list[str], filename: str) -> list[Any]:
        errors: list[ErrorEntry] = []

        for i, line in enumerate(lines):

            method_name_match = JavaPatterns.METHOD_PATTERN.search(line)

            if method_name_match and "(" in line and ")" in line:
                method_name = method_name_match.group(2)

                if self._method_dialect == NamingRule.SNAKE_CASE:
                    if not self._check_is_snake_case(method_name):
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=method_name_match.start(2) + 1,
                                message="Имена методов должны быть в snake_case",
                            )
                        )

                else:
                    if "_" in method_name:
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=method_name_match.start(2) + 1,
                                message="Имена методов не должны быть в snake_case"
                            )
                        )

                if self._method_dialect == NamingRule.CAMEL_CASE_CAPITAL:
                    if not method_name[0].isupper():
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=method_name_match.start(2) + 1,
                                message="Имена методов должны начинаться с заглавной буквы"
                            )
                        )

                elif self._method_dialect == NamingRule.CAMEL_CASE_LOWER:
                    if not method_name[0].islower():
                        errors.append(
                            ErrorEntry(
                                file_name=filename,
                                line=i + 1,
                                column=method_name_match.start(2) + 1,
                                message="Имена методов должны начинаться со строчной буквы",
                            )
                        )

        return errors

    def _check_var_names(self, lines: list[str], filename: str) -> list[Any]:
        errors: list[ErrorEntry] = []

        for i, line in enumerate(lines):

            variable_declaration_match = JavaPatterns.VAR_PATTERN.search(line)
            if variable_declaration_match:

                variable_name = variable_declaration_match.group(2)

                if variable_declaration_match.group(1) not in (
                        "class",
                        "return",
                        "for",
                        "switch",
                        "case",
                        "if",
                        "extends",
                        "import",
                        "package",
                ):

                    if self._var_dialect == NamingRule.SNAKE_CASE:
                        if not self._check_is_snake_case(variable_name):
                            errors.append(
                                ErrorEntry(
                                    file_name=filename,
                                    line=i + 1,
                                    column=variable_declaration_match.start(2) + 1,
                                    message="Имена переменных должны быть в snake_case"
                                )
                            )

                    else:
                        if "_" in variable_name:
                            errors.append(
                                ErrorEntry(
                                    file_name=filename,
                                    line=i + 1,
                                    column=variable_declaration_match.start(2) + 1,
                                    message="Имена переменных не должны быть в snake_case"
                                )
                            )

                    if self._var_dialect == NamingRule.CAMEL_CASE_CAPITAL:
                        if not variable_name[0].isupper():
                            errors.append(
                                ErrorEntry(
                                    file_name=filename,
                                    line=i + 1,
                                    column=variable_declaration_match.start(2) + 1,
                                    message="Имена переменных должны начинаться с заглавной буквы"
                                )
                            )

                    elif self._var_dialect == NamingRule.CAMEL_CASE_LOWER:

                        if not variable_name[0].islower():
                            errors.append(
                                ErrorEntry(
                                    file_name=filename,
                                    line=i + 1,
                                    column=variable_declaration_match.start(2) + 1,
                                    message="Имена переменных должны начинаться со строчной буквы"
                                )
                            )

        return errors

    def _check_is_snake_case(self, name: str) -> bool:
        """
        Проверяет, соответствует ли имя класса соглашению snake_case

        Args:
            name (str): Имя класса для проверки (без слова 'class' и двоеточия)

        Returns:
            bool: True если имя валидно, False если нет
        """
        name = name.strip()

        if not re.fullmatch(r"^[a-z][a-z0-9_]*[a-z0-9]$", name):
            return False

        if "__" in name:
            return False

        parts = name.split("_")
        for part in parts[1:]:
            if not part or not part[0].isalpha():
                return False

        return True
