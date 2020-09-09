from lexer import Lexer

text_input = """
a -> b
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

for token in tokens:
    print(token)