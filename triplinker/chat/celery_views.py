import json
from django.shortcuts import get_object_or_404

from .models import Message, GroupChat, GroupChatMessage
from accounts.models.TLAccount_frequest import TLAccount


def get_associated_messages_celery(from_user, to_user):
    from_user = get_object_or_404(TLAccount, id=from_user)
    to_user = get_object_or_404(TLAccount, id=to_user)

    msg = Message.objects.filter(from_user=from_user).filter(to_user=to_user)
    msg2 = Message.objects.filter(from_user=to_user).filter(to_user=from_user)

    raw_all_messages = msg | msg2  # Merge Querysets
    ordered_messages = raw_all_messages.order_by('timestamp')

    for message in ordered_messages:
        message.users_who_read_message.add(from_user)

    context = {}
    for message in ordered_messages:
        context[message.id] = [message.from_user.email, message.message]
    return json.dumps(context)


def get_associated_messages_group_chat_celery(chat_name_slug):
    # Chat
    c = GroupChat.objects.get(slug=chat_name_slug)
    mssges = GroupChatMessage.objects.filter(group_chat=c).order_by('timestamp')

    context = {}

    for message in mssges:
        context[message.id] = [message.msg_from_user.email, message.message]

    return json.dumps(context)
