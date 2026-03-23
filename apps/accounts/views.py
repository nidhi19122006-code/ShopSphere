from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import User


class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy("accounts:login")
	template_name = "accounts/signup.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
	model = User
	form_class = ProfileUpdateForm
	template_name = "accounts/profile.html"
	success_url = reverse_lazy("accounts:profile")

	def get_object(self, queryset=None):
		# Always edit the logged-in user's profile.
		return self.request.user
