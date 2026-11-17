from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=[choice for choice in User.ROLE_CHOICES if choice[0] != 'ADMIN'])

    class Meta:
        model = User
        fields = [
            "username", "email", "role", "password1", "password2",
            "company_name", "full_address", "aadhar_number", "id_number", "id_card_pdf"
        ]


# ✅ NEW FORM (THIS FIXES YOUR ERROR)
class DeliveryBoyCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "DELIVERY_BOY"
        user.is_active = True
        if commit:
            user.save()
        return user
