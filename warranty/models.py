# warranty/models.py
from django.db import models
from django.contrib.auth.models import User

class WarrantyRegistration(models.Model):
    asset_id = models.CharField(max_length=255, unique=True)
    asset_name = models.CharField(max_length=255, default='Unknown Asset')
    serial_number = models.CharField(max_length=255, default='N/A')
    purchase_date = models.DateField(null=True, blank=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Warranty for Asset: {self.asset_name} ({self.asset_id})"
