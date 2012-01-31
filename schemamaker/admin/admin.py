from django.contrib import admin

from dockit.admin.documentadmin import DocumentAdmin

from schemamaker.models import DocumentDesign

#from views import FieldProxyFragmentView

class DocumentDesignAdmin(DocumentAdmin):
    pass
    #default_fragment = FieldProxyFragmentView
    #TODO adding fields must signal the type somehow

admin.site.register([DocumentDesign], DocumentDesignAdmin)

