from django.shortcuts import get_object_or_404

from .models import Message
from accounts.models.TLAccount_frequest import TLAccount


def new_messages_notification(request):
    if not request.user.is_authenticated:
        context = {
            'new_messages': None,
        }
        return context

    usr = get_object_or_404(TLAccount, id=request.user.id)
    the_friends_of_user = usr.friends.all()

    last_messages = []
    for frnd in the_friends_of_user:
        message_to_frnd = Message.objects.filter(from_user=usr, to_user=frnd)
        messages_from_frnd = Message.objects.filter(from_user=frnd, to_user=usr)
        message_with_frnd = message_to_frnd | messages_from_frnd
        last_msg = message_with_frnd.order_by('-timestamp').first()
        last_messages.append(last_msg)

    last_messages = list(filter(None, last_messages))
    new_messages = []

    if len(last_messages) == 0:
        new_messages = None
    else:
        for message in last_messages:
            if usr not in message.users_who_read_message.all():
                new_messages.append(message)

    context = {
        'new_messages': new_messages,
        'number_of_new_messages': len(new_messages),
    }
    return context
