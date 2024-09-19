from dataclasses import dataclass


@dataclass
class ProductionRule:
    origin: str
    target: str
    
    def target_symbols(self):
        return (i for i in self.target)

    def non_empty_symbols(self):
        return (i for i in self.target_symbols() if not isinstance(i, int))

    def __str__(self) -> str:
        def representation(x):
            if type(x) == str:
                return f'"{x}"'
            return str(x)

        targets = " ".join(representation(i) for i in self.target_symbols())
        return f"{self.origin} → {targets}"
