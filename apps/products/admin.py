from django.contrib import admin

from shopsphere.admin import admin_site

from .models import Category, Product


@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "slug", "is_active")
	list_filter = ("is_active",)
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}


@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "sku", "seller", "category", "price", "stock", "is_active")
	list_filter = ("is_active", "category", "seller")
	search_fields = ("name", "sku", "seller__email")
	prepopulated_fields = {"slug": ("name",)}
