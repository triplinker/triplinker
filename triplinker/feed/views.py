# Django modules.
from django.http import JsonResponse
from django.shortcuts import render

# !Triplinker modules:

# Another app modules.
from accounts.models.TLAccount_frequest import TLAccount

# Current app modules.
from .models import Post, Comment, Notification


# Notifications
def notifications_list(request):
    """Renders page with notifications for user:
    1) user's friend has joined a journey.
    2) user's friend is following any news of a place.
    """
    user = request.user
    notifications = Notification.objects.filter(users__in=[user])
    for n in notifications:
        n.is_seen.add(user)
    return render(request, "feed/notifications.html",
                  {"notifications": notifications})


# Likes
def like_post_api(request, post_id):
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


def like_comment_api(request, comment_id):
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
