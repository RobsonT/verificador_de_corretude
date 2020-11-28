from rply import ParserGenerator
#from ast import negationDef, binaryDef
from formule import BinaryFormule, NegationFormule, AthomFormule

class Parser():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUM', 'DOT', 'COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 
             'ATHOM', 'NOT', 'IMPLIE', 'AND', 'OR', 'IMP_INTROD', 'AND_INTROD',
             'NEG_INTROD', 'NEG_ELIM', 'HYPOTESIS', 'PREMISE'],
            precedence=[
                ('left', ['NOT','AND', 'OR', 'IMPLIE'])
            ]
        )

    def parse(self):
        @self.pg.production('program : steps')
        def program(p):
            #TODO 
            print('Fórmula está correta')

        @self.pg.production('steps : steps step')
        @self.pg.production('steps : step')
        def steps(p):
            #TODO 
            print("fim")

        @self.pg.production('step : NUM DOT formule NEG_ELIM NUM COMMA NUM')
        def Negation(p):
            print("Negação")

        @self.pg.production('formule : NOT formule')
        @self.pg.production('formule : ATHOM')
        def formule(p):
            if len(p) == 1:
                print('test 1')
                return p[0].value
            else:
                print('test 2')
                return p[0].value + p[1]

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
        