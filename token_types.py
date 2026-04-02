from enum import Enum, auto


class TokenTypes(Enum):
    DOT = auto()
    IDENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    STRING = auto()
    NUMBER = auto()
    COMMA = auto()
    OPERAND = auto()
