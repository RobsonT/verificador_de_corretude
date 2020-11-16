from lexer import Lexer
from analisys import Parser
import sys

text_input = ""

for param in sys.argv[1:] :
    text_input += param

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

pg = Parser(state=text_input)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens)