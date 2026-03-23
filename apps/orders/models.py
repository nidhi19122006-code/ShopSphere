from django.conf import settings
from django.db import models


class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE)
	label = models.CharField(max_length=60, blank=True)
	full_name = models.CharField(max_length=150)
	phone_number = models.CharField(max_length=20)
	line1 = models.CharField(max_length=255)
	line2 = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120)
	postal_code = models.CharField(max_length=20)
	country = models.CharField(max_length=120, default="India")
	is_default = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-is_default", "-created_at"]

	def __str__(self):
		label = self.label or self.line1
		return f"{label} - {self.city}"


class Order(models.Model):
	STATUS_PENDING = "pending"
	STATUS_PAID = "paid"
	STATUS_SHIPPED = "shipped"
	STATUS_COMPLETED = "completed"
	STATUS_CANCELLED = "cancelled"

	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_PAID, "Paid"),
		(STATUS_SHIPPED, "Shipped"),
		(STATUS_COMPLETED, "Completed"),
		(STATUS_CANCELLED, "Cancelled"),
	]

	PAYMENT_PENDING = "pending"
	PAYMENT_SUCCESS = "success"
	PAYMENT_FAILED = "failed"

	PAYMENT_CHOICES = [
		(PAYMENT_PENDING, "Pending"),
		(PAYMENT_SUCCESS, "Success"),
		(PAYMENT_FAILED, "Failed"),
	]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE)
	address = models.ForeignKey(Address, related_name="orders", on_delete=models.PROTECT)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)
	payment_reference = models.CharField(max_length=120, blank=True)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Order #{self.id}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
	product = models.ForeignKey("products.Product", related_name="order_items", on_delete=models.PROTECT)
	seller = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name="sold_items",
		on_delete=models.PROTECT,
		null=True,
		blank=True,
	)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.product.name} ({self.quantity})"

	def get_total_price(self):
		return self.price * self.quantity
