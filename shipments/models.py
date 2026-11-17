from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("PENDING_APPROVAL", "Pending Approval"),
        ("APPROVED", "Approved"),
        ("IN_TRANSIT", "In Transit"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("REJECTED", "Rejected"),
    ]

    risk_score = models.CharField(
        max_length=10,
        default="LOW",
        choices=[
            ('LOW', 'Low Risk'),
            ('MEDIUM', 'Medium Risk'),
            ('HIGH', 'High Risk')
        ]
    )
    risk_details = models.TextField(blank=True)

    tracking_number = models.CharField(max_length=20, unique=True, editable=False)

    courier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courier_shipments",
    )

    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20, default='')
    sender_email = models.EmailField(blank=True, null=True)
    sender_house_no = models.CharField(max_length=100, default='')
    sender_street = models.CharField(max_length=255, default='')
    sender_city = models.CharField(max_length=100, default='')
    sender_state = models.CharField(max_length=100, default='')
    sender_pincode = models.CharField(max_length=20, default='')
    sender_landmark = models.CharField(max_length=255, blank=True, null=True)

    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20, default='')
    receiver_email = models.EmailField(blank=True, null=True)
    receiver_house_no = models.CharField(max_length=100, default='')
    receiver_street = models.CharField(max_length=255, default='')
    receiver_city = models.CharField(max_length=100, default='')
    receiver_state = models.CharField(max_length=100, default='')
    receiver_pincode = models.CharField(max_length=20, default='')
    receiver_landmark = models.CharField(max_length=255, blank=True, null=True)

    contents_description = models.TextField()
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2)
    declared_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    package_photo = models.ImageField(upload_to='package_photos/', null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING_APPROVAL"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tracking_number
class DeliveryAssignment(models.Model):
    delivery_boy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_deliveries"
    )

    shipment = models.OneToOneField(
        Shipment,
        on_delete=models.CASCADE,
        related_name="delivery_assignment"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.delivery_boy.username} → {self.shipment.tracking_number}"
