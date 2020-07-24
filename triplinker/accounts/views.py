from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import render, get_object_or_404


from .forms import SignUpForm, LoginForm, ProfileEditForm
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


class ProfileView(generic.FormView):
    model = TLAccount
    form_class = ProfileEditForm
    template_name = 'accounts/profile.html'
    user = None
    success_url = 'accounts/profile/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'user'):
            kwargs.update({'instance': self.request.user})
        return kwargs


    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)





# class MyFormView(View):
#     form_class = MyForm
#     initial = {'key': 'value'}
#     template_name = 'form_template.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')

#         return render(request, self.template_name, {'form': form})


# Friends system
class AllUsersList(generic.ListView):
    template_name = 'accounts/all_users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return TLAccount.objects.exclude(id=self.request.user.id)


def detail_profile(request, user_id):
    who_makes_a_request = request.user.email 
    user_acc = get_object_or_404(TLAccount, id=user_id)
    context = {
        'who_makes_a_request': who_makes_a_request,
        'user_acc': user_acc
    }
    return render(request, 'accounts/user_profile.html', context)
    