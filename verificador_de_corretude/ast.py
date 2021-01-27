from formule import NegationFormule

class NegationEliminationDef():
    def __init__(self,line, formule, reference1, reference2):
        self.line = line
        self.formule = formule
        self.reference1 = reference1
        self.reference2 = reference2

    def eval(self, formule1, formule2):
        if(formule1 == None):
            return 0
        if (formule2 == None):
            return 1
        if(formule2.toString() != NegationFormule(formule1).toString()):
            return 2
        if(self.formule.toString() != '@'):
            return 3

        return 4

class HypotesisDef():
    def __init__(self,line, formule):
        self.line = line
        self.formule = formule

    def eval(self):
        return

class PremisseDef():
    def __init__(self,line, formule):
        self.line = line
        self.formule = formule

    def eval(self):
        return