from django.contrib import admin

from dockit.admin.documentadmin import DocumentAdmin

from schemamaker.models import DocumentDesign

#TODO consider a better name
class AdminAwareDocumentAdmin(DocumentAdmin):
    def get_admin_class_for_schema(self, schema):
        for cls, admin_class in self.schema_inlines:
            if schema == cls:
                return admin_class
        if hasattr(schema, 'get_admin_class'):
            return schema.get_admin_class()
        return self.default_schema_admin

class DocumentDesignAdmin(AdminAwareDocumentAdmin):
    pass
    

admin.site.register([DocumentDesign], DocumentDesignAdmin)

