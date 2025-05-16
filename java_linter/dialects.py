from dataclasses import dataclass
from enum import Enum


class NamingRule(Enum):
    CAMEL_CASE_CAPITAL = "CAMEL_CASE_CAPITAL"
    CAMEL_CASE_LOWER = "CAMEL_CASE_LOWER"
    SNAKE_CASE = "SNAKE_CASE"


@dataclass
class NamingDialect:
    classes: NamingRule
    methods: NamingRule
    variables: NamingRule


@dataclass
class EmptyLineCountDialect:
    max_empty: int
    after_method: int
    after_class: int


@dataclass
class SpaceDialect:
    around_operators: bool
    no_around_brackets: bool
    after_comma: bool
    no_before_comma: bool
    no_before_dot_comma: bool
    no_around_dot: bool
    may_be_more_that_one_space: bool


@dataclass
class Dialect:
    naming: NamingDialect
    spaces: SpaceDialect
    empty_lines: EmptyLineCountDialect
