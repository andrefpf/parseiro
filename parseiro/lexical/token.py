class Token:
    def __init__(self, lexeme="") -> None:
        self.lexeme = lexeme

    def consume(self, string: str) -> str:
        '''
        Use the input string to get a lexeme and return the remaining part.
        '''
        self.lexeme = ""
        return string
