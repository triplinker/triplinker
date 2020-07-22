from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import views

from .forms import SignUpForm, LoginForm
from .models import TLAccount

class SignUpView(generic.FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


class LoginView(views.LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'registration/login.html'


class LogoutView(views.LogoutView):
    template_name = 'registration/logout.html'


class ProfileView(generic.ListView):
    model = TLAccount
    template_name = 'accounts/profile.html'
