from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404

from accounts.feed_app_link import AddPostToProfileForm, AddCommentForm
from accounts.models.TLAccount_frequest import TLAccount
from accounts.feed_app_link import Post
from accounts.helpers.views.get_context_profile import get_context_for_profile


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
        self.context = get_context_for_profile(self.request, user_acc,
                                               accType='profile')
        form = AddPostToProfileForm()
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

            form = AddPostToProfileForm(content_for_form)
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


def detail_profile(request, user_id):
    """Function makes the same work as ProfileView class but with other profiles
    on site(it doesn't work with current user's profile)."""

    user_acc = get_object_or_404(TLAccount, id=user_id)
    accType = 'another_user'
    context = detail_profile.context = get_context_for_profile(request,
                                                               user_acc,
                                                               accType=accType)

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
            form = AddPostToProfileForm(initial={'content': request.POST,
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
        form = AddPostToProfileForm()
        comment_form = AddCommentForm()
        context['form'] = form
        context['comment_form'] = comment_form
    return render(request, template_name, context)
