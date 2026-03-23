from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "label",
            "full_name",
            "phone_number",
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        ]
