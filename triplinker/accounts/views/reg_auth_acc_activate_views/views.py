from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth import views, authenticate, login
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from accounts.forms.forms import SignUpForm, LoginForm, AccountActivationForm


class SignUpView(generic.FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:activate')
    template_name = 'registration/signup.html'
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user \
                and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                 "Redirection loop for authenticated user detected. Check that "
                 "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        new_user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'],
                                )
        login(self.request, new_user)
        return super().form_valid(form)


class ActivateView(views.FormView):
    form_class = AccountActivationForm
    success_url = reverse_lazy('accounts:index')
    template_name = 'registration/activate.html'
    user = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print('try')
        if hasattr(self, 'user'):
            print(self.request.user)
            kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class LoginView(views.LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class LogoutView(views.LogoutView):
    template_name = 'registration/logout.html'
