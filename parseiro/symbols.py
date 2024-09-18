class CustomSymbol(str):
    def __hash__(self) -> int:
        return hash(f"{self.__class__.__name__}({self})")
    
    def __eq__(self, other: object) -> bool:
        return type(self) == type(other)


class Epsilon(CustomSymbol):
    def __repr__(self) -> str:
        return "Є"


class EndMarker(CustomSymbol):
    def __repr__(self) -> str:
        return "$"
