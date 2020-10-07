import json
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .models import (Message, DialogPhoto, GroupChat, GroupChatMessage,
                     GroupChatMessagePhoto)
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
        image_or_none = 'no_img'
        try:
            img_field = DialogPhoto.objects.get(message=message).image.url
            index = img_field.rfind('/media')
            image_or_none = img_field[index:]
        except ObjectDoesNotExist:
            pass

        context[message.id] = [message.from_user.email, message.message,
                               image_or_none]
    return json.dumps(context)


def get_avatar(message):
    avtr = None
    try:
        avtr = message.msg_from_user.get_avatar.all().first().profile_image.url
    except AttributeError:
        pass
    return avtr


def get_associated_messages_group_chat_celery(chat_name_slug):
    # Chat
    c = GroupChat.objects.get(slug=chat_name_slug)
    mssges = GroupChatMessage.objects.filter(group_chat=c).order_by('timestamp')

    context = {}

    for message in mssges:
        image_or_none = 'no_img'
        try:
            # Image field
            img_f = GroupChatMessagePhoto.objects.get(message=message).image.url
            index = img_f.rfind('/media')
            image_or_none = img_f[index:]
        except ObjectDoesNotExist:
            pass

        avtr = get_avatar(message)
        context[message.id] = [message.msg_from_user.email, message.message,
                               image_or_none, avtr]

    return json.dumps(context)
