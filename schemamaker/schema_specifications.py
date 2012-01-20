from django.utils.datastructures import SortedDict

from resource import FieldRegistry

class SchemaSpecification(object):
    def __init__(self):
        self.field_registry = FieldRegistry()
    
    example = [
                   {'name':'email',
                    'field':'EmailField',
                    'field_spec':{'max_length':'128'},
                    'widget':'TextInput',
                    'widget_spec':{},}
              ]
    
    def create_schema(self, data):
        pass
    
    def get_fields(self, data):
        field_dict = SortedDict()
        for field_def in data:
            #fetch the makers
            try:
                field_maker = self.field_registry.fields[field_def['field']]
            except KeyError:
                print self, self.field_registry.fields
                raise
            widget_maker = self.field_registry.widgets[field_def['widget']]
            
            widget = widget_maker.create_widget(field_def['widget_spec'])
            field_kwargs = field_def['field_spec']
            field = field_maker.create_field(field_kwargs, widget=widget)
            
            field_dict[field_def['name']] = field
        return field_dict
    
    def register_field(self, name, field):
        self.field_registry.register_field(name, field)
    
    @property
    def fields(self):
        return self.field_registry.fields

default_schema_specification = SchemaSpecification()

