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
            if ((type(self.left) is NegationFormule) and (self.left.check_is_athom())) | ((type(self.left) is BinaryFormule) and (self.left.left is None)):
                string += self.left.toString()
            else:
                string += '({})'.format(self.left.toString())
        string += self.key
        if self.right is not None :
            if ((type(self.right) is NegationFormule) and (self.right.check_is_athom())) | ((type(self.right) is BinaryFormule) and (self.right.left is None)):
                string += self.right.toString()
            else:
                string += '({})'.format(self.right.toString())
        return string

class NegationFormule():
    def __init__(self, key = None):
        self.key = key

    def toString(self):
        if isinstance(self.key, AthomFormule):
            string = '~' + self.key.toString()
        else:
            string = '~({})'.format(self.key.toString())
        return string    

class AthomFormule():
    def __init__(self, key = None):
        self.key = key

    def toString(self):
        return self.key    
