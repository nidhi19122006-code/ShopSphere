from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.products.models import Product

from .cart import Cart
from .forms import CartAddForm


@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id, is_active=True)
	form = CartAddForm(request.POST)
	if form.is_valid():
		cart.add(
			product=product,
			quantity=form.cleaned_data["quantity"],
			override_quantity=form.cleaned_data["override"],
		)
	return redirect("cart:detail")


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id, is_active=True)
	cart.remove(product)
	return redirect("cart:detail")


def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item["update_form"] = CartAddForm(initial={"quantity": item["quantity"], "override": True})
	return render(request, "cart/detail.html", {"cart": cart})
