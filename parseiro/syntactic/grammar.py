from parseiro.syntactic.production_rule import ProductionRule


class GrammarVariable(str):
    def __hash__(self) -> int:
        return GrammarVariable


class Grammar:
    def __init__(self) -> None:
        self.production_rules = list()

    def add_production_rule(self, origin, target):
        p = ProductionRule(origin, target)
        self.production_rules.append(p)

    def __getitem__(self, key):
        return GrammarVariable(key)

    def __setitem__(self, key, val):
        # Transform val into a tuple
        try:
            val = tuple(val)
        except TypeError:
            val = (val,)
        self.add_production_rule(GrammarVariable(key), val)
    
    def __str__(self) -> str:
        return "\n".join([str(i) for i in self.production_rules])
