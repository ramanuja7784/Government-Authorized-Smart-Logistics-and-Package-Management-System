from django import forms
from .models import Shipment

CONTENT_CHOICES = [
    ('', 'Select Content Type'),
    ('documents', 'Documents'),
    ('products', 'Products'),
    ('pickles', 'Pickles'),
    ('electronics', 'Electronics'),
    ('clothes', 'Clothes'),
    ('other', 'Other'),
]

class ShipmentForm(forms.ModelForm):
    contents_description = forms.ChoiceField(choices=CONTENT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Shipment
        exclude = [
            "tracking_number", "status", "created_at", "updated_at",
            "risk_score",       # 🔥 ADD THIS
            "risk_details",     # 🔥 ADD THIS
            "courier"           # 🔥 ADD THIS (auto-filled)
        ]
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sender Name'}),
            'sender_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sender Phone'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Sender Email'}),
            'sender_house_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House No / Flat'}),
            'sender_street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'sender_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'sender_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'sender_pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'sender_landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Landmark (Optional)'}),

            'receiver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Name'}),
            'receiver_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Phone'}),
            'receiver_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Email'}),
            'receiver_house_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House No / Flat'}),
            'receiver_street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'receiver_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'receiver_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'receiver_pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'receiver_landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Landmark (Optional)'}),

            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kg'}),
            'declared_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Declared Value in Rs'}),
            'package_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }