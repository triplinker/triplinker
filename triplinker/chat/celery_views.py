import json
from django.shortcuts import get_object_or_404

from .models import Message
from accounts.models.TLAccount_frequest import TLAccount


def get_associated_messages_celery(from_user, to_user):
    from_user = get_object_or_404(TLAccount, id=from_user)
    to_user = get_object_or_404(TLAccount, id=to_user)
    msg = Message.objects.filter(from_user=from_user).filter(to_user=to_user)
    msg2 = Message.objects.filter(from_user=to_user).filter(to_user=from_user)

    msg = Message.objects.filter(from_user=from_user).filter(to_user=to_user)
    msg2 = Message.objects.filter(from_user=to_user).filter(to_user=from_user)

    raw_all_messages = msg | msg2  # Merge Querysets
    ordered_messages = raw_all_messages.order_by('timestamp')

    context = {}
    for message in ordered_messages:
        context[message.id] = [message.from_user.email, message.message]
    return json.dumps(context)
