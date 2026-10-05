from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm


class RegisterView(CreateView):

      form_class = RegisterForm
      template_name = "accounts/register.html"
      success_url = reverse_lazy("accounts:login")

      def form_valid(self, form):
            response = super().form_valid(form)

            login(self.request, self.object)

            return response


class UserLoginView(LoginView):
      authentication_form = LoginForm
      template_name = "accounts/login.html"

      def get_success_url(self):
            return reverse_lazy("dashboard:candidate")


class UserLogoutView(LogoutView):
      next_page = reverse_lazy("pages:home")