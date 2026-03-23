from django.contrib import admin

from shopsphere.admin import admin_site

from .models import Address, Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "status", "payment_status", "total_amount", "created_at")
	list_filter = ("status", "payment_status", "created_at")
	search_fields = ("id", "user__email")
	inlines = [OrderItemInline]


@admin.register(Address, site=admin_site)
class AddressAdmin(admin.ModelAdmin):
	list_display = ("user", "label", "city", "is_default")
	list_filter = ("is_default", "city")
	search_fields = ("user__email", "label", "city", "line1")
