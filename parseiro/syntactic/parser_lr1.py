from dataclasses import dataclass
from production_rule import ProductionRule


class LR1Action:
    pass

@dataclass
class Stack(LR1Action):
    state: int


@dataclass
class Reduce(LR1Action):
    production: ProductionRule


class Accept(LR1Action):
    pass


class ParserLR1:
    def analyze(self, string: str):
        pass


if __name__ == "__main__":
    p = ParserLR1()
    p.analyze("n+n*n")


