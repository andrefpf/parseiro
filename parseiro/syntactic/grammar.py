from typing import Any
from parseiro.syntactic.production_rule import ProductionRule


class GrammarVariable(str):
    def __hash__(self) -> int:
        return GrammarVariable


class Grammar:
    def __init__(self) -> None:
        self._production_rules = list()
    
    def get_production_rule(self):
        return self._production_rules

    def add_production_rule(self, origin, target):
        # Transform target into a tuple
        try:
            target = tuple(target)
        except TypeError:
            target = (target,)

        p = ProductionRule(origin, target)
        self._production_rules.append(p)
    
    def __getattr__(self, name: str):
        if name.isupper():
            return GrammarVariable(name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.isupper():
            self.add_production_rule(GrammarVariable(name), value)
        else:
            return super().__setattr__(name, value)

    def __str__(self) -> str:
        return "\n".join([str(i) for i in self._production_rules])


if __name__ == "__main__":
    from parseiro.lexical.token import Token

    class IdToken(Token):
        pass

    g = Grammar()

    g.A = "a", g.A
    g.A = "b"

    # print(Token)
    print(g)

    # g._A = "a", g._A
    # g._A = IdToken