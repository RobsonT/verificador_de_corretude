from rply import ParserGenerator
from ast import negationDef, binaryDef
from formule import BinaryFormule, UnaryFormule
import sys
from file_handle import fileHandle
sys.tracebacklimit = 0

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
        self.formule_latex = ''
        self.error = {
            'messages': []
        }

    def parse(self):
        @self.pg.production('program : steps')
        def program(p):
            data = {}

            if len(self.error['messages']):
                firstMessage = 'Os seguintes erros foram encontrados:'
                
                data["status"] = "error"
                data["firstMessage"] = firstMessage

                error_number = 1
                errorList = []

                for error_message in self.error['messages']:
                    errorList.append('Erro {}: {}'.format(error_number, error_message))
                    error_number += 1

                data["errorList"] = errorList
                data["errorNumber"] = error_number
            else:
                firstMessage = 'Fórmulas estão corretas. Código látex:'

                data["status"] = 'ok'
                data["firstMessage"] = firstMessage

                latex = '\\[\n' + self.variables[list(self.variables)[-1]][0].toLatex() +'\\]\n'
                
                data["latex"] = latex

            fileHandle(data)


        @self.pg.production('steps : steps step')
        @self.pg.production('steps : step')
        def steps(p):
            return self.variables

        @self.pg.production('step : NUMBER DOT ATHOM athoms DEF_BASE')
        def step_base(p):
            number_line = p[0].value
            athoms = [p[2].value] + p[3]

            if number_line in self.variables:
                for athom in athoms:
                    self.variables[number_line].append(BinaryFormule(key=athom))
                source_position = p[0].getsourcepos()
                line_error = source_position.lineno
                self.set_error(1, line_error, number_line)
                return
                
            self.variables[number_line] = []
            for athom in athoms:
                self.variables[number_line].append(BinaryFormule(key=athom))

        @self.pg.production('step : NUMBER DOT formule DEF_NOT NUMBER')
        def step_negation(p):
            number_line = p[0].value
            formule = p[2]

            source_position = p[0].getsourcepos()
            line_error = source_position.lineno

            if isinstance(formule, BinaryFormule):
                self.variables[number_line] = [formule]
                self.set_error(3, line_error, formule.toString())
                return

            if number_line in self.variables:
                self.variables[number_line] = self.variables[number_line] + [formule]
                
                self.set_error(1, line_error, number_line)
                return

            if not(p[4].value in self.variables):
                self.variables[number_line] = [formule]
                self.set_error(2, line_error, p[4].value)
                return

            self.variables[number_line] = [formule]
            if not(negationDef().eval(formule, p[4].value, self.variables)):
                self.set_error(4, line_error, formule.toString())

        @self.pg.production('step : NUMBER DOT formule DEF_AND NUMBER HYPHEN NUMBER')
        @self.pg.production('step : NUMBER DOT formule DEF_OR NUMBER HYPHEN NUMBER')
        @self.pg.production('step : NUMBER DOT formule DEF_IMPLIE NUMBER HYPHEN NUMBER')
        @self.pg.production('step : NUMBER DOT formule DEF_IFF NUMBER HYPHEN NUMBER')
        def step(p):
            formule = p[2]
            operator = formule.key
            
            line_error = p[0].getsourcepos().lineno

            number_line = p[0].value 

            used_formule1_line = p[4].value
            used_formule2_line = p[6].value

            if number_line in self.variables:
                self.variables[number_line] = self.variables[number_line] + [formule]
                self.set_error(1, line_error, number_line)
                return

            if not(used_formule1_line in self.variables):
                self.variables[number_line] = [formule]
                self.set_error(2, line_error, used_formule1_line)
                return

            if not(used_formule2_line in self.variables):
                self.variables[number_line] = [formule]
                self.set_error(2, line_error, used_formule2_line)
                return

            self.variables[number_line] = [formule]
            result = binaryDef().eval(p[2], operator, used_formule1_line, used_formule2_line, self.variables)
            if result == 0:
                self.set_error(0, line_error, formule.left.toString())
            elif result == 1:
                self.set_error(0, line_error, formule.right.toString())

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
            error = ''
            if(productions == ['']):
                error = 'Nenhuma demonstração foi recebida, verifique a entrada.'
            if token.gettokentype() == '$end':
                error = 'Uma das definições não está completa, verifica se todas regras foram aplicadas corretamente.'
            else:
                source_position = token.getsourcepos()
                line = source_position.lineno
                error = "token {} não esperado na linha {}: {}".format(token.value, line, productions[line-1])
                
            data = {
                'status': 'error',
                'firstMessage': 'O seguinte erro foi encontrado',
                'error': error
            }

            fileHandle(data)

            raise ValueError(error)


    def set_error(self, type, line_error, token_error):
        productions = self.state.splitlines()
        if type == 0:
            self.error['messages'].append("A fórmula {} não foi definido anteriormente, na linha {}: {}".format(token_error, line_error, productions[line_error-1]))
        elif type == 1:
            self.error['messages'].append("Número {} já foi definido antes da linha {}: {}".format(token_error, line_error, productions[line_error-1]))
        elif type == 2:
            self.error['messages'].append("linha não definida {} referenciado na linha {}: {}".format(token_error, line_error, productions[line_error-1]))
        elif type == 3:
            self.error['messages'].append("Fórmula {} é binaria, quando o esperado é uma negação, na linha {}: {}".format(token_error, line_error, productions[line_error-1]))
        else: 
            self.error['messages'].append("Fórmula {} utilizado na linha {} não foi definido anteriormente: {}".format(token_error[1:], line_error, productions[line_error-1]))
            
    def get_parser(self):
        return self.pg.build()