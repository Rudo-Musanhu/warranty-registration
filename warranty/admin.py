from django.contrib import admin
from .models import WarrantyRegistration

@admin.register(WarrantyRegistration)
class WarrantyRegistrationAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'registration_date', 'registered_by')
    list_filter = ('registration_date',)
    search_fields = ('asset_id',)