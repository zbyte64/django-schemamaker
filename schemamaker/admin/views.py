from dockit.admin.views import SingleObjectFragmentView, CreateView, UpdateView, BaseFragmentViewMixin
from dockit.forms import DocumentForm
from dockit.schema.exceptions import DotPathNotFound
import dockit

from schemamaker.schema_specifications import default_schema_specification
from schemamaker.properties import GenericFieldEntryField

from fields import FieldEntryField

class FieldsMixin(object):
    def formfield_for_field(self, prop, field, **kwargs):
        if isinstance(prop, dockit.ListField) and isinstance(prop.schema, GenericFieldEntryField):
            field = FieldEntryField
            kwargs['dotpath'] = self.dotpath()
            if self.next_dotpath():
                kwargs['required'] = False
            return field(**kwargs)
        return BaseFragmentViewMixin.formfield_for_field(self, prop, field, **kwargs)

class CreateDocumentDesignView(FieldsMixin, CreateView):
    pass

class UpdateDocumentDesignView(FieldsMixin, UpdateView):
    pass

class FieldProxyFragmentView(FieldsMixin, SingleObjectFragmentView):
    def get_field_type_value(self):
        obj = self.get_temporary_store()
        if obj:
            try:
                frag = obj.dot_notation(self.dotpath())
            except DotPathNotFound:
                pass
            else:
                if frag.field_type:
                    return frag.field_type
        if 'field_type' in self.request.GET:
            return self.request.GET['field_type']
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        field_type = self.get_field_type_value()
        if field_type:
            field_spec = default_schema_specification.fields[field_type]
            kwargs = self.admin.get_view_kwargs()
            kwargs['field_type'] = field_type
            view = field_spec.get_admin_view(**kwargs)
            return view(request, *args, **kwargs)
        return super(FieldProxyFragmentView, self).dispatch(request, *args, **kwargs)

class FieldDesignerFragmentView(FieldsMixin, SingleObjectFragmentView):
    '''
    default admin handler for designing fields
    '''
    field_spec = None
    field_type = None
    
    def _generate_form_class(self, field_schema):
        view_cls = self
        
        class CustomDocumentForm(DocumentForm):
            class Meta:
                schema = field_schema
                document = self.document
                form_field_callback = self.formfield_for_field
                dotpath = self.dotpath() or None
                exclude = ['field_type']
            
            def _inner_save(self, *args, **kwargs):
                obj = super(CustomDocumentForm, self)._inner_save(*args, **kwargs)
                obj.field_type = view_cls.field_type
                return obj
        
        return CustomDocumentForm
    
    def get_form_class(self):
        return self._generate_form_class(self.field_spec.schema)

