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

        # Connectives
        self.lexer.add('NOT', r'\~')
        self.lexer.add('IMPLIE', r'\->')
        self.lexer.add('AND', r'\&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('RAA', r'raa')
        self.lexer.add('BOTTOM', r'\@')

        #rules
        #TODO implie elimination
        #TODO implie introduction
        #TODO or elimination
        #TODO or introduction
        #TODO And elimination
        #TODO And introduction
        self.lexer.add('NEG_INTROD', r'\~i')
        self.lexer.add('NEG_ELIM', r'\~e')
        self.lexer.add('RAA', r'raa')
        self.lexer.add('BOTTOM', r'\@')

        # Number
        self.lexer.add('NUM', r'\d+')

        # Athom
        self.lexer.add('ATHOM', r'[a-zA-Z][a-zA-Z0-9]*' )

        #justification
        #TODO hypothesis
        #TODO premise

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()