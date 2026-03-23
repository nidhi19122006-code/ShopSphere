from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from shopsphere.admin import admin_site

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User, site=admin_site)
class UserAdmin(DjangoUserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = User
	ordering = ("email",)
	list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
	list_filter = ("is_staff", "is_active")
	search_fields = ("email", "first_name", "last_name")

	fieldsets = (
		(None, {"fields": ("email", "password")}),
		("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
		("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
		("Important dates", {"fields": ("last_login", "date_joined")}),
	)

	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("email", "first_name", "last_name", "phone_number", "password1", "password2", "is_staff", "is_active"),
			},
		),
	)
