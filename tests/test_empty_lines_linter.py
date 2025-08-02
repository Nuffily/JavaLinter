import pytest

from java_linter.dialects import Dialect, EmptyLineCountDialect, NamingDialect, NamingRule, SpaceDialect
from java_linter.empty_lines_liner import EmptyLineLinter
from java_linter.shared import ErrorEntry


class TestEmptyLineLinter:

    @pytest.fixture
    def dialect(self, after_class: int = 3, after_method: int = 2, max_empty: int = 3) -> Dialect:
        return Dialect(
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
            empty_lines=EmptyLineCountDialect(max_empty=max_empty, after_method=after_method, after_class=after_class),
        )

    @pytest.fixture
    def linter(self, dialect: Dialect) -> EmptyLineLinter:
        return EmptyLineLinter(dialect)

    @pytest.mark.parametrize(
        "lines,max_empty,expected_errors",
        [
            (
                ["line1", "", "", "", "line2"],
                2,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=4,
                        column=1,
                        message="Обнаружено 3 последовательных пустых строк, а должно быть не больше 2",
                    )
                ],
            ),
            (
                ["some1", "", "", "", "", "some2"],
                2,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=5,
                        column=1,
                        message="Обнаружено 4 последовательных пустых строк, а должно быть не больше 2",
                    )
                ],
            ),
            (
                ["", "", ""],
                1,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=3,
                        column=1,
                        message="Обнаружено 3 последовательных пустых строк, а должно быть не больше 1",
                    )
                ],
            ),
            ([], 2, []),
            (["str1", "", "str2"], 2, []),
            (["line1", "line2"], 2, []),
        ],
    )
    def test_check_consecutive_empty_lines(
        self, linter: EmptyLineLinter, lines: list[str], max_empty: int, expected_errors: list[ErrorEntry]
    ) -> None:
        linter._max_empty = max_empty

        errors = linter._check_consecutive_empty_lines(lines, "test.java")

        assert len(errors) == len(expected_errors)

        for expected in expected_errors:
            assert expected in errors

    @pytest.mark.parametrize(
        "lines,after_class,expected_errors",
        [
            (["class MyClass {", "}", "", "", "", "line"], 3, []),
            (
                ["class SomeClass {", "}", "", "", "line"],
                3,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=3,
                        column=1,
                        message="Обнаружено 2 пустых строк после класса, а должно быть 3",
                    )
                ],
            ),
            (
                ["enum AgainEnum {", "}", "nothing"],
                3,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=3,
                        column=1,
                        message="Обнаружено 0 пустых строк после класса, а должно быть 3",
                    )
                ],
            ),
            (
                ["abstract interface MyInt {", "{", "}", "}", "", "", "", "", "line"],
                3,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=5,
                        column=1,
                        message="Обнаружено 4 пустых строк после класса, а должно быть 3",
                    )
                ],
            ),
            (["class MyClass {}"], 3, []),
            (["interface MyInterface {}"], 3, []),
            (["abstract enum MyEnum {}"], 3, []),
            (["abstract class MyAbstractClass {}"], 3, []),
        ],
    )
    def test_check_empty_lines_after_class(
        self, linter: EmptyLineLinter, lines: list[str], after_class: int, expected_errors: list[ErrorEntry]
    ) -> None:
        linter._after_class = after_class

        errors = linter._check_empty_lines_after_class(lines, "test.java")

        assert len(errors) == len(expected_errors)

        for expected in expected_errors:
            assert expected in errors

    @pytest.mark.parametrize(
        "lines,after_method,expected_errors",
        [
            (["void method() {", "}", "", "", "a"], 2, []),
            (
                ["int calc(qweqw qtrrwet) {", "}", "", "a"],
                2,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=3,
                        column=1,
                        message="Обнаружено 1 пустых строк после метода, а должно быть 2",
                    )
                ],
            ),
            (
                ["void method() {", "}", "", "", "anotherMethod() {}"],
                3,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=3,
                        column=1,
                        message="Обнаружено 2 пустых строк после метода, а должно быть 3",
                    )
                ],
            ),
            (["void method() {", "some code lol", "}", "", "", "anotherMethod() {", "}"], 2, []),
            (["void method() {}"], 2, []),
            (
                ["int get() { return 1; }", "", "qwe"],
                2,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=2,
                        column=1,
                        message="Обнаружено 1 пустых строк после метода, а должно быть 2",
                    )
                ],
            ),
            (
                ["void method() return nothing literally;", "", "", "", "class MyClass {}"],
                2,
                [
                    ErrorEntry(
                        file_name="test.java",
                        line=2,
                        column=1,
                        message="Обнаружено 3 пустых строк после метода, а должно быть 2",
                    )
                ],
            ),
        ],
    )
    def test_check_empty_lines_after_method(
        self, linter: EmptyLineLinter, lines: list[str], after_method: int, expected_errors: list[ErrorEntry]
    ) -> None:

        linter._after_method = after_method

        errors = linter._check_empty_lines_after_method(lines, "test.java")

        assert len(errors) == len(expected_errors)

        for expected in expected_errors:
            assert expected in errors

    def test_seek_for_errors(self, linter: EmptyLineLinter) -> None:

        lines = [
            "interface MyClass {",
            "",
            "}",
            "",
            "",
            "void method1() {}",
            "",
            "",
            "void method2() {}",
            "",
            "",
            "",
            "int x = 5;",
            "",
            "",
            "",
            "",
        ]

        errors = linter.seek_for_errors(lines, "test.java")

        expected_errors = [
            ErrorEntry(
                file_name="test.java",
                line=17,
                column=1,
                message="Обнаружено 4 последовательных пустых строк, а должно быть не больше 3",
            ),
            ErrorEntry(
                file_name="test.java",
                line=4,
                column=1,
                message="Обнаружено 2 пустых строк после класса, а должно быть 3",
            ),
            ErrorEntry(
                file_name="test.java",
                line=10,
                column=1,
                message="Обнаружено 3 пустых строк после метода, а должно быть 2",
            ),
        ]

        assert len(errors) == len(expected_errors)

        for expected in expected_errors:
            assert expected in errors

    def test_disabled_checks(self, linter: EmptyLineLinter) -> None:

        linter._max_empty = 0
        linter._after_class = 0
        linter._after_method = 0

        lines = [
            "interface MyClass {",
            "",
            "}",
            "",
            "",
            "void method1() {}",
            "",
            "",
            "void method2() {}",
            "",
            "",
            "",
            "int x = 5;",
            "",
            "",
            "",
            "",
        ]

        errors = linter.seek_for_errors(lines, "test.java")

        assert len(errors) == 0
