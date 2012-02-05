from django.contrib import admin

from dockit.admin.documentadmin import DocumentAdmin

from schemamaker.models import DocumentDesign

class DocumentDesignAdmin(DocumentAdmin):
    pass

admin.site.register([DocumentDesign], DocumentDesignAdmin)

