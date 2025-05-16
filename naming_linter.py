import re

from dialects import Dialect


class NamingLinter:

    def __init__(self, dialect: Dialect):
        self.class_dialect = dialect.naming.classes
        self.method_dialect = dialect.naming.methods
        self.var_dialect = dialect.naming.variables
        self.CLASS_RE = re.compile(r"class\s+([A-Za-z_]\w*)")
        self.METHOD_RE = self.complile_method_re()
        self.VAR_RE = self.complile_var_re()


    def get_errors(self, lines: str, filename: str):
        errors = []
        errors.extend(self.check_class_names(lines, filename))
        errors.extend(self.check_method_names(lines, filename))
        errors.extend(self.check_var_names(lines, filename))
        return errors

    def check_class_names(self, lines: str, filename: str):
        errors = []

        for i, line in enumerate(lines):
            class_name_match = self.CLASS_RE.search(line)
            if class_name_match:
                class_name = class_name_match.group(1)

                if not class_name[0].isupper():
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': class_name_match.start(1) + 1,
                        'message': "Имена классов должны начинаться с заглавной буквы"
                    })

        return errors

    def check_method_names(self, lines: str, filename: str):
        errors = []

        for i, line in enumerate(lines):

            method_name_match = self.METHOD_RE.search(line)

            if method_name_match and "(" in line and ")" in line:
                method_name = method_name_match.group(2)
                if not method_name[0].islower():
                    print(method_name_match.group(1))
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': method_name_match.start(2) + 1,
                        'message': "Имена методов должны начинаться со строчной буквы"
                    })

        return errors

    def check_var_names(self, lines: str, filename: str):
        errors = []

        for i, line in enumerate(lines):

            variable_declaration_match = self.VAR_RE.search(line)
            if variable_declaration_match:

                variable_name = variable_declaration_match.group(2)

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

    def complile_method_re(self) -> Pattern:
        return re.compile(
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
                (\w+)
                \s+
                ([a-zA-Z_]\w*)
                \s*
                \(
                [^)]*
                \)
                \s*
                (?:throws\s+[\w\s,]+)?
                \s*
            """
        )

    def complile_var_re(self) -> Pattern:
        return re.compile(
            r"""
                ^\s*
                (?:(?:public|private|protected|static|final)\s+)*
                ([\w<>[\],]+)
                \s+
                ([\w]+)
                \s*
                (?!\()
            """
        )