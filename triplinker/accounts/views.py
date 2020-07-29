from django.urls import reverse_lazy
from django.contrib.auth import views, authenticate, login
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import render, get_object_or_404

from .forms import SignUpForm, LoginForm, ProfileEditForm, CreateUser
from .models import TLAccount, FriendRequest

from .helpers.views.status_between_users_definer import define_status


class IndexView(generic.ListView):
    template_name = 'accounts/index.html'
    def get_queryset(self):
        return TLAccount.objects.all()


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
    form_class = CreateUser
    success_url = reverse_lazy('accounts:index')
    template_name = 'registration/activate.html'
    redirect_authenticated_user = True

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


class ProfileView(generic.ListView):
    model = TLAccount
    template_name = 'accounts/user_profile.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        user_acc = self.request.user

        try:
            amount_of_friends = user_acc.friends.all().count()
            amount_of_frequests = FriendRequest.objects.filter(
                to_user=user_acc).count()


        except AttributeError:
            amount_of_friends = 0
            amount_of_frequests = 0


        return {
            'user_acc': user_acc,
            'who_makes_a_request': user_acc.email,
            'amount_of_friends': amount_of_friends,
            'amount_of_frequests': amount_of_frequests,
        }


class ProfileEditView(generic.FormView):
    model = TLAccount
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    user = None
    success_url = '/profile/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'user'):
            kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


# Friends system
class AllUsersList(generic.ListView):
    template_name = 'accounts/all_users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return TLAccount.objects.exclude(id=self.request.user.id)


def all_incoming_friquests_list(request, user_id):
    user = FriendRequest.objects.filter(to_user=user_id)
    context = {'incom_friquests': user}
    return render(request, 'accounts/incoming_frequests_list.html', context)


def all_outgoing_friquests_list(request, user_id):
    user = FriendRequest.objects.filter(from_user=user_id)
    context = {'outcom_friquests': user}
    return render(request, 'accounts/outgoing_frequest_list.html', context)


def detail_profile(request, user_id):
    user_acc = get_object_or_404(TLAccount, id=user_id)

    try:
        amount_of_friends = user_acc.friends.all().count()
        amount_of_frequests = FriendRequest.objects.filter(
            to_user=user_id).count()

        current_user = request.user
        another_user = user_acc

    except AttributeError:
        amount_of_friends = 0
        amount_of_frequests = 0

    status_between_users = define_status(FriendRequest, current_user,
                                         another_user)

    context = {
        'user_acc': user_acc,
        'who_makes_a_request': request.user.email,
        'amount_of_friends': amount_of_friends,
        'amount_of_frequests': amount_of_frequests,
        'status_between_users': status_between_users
    }

    return render(request, 'accounts/user_profile.html', context)


def friends_list(request, user_id):
    user_acc = get_object_or_404(TLAccount, id=user_id)

    try:
        user_friends = user_acc.friends.all()
    except AttributeError:
        user_friends = 0

    context = {
        "user_acc": user_acc,
        'who_makes_a_request': request.user.email,
        "user_friends": user_friends
    }

    return render(request, 'accounts/friends_list.html', context)


def delete_user_from_friends(request, user_id):
    user_who_deletes = get_object_or_404(TLAccount, id=request.user.id)
    friends_to_delete = get_object_or_404(TLAccount, id=user_id)
    user_who_deletes.friends.remove(friends_to_delete)
    friends_to_delete.friends.remove(user_who_deletes)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def send_request(request, user_id):
    request_from_user = request.user
    request_to_user = TLAccount.objects.get(id=user_id)

    friend_request = FriendRequest.objects.create(
        from_user=request_from_user,
        to_user=request_to_user
    )
    friend_request  # for flake8, never used

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def accept_friend_request(request, user_id):
    from_user = get_object_or_404(TLAccount, id=user_id)
    to_user = get_object_or_404(TLAccount, id=request.user.id)

    friend_request = FriendRequest.objects.filter(from_user=from_user,
                                                  to_user=to_user)

    user1 = from_user
    user2 = to_user
    user1.friends.add(user2)
    user2.friends.add(user1)
    friend_request.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_friend_request(request, user_id):
    from_user = get_object_or_404(TLAccount, id=user_id)
    to_user = get_object_or_404(TLAccount, id=request.user.id)

    friend_request = FriendRequest.objects.filter(
        from_user=from_user,
        to_user=to_user)
    friend_request.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cancel_friend_request(request, user_id):
    from_user = get_object_or_404(TLAccount, id=request.user.id)
    to_user = get_object_or_404(TLAccount, id=user_id)

    friend_request = FriendRequest.objects.filter(
        from_user=from_user,
        to_user=to_user
    )
    friend_request.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
