from dockit.admin.views import SingleObjectFragmentView
from dockit.forms import DocumentForm

from schemamaker.schema_specifications import default_schema_specification

class FieldProxyFragmentView(SingleObjectFragmentView):
    def get_field_type_value(self):
        if not hasattr(self, 'object'):
            if 'pk' in self.kwargs:
                self.object = self.get_object()
            else:
                self.object = None
        if self.object:
            try:
                frag = self.object.dot_path(self.dotpath())
            except:
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
            view = field_spec.get_admin_view(**kwargs)
            return view(request, *args, **kwargs)
        return super(FieldProxyFragmentView, self).dispatch(request, *args, **kwargs)

class FieldDesignerFragmentView(SingleObjectFragmentView):
    '''
    default admin handler for designing fields
    '''
    field_spec = None
    
    def _generate_form_class(self, schema):
        class CustomDocumentForm(DocumentForm):
            class Meta:
                schema = schema
                document = self.document
                form_field_callback = self.formfield_for_field
                dotpath = self.dotpath() or None
        return CustomDocumentForm
    
    def get_form_class(self):
        return self._generate_form_class(self.field_spec.schema)

