from formule import BinaryFormule, UnaryFormule

class negationDef():
    def __init__(self):
        pass

    def eval(self, formule, formule_line, variables):
        for used_formule in variables[formule_line]:
            if formule.toString() == UnaryFormule(used_formule).toString():
                return True 

        return False

class binaryDef():
    def __init__(self):
        pass

    def eval(self, formule, operator, formule1_line, formule2_line, variables):
        if formule.left.toString() in [item.toString() for item in variables[formule1_line]]:
            if formule.right.toString() in [item.toString() for item in variables[formule2_line]]:
                return 2
            return 1
        return 0
