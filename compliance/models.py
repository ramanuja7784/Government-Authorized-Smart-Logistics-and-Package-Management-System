from django.db import models
from django.conf import settings
from shipments.models import Shipment

class GovernmentLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    document = models.FileField(upload_to="licenses/")

    def __str__(self):
        return self.license_number

class ComplianceCheck(models.Model):
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_checks"
    )
    has_valid_invoice = models.BooleanField(default=False)
    has_complete_address = models.BooleanField(default=False)
    contains_restricted_items = models.BooleanField(default=False)
    comments = models.TextField(blank=True)

    def is_compliant(self):
        return (
            self.has_valid_invoice
            and self.has_complete_address
            and not self.contains_restricted_items
        )
