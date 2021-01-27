from rply import ParserGenerator
from ast import NegationEliminationDef, HypotesisDef, PremisseDef
from formule import BinaryFormule, NegationFormule, AthomFormule
from symbol_table import SymbolTable

class Parser():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUM', 'DOT', 'COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT', 'IMPLIE',
             'AND', 'OR', 'IMP_INTROD', 'AND_INTROD', 'BOTTOM', 'OPEN_BRACKET',
             'NEG_INTROD', 'NEG_ELIM', 'HYPOTESIS', 'PREMISE', 'ATHOM', 'CLOSE_BRACKET'],
            precedence=[
                ('left', ['NOT','AND', 'OR', 'IMPLIE']),
            ]
        )
        self.symbol_table = SymbolTable()

    def parse(self):
        @self.pg.production('program : steps')
        def program(p):
            formules = p[0]
            for i in range(0, len(formules)):
                formule = formules[i]
                rule = self.symbol_table.get_rule(formule.toString())
                if(isinstance(rule, PremisseDef) ):
                    pass
                elif(isinstance(rule, HypotesisDef)):
                    pass
                elif(isinstance(rule, NegationEliminationDef)):
                    formule1 = self.symbol_table.lookup_formule_by_line(rule.formule, rule.reference1)
                    formule2 = self.symbol_table.lookup_formule_by_line(rule.formule, rule.reference2)
                    if(rule.eval(formule1, formule2) == 4):
                        print('Deu certo')
                    else:
                        print('Algo deu errado')
                

        @self.pg.production('steps : steps step')
        @self.pg.production('steps : step')
        def steps(p):
            if len(p) == 1:
                return [p[0]]
            else:
                p[0].append(p[1])
                return p[0]

        @self.pg.production('step : NUM DOT formule PREMISE')
        def Premisse(p):
            formule = p[2]
            premisse = PremisseDef(p[0].value, formule)
            self.symbol_table.insert(premisse)
            return formule

        @self.pg.production('step : NUM DOT formule HYPOTESIS')
        @self.pg.production('step : NUM DOT formule HYPOTESIS OPEN_BRACKET')
        def Hypotesis(p):
            if len(p) > 4:
                self.symbol_table.add_scope()
            
            formule = p[2]
            hypotesis = HypotesisDef(p[0].value, formule)
            self.symbol_table.insert(hypotesis)
            return formule

        @self.pg.production('step : NUM DOT formule NEG_ELIM NUM COMMA NUM')
        @self.pg.production('step : NUM DOT formule NEG_ELIM NUM COMMA NUM CLOSE_BRACKET')
        def Negation_elim(p):
            formule = p[2]
            negationElimination = NegationEliminationDef(p[0].value, formule, p[4].value, p[6].value)
            self.symbol_table.insert(negationElimination)
            if len(p) == 8:
                self.symbol_table.end_scope()
            return formule

        @self.pg.production('formule : NOT formule')
        @self.pg.production('formule : ATHOM')
        @self.pg.production('formule : BOTTOM')
        @self.pg.production('formule : formule AND formule')
        @self.pg.production('formule : formule OR formule')
        @self.pg.production('formule : formule IMPLIE formule')
        def formule(p):
            if len(p) < 3:
                if p[0].gettokentype() == 'ATHOM':
                    return AthomFormule(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return AthomFormule(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    return NegationFormule(key=p[1])
            else:
                return BinaryFormule(key=p[1].value, left=p[0], right=p[2])

        @self.pg.production('formule : OPEN_PAREN formule CLOSE_PAREN')
        def paren_formule(p):
            return p[1]

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
        