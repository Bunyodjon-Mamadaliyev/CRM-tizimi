from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('subject', 'activity_type', 'company', 'contact', 'deal', 'due_date', 'status', 'assigned_to', 'is_overdue')
    list_filter = ('activity_type', 'status', 'due_date', 'company')
    search_fields = ('subject', 'description', 'company__name', 'contact__name', 'deal__title')
    autocomplete_fields = ('company', 'contact', 'deal', 'assigned_to')
    date_hierarchy = 'due_date'
    ordering = ('-due_date',)
    readonly_fields = ('created_at', 'updated_at', 'is_overdue')
    fieldsets = (
        (None, {
            'fields': (
                'subject', 'description', 'activity_type', 'status', 'due_date'
            )
        }),
        (_('Aloqadorlar'), {
            'fields': (
                'company', 'contact', 'deal', 'assigned_to'
            )
        }),
        (_('Vaqt ma\'lumotlari'), {
            'fields': ('created_at', 'updated_at', 'is_overdue')
        }),
    )
