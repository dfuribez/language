class Filter:
    def __init__(self, name, args, field):
        self.name = name
        self.args = args
        self.field = field

    def __repr__(self) -> str:
        return f"<Filter name={self.name} field={self.field} args={self.args}>"
