from dataclasses import dataclass

from parseiro.syntactic.production_rule import ProductionRule
from parseiro.syntactic.grammar import Grammar
from parseiro.symbols import EndMarker, GrammarVariable

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
        g = Grammar()
        g['S'] = g['A'], g['A']
        g['A'] = "a", g['A']
        g['A'] = "b"

        prods = g.get_production_rules()

        table_actions = {
            (0, "a"): Stack(3),
            (0, "b"): Stack(4),

            (1, EndMarker()): Accept,
            
            (2, "a"): Stack(3),
            (2, "b"): Stack(4),
            
            (3, "a"): Stack(3),
            (3, "b"): Stack(4),

            (4, "a"): Reduce(prods[2]),
            (4, "b"): Reduce(prods[2]),
            (4, "c"): Reduce(prods[2]),

            (5, "a"): Reduce(prods[0]),
            (5, "b"): Reduce(prods[0]),
            (5, "c"): Reduce(prods[0]),

            (6, "a"): Reduce(prods[1]),
            (6, "b"): Reduce(prods[1]),
            (6, "c"): Reduce(prods[1]),
        }

        table_goto = {
            (0, g['A']): 2,
            (0, g['S']): 1,
            (2, g['A']): 5,
            (3, g['A']): 6,
        }

        sequence = string[:]
        state_stack = [0]
        symbol_stack = []

        symbol, *sequence = sequence

        while True:
            state = state_stack[-1]
            action = table_actions[state, symbol]
            
            print(state_stack)
            print(symbol_stack)
            print(symbol)
            print(sequence)

            if isinstance(action, Accept):
                print("Accept")
                break

            elif isinstance(action, Stack):
                print("Stack")
                symbol_stack.append(symbol)
                state_stack.append(action.state)
                symbol, *sequence = sequence

            elif isinstance(action, Reduce):
                print("Reduce", action.production)
                state_stack.pop()
                for _ in action.production.get_target_symbols():
                    symbol_stack.pop()
                
                state = state_stack[-1]
                symbol_stack.append(action.production.origin)
                goto = table_goto[state, action.production.origin]
                state_stack.append(goto)

            print()



if __name__ == "__main__":
    p = ParserLR1()
    p.analyze("abaab")


