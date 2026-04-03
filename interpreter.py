from filters import Filter
from lexer import tokenize
from my_token import Token
from parser import Parser
from token_types import TokenTypes


class Interpreter:
    def interpret(self, data, filters: list[Filter]):
        for filter in filters:
            if filter.name == "contains":
                data = self.contains(data, filter.field, filter.args, False)
            if filter.name == "containsi":
                data = self.contains(data, filter.field, filter.args, True)

        return data

    def contains(self, object: dict, key: str, args: list[Token], ignore_case=False):
        filtered = self.__check_data(object, key)
        for arg in args:
            if arg.type != TokenTypes.STRING:
                raise Exception(f"Unexpected argument type: {arg}")

            for data in object[key]:
                if ignore_case:
                    if arg.value.lower() in data["name"].lower():
                        filtered.append(data)
                else:
                    if arg.value in data["name"]:
                        filtered.append(data)

        return {key: filtered}

    def __check_data(self, data: dict, key: str):
        if key not in data:
            raise Exception(f"Not {key} in provided data")

        return []

    def __repr__(self) -> str:
        return f"Filtered<{self.filtered}>"


if __name__ == "__main__":
    data = {
        "url": [
            {"name": "https://test", "value": 12},
            {"name": "https://interpreter", "value": 12},
            {"name": "https://gomita", "value": 12},
            {"name": "https://frunita", "value": 12},
            {"name": "https://sadsad", "value": 12},
        ],
        "data": [{"name": "asdadsasdsad"}],
    }

    CODE = """
    url
    .containsi(1)
    #.contains("it")
    .gt(1.2)
    .lt(0234)"""
    # print(CODE)
    tokens = tokenize(CODE)

    p = Parser(tokens)
    filters = p.parse()

    i = Interpreter()
    print(i.interpret(data, filters))
