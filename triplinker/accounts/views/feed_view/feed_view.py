from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.models.TLAccount_frequest import TLAccount
from accounts.feed_app_link import AddCommentForm
from accounts.feed_app_link import Post


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
            friend_posts = Post.objects.filter(author=friend, is_place=False)
            for post in friend_posts:
                posts_id.add(post.id)

        for following_user in user.people_which_follow.all():
            following_user_posts = Post.objects.filter(author=following_user,
                                                       is_place=False)
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
