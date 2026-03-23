from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Sum


class ShopSphereAdminSite(admin.AdminSite):
    site_header = "ShopSphere Admin"
    site_title = "ShopSphere Admin"
    index_title = "Dashboard"
    index_template = "admin/custom_index.html"

    def each_context(self, request):
        context = super().each_context(request)
        context["site_brand"] = "ShopSphere"
        return context

    def get_dashboard_stats(self):
        User = get_user_model()
        from apps.orders.models import Order
        from apps.products.models import Product

        total_sales = Order.objects.filter(payment_status=Order.PAYMENT_SUCCESS).aggregate(
            total=Sum("total_amount")
        )["total"]
        return {
            "total_users": User.objects.count(),
            "total_products": Product.objects.count(),
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status=Order.STATUS_PENDING).count(),
            "total_sales": total_sales or 0,
        }

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["dashboard_stats"] = self.get_dashboard_stats()
        return super().index(request, extra_context=extra_context)


admin_site = ShopSphereAdminSite(name="shopsphere_admin")
