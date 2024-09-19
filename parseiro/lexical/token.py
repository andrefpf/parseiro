class MetaToken(type):
    def __str__(self) -> str:
        obj, *_ = self.mro()
        return f"<{obj.__name__}>"


class Token(str, metaclass=MetaToken):
    def __init__(self, lexeme="") -> None:
        self.lexeme = lexeme

    def consume(self, string: str) -> str:
        '''
        Use the input string to get a lexeme and return the remaining part.
        '''
        self.lexeme = string[0]
        return string[1:]
