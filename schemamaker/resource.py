class FieldRegistry(object): #TODO make inheritable
    def __init__(self):
        self.fields = dict()
    
    def register_field(self, name, field):
        assert name not in self.fields
        if isinstance(field, type):
            field = field()
        self.fields[name] = field

