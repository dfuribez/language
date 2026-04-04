from filters import Filter
from lexer import tokenize
from my_token import Token
from token_type import TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos: int = 0

    def __current(self) -> Token:
        if self.pos >= len(self.tokens):
            return Token(TokenType.END, "END")
        return self.tokens[self.pos]

    def __eat(self, type: TokenType):
        tok = self.__current()

        if tok and tok.type != type:
            raise Exception(f"Expected: {type} but got {tok.type}")

        self.pos += 1
        return tok

    def __skip_new_lines(self) -> None:
        while self.__current().type == TokenType.NEWLINE:
            self.pos += 1

    def __parse_query(self) -> dict:
        self.__skip_new_lines()

        field = self.__eat(TokenType.IDENT).value
        filters = []

        while True:
            self.__skip_new_lines()

            if self.__current().type != TokenType.DOT:
                break

            filters.append(self.__parse_call(field))

            if self.__current().type == TokenType.IDENT:
                break

        return {"field": field, "filters": filters}

    def __parse_call(self, field: str) -> Filter:
        self.__eat(TokenType.DOT)
        method = self.__eat(TokenType.IDENT).value

        self.__eat(TokenType.LPAREN)
        args = self.__parse_args()
        self.__eat(TokenType.RPAREN)

        return Filter(method, args)

    def __parse_args(self) -> list:
        args: list = []

        while self.__current().type != TokenType.RPAREN:
            tok = self.__current()
            if tok.type == TokenType.COMMA:
                self.pos += 1
            elif tok.type in (TokenType.STRING, TokenType.NUMBER):
                args.append(tok.value)
                self.pos += 1
            else:
                raise Exception(f"args: Unexpected token: {tok.type}")

        return args

    def parse(self) -> list:
        queries = []

        while self.pos < len(self.tokens):
            if self.__current().type == TokenType.END:
                break

            queries.append(self.__parse_query())

        return queries


if __name__ == "__main__":
    import test

    for code in [test.CODE1, test.CODE2]:
        tokens = tokenize(code)

        p = Parser(tokens)
        print(p.parse())
