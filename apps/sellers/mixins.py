from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow access only to seller accounts."""

    def test_func(self):
        return getattr(self.request.user, "is_seller", False)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, "Seller access required. Contact support to enable your seller account.")
        return redirect(reverse_lazy("accounts:profile"))
