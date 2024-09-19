from parseiro.syntactic.grammar import Grammar
from parseiro.symbols import Epsilon, GrammarVariable


def test_terminal_and_non_terminal():
    g = Grammar()

    g.E  = g.T, g.E1
    g.E1 = "+", g.T, g.E1
    g.E1 = Epsilon()

    g.T  = g.F, g.T1
    g.T1 = "*", g.F, g.T1
    g.T1 = Epsilon()

    g.F  = "id"
    g.F  = "(", g.E, ")"

    correct_terminal = {Epsilon(), "(", ")", "*", "+", "id"}
    correct_non_terminal = {GrammarVariable(i) for i in ["E", "E1", "F", "T", "T1"]}

    assert g.get_terminal_symbols() == correct_terminal
    assert g.get_non_terminal_symbols() == correct_non_terminal


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

    print()
    g.print_first_follow_table()

    # print(g.get_first_set())
    # print(g.get_follow_set())