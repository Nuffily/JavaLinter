from typing import Any

import pytest

from java_linter.dialects import Dialect, NamingRule, NamingDialect, EmptyLineCountDialect, SpaceDialect
from java_linter.naming_linter import NamingLinter


class TestNamingLinter:

    @pytest.fixture
    def linter(self) -> NamingLinter:
        naming_linter = NamingLinter(Dialect(
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
            empty_lines=EmptyLineCountDialect(max_empty=2, after_method=2, after_class=3),
        )
        )
        return naming_linter

    @pytest.mark.parametrize(
        "line,class_dialect,expected_errors",
        [
            ("class MyClass {}", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 7, "message": "Имена классов должны быть в snake_case"}
            ]),
            ("class my_class {}", NamingRule.CAMEL_CASE_CAPITAL, [
                {"line": 1, "column": 7, "message": "Имена классов не должны быть в snake_case"},
                {"line": 1, "column": 7, "message": "Имена классов должны начинаться с заглавной буквы"}
            ]),
            ("class my_Class {}", NamingRule.CAMEL_CASE_CAPITAL, [
                {"line": 1, "column": 7, "message": "Имена классов не должны быть в snake_case"},
                {"line": 1, "column": 7, "message": "Имена классов должны начинаться с заглавной буквы"}
            ]),
            ("class My_class {}", NamingRule.CAMEL_CASE_LOWER, [
                {"line": 1, "column": 7, "message": "Имена классов не должны быть в snake_case"},
                {"line": 1, "column": 7, "message": "Имена классов должны начинаться со строчной буквы"}
            ]),
            ("class Myclass {}", NamingRule.CAMEL_CASE_LOWER, [
                {"line": 1, "column": 7, "message": "Имена классов должны начинаться со строчной буквы"}
            ]),
            ("interface MyInterface {}", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 11, "message": "Имена классов должны быть в snake_case"}
            ]),
            ("enum MyEnum {}", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 6, "message": "Имена классов должны быть в snake_case"}
            ]),
            ("class MyClass {}", NamingRule.CAMEL_CASE_CAPITAL, []),
            ("class my_class_name {}", NamingRule.SNAKE_CASE, [])
        ],
    )
    def test_check_class_names(self, linter: NamingLinter, line: str, class_dialect: NamingRule,
                               expected_errors: list[dict[str, Any]]):

        linter._class_dialect = class_dialect

        errors = linter._check_class_names([line], "test.java")
        assert len(errors) == len(expected_errors)

        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    @pytest.mark.parametrize(
        "line,method_dialect,expected_errors",
        [
            ("void myMethod() {}", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 6, "message": "Имена методов должны быть в snake_case"}
            ]),
            ("void his_method() {}", NamingRule.CAMEL_CASE_LOWER, [
                {"line": 1, "column": 6, "message": "Имена методов не должны быть в snake_case"}
            ]),
            ("void Her_method() {}", NamingRule.CAMEL_CASE_LOWER, [
                {"line": 1, "column": 6, "message": "Имена методов не должны быть в snake_case"},
                {"line": 1, "column": 6, "message": "Имена методов должны начинаться со строчной буквы"}
            ]),
            ("public String get_value() {}", NamingRule.CAMEL_CASE_LOWER, [
                {"line": 1, "column": 15, "message": "Имена методов не должны быть в snake_case"}
            ]),
            ("public void setVALUE(int value) {}", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 13, "message": "Имена методов должны быть в snake_case"}
            ]),
            ("public static void main(String[] args) {}", NamingRule.SNAKE_CASE, []),
            ("private volatile void main(String[] args) {}", NamingRule.CAMEL_CASE_LOWER, []),
        ],
    )
    def test_check_method_names(self, linter: NamingLinter, line: str, method_dialect: NamingRule,
                                expected_errors: list[dict[str, Any]]):
        linter._method_dialect = method_dialect
        errors = linter._check_method_names([line], "test.java")
        assert len(errors) == len(expected_errors)
        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    @pytest.mark.parametrize(
        "line,var_dialect,expected_errors",
        [
            ("int myVariable;", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 5, "message": "Имена переменных должны быть в snake_case"}
            ]),
            ("String my_variable;", NamingRule.CAMEL_CASE_LOWER, [
                {"line": 1, "column": 8, "message": "Имена переменных не должны быть в snake_case"}
            ]),
            ("final int MY_VARIABLE = 123;", NamingRule.CAMEL_CASE_LOWER, [
                {"line": 1, "column": 11, "message": "Имена переменных не должны быть в snake_case"},
                {"line": 1, "column": 11, "message": "Имена переменных должны начинаться со строчной буквы"}
            ]),
            ("private List<String> ListList;", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 22, "message": "Имена переменных должны быть в snake_case"}
            ]),
            ("int _underscoreVar;", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 5, "message": "Имена переменных должны быть в snake_case"}
            ]),
            ("int __invalidVar;", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 5, "message": "Имена переменных должны быть в snake_case"}
            ]),
            ("int invalid_Var;", NamingRule.SNAKE_CASE, [
                {"line": 1, "column": 5, "message": "Имена переменных должны быть в snake_case"}
            ]),
        ],
    )
    def test_check_var_names(self, linter: NamingLinter, line: str, var_dialect: NamingRule,
                             expected_errors: list[dict[str, Any]]):
        linter._var_dialect = var_dialect
        errors = linter._check_var_names([line], "test.java")
        assert len(errors) == len(expected_errors)
        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    def test_seek_for_errors_integration(self, linter: NamingLinter):
        lines = [
            "class myClass {}",
            "public void MyMethod() {}",
            "int SOME_VAR = 5;",
        ]
        errors = linter.seek_for_errors(lines, "test.java")
        expected_errors = [
            {"line": 1, "column": 7, "message": "Имена классов должны начинаться с заглавной буквы"},
            {"line": 2, "column": 13, "message": "Имена методов должны начинаться со строчной буквы"},
            {"line": 3, "column": 5, "message": "Имена переменных должны начинаться со строчной буквы"},
            {"line": 3, "column": 5, "message": "Имена переменных не должны быть в snake_case"},
        ]
        assert len(errors) == len(expected_errors)
        actual_errors = sorted([{"line": e.line, "column": e.column, "message": e.message} for e in errors],
                               key=lambda x: (x["line"], x["column"]))
        assert actual_errors == sorted(expected_errors, key=lambda x: (x["line"], x["column"]))

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("snake_case_name", True),
            ("singleword", True),
            ("snake_case123", True),
            ("snake_1_case", True),
            ("startsWithUppercase", False),
            ("ends_with_underscore_", False),
            ("_startsWithUnderscore", False),
            ("two__underscores", False),
            ("part_With_Uppercase", False),
            ("", False),
            ("_", False),
            ("__", False),
            ("1_starts_with_digit", False),
            ("ends_with_digit_1", True),
            ("a_b_", False),
            ("a__b", False),
        ],
    )
    def test_check_is_snake_case(linter: NamingLinter, name: str, expected: bool):
        assert linter._check_is_snake_case(name) == expected
