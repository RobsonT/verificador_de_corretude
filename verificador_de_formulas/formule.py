class BinaryFormule():
    def __init__(self, key = '', left = None, right = None):
        self.key = key
        self.left = left
        self.right = right

    def toString(self):
        string = ''
        if self.left is not None :
            string += self.left.toString()
        string += self.key
        if self.right is not None :
            string += self.right.toString()
        return string

class UnaryFormule():
    def __init__(self, key = None):
        self.key = key

    def toString(self):
        if isinstance(self.key, str):
            string = '~' + self.key
        else:
            string = '~' + self.key.toString()
        return string    