from django.contrib.contenttypes.models import ContentType

from models import SchemaEntry, FieldEntry

import dockit

class BaseFieldEntry(FieldEntry):
    verbose_name = dockit.CharField(blank=True, null=True)
    blank = dockit.BooleanField(default=True)
    null = dockit.BooleanField(default=True)
    
    default = dockit.CharField(blank=True, null=True)
    help_text = dockit.CharField(blank=True, null=True)
    
    scaffold_template_name = 'schemamaker/scaffold/field.html'
    
    class Meta:
        proxy = True


class ListFieldMixin(object):
    list_field_class = dockit.ListField
    
    def get_list_field_kwargs(self):
        raise NotImplementedError
    
    def create_field(self):
        kwargs = self.get_list_field_kwargs()
        return self.list_field_class(**kwargs)

class BooleanField(BaseFieldEntry):
    field_class = dockit.BooleanField
    
    class Meta:
        typed_key = 'BooleanField'

class CharField(BaseFieldEntry):
    field_class = dockit.CharField
    
    class Meta:
        typed_key = 'CharField'

class ListCharField(ListFieldMixin, CharField):
    def get_list_field_kwargs(self):
        subfield = super(ListCharField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListCharField'

class TextField(BaseFieldEntry):
    field_class = dockit.TextField
    
    class Meta:
        typed_key = 'TextField'

class ListTextField(ListFieldMixin, TextField):
    def get_list_field_kwargs(self):
        subfield = super(ListTextField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListTextField'

class ChoiceOptionSchema(dockit.Schema):
    label = dockit.CharField()
    value = dockit.CharField()
    
    def __unicode__(self):
        return self.label

class ChoiceField(BaseFieldEntry):
    choices = dockit.ListField(dockit.SchemaField(ChoiceOptionSchema))
    field_class = dockit.CharField
    
    def get_field_kwargs(self):
        kwargs = super(ChoiceField, self).get_field_kwargs()
        kwargs['choices'] = [(entry['value'], entry['label']) for entry in kwargs['choices']]
        return kwargs
    
    class Meta:
        typed_key = 'ChoiceField'

class ListChoiceField(ListFieldMixin, ChoiceField):
    def get_list_field_kwargs(self):
        subfield = super(ListChoiceField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListChoiceField'

class MultipleChoiceField(ChoiceField):
    def create_field(self):
        kwargs = self.get_field_kwargs()
        return dockit.ListField(self.field_class(**kwargs))
    
    class Meta:
        typed_key = 'MultipleChoiceField'

class DateField(BaseFieldEntry):
    field_class = dockit.DateField
    
    class Meta:
        typed_key = 'DateField'

class ListDateField(ListFieldMixin, DateField):
    def get_list_field_kwargs(self):
        subfield = super(ListDateField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListDateField'

class DateTimeField(BaseFieldEntry):
    field_class = dockit.DateTimeField
    
    class Meta:
        typed_key = 'DateTimeField'

class ListDateTimeField(ListFieldMixin, DateTimeField):
    def get_list_field_kwargs(self):
        subfield = super(ListDateTimeField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListDateTimeField'

class DecimalField(BaseFieldEntry):
    max_value = dockit.IntegerField(blank=True, null=True)
    min_value = dockit.IntegerField(blank=True, null=True)
    max_digits = dockit.IntegerField(blank=True, null=True)
    decimal_places = dockit.IntegerField(blank=True, null=True)
    
    field_class = dockit.DecimalField

    class Meta:
        typed_key = 'DecimalField'

class ListDecimalField(ListFieldMixin, DecimalField):
    def get_list_field_kwargs(self):
        subfield = super(ListDecimalField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListDecimalField'

class EmailField(BaseFieldEntry):
    field_class = dockit.EmailField
    
    class Meta:
        typed_key = 'EmailField'

class ListEmailField(ListFieldMixin, EmailField):
    def get_list_field_kwargs(self):
        subfield = super(ListEmailField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListEmailField'

class FileField(BaseFieldEntry):
    field_class = dockit.FileField
    
    class Meta:
        typed_key = 'FileField'

class ListFileField(ListFieldMixin, FileField):
    def get_list_field_kwargs(self):
        subfield = super(ListFileField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListFileField'

class ImageField(BaseFieldEntry):
    #TODO dockit.ImageField
    field_class = dockit.FileField
    scaffold_template_name = 'schemamaker/scaffold/image.html'

    class Meta:
        typed_key = 'ImageField'

class ListImageField(ListFieldMixin, ImageField):
    def get_list_field_kwargs(self):
        subfield = super(ListImageField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListImageField'

class FloatField(BaseFieldEntry):
    field_class = dockit.FloatField
    #max_value = dockit.IntegerField(blank=True, null=True)
    #min_value = dockit.IntegerField(blank=True, null=True)
    
    class Meta:
        typed_key = 'FloatField'

class ListFloatField(ListFieldMixin, FloatField):
    def get_list_field_kwargs(self):
        subfield = super(ListFloatField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListFloatField'

class IntegerField(BaseFieldEntry):
    field_class = dockit.IntegerField
    #max_value = dockit.IntegerField(blank=True, null=True)
    #min_value = dockit.IntegerField(blank=True, null=True)

    field_class = dockit.IntegerField
    
    class Meta:
        typed_key = 'IntegerField'

class ListIntegerField(ListFieldMixin, IntegerField):
    def get_list_field_kwargs(self):
        subfield = super(ListIntegerField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListIntegerField'


class IPAddressField(BaseFieldEntry):
    field_class = dockit.IPAddressField

    class Meta:
        typed_key = 'IPAddressField'

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
class SlugField(BaseFieldEntry):
    field_class = dockit.SlugField

    class Meta:
        typed_key = 'SlugField'

class ListSlugField(ListFieldMixin, SlugField):
    def get_list_field_kwargs(self):
        subfield = super(ListSlugField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListSlugField'

class TimeField(BaseFieldEntry):
    field_class = dockit.TimeField

    class Meta:
        typed_key = 'TimeField'

class ListTimeField(ListFieldMixin, TimeField):
    def get_list_field_kwargs(self):
        subfield = super(ListTimeField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListTimeField'

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
class ModelReferenceField(BaseFieldEntry):
    model = dockit.ModelReferenceField(ContentType)

    field_class = dockit.ModelReferenceField
    
    def get_field_kwargs(self):
        kwargs = super(ModelReferenceField, self).get_field_kwargs()
        ct_id = kwargs.pop('model')
        if not isinstance(ct_id, (long, int)):
            model = ct_id
        else:
            model = ContentType.objects.get(pk=ct_id).model_class()
        kwargs['queryset'] = model.objects.all()
        return kwargs

    class Meta:
        typed_key = 'ModelReferenceField'

class ListModelReferenceField(ListFieldMixin, ModelReferenceField):
    def get_list_field_kwargs(self):
        subfield = super(ListModelReferenceField, self).create_field()
        return {'subfield': subfield}

    class Meta:
        typed_key = 'ListModelReferenceField'

class SchemaField(SchemaEntry):
    field_class = dockit.SchemaField
    scaffold_template_name = 'schemamaker/scaffold/schema.html'
    
    def get_field_kwargs(self):
        schema = self.get_schema()
        kwargs = {'schema':schema}
        return kwargs
    
    def get_scaffold_example(self, data, context, varname):
        fields = list()
        #TODO populate fields
        context['fields'] = fields
        return super(SchemaField, self).get_scaffold_example(data, context, varname)

    class Meta:
        typed_key = 'SchemaField'

class ComplexListField(SchemaEntry):
    field_class = dockit.ListField
    saffold_template_name = 'schemamaker/scaffold/list.html'
    
    def get_field_kwargs(self):
        schema = self.get_schema()
        kwargs = {'subfield':dockit.SchemaField(schema)}
        return kwargs
    
    def get_scaffold_example(self, data, context, varname):
        schema = data.get_schema()
        #TODO
        context['subschema'] = ''
        context['subvarname'] = 'subitem'
        return super(ComplexListField, self).get_scaffold_example(data, context, varname)

    class Meta:
        typed_key = 'ComplexListField'
'''
class ListField(FieldEntry):
    subfield = dockit.SchemaField(FieldEntry)
    field_class = dockit.ListField
    
    def get_field_kwargs(self):
        subfield = self.subfield.create_field()
        kwargs = {'subfield':subfield}
        return kwargs

    class Meta:
        typed_key = 'ListField'
'''
