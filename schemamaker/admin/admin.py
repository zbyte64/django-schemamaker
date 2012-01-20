from django.contrib import admin

from dockit.admin.documentadmin import DocumentAdmin

from schemamaker.models import DocumentDesign

from views import FieldProxyFragmentView, CreateDocumentDesignView, UpdateDocumentDesignView

class DocumentDesignAdmin(DocumentAdmin):
    create = CreateDocumentDesignView
    update = UpdateDocumentDesignView
    default_fragment = FieldProxyFragmentView
    #TODO adding fields must signal the type somehow

admin.site.register([DocumentDesign], DocumentDesignAdmin)

