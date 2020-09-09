from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Dot
        # TODO

        # Epsilon
        # TODO

        # Parentheses
        # TODO open parentheses
        # TODO close parentheses

        # Connectives and rules
        self.lexer.add('NOT', r'\~')
        self.lexer.add('IMPLIE', r'\->')
        self.lexer.add('AND', r'\&')
        self.lexer.add('OR', r'\|')
        # TODO RAA
        # TODO Contradiction

        # Number
        self.lexer.add('NUM', r'\d+')

        # Proposition
        self.lexer.add('PROPOSITION', r'[a-zA-Z][a-zA-Z0-9]*' )

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()