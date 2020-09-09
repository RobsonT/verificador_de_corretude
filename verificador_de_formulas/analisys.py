from rply import ParserGenerator
from ast import negationDef, binaryDef
from formule import BinaryFormule, UnaryFormule
import sys
#sys.tracebacklimit = 0

class Parser():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'DOT', 'COMMA', 'HYPHEN', 'OPEN_PAREN', 'CLOSE_PAREN', 
             'ATHOM', 'DEF_BASE', 'DEF_NOT', 'NOT', 'IFF', 'IMPLIE', 'AND', 'OR',
             'DEF_IFF', 'DEF_IMPLIE', 'DEF_AND', 'DEF_OR'],
            precedence=[
                ('left', ['NOT','AND', 'OR', 'IMPLIE', 'IFF'])
            ]
        )
        self.variables = {}
        self.error = {
            'messages': []
        }

    def parse(self):
        @self.pg.production('program : steps')
        def program(p):
            formules = p[0]
            if len(self.error['messages']):
                print('Os seguintes erros foram encontrados:')
                error_number = 1

                for error_message in self.error['messages']:
                    print('Erro {}: {}'.format(error_number, error_message))
                    error_number += 1
            else:
                print('Fórmulas estão corretas.')

        @self.pg.production('steps : steps step')
        @self.pg.production('steps : step')
        def steps(p):
            return self.variables

        @self.pg.production('step : NUMBER DOT ATHOM athoms DEF_BASE')
        def step_base(p):
            number_line = p[0].value
            athoms = [p[2].value] + p[3]
            line_text = '{}. {} def A'.format(number_line, athoms)

            if number_line in self.variables:
                for athom in athoms:
                    self.variables[number_line].append(BinaryFormule(key=athom))
                source_position = p[0].getsourcepos()
                line_error = source_position.lineno
                self.set_error(1, line_error, line_text, number_line)
                return
                
            self.variables[number_line] = []
            for athom in athoms:
                self.variables[number_line].append(BinaryFormule(key=athom))

        @self.pg.production('step : NUMBER DOT formule DEF_NOT NUMBER')
        def step_negation(p):
            number_line = p[0].value
            formule = p[2] 
            if not isinstance(formule.key, str):
                operator = formule.key.key
            else:
                operator = formule.key

            line_text = '{}. {} def ~ {}'.format(number_line, formule.toString(), p[4].value)

            source_position = p[0].getsourcepos()
            line_error = source_position.lineno

            if operator in ['<->', '->', '&', '|']:
                self.variables[number_line] = [formule]
                self.set_error(3, line_error, line_text, formule.toString())
                return

            if number_line in self.variables:
                self.variables[number_line] = self.variables[number_line] + [formule]
                
                self.set_error(1, line_error, line_text, number_line)
                return

            if not(p[4].value in self.variables):
                self.variables[number_line] = [formule]
                self.set_error(2, line_error, line_text, p[4].value)
                return

            self.variables[number_line] = [formule]
            if not(negationDef().eval(formule, p[4].value, self.variables)):
                self.set_error(4, line_error, line_text, formule.toString())

        @self.pg.production('step : NUMBER DOT formule AND formule DEF_AND NUMBER HYPHEN NUMBER')
        @self.pg.production('step : NUMBER DOT formule OR formule DEF_OR NUMBER HYPHEN NUMBER')
        @self.pg.production('step : NUMBER DOT formule IMPLIE formule DEF_IMPLIE NUMBER HYPHEN NUMBER')
        @self.pg.production('step : NUMBER DOT formule IFF formule DEF_IFF NUMBER HYPHEN NUMBER')
        def step(p):
            number_line = p[0].value
            operator = p[3].value    
            used_formule1_line = p[6].value
            used_formule2_line = p[8].value

            formule = BinaryFormule(key = operator, left=p[2], right=p[4])

            line_text = '{}. {} {} {}-{}'.format(number_line, formule.toString(), p[5].value, p[6].value, p[8].value)
            
            line_error = p[0].getsourcepos().lineno

            if number_line in self.variables:
                self.variables[number_line] = self.variables[number_line] + [formule]
                self.set_error(1, line_error, line_text, number_line)
                return

            if not(used_formule1_line in self.variables):
                self.variables[number_line] = [formule]
                self.set_error(2, line_error, line_text, used_formule1_line)
                return

            if not(used_formule2_line in self.variables):
                self.variables[number_line] = [formule]
                self.set_error(2, line_error, line_text, used_formule2_line)
                return

            self.variables[number_line] = [formule]
            result = binaryDef().eval(p[2], p[4], operator, used_formule1_line, used_formule2_line, self.variables)
            if result == 0:
                self.set_error(0, line_error, line_text, p[2].toString())
            elif result == 1:
                self.set_error(0, line_error, line_text, p[4].toString())

        @self.pg.production('formule : NOT formule')
        @self.pg.production('formule : ATHOM')
        @self.pg.production('formule : formule AND formule')
        @self.pg.production('formule : formule OR formule')
        @self.pg.production('formule : formule IMPLIE formule')
        @self.pg.production('formule : formule IFF formule')
        def formule(p):
            if len(p) < 3:
                if p[0].gettokentype() == 'ATHOM':
                    return BinaryFormule(key=p[0].value)
                if p[0].gettokentype() == 'NOT':
                    return UnaryFormule(key=p[1])
            else:
                return BinaryFormule(key=p[1].value, left=p[0], right=p[2])

        @self.pg.production('formule : OPEN_PAREN formule CLOSE_PAREN')
        def paren_formule(p):
            return p[1]
        @self.pg.production('athoms : COMMA ATHOM athoms')
        @self.pg.production('athoms : ')
        def athoms(p):
            if(len(p) == 0):
                return []
            else:
                return [p[1].value]+p[2]

        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            source_position = token.getsourcepos()
            line, column = source_position.lineno, source_position.colno
            raise ValueError("token {} não esperado na linha {}: {}".format(token.value, line, productions[line-1]))


    def set_error(self, type, line_error, line_text, token_error):
        if type == 0:
            self.error['messages'].append("A fórmula {} não foi definido anteriormente, na linha {}: {}".format(token_error, line_error, line_text))
        elif type == 1:
            self.error['messages'].append("Número {} já foi definido antes da linha {}: {}".format(token_error, line_error, line_text))
        elif type == 2:
            self.error['messages'].append("linha não definida {} referenciado na linha {}: {}".format(token_error, line_error, line_text))
        elif type == 3:
            self.error['messages'].append("Fórmula {} é binaria, quando o esperado é uma negação, na linha {}: {}".format(token_error, line_error, line_text))
        else: 
            self.error['messages'].append("Fórmula {} não urilizado na linha {} não foi definido anteriormente: {}".format(token_error[1:], line_error, line_text))
            
    def get_parser(self):
        return self.pg.build()