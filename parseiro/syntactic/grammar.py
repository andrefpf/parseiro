from collections import defaultdict
from functools import cache
from itertools import pairwise
from typing import Any, Iterator

from tabulate import tabulate

from parseiro.lexical.token import Token
from parseiro.symbols import EndMarker, Epsilon, GrammarVariable
from parseiro.syntactic.production_rule import ProductionRule


class Grammar:
    def __init__(self) -> None:
        self._production_rules: list[ProductionRule] = list()

    def get_production_rules(self):
        return self._production_rules

    def add_production_rule(self, origin: (GrammarVariable | str), target: tuple[GrammarVariable | str | Token]):
        if not isinstance(origin, GrammarVariable):
            origin = GrammarVariable(origin)

        self.get_first_set.cache_clear()
        self.get_follow_set.cache_clear()

        p = ProductionRule(origin, target)
        self._production_rules.append(p)

    def get_non_terminal_symbols(self) -> Iterator[GrammarVariable]:
        repeated = set()
        for production in self.get_production_rules():
            if production.origin in repeated:
                continue
            repeated.add(production.origin)
            yield production.origin

    def get_terminal_symbols(self) -> Iterator[Token | str]:
        repeated = set()
        for production in self.get_production_rules():
            for symbol in production.get_target_symbols():
                if symbol in repeated:
                    continue

                if isinstance(symbol, GrammarVariable):
                    continue

                repeated.add(symbol)
                yield symbol

    @cache
    def get_first_set(self):
        first = defaultdict(set)

        for symbol in self.get_terminal_symbols():
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
                target_symbols = list(production.get_target_symbols())

                sym_a, sym_b = None, None
                for sym_a, sym_b in pairwise(target_symbols):
                    to_append = first[sym_b] - {Epsilon()}
                    modified |= not to_append.issubset(follow[sym_a])
                    follow[sym_a] |= to_append

                if (sym_a is None) and (sym_b is None):
                    continue

                if target_symbols:
                    last_symbol = target_symbols[-1]
                    modified |= not follow[production.origin].issubset(
                        follow[last_symbol]
                    )
                    follow[last_symbol] |= follow[production.origin]

                if len(target_symbols) >= 2:
                    if Epsilon() in first[sym_b]:
                        follow[sym_a] |= follow[production.origin]

        for symbol in self.get_terminal_symbols():
            follow.pop(symbol, None)
        follow.pop(Epsilon(), None)

        return dict(follow)

    def print_first_follow_table(self):
        first_set = self.get_first_set()
        follow_set = self.get_follow_set()

        headers = ["Symbol", "First", "Follow"]
        data = []

        for symbol in self.get_non_terminal_symbols():
            first = " ".join(str(i) for i in sorted(first_set[symbol]))
            follow = " ".join(str(i) for i in sorted(follow_set[symbol]))
            row = (symbol, first, follow)
            data.append(row)

        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print(table)

    def __getitem__(self, name: str) -> GrammarVariable:
        return GrammarVariable(name)

    def __setitem__(self, name: GrammarVariable | str, value: Any) -> None:        
        # turn value into a tuple
        if isinstance(value, (str, GrammarVariable, Token)):
            value = (value,)
        self.add_production_rule(name, value)

    def __str__(self) -> str:
        return "\n".join([str(i) for i in self._production_rules])


if __name__ == "__main__":
    from parseiro.lexical.token import RegexToken

    class Identifier(RegexToken):
        regex = r"1234"

    g = Grammar()
    g["Hello"] = "a", g["Hello"]
    g["Hello"] = "b", Identifier
