import dockit
from dockit.schema.schema import create_schema

from django.utils.datastructures import SortedDict

#from properties import GenericFieldEntryField

class FieldEntry(dockit.Schema):
    '''
    This schema is extended by others to define a field entry
    '''
    name = dockit.SlugField()
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.field_type)
    
    def create_field(self):
        raise NotImplementedError
    
    def get_scaffold_example(self, context, varname):
        raise NotImplementedError
    
    class Meta:
        typed_field = 'field_type'

class DesignMixin(object):
    def get_fields(self):
        fields = SortedDict()
        for field_entry in self.fields:
            assert field_entry.name
            field = field_entry.create_field()
            fields[field_entry.name] = field
        return fields
    
    def get_schema(self):
        fields = self.get_fields()
        schema = create_schema('temp_schema', fields, module='schemamaker.models')
        
        def __unicode__(instance):
            if not self.object_label:
                return repr(instance)
            try:
                return self.object_label % instance
            except (KeyError, TypeError):
                return repr(instance)
        
        schema.__unicode__ = __unicode__
        return schema

class SchemaEntry(FieldEntry, DesignMixin):
    fields = dockit.ListField(dockit.SchemaField(FieldEntry))
    object_label = dockit.CharField(blank=True)

class DocumentDesign(dockit.Document, DesignMixin):
    #inherit_from = schema.ReferenceField('DocumentDesign')
    title = dockit.CharField()
    fields = dockit.ListField(dockit.SchemaField(FieldEntry))
    object_label = dockit.CharField(blank=True)
    
    def __unicode__(self):
        return self.title or ''

