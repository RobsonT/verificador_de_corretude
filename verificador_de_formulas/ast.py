from formule import BinaryFormule, UnaryFormule

class negationDef():
    def __init__(self):
        pass

    def eval(self, formule, formule_line, variables):
        print(formule.toString())
        for used_formule in variables[formule_line]:
            if formule.toString() == UnaryFormule(used_formule).toString():
                return True 

        return False

class binaryDef():
    def __init__(self):
        pass

    def eval(self, formule, operator, formule1_line, formule2_line, variables):
        print(formule.toString())
        for formule_1 in variables[formule1_line]:
            for formule_2 in variables[formule2_line]:
                formule_test = BinaryFormule(key=operator, left=formule_1, right=formule_2).toString()
                if formule.toString() == formule_test:
                    return True
             
        return False
