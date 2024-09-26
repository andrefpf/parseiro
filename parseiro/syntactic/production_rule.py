from dataclasses import dataclass

from parseiro.lexical.token import Token
from parseiro.symbols import EndMarker, Epsilon, GrammarVariable


@dataclass
class ProductionRule:
    origin: GrammarVariable
    target: tuple[str]

    def get_target_symbols(self):
        return (i for i in self.target if isinstance(i, Token) or not callable(i))

    def get_non_empty_symbols(self):
        return (
            i
            for i in self.get_target_symbols()
            if not isinstance(i, (Epsilon, EndMarker, GrammarVariable))
        )

    def __str__(self) -> str:
        def representation(x):
            if type(x) == str:
                return f'"{x}"'
            return str(x)

        targets = " ".join(representation(i) for i in self.get_target_symbols())
        return f"{self.origin} → {targets}"
