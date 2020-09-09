from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Parentheses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        # definitions
        self.lexer.add('DEF_NOT', r'def \~')
        self.lexer.add('DEF_IMPLIE', r'def \->')
        self.lexer.add('DEF_AND', r'def \&')
        self.lexer.add('DEF_OR', r'def \|')
        self.lexer.add('DEF_IFF', r'def \<->')
        self.lexer.add('DEF_BASE', r'def A')

        # conectives
        self.lexer.add('NOT', r'\~')
        self.lexer.add('IMPLIE', r'\->')
        self.lexer.add('AND', r'\&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('IFF', r'\<->')

        #hifen
        self.lexer.add('HYPHEN', r'\-')

        #dot
        self.lexer.add('DOT', r'\.')
        self.lexer.add('COMMA', r'\,')

        # Number
        self.lexer.add('NUMBER', r'\d+')

        # Atomo
        self.lexer.add('ATHOM', r'[a-zA-Z][a-zA-Z0-9]*' )

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()