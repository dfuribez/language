from filters import Filter
from lexer import tokenize
from my_token import Token
from parser import Parser
from token_type import TokenType


class Interpreter:
    ALLOWED_TYPES = {
        "contains": (TokenType.STRING, TokenType.NUMBER),
        "gt": (TokenType.NUMBER,),
    }

    def __init__(self, code: str):
        tokens = tokenize(code)
        self.__filters = Parser(tokens).parse()

    def interpret(self):
        result = {}
        for filter in self.__filters:
            result = self.__parse_dict(filter["field"], result)
            for f in filter["filters"]:
                if f.method == "contains":
                    print(f.args)
                    result[filter["field"]].extend(self.__contains(f.args))
                if f.method == "gt":
                    result[filter["field"]].extend(self.__gt(f.args))

        return result

    def __parse_dict(self, field: str, result: dict) -> dict:
        if field in result:
            return result
        result[field] = []
        return result

    def __contains(self, args: list[Token], ignore_case=False):
        self.__check_argument_type(args, self.ALLOWED_TYPES["contains"])

        args_values = [arg.value for arg in args]

        def f(d):
            return any(v in d for v in args_values)

        return [f]

    def __gt(self, args: list[Token]):
        if len(args) > 1:
            args = [args[-1]]
        self.__check_argument_type(args, self.ALLOWED_TYPES["gt"])

        def f(data):
            return data > args[0].value

        return [f]

    def __check_argument_type(self, arguments: list[Token], allowed: tuple):
        for argument in arguments:
            if argument.type not in allowed:
                raise Exception("method has invalid arguments")

    def __repr__(self) -> str:
        return f"Filtered<{self.filtered}>"


def generator(data, functions):
    for function in functions:
        data = [d for d in data if function(d)]
    print(data)


if __name__ == "__main__":
    import test

    data = {
        "url": [
            "https://test",
            "https://interpreter",
            "https://gomita",
            "https://frunita",
            "https://sadsad",
        ],
        "data": ["asdadsasdsad"],
    }

    CODE = """url.contains("a", "b").contains("a")"""

    for code in [CODE]:
        i = Interpreter(code)

        function = i.interpret()
        for field, functions in function.items():
            print(field)
            generator(data[field], functions)
    # print(i.interpret(data, filters))
