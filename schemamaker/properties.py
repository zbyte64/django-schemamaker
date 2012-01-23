from dockit.schema.fields import GenericSchemaField

from schemamaker.schema_specifications import default_schema_specification

class GenericFieldEntryField(GenericSchemaField):
    def to_primitive(self, val):
        if hasattr(val, 'to_primitive'):
            return val.to_primitive(val)
        return super(GenericFieldEntryField, self).to_primitive(val)
    
    def to_python(self, val, parent=None):
        if self.is_instance(val):
            return val
        field_type = val['field_type']
        field_spec = default_schema_specification.fields[field_type]
        return field_spec.schema.to_python(val, parent=parent)
    
    def is_instance(self, val):
        from models import FieldEntry
        return isinstance(val, FieldEntry)
