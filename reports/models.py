from django.db import models
from django.conf import settings
from shipments.models import Shipment

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("CREATED", "Created"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("STATUS_UPDATE", "Status Updated"),
        ("DELETED", "Deleted"), 
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs"
    )

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="audit_logs"
    )

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.action}"
