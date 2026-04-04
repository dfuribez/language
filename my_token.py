from token_type import TokenType


class Token:
    type: TokenType
    value: str

    def __init__(self, ttype: TokenType, value: str) -> None:
        self.type = ttype
        self.value = value

    def __repr__(self) -> str:
        return f"<{self.type}, {self.value}>"
