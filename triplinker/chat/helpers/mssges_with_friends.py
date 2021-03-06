# !Triplinker modules:

# Current app modules.
from chat.models import Message


def get_last_mssges_from_dialogs(usr) -> set:
    """Gets last messages from dialogs with different users of the current user.
    Needed to display last messages for messages page."""

    the_friends_of_user = usr.friends.all()
    strangers_of_user = usr.strangers.all()

    last_messages = []
    for frnd in the_friends_of_user:
        message_to_frnd = Message.objects.filter(from_user=usr, to_user=frnd)
        messages_from_frnd = Message.objects.filter(from_user=frnd, to_user=usr)
        message_with_frnd = message_to_frnd | messages_from_frnd
        last_msg = message_with_frnd.order_by('-timestamp').first()
        last_messages.append(last_msg)

    for s in strangers_of_user:
        mssges_to_strngr = Message.objects.filter(from_user=usr, to_user=s)
        mssges_from_strngr = Message.objects.filter(from_user=s, to_user=usr)
        message_with_strngr = mssges_to_strngr | mssges_from_strngr
        last_msg = message_with_strngr.order_by('-timestamp').first()
        last_messages.append(last_msg)

    last_messages: list = list(filter(None, last_messages))
    if len(last_messages) != 0:
        # Exclude the possibility of chatting user with himself.
        for message in last_messages:
            if (message.from_user.email == usr.email and
               usr.email == message.to_user.email):
                last_messages.pop(last_messages.index(message))

    sortMsg = sorted(last_messages, key=lambda msg: msg.timestamp, reverse=True)
    return set(sortMsg)
