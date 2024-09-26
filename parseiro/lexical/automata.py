from dataclasses import dataclass

from tabulate import tabulate

DEAD_STATE_INDEX = -1


@dataclass
class State:
    name: str
    is_final: bool
    tag: str = ""


class FiniteAutomata:
    def __init__(
        self,
        states: list,
        transitions: list[tuple[int, str, int]],
        alphabet: str,
        initial_state_index: int = 0,
    ):
        self.states = states
        self.initial_state_index = initial_state_index
        self.alphabet = list(alphabet)
        self.transition_map = self._create_transition_map(transitions)

    def iterate(self, string: str):
        """
        Iterates over a string yielding the current state of the automata.
        """

        current_state_index = self.initial_state_index
        yield current_state_index

        if current_state_index is DEAD_STATE_INDEX:
            return

        for symbol in string:
            current_state_index = self.compute(current_state_index, symbol)
            yield current_state_index
            if current_state_index is DEAD_STATE_INDEX:
                break

    def evaluate(self, string: str):
        """
        Checks if the string bellows to the automata language.
        """

        last_state_index = DEAD_STATE_INDEX
        for state_index in self.iterate(string):
            last_state_index = state_index

        if last_state_index == DEAD_STATE_INDEX:
            return False
        else:
            state = self.states[last_state_index]
            return state.is_final

    def match(self, string: str):
        """
        Finds the longest portion of the string (from its beginning)
        that still matches the automata language.
        """
        length = 0

        for i, state_index in enumerate(self.iterate(string)):
            if state_index == DEAD_STATE_INDEX:
                break

            state: State = self.states[state_index]
            if state.is_final:
                length = i

        return string[:length]

    def compute(self, origin, symbol):
        """
        Executes a single step of computation from a origin state through a symbol, then returns the next state.
        """
        transition = (origin, symbol)
        return self.transition_map.get(transition, DEAD_STATE_INDEX)

    def _create_transition_map(self, transitions):
        """
        Turns a list of transitions in the format [(origin, symbol, state), ..., (origin, symbol, state)] into a dict
        """
        transition_map = dict()
        for origin, symbol, target in transitions:
            transition_map[(origin, symbol)] = target
        return transition_map

    def __str__(self):
        headers = ["Q/Σ"] + self.alphabet
        data = []

        for i, state in enumerate(self.states):
            name = '"' + state.name + '"'

            if state.is_final:
                name = "* " + name

            if i == self.initial_state_index:
                name = "→ " + name

            line = [name]
            for symbol in self.alphabet:
                index = self.transition_map.get((i, symbol))
                if index is not None:
                    target = self.states[index]
                    state_name = '"' + str(target.name) + '"'  # name in quotes
                    line.append(state_name)
                else:
                    line.append("")
            data.append(line)

        return tabulate(data, headers=headers, tablefmt="fancy_grid")
