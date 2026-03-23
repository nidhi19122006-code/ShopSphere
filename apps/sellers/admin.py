from django.contrib import admin

from .models import SellerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
	list_display = ("shop_name", "contact_email", "user", "created_at")
	search_fields = ("shop_name", "contact_email", "user__email")
