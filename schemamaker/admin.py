from django.contrib import admin

from dockit.admin.documentadmin import DocumentAdmin, SchemaAdmin

from schemamaker.models import DocumentDesign

#TODO consider a better name
class AdminAwareSchemaAdmin(SchemaAdmin):
    def get_form_class(self, request, obj=None):
        if hasattr(self.schema, 'get_admin_form_class'):
            form_class = self.schema.get_admin_form_class()
            if form_class:
                return form_class
        return super(AdminAwareDocumentAdmin, self).get_form_class(request, obj)

class AdminAwareDocumentAdmin(DocumentAdmin):
    default_schema_admin = AdminAwareSchemaAdmin
    
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

