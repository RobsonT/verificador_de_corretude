class SymbolTable:
    def __init__(self):
        self.symbol_table = {
            'scope_0': {
                'name': 'scope_0',
                'parent': None,
                'rules': [],
            }
        }
        self.current_scope = 'scope_0'

    def insert(self, symbol):
        self.symbol_table[self.current_scope]['rules'].append(symbol)

    def start_scope(self, scope):
        self.current_scope = scope

    def end_scope(self):
        if(self.current_scope['parent'] is not None):
            self.current_scope = self.current_scope['parent']

    def add_scope(self):
        scope = 'scope_{}'.format(len(self.symbol_table))
        self.symbol_table[scope] = {
            'name': scope,
            'parent': self.current_scope,
            'rules': [],
        }
        self.start_scope(scope)

    def find_scope(self, symbol):
        scope = self.current_scope
        while scope != None:
            for rule in self.symbol_table[scope]['rules']:
                if rule.formule == symbol:
                    return scope    
            scope = self.symbol_table[scope]['parent']
        return scope

    def lookup_formule_by_line(self, symbol, line):
        scope = self.find_scope(symbol)
        while scope != None:
            for rule in self.symbol_table[scope]['rules']:
                if rule.line == line:
                    return rule.formule
            scope = self.symbol_table[scope]['parent']
        return None

    def get_rule(self, symbol):
        scope = self.current_scope
        while scope != None:
            for rule in self.symbol_table[scope]['rules']:
                if rule.formule.toString() == symbol:
                    return rule
            scope = self.symbol_table[scope]['parent']
        return None