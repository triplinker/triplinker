# Django modules.
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# !Triplinker modules:

# Current app modules.
from accounts.models.TLAccount_frequest import TLAccount


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
