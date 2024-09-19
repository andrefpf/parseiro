from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from parseiro.lexical.automata import FiniteAutomata


class MetaToken(type):
    def __str__(self) -> str:
        cls, *_ = self.mro()
        return f"<{cls.__name__}>"


class Token(metaclass=MetaToken):
    def __init__(self, lexeme="") -> None:
        self.lexeme = lexeme

    def consume(self, string: str) -> str:
        '''
        Use the input string to get a lexeme and return the remaining part.
        '''
        self.lexeme = string[0]
        return string[1:]

    def __str__(self) -> str:
        cls = self.__class__
        return f'<{cls.__name__} "{self.lexeme}">'


class RegexToken(Token):
    regex: str = ""
    automata: "FiniteAutomata | None"

    def __init_subclass__(cls) -> None:
        # TODO: create the actual automata here with cls.regex
        cls.automata = None
        return super().__init_subclass__()

    def consume(self, string: str) -> str:
        # TODO: consume according to the regex
        return super().consume(string)
