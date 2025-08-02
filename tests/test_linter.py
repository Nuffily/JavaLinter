import pytest

from java_linter.dialects import Dialect, EmptyLineCountDialect, NamingDialect, NamingRule, SpaceDialect
from java_linter.linter import Linter
from java_linter.shared import ErrorEntry


class TestLinter:

    @pytest.mark.parametrize(
        "file_name,dialect,expected_errors",
        [
            (
                "test_files/BadMyJMenu.java",
                Dialect(
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
                ),
                [
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=12,
                        column=7,
                        message="Имена классов должны начинаться с заглавной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=27,
                        column=22,
                        message="Имена методов должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=35,
                        column=19,
                        message="Имена методов не должны быть в snake_case",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=39,
                        column=21,
                        message="Имена методов должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=13,
                        column=26,
                        message="Имена переменных должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=14,
                        column=26,
                        message="Имена переменных не должны быть в snake_case",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=28,
                        column=17,
                        message="Имена переменных должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=33,
                        column=1,
                        message="Обнаружено 2 пустых строк после метода, а должно быть 1",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=39,
                        column=1,
                        message="Обнаружено 0 пустых строк после метода, а должно быть 1",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=17,
                        column=56,
                        message="После запятой должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=36,
                        column=46,
                        message="После запятой должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=17,
                        column=46,
                        message="Не должно быть пробелов перед запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=17,
                        column=12,
                        message="Перед открывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=17,
                        column=14,
                        message="После открывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=17,
                        column=88,
                        message="Перед закрывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=24,
                        column=28,
                        message="Операторы должны быть окружены пробелами",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=1,
                        column=14,
                        message="Не должно быть пробелов перед точкой с запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=30,
                        column=18,
                        message="Не должно быть пробелов перед точкой с запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=37,
                        column=96,
                        message="Не должно быть пробелов перед точкой с запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=3,
                        column=18,
                        message="После точки не должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=31,
                        column=20,
                        message="Не должно быть пробелов перед точкой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=31,
                        column=21,
                        message="После точки не должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=37,
                        column=68,
                        message="После точки не должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=1,
                        column=11,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=3,
                        column=18,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=8,
                        column=29,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=12,
                        column=27,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMyJMenu.java",
                        line=39,
                        column=18,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                ],
            ),
            (
                "test_files/GoodMyJMenu.java",
                Dialect(
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
                ),
                [],
            ),
            (
                "test_files/BadMainApplicationFrame.java",
                Dialect(
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
                ),
                [
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=37,
                        column=14,
                        message="Имена классов должны начинаться с заглавной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=86,
                        column=17,
                        message="Имена методов должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=169,
                        column=19,
                        message="Имена методов должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=41,
                        column=43,
                        message="Имена переменных не должны быть в snake_case",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=43,
                        column=39,
                        message="Имена переменных должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=61,
                        column=19,
                        message="Имена переменных должны начинаться со строчной буквы",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=113,
                        column=18,
                        message="Имена переменных не должны быть в snake_case",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=29,
                        column=1,
                        message="Обнаружено 6 последовательных пустых строк, а должно быть не больше 3",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=51,
                        column=1,
                        message="Обнаружено 5 последовательных пустых строк, а должно быть не больше 3",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=168,
                        column=1,
                        message="Обнаружено 6 последовательных пустых строк, а должно быть не больше 3",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=215,
                        column=1,
                        message="Обнаружено 4 последовательных пустых строк, а должно быть не больше 3",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=84,
                        column=1,
                        message="Обнаружено 2 пустых строк после метода, а должно быть 1",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=95,
                        column=1,
                        message="Обнаружено 0 пустых строк после метода, а должно быть 1",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=163,
                        column=1,
                        message="Обнаружено 6 пустых строк после метода, а должно быть 1",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=211,
                        column=1,
                        message="Обнаружено 0 пустых строк после метода, а должно быть 1",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=102,
                        column=38,
                        message="Не должно быть пробелов перед запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=43,
                        column=76,
                        message="Перед открывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=58,
                        column=23,
                        message="Перед открывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=66,
                        column=38,
                        message="Перед открывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=101,
                        column=26,
                        message="Перед закрывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=107,
                        column=26,
                        message="Перед открывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=107,
                        column=28,
                        message="После открывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=140,
                        column=19,
                        message="Перед закрывающейся скобкой не должно быть пробела",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=52,
                        column=19,
                        message="Операторы должны быть окружены пробелами",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=55,
                        column=33,
                        message="Операторы должны быть окружены пробелами",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=61,
                        column=28,
                        message="Операторы должны быть окружены пробелами",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=113,
                        column=26,
                        message="Операторы должны быть окружены пробелами",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=170,
                        column=29,
                        message="Операторы должны быть окружены пробелами",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=43,
                        column=79,
                        message="Не должно быть пробелов перед точкой с запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=66,
                        column=44,
                        message="Не должно быть пробелов перед точкой с запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=204,
                        column=96,
                        message="Не должно быть пробелов перед точкой с запятой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=12,
                        column=19,
                        message="После точки не должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=13,
                        column=91,
                        message="Не должно быть пробелов перед точкой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=13,
                        column=98,
                        message="После точки не должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=107,
                        column=14,
                        message="Не должно быть пробелов перед точкой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=152,
                        column=17,
                        message="Не должно быть пробелов перед точкой",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=203,
                        column=18,
                        message="После точки не должен быть пробел",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=12,
                        column=19,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=13,
                        column=29,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=13,
                        column=88,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=66,
                        column=35,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                    ErrorEntry(
                        file_name="test_files/BadMainApplicationFrame.java",
                        line=66,
                        column=41,
                        message="Не должно быть более одного пробела подряд внутри строки",
                    ),
                ],
            ),
            (
                "test_files/GoodMainApplicationFrame.java",
                Dialect(
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
                ),
                [],
            ),
        ],
    )
    def test_linter(self, file_name: str, dialect: Dialect, expected_errors: list[ErrorEntry]) -> None:

        linter = Linter(dialect=dialect)

        try:
            with open(file_name, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            assert False

        errors = linter.seek_for_errors(lines, file_name)

        assert len(errors) == len(expected_errors)

        for expected in expected_errors:
            assert expected in errors
