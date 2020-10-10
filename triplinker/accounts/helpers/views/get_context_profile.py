from .status_between_users_definer import define_status
from accounts.models.TLAccount_frequest import FriendRequest
from accounts.feed_app_link import Post


def get_context_for_profile(request, user_acc, accType='another_user') -> dict:
    context = None
    status_between_users = None
    try:
        amount_of_friends = user_acc.friends.all().count()
        amount_of_frequests = FriendRequest.objects.filter(
            to_user=user_acc.id).count()

        current_user = request.user
        another_user = user_acc

    except AttributeError:
        amount_of_friends = 0
        amount_of_frequests = 0

    if accType == 'another_user':
        status_between_users = define_status(FriendRequest, current_user,
                                             another_user)

    posts = Post.objects.filter(author=user_acc, is_place=False)
    notification_posts = Post.objects.filter(author=user_acc,
                                             notification_post=True)
    posts = posts | notification_posts

    user_avatar = None
    try:
        user_avatar = user_acc.get_avatar.all().first()
    except Exception:
        pass

    qualities = user_acc.qualities.all()
    qualities_3 = None
    qualities_more_than_3 = False
    other_qualities = None
    if len(qualities) > 3:
        qualities_more_than_3 = True
        qualities_3 = qualities[:3]
        other_qualities = qualities[3:]
    else:
        qualities_3 = qualities

    context = {
        'user_acc': user_acc,
        'who_makes_a_request': request.user.email,
        'amount_of_friends': amount_of_friends,
        'amount_of_frequests': amount_of_frequests,
        'status_between_users': status_between_users,
        'posts': posts,
        'avatar': user_avatar,
        'qualities': qualities_3,
        'qualities_more_than_3': qualities_more_than_3,
        'other_qualities': other_qualities
    }
    return context
