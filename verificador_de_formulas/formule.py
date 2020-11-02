class BinaryFormule():
    def __init__(self, key = '', left = None, right = None):
        self.key = key
        self.left = left
        self.right = right

    def check_is_athom(self):
        if (self.left is None) and (self.right is None):
            return True
        return False

    def toString(self):
        string = ''
        if self.left is not None :
            if ((type(self.left) is UnaryFormule) and (self.left.check_is_athom())) | ((type(self.left) is BinaryFormule) and (self.left.left is None)):
                string += self.left.toString()
            else:
                string += '({})'.format(self.left.toString())
        string += self.key
        if self.right is not None :
            if ((type(self.right) is UnaryFormule) and (self.right.check_is_athom())) | ((type(self.right) is BinaryFormule) and (self.right.left is None)):
                string += self.right.toString()
            else:
                string += '({})'.format(self.right.toString())
        return string

    def change_symbols(self, formule_latex):
        operators = {
            '<->': '\\iff ',
            '->': '\\rightarrow ',
            '&': '\\wedge ',
            '~': '\\lnot ',
            '|': '\\vee ',
        }

        for key, value in operators.items():
            formule_latex = formule_latex.replace(key, value)

        return formule_latex

    def toLatex(self):
        operators = {
            '<->': '\\iff ',
            '->': '\\rightarrow ',
            '&': '\\wedge ',
            '~': '\\lnot ',
            '|': '\\vee ',
        }
        if (self.left is not None) & (self.right is not None):
            string = '\\infer[\\!\\!{\\text{Def}{'+ operators[self.key] +'}}]'
            string += '{'+ self.change_symbols(self.toString()) +'}'
            string += '{'
            string += self.left.toLatex() + '&' + self.right.toLatex()
            string += '}'
        else:
            string = self.key

        return string

class UnaryFormule():
    def __init__(self, key = None):
        self.key = key

    def check_is_athom(self):
        operators = ['->', '~', '&', '|', '<->']
        formule = self.toString()[1:]
        for operator in operators:
            if operator in formule:
                return False
        return True

    def toString(self):
        if self.key.check_is_athom():
            string = '~' + self.key.toString()
        else:
            string = '~({})'.format(self.key.toString())
        return string    

    def toLatex(self):
        formule = self.toString()
        string = '\\infer[\\!\\!{\\text{Def}{\\lnot}}]\n'
        string += '{'+ formule +'}'
        if(formule[1] == '('):
            string += '{'+ formule[2:-1] +'}'
        else:
            string += '{'+ formule[1:] +'}'
        return string.replace('~', '\\lnot ')