from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'email', 'is_primary', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company__name')
    list_filter = ('company', 'is_primary')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove('owner')
        return fields

    def save_related(self, request, form, formsets, change):
        if form.instance.is_primary:
            Contact.objects.filter(company=form.instance.company, is_primary=True).exclude(id=form.instance.id).update(is_primary=False)
        super().save_related(request, form, formsets, change)

admin.site.register(Contact, ContactAdmin)
