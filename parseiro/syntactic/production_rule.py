from dataclasses import dataclass


@dataclass
class ProductionRule:
    origin: str
    target: str
    
    def target_symbols(self):
        return (i for i in self.target if not callable(i))

    def non_empty_symbols(self):
        return (i for i in self.target_symbols() if not isinstance(i, int))

    def __str__(self) -> str:
        targets = " ".join(str(i) for i in self.target_symbols())
        return f"{self.origin} → {targets}"
