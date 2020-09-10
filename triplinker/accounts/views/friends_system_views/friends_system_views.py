from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from accounts.models.TLAccount_frequest import TLAccount, FriendRequest


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
