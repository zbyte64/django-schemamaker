import dockit
from dockit.schema.schema import create_schema

from django.utils.datastructures import SortedDict

from properties import GenericFieldEntryField

class FieldEntry(dockit.Schema):
    '''
    This schema is extended by others to define a field entry
    '''
    name = dockit.SlugField()
    field_type = dockit.CharField()#editable=False)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.field_type)
    
    def get_field_spec(self, spec):
        return spec.fields[self.field_type]
    
    def get_field(self, spec):
        field_spec = self.get_field_spec(spec)
        return field_spec.create_field(self)

class DesignMixin(object):
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

class SchemaEntry(FieldEntry, DesignMixin):
    fields = dockit.ListField(GenericFieldEntryField())

class DocumentDesign(dockit.Document, DesignMixin):
    #inherit_from = schema.ReferenceField('DocumentDesign')
    fields = dockit.ListField(GenericFieldEntryField())

