from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple

class NamingRule(Enum):
    CAMEL_CASE_CAPITAL = "CAMEL_CASE_CAPITAL"
    CAMEL_CASE_LOWER = "CAMEL_CASE_LOWER"
    SNAKE_CASE = "SNAKE_CASE"

class Preference(Enum):
    SHOULD_BE = "SHOULD_BE"
    SHOULD_NOT_BE = "SHOULD_NOT_BE"
    DOES_NOT_MATTER = "DOES_NOT_MATTER"

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
    around_operators: Preference
    around_brackets: Preference
    after_comma: Preference
    before_comma: Preference
    may_be_more_that_one_space: bool

@dataclass
class Dialect:
    naming: NamingDialect
    spaces: SpaceDialect
    empty_lines: EmptyLineCountDialect
