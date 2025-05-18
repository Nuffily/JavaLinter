import pytest
from java_linter.dialects import Dialect, NamingDialect, SpaceDialect, NamingRule, EmptyLineCountDialect
from java_linter.shared import ErrorEntry
from java_linter.space_linter import SpaceLinter


class TestSpaceLinter:

    @pytest.fixture
    def dialect(self):
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
            empty_lines=EmptyLineCountDialect(max_empty=2, after_method=2, after_class=3),
        )

    @pytest.fixture
    def linter(self, dialect):
        return SpaceLinter(dialect)

    @pytest.mark.parametrize(
        "line,expected_errors",
        [
            ("int a,b,c", [
                {"line": 1, "column": 6, "message": "После запятой должен быть пробел"},
                {"line": 1, "column": 8, "message": "После запятой должен быть пробел"}
            ]),
            ("String s1,s2", [
                {"line": 1, "column": 10, "message": "После запятой должен быть пробел"}
            ]),
            ("Map<String,Integer> map", [
                {"line": 1, "column": 11, "message": "После запятой должен быть пробел"}
            ]),
            ("int x, y, z", []),  # Корректный код - без ошибок
            ("call(a,b,c)", [
                {"line": 1, "column": 7, "message": "После запятой должен быть пробел"},
                {"line": 1, "column": 9, "message": "После запятой должен быть пробел"}
            ])
        ]
    )
    def test_check_spaces_after_comma(self, linter, line, expected_errors):
        errors = linter._check_spaces_after_comma([line], "test.java")

        assert len(errors) == len(expected_errors)

        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    @pytest.mark.parametrize(
        "line,expected_errors",
        [
            ("int a ,b", [
                {"line": 1, "column": 6, "message": "Не должно быть пробелов перед запятой"}
            ]),
            ("String s , t", [
                {"line": 1, "column": 9, "message": "Не должно быть пробелов перед запятой"}
            ]),
            ("int x,y", []),
            ("List< String , Integer , Type>", [
                {"line": 1, "column": 13, "message": "Не должно быть пробелов перед запятой"},
                {"line": 1, "column": 23, "message": "Не должно быть пробелов перед запятой"}
            ])
        ]
    )
    def test_check_no_spaces_before_comma(self, linter, line, expected_errors):
        errors = linter._check_no_spaces_before_comma([line], "test.java")

        assert len(errors) == len(expected_errors)

        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    @pytest.mark.parametrize(
        "line,expected_errors",
        [
            ("obj .method()", [
                {"line": 1, "column": 4, "message": "Не должно быть пробелов перед точкой"}
            ]),
            ("obj. method()", [
                {"line": 1, "column": 4, "message": "После точки не должен быть пробел"}
            ]),
            ("obj . method()", [
                {"line": 1, "column": 4, "message": "Не должно быть пробелов перед точкой"},
                {"line": 1, "column": 5, "message": "После точки не должен быть пробел"}
            ]),
            ("obj.method()", []),
            ("some.obj .field", [
                {"line": 1, "column": 9, "message": "Не должно быть пробелов перед точкой"}
            ])
        ]
    )
    def test_check_no_spaces_around_dot(self, linter, line, expected_errors):
        errors = linter._check_no_spaces_around_dot([line], "test.java")

        assert len(errors) == len(expected_errors)

        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    @pytest.mark.parametrize(
        "line,expected_errors",
        [
            ("int x ;", [
                {"line": 1, "column": 6, "message": "Не должно быть пробелов перед точкой с запятой"}
            ]),
            ("lol (;; ) ;", [
                {"line": 1, "column": 10, "message": "Не должно быть пробелов перед точкой с запятой"}
            ]),
            ("int x;", [])
        ]
    )
    def test_check_no_spaces_before_dot_comma(self, linter, line, expected_errors):
        errors = linter._check_no_spaces_before_dot_comma([line], "test.java")

        assert len(errors) == len(expected_errors)

        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    @pytest.mark.parametrize(
        "line,expected_errors",
        [
            ("method (arg)", [
                {"line": 1, "column": 7, "message": "Перед открывающейся скобкой не должно быть пробела"}
            ]),
            ("method( arg )", [
                {"line": 1, "column": 8, "message": "После открывающейся скобкой не должно быть пробела"},
                {"line": 1, "column": 12, "message": "Перед закрывающейся скобкой не должно быть пробела"}
            ]),
            ("if ( condition ) {", [
                {"line": 1, "column": 5, "message": "После открывающейся скобкой не должно быть пробела"},
                {"line": 1, "column": 15, "message": "Перед закрывающейся скобкой не должно быть пробела"}
            ]),
            ("(qwe )", [
                {"line": 1, "column": 5, "message": "Перед закрывающейся скобкой не должно быть пробела"}
            ]),
            ("( asd)", [
                {"line": 1, "column": 2, "message": "После открывающейся скобкой не должно быть пробела"}
            ]),
            ("( zxc )", [
                {"line": 1, "column": 2, "message": "После открывающейся скобкой не должно быть пробела"},
                {"line": 1, "column": 6, "message": "Перед закрывающейся скобкой не должно быть пробела"}
            ]),
            ("for (i = 0; i < 10; i++)", []),
            ("method()", [])
        ]
    )
    def test_check_no_spaces_around_brackets(self, linter, line, expected_errors):
        errors = linter._check_no_spaces_around_brackets([line], "test.java")

        assert len(errors) == len(expected_errors)

        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == expected["message"]

    @pytest.mark.parametrize(
        "line,expected_errors",
        [
            ("x=5", [
                {"line": 1, "column": 2, "message": "Операторы должны быть окружены пробелами"}
            ]),
            ("y ==2", [
                {"line": 1, "column": 3, "message": "Операторы должны быть окружены пробелами"}
            ]),
            ("z* 3", [
                {"line": 1, "column": 2, "message": "Операторы должны быть окружены пробелами"}
            ]),
            ("a +b", [
                {"line": 1, "column": 3, "message": "Операторы должны быть окружены пробелами"}
            ]),
            ("x + y", []),
            ("python = cool", []),
        ]
    )
    def test_check_no_spaces_around_operators(self, linter, line, expected_errors):
        errors = linter._check_no_spaces_around_operators([line], "test.java")

        assert len(errors) == len(expected_errors)

        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]

    @pytest.mark.parametrize(
        "line,expected_errors",
        [
            ("int  x = 5", [
                {"line": 1, "column": 3, "message": "Не должно быть более одного пробела подряд внутри строки"}
            ]),
            ("String  s = \"test\"", [
                {"line": 1, "column": 6, "message": "Не должно быть более одного пробела подряд внутри строки"}
            ]),
            ("public   class Main", [
                {"line": 1, "column": 6, "message": "Не должно быть более одного пробела подряд внутри строки"}
            ]),
            ("  for (int  i = 0; i <  3; i  ++)", [
                {"line": 1, "column": 10, "message": "Не должно быть более одного пробела подряд внутри строки"},
                {"line": 1, "column": 22, "message": "Не должно быть более одного пробела подряд внутри строки"},
                {"line": 1, "column": 28, "message": "Не должно быть более одного пробела подряд внутри строки"}
            ]),
            ("int j = i                     // all good", []),
            ("int y = 1", []),
        ]
    )
    def test_check_no_spaces_more_that_one(self, linter, line, expected_errors):
        errors = linter.check_no_spaces_more_that_one([line], "test.java")

        assert len(errors) == len(expected_errors)
        for expected, actual in zip(expected_errors, errors):
            assert actual.line == expected["line"]
            assert actual.column == expected["column"]
            assert actual.message == "Не должно быть более одного пробела подряд внутри строки"

    def test_seek_for_errors(self, linter):
        lines = [
            "int a,b;",
            "int x ,y;",
            "obj . method();",
            "x=5+y",
            "int  z = 10;"
        ]
        errors = linter.seek_for_errors(lines, "test.java")

        expected_errors = [{'column': 6, 'line': 1, 'message': 'После запятой должен быть пробел'},
                           {'column': 6, 'line': 2, 'message': 'Не должно быть пробелов перед запятой'},
                           {'column': 7, 'line': 2, 'message': 'После запятой должен быть пробел'},
                           {'column': 4, 'line': 3, 'message': 'Не должно быть пробелов перед точкой'},
                           {'column': 5, 'line': 3, 'message': 'После точки не должен быть пробел'},
                           {'column': 2,
                            'line': 4,
                            'message': 'Операторы должны быть окружены пробелами'},
                           {'column': 3,
                            'line': 5,
                            'message': 'Не должно быть более одного пробела подряд внутри строки'}]

        assert len(errors) == len(expected_errors)

        actual_errors = sorted([{"line": e.line, "column": e.column, "message": e.message} for e in errors],
                               key=lambda x: (x["line"], x["column"]))
        assert actual_errors == sorted(expected_errors, key=lambda x: (x["line"], x["column"]))

    def test_disabled_checks(self):
        custom_dialect = Dialect(
            naming=NamingDialect(
                classes=NamingRule.CAMEL_CASE_CAPITAL,
                methods=NamingRule.CAMEL_CASE_LOWER,
                variables=NamingRule.CAMEL_CASE_LOWER,
            ),
            spaces=SpaceDialect(
                around_operators=False,
                no_around_brackets=False,
                after_comma=False,
                no_before_comma=False,
                no_around_dot=False,
                no_before_dot_comma=False,
                may_be_more_that_one_space=True,
            ),
            empty_lines=EmptyLineCountDialect(max_empty=2, after_method=2, after_class=3),
        )
        linter = SpaceLinter(custom_dialect)
        lines = [
            "int a,b",
            "x ,y",
            "object . method (     )",
            "x=5"
        ]
        errors = linter.seek_for_errors(lines, "test.java")

        assert len(errors) == 0
