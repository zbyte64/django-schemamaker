import dockit
from dockit.schema.schema import create_schema

from django.utils.datastructures import SortedDict

from properties import SchemaDesignChoiceField

class FieldEntry(dockit.Schema):
    '''
    This schema is extended by others to define a field entry
    '''
    name = dockit.SlugField()
    
    field_class = None
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.field_type)
    
    def get_field_kwargs(self):
        kwargs = self.to_primitive(self)
        kwargs.pop('field_type', None)
        kwargs.pop('name', None)
        if kwargs.get('verbose_name', None) == '':
            del kwargs['verbose_name']
        for key in kwargs.keys():
            if key not in self._meta.fields:
                kwargs.pop(key)
        return kwargs
    
    def create_field(self):
        kwargs = self.get_field_kwargs()
        return self.field_class(**kwargs)
    
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
        if self.inherit_from:
            parent = self._meta.fields['inherit_from'].get_schema(self.inherit_from)
            if parent:
                parents = (parent, )
                schema = create_schema('temp_schema', fields, module='schemamaker.models', parents=parents)
            else:
                schema = create_schema('temp_schema', fields, module='schemamaker.models')
        else:
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
    inherit_from = SchemaDesignChoiceField(blank=True)
    fields = dockit.ListField(dockit.SchemaField(FieldEntry))
    object_label = dockit.CharField(blank=True)
    
    class Meta:
        proxy = True

class DocumentDesign(dockit.Document, DesignMixin):
    title = dockit.CharField()
    inherit_from = SchemaDesignChoiceField(blank=True)
    fields = dockit.ListField(dockit.SchemaField(FieldEntry))
    object_label = dockit.CharField(blank=True)
    
    def __unicode__(self):
        return self.title or ''

