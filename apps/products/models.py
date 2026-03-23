from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
	name = models.CharField(max_length=150, unique=True)
	slug = models.SlugField(max_length=160, unique=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)


class Product(models.Model):
	# Seller is nullable for existing products; will be enforced later via data cleanup.
	seller = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name="products",
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True)
	description = models.TextField(blank=True)
	sku = models.CharField(max_length=60, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField(default=0)
	image = models.ImageField(upload_to="products/", blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]
		indexes = [
			models.Index(fields=["slug"]),
			models.Index(fields=["sku"]),
			models.Index(fields=["is_active"]),
		]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("products:detail", kwargs={"slug": self.slug})
