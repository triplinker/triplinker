from datetime import timedelta

from django.urls import reverse

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth import views, authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q

from django.views import generic

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import render, get_object_or_404

from .forms.forms import (SignUpForm, LoginForm, ProfileEditForm,
                          AccountActivationForm)
from .forms.forms_feed import AddPostForm, AddCommentForm

from .models.TLAccount_frequest import TLAccount, FriendRequest
from .models.feed import Post, Comment


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


class ProfileView(generic.ListView):
    """Class provides the person with his own page on triplinker.
    It saves posts and comments which was wrote on the page of user's own
    profile if HTTP method is POST and rendering the final child of the chain of
    HTML documents for profile if HTTP method is GET.
    """

    context = None
    model = TLAccount
    template_name = 'accounts/profile/profile_final_child_5.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        user_acc = self.request.user

        try:
            amount_of_friends = user_acc.friends.all().count()
            amount_of_frequests = FriendRequest.objects.filter(
                to_user=user_acc).count()

        except AttributeError:
            amount_of_friends = 0
            amount_of_frequests = 0

        posts = Post.objects.filter(author=user_acc)

        self.context = {
            'user_acc': user_acc,
            'who_makes_a_request': user_acc.email,
            'amount_of_friends': amount_of_friends,
            'amount_of_frequests': amount_of_frequests,
            'posts': posts,
        }
        form = AddPostForm()
        comment_form = AddCommentForm()
        self.context['form'] = form
        self.context['comment_form'] = comment_form
        return self.context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        post_id = request.POST.get("post_id", )
        if post_id:
            # User adds a comment.
            content_for_comment_form = {
                'body': request.POST.get("body", ),  # Text of comment.
                'user': request.user,
                'post': post_id
            }
            comment_form = AddCommentForm(content_for_comment_form)
            if comment_form.is_valid():
                comment_form.save()
                return HttpResponseRedirect(
                       reverse('accounts:profile',) + '#post-' +
                       str(post_id) + "-content")
            else:
                # Form is not valid.
                context['comment_form'] = comment_form
                return render(request, self.template_name, context)

        else:
            # User adds a post.
            content_for_form = {
                'content': request.POST.get("content", ),
                'author': request.user,
            }

            form = AddPostForm(content_for_form)
            if form.is_valid():
                form.save()
                user_acc_id = request.user
                postProfileLST = Post.objects.filter(author=user_acc_id).first()
                return HttpResponseRedirect(
                       reverse('accounts:profile', ) + '#post-' +
                       str(postProfileLST.id) + "-content")
            else:
                # Form is not valid.
                context['form'] = form
                return render(request, self.template_name, context)


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
    """Renders the list of users of site without the user who makes this
    request."""

    template_name = 'accounts/all_users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        """Forms query set that will be used in the context of django template.
        """
        query = self.request.GET.get('q')
        if query is None:
            query = ''
        users_list = TLAccount.objects.filter(
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=self.request.user.id)
        return users_list

def all_incoming_friquests_list(request, user_id):
    """Shows the list of all incoming friend requests for user who makes this
    request."""
    user = FriendRequest.objects.filter(to_user=user_id)
    context = {'incom_friquests': user}
    return render(request, 'accounts/incoming_frequests_list.html', context)


def all_outgoing_friquests_list(request, user_id):
    user = FriendRequest.objects.filter(from_user=user_id)
    context = {'outcom_friquests': user}
    return render(request, 'accounts/outgoing_frequest_list.html', context)


def detail_profile(request, user_id):
    """Function makes the same work as ProfileView class but with other profiles
    on site(it doesn't work with current user's profile)."""

    user_acc = get_object_or_404(TLAccount, id=user_id)
    context = None
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

    posts = Post.objects.filter(author=user_acc)

    context = detail_profile.context = {
        'user_acc': user_acc,
        'who_makes_a_request': request.user.email,
        'amount_of_friends': amount_of_friends,
        'amount_of_frequests': amount_of_frequests,
        'status_between_users': status_between_users,
        'posts': posts,
    }

    template_name = 'accounts/profile/profile_final_child_5.html'

    if request.method == 'POST':
        post_id = request.POST.get("post_id", )
        if post_id:
            # User adds a comment.
            content_for_comment_form = {
                'body': request.POST.get("body", ),
                'user': request.user,
                'post': post_id
            }
            comment_form = AddCommentForm(content_for_comment_form)
            if comment_form.is_valid():
                comment_form.save()
                html_anchor = '#post-' + str(post_id) + "-content"
                return HttpResponseRedirect(
                       reverse('accounts:detail_profile',
                               kwargs={'user_id': user_acc.id}) + html_anchor)
            else:
                context['comment_form'] = comment_form
                return render(request, template_name, context)
        else:
            # User adds a post.
            form = AddPostForm(initial={'content': request.POST,
                                        'author': request.user})
            if form.is_valid():
                form.save()
                user_acc = request.user
                postProfileLST = Post.objects.filter(user=user_acc).first()
                html_anchor = '#post-' + str(postProfileLST.id) + "-content"
                return HttpResponseRedirect(
                       reverse('accounts:detail_profile',
                               kwargs={'user_id': user_acc.id}) + html_anchor)
            else:
                context['form'] = form
                comment_form = AddCommentForm()

                context['comment_form'] = comment_form

    else:
        # HTTP method is GET.
        form = AddPostForm()
        comment_form = AddCommentForm()
        context['form'] = form
        context['comment_form'] = comment_form
    return render(request, template_name, context)


def friends_list(request, user_id):
    """Shows the list of user's friends."""
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
    """Deletes user from friend list (the user who will be deleted from friends
    is already in friend list)."""
    user_who_deletes = get_object_or_404(TLAccount, id=request.user.id)
    friends_to_delete = get_object_or_404(TLAccount, id=user_id)
    user_who_deletes.friends.remove(friends_to_delete)
    friends_to_delete.friends.remove(user_who_deletes)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def send_request(request, user_id):
    """Sends friend request to user."""
    request_from_user = request.user
    request_to_user = TLAccount.objects.get(id=user_id)

    friend_request = FriendRequest.objects.create(
        from_user=request_from_user,
        to_user=request_to_user
    )
    friend_request  # for flake8, never used.

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def accept_friend_request(request, user_id):
    """Gives the possibility to accept friend request from other users."""
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
    """The person who get friend request can delete it from incoming friend
    requests."""
    from_user = get_object_or_404(TLAccount, id=user_id)
    to_user = get_object_or_404(TLAccount, id=request.user.id)

    friend_request = FriendRequest.objects.filter(
        from_user=from_user,
        to_user=to_user)
    friend_request.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cancel_friend_request(request, user_id):
    """The user who sends to another user friend request can cancel it."""
    from_user = get_object_or_404(TLAccount, id=request.user.id)
    to_user = get_object_or_404(TLAccount, id=user_id)

    friend_request = FriendRequest.objects.filter(
        from_user=from_user,
        to_user=to_user
    )
    friend_request.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# Feed
def show_feed(request):
    """Shows all posts with comments from users which are in friend list of
    current user or which are followed by current user."""
    template = 'accounts/feed/feed_final_child_3.html'

    if request.method == 'GET':
        user = TLAccount.objects.get(id=request.user.id)
        posts_id = set()

        # Creating a feed -> O(A^2 + B^2) !
        for friend in user.friends.all():
            friend_posts = Post.objects.filter(author=friend)
            for post in friend_posts:
                posts_id.add(post.id)

        for following_user in user.people_which_follow.all():
            following_user_posts = Post.objects.filter(author=following_user)
            for post in following_user_posts:
                posts_id.add(post.id)

        # Will be shown posts and comments for last 7 days.
        enddate = timezone.now()
        startdate = enddate - timedelta(days=7)

        feed = Post.objects.filter(pk__in=posts_id).filter(timestamp__range=[
                                                           startdate, enddate])

        context = {'feed': feed}

        comment_form = AddCommentForm()
        context['comment_form'] = comment_form

        return render(request, template, context)
    else:
        post_id = request.POST.get("post_id", )
        if post_id:
            # User adds a comment.
            content_for_comment_form = {
                'body': request.POST.get("body", ),
                'user': request.user,
                'post': post_id
            }
            comment_form = AddCommentForm(content_for_comment_form)
            if comment_form.is_valid():
                comment_form.save()
                return HttpResponseRedirect(
                       reverse('accounts:feed', ) + '#post-' +
                       str(post_id) + "-content")
            else:
                context['comment_form'] = comment_form
                return render(request, template, context)


# Followers
def follow_user(request, user_id):
    """Adds user1 to followers of user2 and adds user2 to  people_which_follow
    of user1."""
    user_who_wanna_follow = get_object_or_404(TLAccount, id=request.user.id)
    user_who_gets_follower = get_object_or_404(TLAccount, id=user_id)
    user_who_wanna_follow.people_which_follow.add(user_who_gets_follower)
    user_who_gets_follower.followers.add(user_who_wanna_follow)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def unfollow_user(request, user_id):
    """Deletes user1 from followers of user2 and deletes user2 from
    following of user1."""
    user_who_unfollow = get_object_or_404(TLAccount, id=request.user.id)
    user_who_loses_follower = get_object_or_404(TLAccount, id=user_id)
    user_who_unfollow.people_which_follow.remove(user_who_loses_follower)
    user_who_loses_follower.followers.remove(user_who_unfollow)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def followers_list(request, user_id):
    """Shows the list of followers of user."""
    user_acc = get_object_or_404(TLAccount, id=user_id)

    try:
        followers = user_acc.followers.all()
    except AttributeError:
        followers = 0

    context = {
        "user_acc": user_acc,
        'who_makes_a_request': request.user.email,
        "followers": followers
    }
    return render(request, 'accounts/followers_list.html', context)


def following_list(request, user_id):
    """Shows the list of people which are followed by user."""
    user_acc = get_object_or_404(TLAccount, id=user_id)

    try:
        following_users = user_acc.people_which_follow.all()
    except AttributeError:
        following_users = 0

    context = {
        "user_acc": user_acc,
        'who_makes_a_request': request.user.email,
        "following_users": following_users
    }
    return render(request, 'accounts/following_list.html', context)


# Likes
def like_post(request, post_id):
    """Adds user to 'likes' field of Post model / deletes user from 'likes'
    field of Post model and returns json which will be used in front end for
    dynamical update of page without refreshing the whole page."""
    liked = False
    user_acc = TLAccount.objects.get(id=request.user.id)

    post = Post.objects.get(id=post_id)
    if user_acc not in post.likes.all():
        post.likes.add(user_acc)
        liked = True
    else:
        post.likes.remove(user_acc)
        liked = False

    context = {
        'post_id': post_id,
        'status': liked
    }
    return JsonResponse(context, safe=False)


def likes_api_comment(request, comment_id):
    """Adds user to 'likes' field of Comment model / deletes user from 'likes'
    field of Comment model and returns json which will be used in front end for
    dynamical update of page without refreshing the whole page."""
    liked = False
    user_acc = TLAccount.objects.get(id=request.user.id)

    comment = Comment.objects.get(id=comment_id)
    if user_acc not in comment.likes.all():
        comment.likes.add(user_acc)
        liked = True
    else:
        comment.likes.remove(user_acc)
        liked = False

    context = {
        'comment_id': comment_id,
        'status': liked
    }
    return JsonResponse(context, safe=False)
