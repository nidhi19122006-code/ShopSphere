from django import forms

from apps.products.models import Product


class SellerProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category",
            "name",
            "description",
            "sku",
            "price",
            "stock",
            "image",
            "is_active",
        )
