import re

from my_token import Token
from token_type import TokenType

PARAMS = [
    (TokenType.NEWLINE, re.compile(r"^(\n+)", re.MULTILINE), "NEWLINE"),
    (TokenType.OPERAND, re.compile(r"^(or|and)\b", re.IGNORECASE), None),
    (TokenType.IDENT, re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)"), None),
    (TokenType.DOT, re.compile(r"^(\.)"), "DOT"),
    (TokenType.LPAREN, re.compile(r"^(\()"), None),
    (TokenType.RPAREN, re.compile(r"^(\))"), None),
    (TokenType.STRING, re.compile(r"^([\"'][^\"']+[\"'])"), None),
    (TokenType.COMMA, re.compile(r"^(,)"), None),
    (TokenType.NUMBER, re.compile(r"^(\d+(\.\d+)?)"), None),
]


COMMENT = re.compile(r"^(\s*#.*)$", re.MULTILINE)


def log(*params) -> None:
    if DEBUG:
        print(*params)


def tokenize(code: str) -> list[Token]:
    tokens: list[Token] = []

    code = code.strip()
    c: int = 0

    while c < len(code):
        chunk = code[c:]

        if chunk[0] in (" ", "\t"):
            c += 1
            continue

        comment = re.match(COMMENT, chunk)
        if comment is not None:
            c += len(comment.group(1))
            continue

        for token_type, pattern, replace in PARAMS:
            if not pattern:
                continue

            match = re.match(pattern, chunk)

            if match is not None:
                value = match.group(1)
                log("[+] Matched:", token_type, " -> ", value, f"({len(value)})")
                c += len(value)

                if token_type == TokenType.STRING:
                    value = value[1:-1]

                if replace is not None:
                    value = replace

                tokens.append(Token(token_type, value))
                break
        else:
            raise Exception(f"Unexpected character: {chunk[0]}")

    tokens.append(Token(TokenType.END, "END"))

    return tokens


DEBUG = 0


if __name__ == "__main__":
    import test

    for code in [test.CODE1, test.CODE2]:
        print("----")
        for x in tokenize(code):
            print(x)
