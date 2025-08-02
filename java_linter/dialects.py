from enum import Enum
from typing import NamedTuple


class NamingRule(Enum):
    CAMEL_CASE_CAPITAL = "CAMEL_CASE_CAPITAL"
    CAMEL_CASE_LOWER = "CAMEL_CASE_LOWER"
    SNAKE_CASE = "SNAKE_CASE"


class NamingDialect(NamedTuple):
    classes: NamingRule
    methods: NamingRule
    variables: NamingRule


class EmptyLineCountDialect(NamedTuple):
    max_empty: int
    after_method: int
    after_class: int


class SpaceDialect(NamedTuple):
    around_operators: bool
    no_around_brackets: bool
    after_comma: bool
    no_before_comma: bool
    no_before_dot_comma: bool
    no_around_dot: bool
    may_be_more_that_one_space: bool


class Dialect(NamedTuple):
    naming: NamingDialect
    spaces: SpaceDialect
    empty_lines: EmptyLineCountDialect
