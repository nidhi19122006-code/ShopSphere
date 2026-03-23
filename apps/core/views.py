from django.views.generic import TemplateView

from apps.products.models import Product


class HomeView(TemplateView):
	template_name = "core/home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["latest_products"] = Product.objects.filter(is_active=True)[:8]
		return context
