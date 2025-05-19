import re

from typing import NamedTuple


class ErrorEntry(NamedTuple):
    file_name: str
    line: int
    column: int
    message: str


class JavaPatterns:
    CLASS_PATTERN = re.compile(
        r"""
        ^\s*
        (?:
            (?:public|private|protected|
            static|final|
            synchronized|abstract|default)
            \s+
        )*
        (?:class|interface|enum)\s+([A-Za-z_]\w*
    )
    """,
        re.VERBOSE,
    )

    VAR_PATTERN = re.compile(
        r"""
                    ^\s*
            (?:
                (?:public|private|protected|
                static|final|
                synchronized|abstract|default|volatile)
                \s+
            )*
            (
                (?!public|private|protected|
                static|final|
                synchronized|abstract|default|volatile)
                \w+
                (?:\s*<.+>)*
                (?:\s*\[.*])*
            )
            \s+
            \b([a-zA-Z_]\w*)\b
            \s*
            (?!\()
            """,
        re.VERBOSE,
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
        """,
        re.VERBOSE,
    )
