from django.urls import path

from .views import (
    SellerDashboardView,
    SellerOrdersView,
    SellerProductCreateView,
    SellerProductDeleteView,
    SellerProductListView,
    SellerProductUpdateView,
)

app_name = "sellers"

urlpatterns = [
    path("dashboard/", SellerDashboardView.as_view(), name="dashboard"),
    path("products/", SellerProductListView.as_view(), name="products"),
    path("products/add/", SellerProductCreateView.as_view(), name="product_add"),
    path("products/<int:pk>/edit/", SellerProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", SellerProductDeleteView.as_view(), name="product_delete"),
    path("orders/", SellerOrdersView.as_view(), name="orders"),
]
