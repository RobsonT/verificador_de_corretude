from lexer import Lexer
from analisys import Parser

text_input = """1. Ab def A
2. ~Ab def ~ 1
3. Ab & ~Ab def & 1-2
4. Ab <-> (Ab & ~Ab) def <-> 1-3
5. ~Ab <-> (Ab & ~Ab) def ~ 4
6. b, c def A
7. ((b)) | ((c)) def | 6-6
8. (b | c) -> (~(Ab <-> (Ab & ~Ab))) def -> 7-5
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

pg = Parser(state=text_input)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens)