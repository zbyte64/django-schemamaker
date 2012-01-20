import dockit
from dockit.schema.schema import create_schema

from django.utils.datastructures import SortedDict

class FieldEntry(dockit.Schema):
    name = dockit.SlugField()
    field_type = dockit.CharField()
    field_spec = dockit.DictField()
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.field_type)
    
    def get_field_spec(self, spec):
        return spec.fields[self.field_type]
    
    def get_field(self, spec):
        field_spec = self.get_field_spec(spec)
        return field_spec.create_field(self.field_spec)

class SchemaEntry(dockit.Schema):
    fields = dockit.ListField(dockit.SchemaField(FieldEntry))
    
    def get_specification(self):
        from schema_specifications import default_schema_specification
        return default_schema_specification
    
    def get_fields(self):
        fields = SortedDict()
        spec = self.get_specification()
        for field_entry in self.fields:
            field = field_entry.get_field(spec)
            fields[field_entry.name] = field
        return fields
    
    def get_schema(self):
        fields = self.get_fields()
        schema = create_schema('temp_schema', fields, module='schemamaker.models')
        return schema

class DocumentDesign(dockit.Document):
    #inherit_from = schema.ReferenceField('DocumentDesign')
    fields = dockit.ListField(dockit.SchemaField(FieldEntry))
    
    def get_specification(self):
        from schema_specifications import default_schema_specification
        return default_schema_specification
    
    def get_fields(self):
        fields = SortedDict()
        spec = self.get_specification()
        for field_entry in self.fields:
            field = field_entry.get_field(spec)
            fields[field_entry.name] = field
        return fields
    
    def get_schema(self):
        fields = self.get_fields()
        schema = create_schema('temp_schema', fields, module='schemamaker.models')
        return schema

