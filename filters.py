class Filter:
    def __init__(self, method: str, args: list):
        self.method = method
        self.args = args

    def __repr__(self) -> str:
        return f"<Filter name={self.method} args={self.args}>"
