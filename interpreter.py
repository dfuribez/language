from lexer import tokenize
from parser import Parser


class Interpreter:
    def __init__(self) -> None:
        self.filtered = {}

    def contains(self, object: dict, key: str, *args):
        self.__check_data(object, key)
        for arg in args:
            for data in object[key]:
                if arg in data["name"]:
                    self.filtered[key].append(data)

        return self

    def __check_data(self, data: dict, key: str):
        if key not in data:
            raise Exception(f"Not {key} in provided data")

        if key not in self.filtered:
            self.filtered[key] = []

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
        ]
    }

    CODE = """
    url
    .contains("test1", "test2", "sad")
    .gt(1.2)
    .lt(0234)"""
    print(CODE)
    tokens = tokenize(CODE)

    p = Parser(tokens)
    print(p.parse())
