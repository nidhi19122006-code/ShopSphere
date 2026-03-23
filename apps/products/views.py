from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Category, Product


class ProductListView(ListView):
	model = Product
	template_name = "products/list.html"
	context_object_name = "products"
	paginate_by = 12

	def get_queryset(self):
		queryset = Product.objects.filter(is_active=True).select_related("category")
		category_slug = self.kwargs.get("category_slug")
		if category_slug:
			queryset = queryset.filter(category__slug=category_slug)

		query = self.request.GET.get("q")
		if query:
			queryset = queryset.filter(
				Q(name__icontains=query)
				| Q(description__icontains=query)
				| Q(sku__icontains=query)
			)

		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = Category.objects.filter(is_active=True)
		context["selected_category"] = self.kwargs.get("category_slug")
		context["search_query"] = self.request.GET.get("q", "")
		return context


class ProductDetailView(DetailView):
	model = Product
	template_name = "products/detail.html"
	context_object_name = "product"

	def get_queryset(self):
		return Product.objects.filter(is_active=True).select_related("category")
