from django import forms
from django.contrib.contenttypes.models import ContentType

from schema_specifications import default_schema_specification as registry
from utils import prep_for_kwargs
from models import SchemaEntry, FieldEntry

import dockit

class BaseFieldSchema(FieldEntry):
    verbose_name = dockit.CharField(blank=True, null=True)
    blank = dockit.BooleanField(default=True)
    null = dockit.BooleanField(default=True)
    
    default = dockit.CharField(blank=True, null=True)
    help_text = dockit.CharField(blank=True, null=True)


class BaseField(object):
    field = None
    schema = BaseFieldSchema
    
    def create_field(self, data):
        kwargs = prep_for_kwargs(data)
        kwargs.pop('field_type', None)
        kwargs.pop('name', None)
        if kwargs.get('verbose_name', None) == '':
            del kwargs['verbose_name']
        return self.field(**kwargs)
    
    def get_admin_view(self, **kwargs):
        from admin import FieldDesignerFragmentView
        kwargs['field_spec'] = self
        return FieldDesignerFragmentView.as_view(**kwargs)

class BooleanField(BaseField):
    field = dockit.BooleanField

registry.register_field('BooleanField', BooleanField)

class CharFieldSchema(BaseFieldSchema):
    pass
    #max_length = dockit.IntegerField(blank=True, null=True)
    #min_length = dockit.IntegerField(blank=True, null=True)

class CharField(BaseField):
    schema = CharFieldSchema
    field = dockit.CharField

registry.register_field('CharField', CharField)

class ChoiceOptionSchema(dockit.Schema):
    label = dockit.CharField()
    value = dockit.CharField()
    
    def __unicode__(self):
        return self.label

class ChoiceFieldSchema(BaseFieldSchema):
    choices = dockit.ListField(dockit.SchemaField(ChoiceOptionSchema))

class ChoiceField(BaseField):
    schema = ChoiceFieldSchema
    field = dockit.CharField
    
    def create_field(self, data):
        kwargs = prep_for_kwargs(data)
        kwargs['choices'] = [(entry['value'], entry['label']) for entry in kwargs['choices']]
        return self.field(**kwargs)

registry.register_field('ChoiceField', ChoiceField)

class MultipleChoiceField(BaseField):
    schema = ChoiceFieldSchema
    field = lambda **kwargs: dockit.ListField(dockit.CharField(**kwargs))

    def create_field(self, data):
        kwargs = prep_for_kwargs(data)
        kwargs['choices'] = [(entry['value'], entry['label']) for entry in kwargs['choices']]
        return self.field(**kwargs)

registry.register_field('MultipleChoiceField', MultipleChoiceField)

class DateField(BaseField):
    field = dockit.DateField

registry.register_field('DateField', DateField)

class DateTimeField(BaseField):
    field = dockit.DateTimeField

registry.register_field('DateTimeField', DateTimeField)

class DecimalFieldSchema(BaseFieldSchema):
    max_value = dockit.IntegerField(blank=True, null=True)
    min_value = dockit.IntegerField(blank=True, null=True)
    max_digits = dockit.IntegerField(blank=True, null=True)
    decimal_places = dockit.IntegerField(blank=True, null=True)

class DecimalField(BaseField):
    schema = DecimalFieldSchema
    field = forms.DecimalField

registry.register_field('DecimalField', DecimalField)

class EmailField(CharField):
    field = dockit.EmailField

registry.register_field('EmailField', EmailField)

class FileField(BaseField):
    field = dockit.FileField

registry.register_field('FileField', FileField)

class FloatFieldSchema(BaseFieldSchema):
    max_value = dockit.IntegerField(blank=True, null=True)
    min_value = dockit.IntegerField(blank=True, null=True)

class FloatField(BaseField):
    schema = FloatFieldSchema
    field = dockit.FloatField

registry.register_field('FloatField', FloatField)
'''
class ImageField(BaseField):
    field = dockit.ImageField

registry.register_field('ImageField', ImageField)
'''
class IntegerFieldSchema(BaseFieldSchema):
    max_value = dockit.IntegerField(blank=True, null=True)
    min_value = dockit.IntegerField(blank=True, null=True)

class IntegerField(BaseField):
    schema = IntegerFieldSchema
    field = dockit.IntegerField

registry.register_field('IntegerField', IntegerField)

class IPAddressField(BaseField):
    field = dockit.IPAddressField

registry.register_field('IPAddressField', IPAddressField)
'''
class NullBooleanField(BaseField):
    field = dockit.NullBooleanField

registry.register_field('NullBooleanField', NullBooleanField)
'''
'''
class RegexFieldSchema(CharFieldSchema):
    regex = dockit.CharField()

class RegexField(BaseField):
    schema = RegexFieldSchema
    field = dockit.RegexField

registry.register_field('RegexField', RegexField)
'''
class SlugField(BaseField):
    field = dockit.SlugField

registry.register_field('SlugField', SlugField)

class TimeField(BaseField):
    field = dockit.TimeField

registry.register_field('TimeField', TimeField)
'''
class URLFieldSchema(BaseFieldSchema):
    max_length = dockit.IntegerField(blank=True, null=True)
    min_length = dockit.IntegerField(blank=True, null=True)
    verify_exists = dockit.BooleanField(initial=False)
    validator_user_agent = dockit.CharField(blank=True)

class URLField(BaseField):
    form = URLFieldSchema
    field = dockit.URLField

registry.register_field('URLField', URLField)
'''
class ModelReferenceFieldSchema(BaseFieldSchema):
    model = dockit.ModelReferenceField(ContentType)

class ModelReferenceField(BaseField):
    schema = ModelReferenceFieldSchema
    field = dockit.ModelReferenceField
    
    def create_field(self, data):
        kwargs = prep_for_kwargs(data)
        ct_id = kwargs.pop('model')
        if not isinstance(ct_id, (long, int)):
            model = ct_id
        else:
            model = ContentType.objects.get(pk=ct_id).model_class()
        kwargs['queryset'] = model.objects.all()
        return self.field(**kwargs)

registry.register_field('ModelReferenceField', ModelReferenceField)

class SchemaField(BaseField):
    schema = SchemaEntry
    field = dockit.SchemaField
    
    def create_field(self, data):
        schema = data.get_schema()
        kwargs = {'schema':schema}
        return self.field(**kwargs)

registry.register_field('SchemaField', SchemaField)

class ComplexListField(BaseField):
    schema = SchemaEntry
    field = dockit.ListField
    
    def create_field(self, data):
        schema = data.get_schema()
        kwargs = {'schema':dockit.SchemaField(schema)}
        return self.field(**kwargs)

registry.register_field('ComplexListField', ComplexListField)

