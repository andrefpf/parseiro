from pprint import pprint

from parseiro.symbols import EndMarker, Epsilon, GrammarVariable
from parseiro.syntactic.grammar import Grammar


def test_terminal_and_non_terminal():
    g = Grammar()

    g.E = g.T, g.E1
    g.E1 = "+", g.T, g.E1
    g.E1 = Epsilon()

    g.T = g.F, g.T1
    g.T1 = "*", g.F, g.T1
    g.T1 = Epsilon()

    g.F = "id"
    g.F = "(", g.E, ")"

    correct_terminal = {Epsilon(), "(", ")", "*", "+", "id"}
    correct_non_terminal = {GrammarVariable(i) for i in ["E", "E1", "F", "T", "T1"]}

    assert set(g.get_terminal_symbols()) == correct_terminal
    assert set(g.get_non_terminal_symbols()) == correct_non_terminal


def test_first_follow():
    g = Grammar()

    g.E = g.T, g.E1
    g.E1 = "+", g.T, g.E1
    g.E1 = Epsilon()

    g.T = g.F, g.T1
    g.T1 = "*", g.F, g.T1
    g.T1 = Epsilon()

    g.F = "id"
    g.F = "(", g.E, ")"

    # https://www.geeksforgeeks.org/construction-of-ll1-parsing-table/
    correct_first_set = {
        "id": {"id"},
        "(": {"("},
        ")": {")"},
        "+": {"+"},
        "*": {"*"},
        GrammarVariable("E"): {"id", "("},
        GrammarVariable("E1"): {"+", Epsilon()},
        GrammarVariable("T"): {"id", "("},
        GrammarVariable("T1"): {"*", Epsilon()},
        GrammarVariable("F"): {"id", "("},
    }

    correct_follow_set = {
        GrammarVariable("E"): {EndMarker(), ")"},
        GrammarVariable("E1"): {EndMarker(), ")"},
        GrammarVariable("T"): {"+", EndMarker(), ")"},
        GrammarVariable("T1"): {"+", EndMarker(), ")"},
        GrammarVariable("F"): {"*", "+", EndMarker(), ")"},
    }

    for s in correct_first_set.keys():
        assert correct_first_set[s] == g.get_first_set()[s]

    for s in correct_follow_set.keys():
        assert correct_follow_set[s] == g.get_follow_set()[s]

    assert correct_first_set == g.get_first_set()
    assert correct_follow_set == g.get_follow_set()

    print()
    g.print_first_follow_table()
