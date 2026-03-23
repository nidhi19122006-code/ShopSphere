from django.conf import settings
from django.db import models


class SellerProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="seller_profile", on_delete=models.CASCADE)
	shop_name = models.CharField(max_length=150)
	shop_description = models.TextField(blank=True)
	contact_email = models.EmailField()
	profile_image = models.ImageField(upload_to="sellers/", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return self.shop_name
