from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        #Comma
        self.lexer.add('COMMA', r'\,')

        # Dot
        self.lexer.add('DOT', r'\.')

        # Parentheses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        #Brackets
        self.lexer.add('OPEN_BRACKET', r'\{')
        self.lexer.add('CLOSE_BRACKET', r'\}')

        #rules
        self.lexer.add('IMP_INTROD', r'\->i')
        self.lexer.add('IMP_ELIM', r'\->e')
        self.lexer.add('OR_INTROD', r'\|i')
        self.lexer.add('OR_ELIM', r'\|e')
        self.lexer.add('AND_INTROD', r'\&i')
        self.lexer.add('AND_ELIM', r'\&e')
        self.lexer.add('NEG_INTROD', r'\~i')
        self.lexer.add('NEG_ELIM', r'~e')
        self.lexer.add('RAA', r'raa')
        self.lexer.add('BOTTOM', r'\@')

        # Connectives
        self.lexer.add('NOT', r'\~')
        self.lexer.add('IMPLIE', r'\->')
        self.lexer.add('AND', r'\&')
        self.lexer.add('OR', r'\|')

        # Number
        self.lexer.add('NUM', r'\d+')

        #justification
        self.lexer.add('HYPOTESIS', r'hip')
        self.lexer.add('PREMISE', r'pre')

        # Athom
        self.lexer.add('ATHOM', r'[a-zA-Z][a-zA-Z0-9]*' )

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()