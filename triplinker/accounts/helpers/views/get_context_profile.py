from .status_between_users_definer import define_status
from accounts.models.TLAccount_frequest import FriendRequest
from accounts.models.feed import Post


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

    posts = Post.objects.filter(author=user_acc)

    context = {
        'user_acc': user_acc,
        'who_makes_a_request': request.user.email,
        'amount_of_friends': amount_of_friends,
        'amount_of_frequests': amount_of_frequests,
        'status_between_users': status_between_users,
        'posts': posts,
    }
    return context
