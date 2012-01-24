from dockit.schema.fields import TypedSchemaField

from schemamaker.schema_specifications import default_schema_specification

class GenericFieldEntryField(TypedSchemaField):
    def __init__(self, schemas=default_schema_specification.fields, field_name='field_type', **kwargs):
        super(GenericFieldEntryField, self).__init__(schemas, field_name, **kwargs)
    
    def lookup_schema(self, key):
        return self.schemas[key].schema
    
    def get_schema_choices(self):
        keys = self.schemas.keys()
        return zip(keys, keys)
    
    def set_schema_type(self, val):
        return #this is done by the admin
    
    def is_instance(self, val):
        if val is None:
            return True
        from models import FieldEntry
        return isinstance(val, FieldEntry)
