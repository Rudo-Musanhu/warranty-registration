from rest_framework import serializers
from .models import WarrantyRegistration

class WarrantySerializer(serializers.ModelSerializer):
    registered_by_username = serializers.CharField(source='registered_by.username', read_only=True)

    class Meta:
        model = WarrantyRegistration
        fields = ['id', 'asset_id', 'asset_name', 'serial_number', 'purchase_date', 'registered_by', 'registered_by_username', 'registration_date']
        read_only_fields = ['id', 'registered_by', 'registered_by_username', 'registration_date']
