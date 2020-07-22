from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .forms import SignUpForm, LoginForm
from .models import TLAccount

class SignUpView(generic.FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

class LoginView(views.LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class LogoutView(views.LogoutView):
    template_name = 'registration/logout.html'


class ProfileView(generic.ListView):
    model = TLAccount
    template_name = 'accounts/profile.html'
