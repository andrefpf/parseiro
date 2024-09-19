class CustomSymbol(str):
    def __hash__(self) -> int:
        name = self.__class__.__name__
        return hash((name, str(self)))
    
    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other)


class Epsilon(CustomSymbol):
    def __repr__(self) -> str:
        return "Є"


class EndMarker(CustomSymbol):
    def __repr__(self) -> str:
        return "$"


class GrammarVariable(str):
    def __hash__(self) -> int:
        return hash(("GrammarVariable", str(self)))
