class negationDef():
    def __init__(self):
        pass

    def eval(self, formule, formule_line, variables):
        for used_formule in variables[formule_line]:
            if formule.toString() == '~'+used_formule.toString():
                return True 

        return False

class binaryDef():
    def __init__(self):
        pass

    def eval(self, formule, operator, formule1_line, formule2_line, variables):
        for formule_1 in variables[formule1_line]:
            if not isinstance(formule_1, str):
                formule_1 = formule_1.toString()
            for formule_2 in variables[formule2_line]:
                if not isinstance(formule_2, str):
                    formule_2 = formule_2.toString()
                if formule.toString() == '{}{}{}'.format(formule_1, operator, formule_2):
                    return True
             
        return False
