from django.utils.encoding import force_unicode
from django.utils.html import escape

from dockit.admin.fields import DotPathField, DotPathWidget

from schemamaker.schema_specifications import default_schema_specification
from schemamaker.properties import GenericFieldEntryField

from urllib import urlencode

class FieldEntryWidget(DotPathWidget):
    input_type = 'submit'
    
    def __init__(self, dotpath=None):
        self.dotpath = dotpath
        super(DotPathWidget, self).__init__()
    
    def render_type_dropdown(self, dotpath):
        options = list()
        for key, field_class in default_schema_specification.fields.iteritems():
            options.append(u'<option>%s</option>' % key)
        data = {'next_dotpath':dotpath,
                'name':'field_type',}
        name = '[fragment-passthrough]%s' % urlencode(data)
        return u'<select name="%s">%s</select>' % (name, '\n'.join(options))
    
    def get_label(self, dotpath, value=None):
        if value:
            return escape(force_unicode(value))
        return self.render_type_dropdown(dotpath)

class FieldEntryField(DotPathField):
    widget = FieldEntryWidget
    
    def to_python(self, value):
        value = super(FieldEntryField, self).to_python(value)
        ret = list()
        for val in value:
            ret.append(GenericFieldEntryField().to_python(val))
        return ret
