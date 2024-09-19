from typing import Any
from parseiro.syntactic.production_rule import ProductionRule


class GrammarVariable(str):
    def __hash__(self) -> int:
        return GrammarVariable


class Grammar:
    def __init__(self) -> None:
        self.__production_rules = list()

    def add_production_rule(self, origin, target):
        # Transform target into a tuple
        try:
            target = tuple(target)
        except TypeError:
            target = (target,)

        p = ProductionRule(origin, target)
        self.__production_rules.append(p)

    def __getitem__(self, name: str) -> GrammarVariable:
        return GrammarVariable(name)

    def __setitem__(self, name: str, value: Any):
        self.add_production_rule(GrammarVariable(name), value)        

    def __str__(self) -> str:
        return "\n".join([str(i) for i in self.__production_rules])


if __name__ == "__main__":
    from parseiro.lexical.token import Token

    class IdToken(Token):
        pass

    g = Grammar()
    g["A"] = "a", g["A"]
    g["A"] = "b"

    # print(Token)
    print(g)

    # g._A = "a", g._A
    # g._A = IdToken