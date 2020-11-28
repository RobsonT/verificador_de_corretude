from lexer import Lexer
from analisys import Parser

f = open('Prova', 'r')

text_input = f.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

pg = Parser(state=text_input)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens)