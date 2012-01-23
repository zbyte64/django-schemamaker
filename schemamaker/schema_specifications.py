from resource import FieldRegistry

class SchemaSpecification(object):
    def __init__(self):
        self.field_registry = FieldRegistry()
    
    def register_field(self, name, field):
        self.field_registry.register_field(name, field)
    
    @property
    def fields(self):
        return self.field_registry.fields

default_schema_specification = SchemaSpecification()

