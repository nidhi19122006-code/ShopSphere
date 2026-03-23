from django.urls import path

from .views import (
    AddressCreateView,
    AddressListView,
    CheckoutSuccessView,
    CheckoutView,
    OrderDetailView,
    OrderHistoryView,
)

app_name = "orders"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("success/", CheckoutSuccessView.as_view(), name="success"),
    path("history/", OrderHistoryView.as_view(), name="history"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("addresses/", AddressListView.as_view(), name="addresses"),
    path("addresses/add/", AddressCreateView.as_view(), name="address_add"),
]
