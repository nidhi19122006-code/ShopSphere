from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.sellers.models import SellerProfile

from .models import User


class CustomUserCreationForm(UserCreationForm):
    register_as_seller = forms.BooleanField(
        required=False,
        label="Register as Seller",
        help_text="Create a seller account to manage products and orders.",
    )
    shop_name = forms.CharField(required=False)
    shop_description = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    contact_email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "phone_number")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("register_as_seller"):
            if not cleaned_data.get("shop_name"):
                self.add_error("shop_name", "Shop name is required for sellers.")
            if not cleaned_data.get("contact_email"):
                self.add_error("contact_email", "Contact email is required for sellers.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("register_as_seller"):
            user.is_seller = True
            user.is_customer = False
        if commit:
            user.save()
            if self.cleaned_data.get("register_as_seller"):
                SellerProfile.objects.create(
                    user=user,
                    shop_name=self.cleaned_data.get("shop_name"),
                    shop_description=self.cleaned_data.get("shop_description", ""),
                    contact_email=self.cleaned_data.get("contact_email"),
                )
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "phone_number", "is_active", "is_staff")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number")
