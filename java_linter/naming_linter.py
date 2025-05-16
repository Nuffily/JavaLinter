import re

from java_linter.dialects import Dialect, NamingRule
from java_linter.shared import JavaPatterns


class NamingLinter:

    def __init__(self, dialect: Dialect):
        self.class_dialect = dialect.naming.classes
        self.method_dialect = dialect.naming.methods
        self.var_dialect = dialect.naming.variables

        self.CLASS_RE = JavaPatterns.CLASS_PATTERN
        self.METHOD_RE = JavaPatterns.METHOD_PATTERN
        self.VAR_RE = JavaPatterns.VAR_PATTERN

    def get_errors(self, lines: list[str], filename: str):
        errors = []
        errors.extend(self.check_class_names(lines, filename))
        errors.extend(self.check_method_names(lines, filename))
        errors.extend(self.check_var_names(lines, filename))
        return errors

    def check_class_names(self, lines: list[str], filename: str):
        errors = []

        for i, line in enumerate(lines):
            class_name_match = self.CLASS_RE.search(line)

            if class_name_match:
                class_name = class_name_match.group(1)

                if self.class_dialect == NamingRule.SNAKE_CASE:
                    if not self.check_is_snake_case(class_name):
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': class_name_match.start(1) + 1,
                            'message': "Имена классов должны быть в snake_case"
                        })

                else:
                    if '_' in class_name:
                        print(class_name)
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': class_name_match.start(1) + 1,
                            'message': "Имена классов не должны быть в snake_case"
                        })

                if self.class_dialect == NamingRule.CAMEL_CASE_CAPITAL:
                    if not class_name[0].isupper():
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': class_name_match.start(1) + 1,
                            'message': "Имена классов должны начинаться с заглавной буквы"
                        })

                elif self.class_dialect == NamingRule.CAMEL_CASE_LOWER:
                    if not class_name[0].islower():
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': class_name_match.start(1) + 1,
                            'message': "Имена классов должны начинаться со строчной буквы"
                        })

        return errors

    def check_method_names(self, lines: list[str], filename: str):
        errors = []

        for i, line in enumerate(lines):

            method_name_match = self.METHOD_RE.search(line)

            if method_name_match and "(" in line and ")" in line:
                method_name = method_name_match.group(2)

                if self.method_dialect == NamingRule.SNAKE_CASE:
                    if not self.check_is_snake_case(method_name):
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': method_name_match.start(2) + 1,
                            'message': "Имена методов должны быть в snake_case"
                        })

                else:
                    if '_' in method_name:
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': method_name_match.start(2) + 1,
                            'message': "Имена методов не должны быть в snake_case"
                        })


                if self.method_dialect == NamingRule.CAMEL_CASE_CAPITAL:
                    if not method_name[0].isupper():
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': method_name_match.start(2) + 1,
                            'message': "Имена методов должны начинаться с заглавной буквы"
                        })

                elif self.method_dialect == NamingRule.CAMEL_CASE_LOWER:
                    if not method_name[0].islower():
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': method_name_match.start(2) + 1,
                            'message': "Имена методов должны начинаться со строчной буквы"
                        })

        return errors

    def check_var_names(self, lines: list[str], filename: str):
        errors = []

        for i, line in enumerate(lines):

            variable_declaration_match = self.VAR_RE.search(line)
            if variable_declaration_match:

                variable_name = variable_declaration_match.group(2)

                if variable_declaration_match.group(1) not in (
                        "class", "return", "for", "switch", "case",  "if", "extends", "import", "package"):

                    if self.var_dialect == NamingRule.SNAKE_CASE:
                        if not self.check_is_snake_case(variable_name):
                            errors.append({
                                'file': filename,
                                'line': i + 1,
                                'column': variable_declaration_match.start(2) + 1,
                                'message': "Имена переменных должны быть в snake_case"
                            })

                    else:
                        if "_" in variable_name:
                            errors.append({
                                'file': filename,
                                'line': i + 1,
                                'column': variable_declaration_match.start(2) + 1,
                                'message': "Имена переменных не должны быть в snake_case"
                            })

                    if self.var_dialect == NamingRule.CAMEL_CASE_CAPITAL:
                        if not variable_name[0].isupper():
                            errors.append({
                                'file': filename,
                                'line': i + 1,
                                'column': variable_declaration_match.start(2) + 1,
                                'message': "Имена переменных должны начинаться с заглавной буквы"
                            })

                    elif self.var_dialect == NamingRule.CAMEL_CASE_LOWER:

                        if not variable_name[0].islower():
                            errors.append({
                                'file': filename,
                                'line': i + 1,
                                'column': variable_declaration_match.start(2) + 1,
                                'message': "Имена переменных должны начинаться со строчной буквы"
                            })

        return errors

    def check_is_snake_case(self, name: str) -> bool:
        """
        Проверяет, соответствует ли имя класса соглашению snake_case

        Args:
            name (str): Имя класса для проверки (без слова 'class' и двоеточия)

        Returns:
            bool: True если имя валидно, False если нет
        """
        name = name.strip()

        if not re.fullmatch(r'^[a-z][a-z0-9_]*[a-z0-9]$', name):
            return False

        if '__' in name:
            return False

        parts = name.split('_')
        for part in parts[1:]:
            if not part or not part[0].isalpha():
                return False

        return True

    # def complile_method_re(self):
    #     return re.compile(
    #         r"""
    #             ^\s*
    #             (?:
    #                 (?:public|private|protected|
    #                 static|final|
    #                 synchronized|abstract|default)
    #                 \s+
    #             )*
    #             (
    #                 (?!public|private|protected|
    #                 static|final|
    #                 synchronized|abstract|default)
    #                 \w+
    #                 (?:\s*<[^>]+>)?
    #                 (?:\s*\[\s*\])*
    #                 \s*
    #             )
    #             \s+
    #             ([a-zA-Z_]\w*)
    #             \s*
    #             \(
    #             [^)]*
    #             \)
    #             \s*
    #             (?:throws\s+[\w\s,]+)?
    #             \s*
    #         """, re.VERBOSE
    #     )
    #
    # def complile_var_re(self):
    #     return re.compile(
    #         r"""
    #                             ^\s*                                  # Начало строки
    #                     (?:                                  # Группа для модификаторов
    #                         (?:public|private|protected|
    #                         static|final|
    #                         synchronized|abstract|default)
    #                         \s+                             # Пробелы после модификатора
    #                     )*                                 # Ноль или более модификаторов
    #                     \b(                                   # Группа для типа (захватывающая)
    #                         (?!public|private|protected|    # Запрет на модификаторы
    #                         static|final|                   # в качестве типа
    #                         synchronized|abstract|default)  #
    #                         \w+                            # Базовый тип
    #                         (?:\s*<[^>]+>)?                # Дженерик часть (опционально)
    #                         (?:\s*\[\s*\])*                # Массив (опционально, многомерный)
    #                         \s*                            # Пробелы после типа
    #                     )\b
    #                     \s+
    #                     \b([a-zA-Z_]\w*)\b                     # Имя метода (захватывающая группа)
    #                     \s*                                # Пробелы
    #                     (?!\()                                 # Открывающая скобка
    #                     """, re.VERBOSE
    #     )
