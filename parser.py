from lexer import tokenize
from my_token import Token
from token_types import TokenTypes


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos: int = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def eat(self, expected_type=None) -> Token:
        tok = self.current()

        if expected_type and tok.type != expected_type:
            raise Exception(f"Expected: {expected_type} but got {tok.type}")

        self.pos += 1

        return tok

    def parse(self):
        field = self.eat(TokenTypes.IDENT).value
        print(field)
        while self.pos < len(self.tokens):
            self.eat(TokenTypes.DOT)
            method = self.eat(TokenTypes.IDENT).value

            self.eat(TokenTypes.LPAREN)
            args: list[str] = []

            while self.current().type != TokenTypes.RPAREN:
                tok = self.current()
                if tok.type in (TokenTypes.STRING, TokenTypes.NUMBER):
                    args.append(tok.value)
                    self.pos += 1
                elif tok.type == TokenTypes.COMMA:
                    self.pos += 1
                else:
                    raise Exception(f"Unexpected token: {tok}")

            self.eat(TokenTypes.RPAREN)
            print(f"{method}({args})")

    def look_ahead(self):
        pass


if __name__ == "__main__":
    CODE = """
    url
    .contains("test1", "test2", "sad")
    .gt(1.2)
    .lt(0234)"""
    print(CODE)
    tokens = tokenize(CODE)

    p = Parser(tokens)
    p.parse()
