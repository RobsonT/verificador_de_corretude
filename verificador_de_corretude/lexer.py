from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Dot
        self.lexer.add('DOT', r'\.')

        # Parentheses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        # Connectives and rules
        self.lexer.add('NOT', r'\~')
        self.lexer.add('IMPLIE', r'\->')
        self.lexer.add('AND', r'\&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('RAA', r'raa')
        self.lexer.add('BOTTOM', r'\@')

        # Number
        self.lexer.add('NUM', r'\d+')

        # Proposition
        self.lexer.add('PROPOSITION', r'[a-zA-Z][a-zA-Z0-9]*' )

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()