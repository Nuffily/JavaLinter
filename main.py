import re
import sys

from linter import Linter


def check_consecutive_empty_lines(lines, filename, n):
    """
    Проверяет, есть ли в коде подряд идущие n пустые строки.

    Args:
        lines (list): Список строк Java-кода.
        filename (str): Имя файла Java-кода.
        n (int): Количество подряд идущих пустых строк для проверки.

    Returns:
        list: Список ошибок, где каждая ошибка - это словарь с ключами
              'file', 'line', 'column', 'message'.
    """
    errors = []
    count = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            count += 1
        else:
            if count > n:
                errors.append({
                    'file': filename,
                    'line': i,
                    'column': 1,
                    'message': f"Обнаружено {count} последовательных пустых строк, а должно быть не больше {n}"
                })
            count = 0  # Сброс счетчика после обнаружения ошибки
    return errors


def check_spacing(lines, filename):
    """
    Проверяет правила расстановки пробелов в Java-коде.

    Args:
        lines (list): Список строк Java-кода.
        filename (str): Имя файла Java-кода.

    Returns:
        list: Список ошибок, где каждая ошибка - это словарь с ключами
              'file', 'line', 'column', 'message'.
    """
    errors = []
    for i, line in enumerate(lines):
        # Пробелы вокруг операторов (например, =, +, -, *, /, <, >)
        operators = r"==|\+|-|\*|/|="
        pattern = rf"\s*{operators}\s*"
        if re.search(pattern, line):
            match = re.search(pattern, line)
            if match:
                start = match.start()
                end = match.end()
                if not (line[start - 1].isspace() or line[end].isspace()):
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': start + 1,
                        'message': "Операторы должны быть окружены пробелами"
                    })

        # Пробелы после запятых
        if "," in line:
            for match in re.finditer(r",\S", line):
                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': match.start() + 1,
                    'message': "После запятой должен быть пробел"
                })
            for match in re.finditer(r"\s,", line):
                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': match.start() + 1,
                    'message': "Не должно быть запятых перед пробелом"
                })
        if "(" in line:
            for match in re.finditer(r"([a-zA-Z_]\w+)\s+(\()", line):
                if match.group(1) not in ("while", "for", "do"):
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': match.start(2),
                        'message': "Перед открывающейся скобкой не должно быть пробела"
                    })

            for match in re.finditer(r"([a-zA-Z_]\w+)\s*(\(\s+)", line):
                if match.group(1) not in ("while", "for", "do"):
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': match.start(2) + 2,
                        'message': "После открывающейся скобкой не должно быть пробела"
                    })

        if ")" in line:
            for match in re.finditer(r"\S\s+(\))", line):
                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': match.start(1),
                    'message': "Перед закрывающейся скобкой не должно быть пробела"
                })

            for match in re.finditer(r"(\))\w", line):
                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': match.start(1),
                    'message': "После закрывающейся скобки должен быть пробел"
                })

        # Пробелы перед открывающей фигурной скобкой
        if "{" in line:
            for match in re.finditer(r"\S{", line):
                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': match.start() + 1,
                    'message': "Перед открывающей фигурной скобкой должен быть пробел"
                })
    return errors


# def check_empty_lines(lines, filename):
#     """
#     Проверяет правила для пустых строк в Java-коде.
#
#     Args:
#         lines (list): Список строк Java-кода.
#         filename (str): Имя файла Java-кода.
#
#     Returns:
#         list: Список ошибок, где каждая ошибка - это словарь с ключами
#               'file', 'line', 'column', 'message'.
#     """
#     errors = []
#     for i, line in enumerate(lines):
#         # Две последовательные пустые строки
#         if i > 0 and lines[i - 1].strip() == "" and line.strip() == "":
#             errors.append({
#                 'file': filename,
#                 'line': i + 1,
#                 'column': 1,
#                 'message': "Недопустимые две последовательные пустые строки"
#             })
#     return errors
#

def check_naming_conventions(lines, filename):
    """
    Проверяет правила именования идентификаторов в Java-коде.

    Args:
        lines (list): Список строк Java-кода.
        filename (str): Имя файла Java-кода.

    Returns:
        list: Список ошибок, где каждая ошибка - это словарь с ключами
              'file', 'line', 'column', 'message'.
    """
    errors = []

    for i, line in enumerate(lines):
        # Имена классов (должны начинаться с заглавной буквы)
        class_name_match = re.search(r"class\s+([A-Za-z_][\w]*)", line)
        if class_name_match:
            class_name = class_name_match.group(1)
            if not class_name[0].isupper():
                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': class_name_match.start(1) + 1,
                    'message': "Имена классов должны начинаться с заглавной буквы"
                })

        # Имена методов (должны начинаться со строчной буквы)
        # method_name_pattern = r"""
        #            ^\s*                                  # Начало строки и пробелы
        #            (?:                                  # Незахватывающая группа для модификаторов
        #                (?:public|private|protected|     # Модификаторы доступа
        #                static|final|                   # Другие модификаторы
        #                synchronized|abstract|default)  # Дополнительные модификаторы
        #                \s+                             # Пробелы после модификатора
        #            )*                                 # Ноль или более модификаторов
        #            (?:[\w<>[\]?]+\s+)+                # Возвращаемый тип (может быть generic)
        #            ([a-zA-Z_]\w*)                     # Имя метода (захватывающая группа)
        #            \s*                                # Пробелы
        #            \(                                 # Открывающая скобка
        #            [^)]*                              # Параметры (все кроме закрывающей скобки)
        #            \)                                 # Закрывающая скобка
        #            \s*                                # Пробелы
        #            (?:                                # Незахватывающая группа для
        #                throws\s+[\w\s,]+             # Объявление исключений
        #            )?                                # (опционально)
        #            \s*                                # Пробелы
        #            # [\{;]                              # Открывающая фигурная скобка или точка с запятой
        #        """
        method_name_pattern = r"""
            ^\s*                                  # Начало строки
            (?:                                  # Группа для модификаторов
                (?:public|private|protected|     # Модификаторы доступа
                static|final|                    # Другие модификаторы
                synchronized|abstract|default)   # Дополнительные модификаторы
                \s+                             # Пробелы после модификатора
            )*                                 # Ноль или более модификаторов
            (                                   # Группа для типа (захватывающая)
                (?!public|private|protected|    # Запрет на модификаторы
                static|final|                   # в качестве типа
                synchronized|abstract|default)  #
                \w+                            # Базовый тип
                (?:\s*<[^>]+>)?                # Дженерик часть (опционально)
                (?:\s*\[\s*\])*                # Массив (опционально, многомерный)
                \s*                            # Пробелы после типа
            )
            \s+
            ([a-zA-Z_]\w*)                     # Имя метода (захватывающая группа)
            \s*                                # Пробелы
            \(                                 # Открывающая скобка
            [^)]*                              # Параметры (все кроме закрывающей скобки)
            \)                                 # Закрывающая скобка
            \s*                                # Пробелы
            (?:                                # Незахватывающая группа для
                throws\s+[\w\s,]+             # Объявление исключений
            )?                                # (опционально)
            \s*                                # Пробелы
            # [\{;]                              # Открывающая фигурная скобка или точка с запятой
        """
        method_name_match = re.search(method_name_pattern, line, re.VERBOSE)

        if method_name_match and "(" in line and ")" in line:
            method_name = method_name_match.group(2)
            if not method_name[0].islower():
                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': method_name_match.start(2) + 1,
                    'message': "Имена методов должны начинаться со строчной буквы"
                })

        variable_declaration_pattern = r"^\s*(?:(?:public|private|protected|static|final)\s+)*([A-Za-z_][\w]+)\s*(?:(?:<.*>|[.*])\s*)*\s+([A-Za-z_][\w]*)\s*(?!\()"
        variable_declaration_pattern = r"^\s*(?:(?:public|private|protected|static|final)\s+)*([A-Za-z_][\w]+)\s*(?:(?:<.*>|[.*])\s*)*\s+\b([A-Za-z_]\w*)\b\s*(?!\()"
        # variable_declaration_pattern = r"""
        #     ^\s*                                  # Начало строки
        #     (?:(?:public|private|protected|static|final)\s+)*  # Модификаторы
        #     ([\w<>[\],]+)                        # Тип (группа 1)
        #     \s+                                  # Пробелы
        #     ([\w]+)                              # Имя (группа 2)
        #     \s*                                  # Пробелы
        #     (?!\()                               # Запрет на открывающую скобку
        # """
        variable_declaration_pattern = r"""
                    ^\s*                                  # Начало строки
            (?:                                  # Группа для модификаторов
                (?:public|private|protected|     # Модификаторы доступа
                static|final|                    # Другие модификаторы
                synchronized|abstract|default)   # Дополнительные модификаторы
                \s+                             # Пробелы после модификатора
            )*                                 # Ноль или более модификаторов
            (                                   # Группа для типа (захватывающая)
                (?!public|private|protected|    # Запрет на модификаторы
                static|final|                   # в качестве типа
                synchronized|abstract|default)  #
                \w+                            # Базовый тип
                (?:\s*<[^>]+>)?                # Дженерик часть (опционально)
                (?:\s*\[\s*\])*                # Массив (опционально, многомерный)
                \s*                            # Пробелы после типа
            )
            \s+
            \b([a-zA-Z_]\w*)\b                     # Имя метода (захватывающая группа)
            \s*                                # Пробелы
            (?!\()                                 # Открывающая скобка
            """


        variable_declaration_match = re.search(variable_declaration_pattern, line, re.VERBOSE)
        if variable_declaration_match:

            variable_name = variable_declaration_match.group(2)
            print(variable_name)
            if not variable_name[0].islower() and variable_declaration_match.group(1) not in (
            "class", "return", "for", "switch", "case"):
                print(variable_name)
                print(variable_declaration_match.start(2))

                errors.append({
                    'file': filename,
                    'line': i + 1,
                    'column': variable_declaration_match.start(2) + 1,
                    'message': "Имена переменных должны начинаться со строчной буквы"
                })

    return errors


def lint_java_code(filename, linter: Linter):
    """
    Выполняет линтинг Java-кода в заданном файле.

    Args:
        filename (str): Имя файла Java-кода.

    Returns:
        list: Список всех ошибок, обнаруженных линтером.
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл не найден: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)



    all_errors = []
    all_errors.extend(check_spacing(lines, filename))
    # all_errors.extend(check_consecutive_empty_lines(lines, filename, 3))
    # all_errors.extend(check_empty_lines(lines, filename))
    # all_errors.extend(check_naming_conventions(lines, filename))
    all_errors.extend(linter.do(lines, filename))

    return all_errors


def main():
    """
    Главная функция для запуска линтера.
    """
    if len(sys.argv) < 3:
        print("Использование: python java_linter.py <java_file1> <java_file2> ...")
        sys.exit(1)

    for filename in sys.argv[2:]:
        linter = Linter(sys.argv[1])
        errors = lint_java_code(filename, linter)
        if errors:
            print(f"Ошибки в файле: {filename}")
            for error in errors:
                print(f"  Строка: {error['line']}, Столбец: {error['column']}, Сообщение: {error['message']}")
            print("-" * 20)
        else:
            print(f"Проблем не найдено в файле: {filename}")


if __name__ == "__main__":
    main()
