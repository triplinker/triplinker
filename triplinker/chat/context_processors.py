# Django modules.
from django.shortcuts import get_object_or_404

# !Triplinker modules:

# Current app modules.
from accounts.models.TLAccount_frequest import TLAccount
from .helpers.mssges_with_friends import get_last_mssges_from_dialogs


def new_messages_notification(request) -> dict:
    """Needed to notify users about incoming messages. On the site it's will be
    displayed as a number of new incoming messages near the envelope."""
    if not request.user.is_authenticated:
        context = {
            'new_messages': None,
        }
        return context

    usr = get_object_or_404(TLAccount, id=request.user.id)

    last_messages = get_last_mssges_from_dialogs(usr)
    new_messages = []

    if len(last_messages) != 0:
        for message in last_messages:
            if usr not in message.users_who_read_message.all():
                new_messages.append(message)

        new_messages = len(new_messages)
    else:
        new_messages = None

    context = {
        'new_messages': new_messages,
        'number_of_new_messages': new_messages,
    }
    return context
