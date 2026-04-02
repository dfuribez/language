import re

from my_token import Token
from token_types import TokenTypes

PARAMS = [
    (TokenTypes.OPERAND, re.compile("^(or|and)\b", re.IGNORECASE)),
    (TokenTypes.IDENT, re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)")),
    (TokenTypes.DOT, re.compile(r"^(\.)")),
    (TokenTypes.LPAREN, re.compile(r"^(\()")),
    (TokenTypes.RPAREN, re.compile(r"^(\))")),
    (TokenTypes.STRING, re.compile(r"^([\"'][^\"']+[\"'])")),
    (TokenTypes.COMMA, re.compile(r"^(,)")),
    (TokenTypes.NUMBER, re.compile(r"^(\d+(\.\d+)?)")),
]


def log(*params) -> None:
    if DEBUG:
        print(*params)


def tokenize(code: str) -> list[Token]:
    tokens: list[Token] = []

    code = code.strip()

    c: int = 0
    while c < len(code):
        chunk = code[c:]

        if chunk[0].isspace() or chunk[0] == ("\n"):
            c += 1
            continue

        for token_type, pattern in PARAMS:
            if not pattern:
                continue

            match = re.match(pattern, chunk)

            if match is not None:
                value = match.group(1)
                log("[+] Matched:", token_type, " -> ", value, f"({len(value)})")
                c += len(value)

                tokens.append(Token(token_type, value))
                break
        else:
            raise Exception(f"Unexpected character: {chunk[0]}")

    return tokens


DEBUG = 0

if __name__ == "__main__":
    CODE = """url.contains("test1" and "test2" or "sad").gt(12).lt(0.234)"""
    print(CODE)
    print(tokenize(CODE))
