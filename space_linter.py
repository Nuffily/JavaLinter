import re
from dialects import Dialect


class SpaceLinter:

    def __init__(self, dialect: Dialect):
        self.after_comma = dialect.spaces.after_comma
        self.before_comma = dialect.spaces.before_comma
        self.around_brackets = dialect.spaces.around_brackets
        self.around_operators = dialect.spaces.around_operators
        self.may_be_more_that_one_space = dialect.spaces.may_be_more_that_one_space



    def get_errors(self, lines: list[str], filename: str):
        errors = []

        if self.after_comma:
            errors.extend(self.check_spaces_after_comma(lines, filename))

        if self.before_comma:
            errors.extend(self.check_spaces_before_comma(lines, filename))

        if self.around_brackets:
            errors.extend(self.check_spaces_around_brackets(lines, filename))

        if self.around_operators:
            errors.extend(self.check_spaces_around_operators(lines, filename))

        return errors

    def check_spaces_after_comma(self, lines: list[str], filename: str):

        errors = []

        for i, line in enumerate(lines):

            if "," in line:
                for match in re.finditer(r",\S", line):
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': match.start() + 1,
                        'message': "После запятой должен быть пробел"
                    })

        return errors

    def check_spaces_before_comma(self, lines: list[str], filename: str):

        errors = []

        for i, line in enumerate(lines):

            if "," in line:
                for match in re.finditer(r"\s,", line):
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': match.start() + 1,
                        'message': "Не должно быть запятых перед пробелом"
                    })

        return errors

    def check_spaces_around_brackets(self, lines: list[str], filename: str):

        errors = []

        for i, line in enumerate(lines):

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

            if "{" in line:
                for match in re.finditer(r"\S{", line):
                    errors.append({
                        'file': filename,
                        'line': i + 1,
                        'column': match.start() + 1,
                        'message': "Перед открывающей фигурной скобкой должен быть пробел"
                    })

        return errors

    def check_spaces_around_operators(self, lines: list[str], filename: str):

        errors = []

        operator_pattern = r"==|\+|-|\*|/(?:/)|="
        # operator_pattern = rf"\s*{operators}"

        for i, line in enumerate(lines):

            if re.search(operator_pattern, line):
                match = re.search(operator_pattern, line)

                if match:
                    start = match.start()
                    end = match.end()
                    print(line[start - 1], line[end])
                    if not ((line[start - 1].isspace() and line[end].isspace())):
                        errors.append({
                            'file': filename,
                            'line': i + 1,
                            'column': start + 1,
                            'message': "Операторы должны быть окружены пробелами"
                        })

        return errors