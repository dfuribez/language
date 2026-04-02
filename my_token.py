from token_types import TokenTypes


class Token:
    type: TokenTypes
    value: str

    def __init__(self, ttype: TokenTypes, value: str) -> None:
        self.type = ttype
        self.value = value

    def __repr__(self) -> str:
        return f"<{self.type}, {self.value}>"
