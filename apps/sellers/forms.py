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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        text_like_fields = ("name", "sku", "price", "stock")
        for field_name in text_like_fields:
            self.fields[field_name].widget.attrs.setdefault("class", "form-control")

        self.fields["category"].widget.attrs.setdefault("class", "form-select")
        self.fields["description"].widget.attrs.setdefault("class", "form-control")
        self.fields["description"].widget.attrs.setdefault("rows", 6)
        self.fields["image"].widget.attrs.setdefault("class", "form-control")
        self.fields["is_active"].widget.attrs.setdefault("class", "form-check-input")

        # Improve clarity of empty fields and default input expectations.
        self.fields["name"].widget.attrs.setdefault("placeholder", "Premium Cotton Hoodie")
        self.fields["sku"].widget.attrs.setdefault("placeholder", "SKU-001")
        self.fields["price"].widget.attrs.setdefault("placeholder", "0.00")
        self.fields["stock"].widget.attrs.setdefault("placeholder", "0")

        if self.is_bound:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    existing_classes = field.widget.attrs.get("class", "")
                    field.widget.attrs["class"] = f"{existing_classes} is-invalid".strip()
