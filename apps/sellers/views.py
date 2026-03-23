from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from apps.orders.models import Order, OrderItem
from apps.products.models import Product

from .forms import SellerProductForm
from .mixins import SellerRequiredMixin


class SellerDashboardView(SellerRequiredMixin, TemplateView):
	template_name = "sellers/dashboard.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		seller = self.request.user
		context["product_count"] = Product.objects.filter(seller=seller).count()
		context["order_count"] = (
			OrderItem.objects.filter(Q(seller=seller) | Q(product__seller=seller))
			.values("order_id")
			.distinct()
			.count()
		)
		context["top_products"] = (
			Product.objects.filter(seller=seller)
			.annotate(order_item_count=Count("order_items"))
			.order_by("-order_item_count")[:5]
		)
		return context


class SellerProductListView(SellerRequiredMixin, ListView):
	model = Product
	template_name = "sellers/product_list.html"
	context_object_name = "products"

	def get_queryset(self):
		return Product.objects.filter(seller=self.request.user).select_related("category")


class SellerProductCreateView(SellerRequiredMixin, CreateView):
	form_class = SellerProductForm
	template_name = "sellers/add_product.html"
	success_url = reverse_lazy("sellers:products")

	def form_valid(self, form):
		product = form.save(commit=False)
		product.seller = self.request.user
		product.save()
		return super().form_valid(form)


class SellerProductUpdateView(SellerRequiredMixin, UpdateView):
	form_class = SellerProductForm
	template_name = "sellers/add_product.html"
	success_url = reverse_lazy("sellers:products")

	def get_queryset(self):
		return Product.objects.filter(seller=self.request.user)


class SellerProductDeleteView(SellerRequiredMixin, DeleteView):
	template_name = "sellers/product_confirm_delete.html"
	success_url = reverse_lazy("sellers:products")

	def get_queryset(self):
		return Product.objects.filter(seller=self.request.user)


class SellerOrdersView(SellerRequiredMixin, ListView):
	template_name = "sellers/orders.html"
	context_object_name = "order_items"

	def get_queryset(self):
		return (
			OrderItem.objects.filter(Q(seller=self.request.user) | Q(product__seller=self.request.user))
			.select_related("order", "product")
			.order_by("-order__created_at")
		)


class SellerOrderApproveView(SellerRequiredMixin, View):
	def post(self, request, order_id):
		order = get_object_or_404(
			Order.objects.filter(
				Q(items__seller=request.user) | Q(items__product__seller=request.user)
			).distinct(),
			id=order_id,
		)

		if order.status == Order.STATUS_PENDING:
			order.status = Order.STATUS_SHIPPED
			order.save(update_fields=["status", "updated_at"])

		return redirect("sellers:orders")
