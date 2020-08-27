from django.http import JsonResponse

from accounts.models.TLAccount_frequest import TLAccount
from .models import Post, Comment


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
