from parseiro.syntactic.grammar import Grammar
from parseiro.symbols import Epsilon


def test_first_follow():
    g = Grammar()

    g.E  = g.T, g.E1
    g.E1 = "+", g.T, g.E1
    g.E1 = Epsilon()

    g.T  = g.F, g.T1
    g.T1 = "*", g.F, g.T1
    g.T1 = Epsilon()

    g.F  = "id"
    g.F  = "(", g.E, ")"

    print(g.get_first_set())
    print(g.get_follow_set())