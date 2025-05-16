import re


class JavaPatterns:

    CLASS_PATTERN = re.compile(r"""
        ^\s*
        (?:
            (?:public|private|protected|
            static|final|
            synchronized|abstract|default)
            \s+
        )*
        (?:class|interface|enum)\s+([A-Za-z_]\w*
    )
    """, re.VERBOSE)

    VAR_PATTERN = re.compile(
        r"""
                            ^\s*                                  # Начало строки
                    (?:                                  # Группа для модификаторов
                        (?:public|private|protected|
                        static|final|
                        synchronized|abstract|default)
                        \s+                             # Пробелы после модификатора
                    )*                                 # Ноль или более модификаторов
                    \b(                                   # Группа для типа (захватывающая)
                        (?!public|private|protected|    # Запрет на модификаторы
                        static|final|                   # в качестве типа
                        synchronized|abstract|default)  #
                        \w+                            # Базовый тип
                        (?:\s*<[^>]+>)?                # Дженерик часть (опционально)
                        (?:\s*\[\s*\])*                # Массив (опционально, многомерный)
                        \s*                            # Пробелы после типа
                    )\b
                    \s+
                    \b([a-zA-Z_]\w*)\b                     # Имя метода (захватывающая группа)
                    \s*                                # Пробелы
                    (?!\()                                 # Открывающая скобка
                    """, re.VERBOSE
    )

    METHOD_PATTERN = re.compile(
        r"""
            ^\s*
            (?:
                (?:public|private|protected|
                static|final|
                synchronized|abstract|default)
                \s+
            )*
            (
                (?!public|private|protected|
                static|final|
                synchronized|abstract|default)
                \w+
                (?:\s*<[^>]+>)?
                (?:\s*\[\s*\])*
                \s*
            )
            \s+
            ([a-zA-Z_]\w*)
            \s*
            \(
            [^)]*
            \)
            \s*
            (?:throws\s+[\w\s,]+)?
            \s*
        """, re.VERBOSE
    )
