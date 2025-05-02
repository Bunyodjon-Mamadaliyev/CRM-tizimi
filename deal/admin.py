from django.contrib import admin
from .models import Deal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'company', 'amount', 'currency', 'stage',
        'expected_closing_date', 'closed_date', 'assigned_to', 'is_closed'
    )
    list_filter = ('stage', 'currency', 'expected_closing_date', 'company')
    search_fields = ('title', 'description', 'company__name', 'assigned_to__username')
    readonly_fields = ('created_at', 'updated_at', 'is_closed')
    ordering = ('-expected_closing_date',)

    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'company', 'amount', 'currency',
                'stage', 'expected_closing_date', 'closed_date', 'assigned_to'
            )
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('is_closed', 'created_at', 'updated_at'),
        }),
    )
