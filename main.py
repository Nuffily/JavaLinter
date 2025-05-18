import sys
from typing import Any

from java_linter.linter import Linter
from java_linter.shared import ErrorEntry

def lint_java_code(filename: str, linter: Linter) -> list[Any]:
    """Выполняет линтинг Java-кода в заданном файле."""
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл не найден: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

    all_errors = linter.seek_for_errors(lines, filename)

    return all_errors


def main() -> None:
    """Главная функция для запуска линтера."""

    if len(sys.argv) < 3:
        print("Использование: python java_linter.py <java_file1> <java_file2> ...")
        sys.exit(1)

    for filename in sys.argv[2:]:

        linter = Linter(sys.argv[1])
        errors = lint_java_code(filename, linter)

        if errors:
            print(f"Ошибки в файле: {filename}")
            for error in errors:
                print(f"  Строка: {error.line}, Столбец: {error.column}, Проблема: {error.message}")
            print("-" * 20)
        else:
            print(f"Проблем не найдено в файле: {filename}")


if __name__ == "__main__":
    main()
