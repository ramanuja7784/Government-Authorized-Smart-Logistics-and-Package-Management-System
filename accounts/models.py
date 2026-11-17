from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("COURIER", "Packager/Courier"),
        ("DELIVERY_BOY", "Delivery Boy"),
        ('govt_auth', 'Government Authorized'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CUSTOMER")

    def is_govt_auth(self):
        return self.role == 'govt_auth'

    def is_admin(self):
        return self.role == "ADMIN"

    def is_courier(self):
        return self.role == "COURIER"
    def is_delivery_boy(self):
        return self.role == "DELIVERY_BOY"

    # Role specific fields
    company_name = models.CharField(max_length=255, blank=True, null=True, help_text="For Couriers")
    full_address = models.TextField(blank=True, null=True, help_text="For Delivery Boys")
    aadhar_number = models.CharField(max_length=20, blank=True, null=True, help_text="For Delivery Boys")
    id_number = models.CharField(max_length=50, blank=True, null=True, help_text="For Govt Authorized")
    id_card_pdf = models.FileField(upload_to="id_cards/", blank=True, null=True, help_text="For Govt Authorized")
    vault_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Earnings vault for Delivery Boys")

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.user.username}: {self.message}"
