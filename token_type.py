from enum import Enum, auto


class TokenType(Enum):
    DOT = auto()
    IDENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    STRING = auto()
    NUMBER = auto()
    COMMA = auto()
    OPERAND = auto()
    END = auto()
    WHITESPACE = auto()
    NEWLINE = auto()
