from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView

from apps.cart.cart import Cart

from .forms import AddressForm
from .models import Address, Order, OrderItem


class CheckoutView(LoginRequiredMixin, FormView):
	template_name = "orders/checkout.html"
	form_class = AddressForm
	success_url = reverse_lazy("orders:success")

	def dispatch(self, request, *args, **kwargs):
		cart = Cart(request)
		if len(cart) == 0:
			return redirect("products:list")
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		cart = Cart(self.request)
		user = self.request.user

		with transaction.atomic():
			address = form.save(commit=False)
			address.user = user
			if address.is_default:
				Address.objects.filter(user=user, is_default=True).update(is_default=False)
			address.save()

			order = Order.objects.create(
				user=user,
				address=address,
				total_amount=cart.get_total_price(),
			)

			for item in cart:
				OrderItem.objects.create(
					order=order,
					product=item["product"],
					seller=item["product"].seller,
					price=item["price"],
					quantity=item["quantity"],
				)

			cart.clear()
			self.request.session["latest_order_id"] = order.id

		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["cart"] = Cart(self.request)
		return context


class CheckoutSuccessView(LoginRequiredMixin, TemplateView):
	template_name = "orders/success.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		order_id = self.request.session.get("latest_order_id")
		if order_id:
			context["order"] = Order.objects.filter(id=order_id, user=self.request.user).first()
		return context


class OrderHistoryView(LoginRequiredMixin, ListView):
	model = Order
	template_name = "orders/history.html"
	context_object_name = "orders"
	paginate_by = 10

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user).prefetch_related("items", "items__product")


class OrderDetailView(LoginRequiredMixin, DetailView):
	model = Order
	template_name = "orders/detail.html"
	context_object_name = "order"

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user).prefetch_related("items", "items__product")


class AddressListView(LoginRequiredMixin, ListView):
	model = Address
	template_name = "orders/addresses.html"
	context_object_name = "addresses"

	def get_queryset(self):
		return Address.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
	model = Address
	form_class = AddressForm
	template_name = "orders/address_form.html"
	success_url = reverse_lazy("orders:addresses")

	def form_valid(self, form):
		address = form.save(commit=False)
		address.user = self.request.user
		if address.is_default:
			Address.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
		address.save()
		return redirect(self.success_url)
