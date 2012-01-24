from dockit.admin.views import SingleObjectFragmentView
from dockit.forms import DocumentForm
from dockit.schema.exceptions import DotPathNotFound

from schemamaker.schema_specifications import default_schema_specification

class FieldProxyFragmentView(SingleObjectFragmentView):
    def get_field_type_value(self):
        obj = self.get_temporary_store()
        if obj:
            try:
                frag = obj.dot_notation(self.dotpath())
            except DotPathNotFound:
                pass
            else:
                if frag and frag.field_type:
                    return frag.field_type
        if 'field_type' in self.request.GET:
            return self.request.GET['field_type']
    
    #TODO
    #if schema==TypedSchemaForm and not field_type is found, then render a simple get drop down form of the options?
    
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

class FieldDesignerFragmentView(SingleObjectFragmentView):
    '''
    default admin handler for designing fields
    '''
    field_spec = None
    field_type = None
    
    def get_schema(self):
        return self.field_spec.schema
    
    def _generate_form_class(self):
        view_cls = self
        
        class CustomDocumentForm(DocumentForm):
            class Meta:
                document = self.document
                schema = self.get_schema()
                form_field_callback = self.formfield_for_field
                dotpath = self.dotpath() or None
                exclude = ['field_type']
            
            def _inner_save(self, *args, **kwargs):
                obj = super(CustomDocumentForm, self)._inner_save(*args, **kwargs)
                obj.field_type = view_cls.field_type
                return obj
        return CustomDocumentForm

