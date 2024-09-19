from typing import Any
from collections import defaultdict
from itertools import pairwise
from functools import cache

from parseiro.symbols import GrammarVariable, Epsilon, EndMarker
from parseiro.syntactic.production_rule import ProductionRule


class Grammar:
    def __init__(self) -> None:
        self._production_rules: list[ProductionRule] = list()
    
    def get_production_rule(self):
        return self._production_rules

    def add_production_rule(self, origin, target):
        # Transform target into a tuple
        try:
            target = tuple(target)
        except TypeError:
            target = (target,)

        self.get_first_set.cache_clear()
        self.get_follow_set.cache_clear()

        p = ProductionRule(GrammarVariable(origin), target)
        self._production_rules.append(p)
    
    def non_terminal_symbols(self):
        return {production.origin for production in self._production_rules}

    def terminal_symbols(self):
        non_empty = {production.non_empty_symbols() for production in self._production_rules}
        return non_empty - self.non_terminal_symbols()

    @cache
    def get_first_set(self):
        first = defaultdict(set)

        for symbol in self.terminal:
            first[symbol].add(symbol)

        modified = True
        while modified:
            modified = False

            for production in self._production_rules:
                for symbol in production.get_target_symbols():
                    if symbol == Epsilon():
                        modified |= Epsilon() not in first[production.origin]
                        first[production.origin].add(Epsilon())

                    to_append = first[symbol] - {Epsilon()}
                    modified |= not to_append.issubset(first[production.origin])
                    first[production.origin] |= to_append

                    if Epsilon() not in first[symbol]:
                        break

                else:
                    modified |= Epsilon() not in first[production.origin]
                    first[production.origin].add(Epsilon())

        first.pop(Epsilon(), None)
        return dict(first)

    @cache
    def get_follow_set(self):
        first = self.get_first_set()
        follow = defaultdict(set)

        start_symbol = self._production_rules[0].origin
        follow[start_symbol].add(EndMarker())

        modified = True
        while modified:
            modified = False

            for production in self._production_rules:
                target_symbols = production.get_target_symbols()

                for sym_a, sym_b in pairwise(target_symbols):
                    to_append = first[sym_b] - {Epsilon()}
                    modified |= not to_append.issubset(follow[sym_a])
                    follow[sym_a] |= to_append

                if target_symbols:
                    last_symbol = target_symbols[-1]
                    modified |= not follow[production.origin].issubset(
                        follow[last_symbol]
                    )
                    follow[last_symbol] |= follow[production.origin]

                if len(target_symbols) >= 2:
                    if Epsilon() in first[sym_b]:
                        follow[sym_a] |= follow[production.origin]

        follow.pop(Epsilon(), None)
        return dict(follow)

    def __getattr__(self, name: str):
        if name.isupper():
            return GrammarVariable(name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.isupper():
            self.add_production_rule(name, value)
        else:
            return super().__setattr__(name, value)

    def __str__(self) -> str:
        return "\n".join([str(i) for i in self._production_rules])


if __name__ == "__main__":
    from parseiro.lexical.token import RegexToken

    class Identifier(RegexToken):
        regex = r"1234"

    g = Grammar()

    g.A = "a", g.A
    g.A = "b", Identifier

    print(g)
