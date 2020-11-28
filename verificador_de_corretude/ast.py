from formule import NegationFormule

class negationDef():
    def __init__(self):
        pass

    def eval(self, formule, formule_line, variables):
        for used_formule in variables[formule_line]:
            if formule.toString() == NegationFormule(used_formule).toString():
                return True 

        return False