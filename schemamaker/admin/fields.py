from django.forms.util import flatatt
from django.utils.safestring import mark_safe

from dockit.admin.fields import DotPathField, DotPathWidget

from schemamaker.schema_specifications import default_schema_specification

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
    
    def render_button(self, dotpath, edit=False):
        if edit:
            label = 'edit'
        else:
            label = 'add'
        data = {'next_dotpath':dotpath}
        name = '[fragment]%s' % urlencode(data)
        submit_attrs = self.build_attrs({}, type=self.input_type, name=name, value=label)
        if edit:
            drop_down = ''
        else:
            drop_down = self.render_type_dropdown(dotpath)
        
        return mark_safe(u'%s<input%s />' % (drop_down, flatatt(submit_attrs)))

class FieldEntryField(DotPathField):
    widget = FieldEntryWidget

