from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'employees_count', 'annual_revenue', 'website', 'created_at')
    list_filter = ('industry', 'created_at')
    search_fields = ('name', 'industry', 'website', 'address')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('name', 'industry', 'employees_count', 'annual_revenue', 'website', 'address')
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
