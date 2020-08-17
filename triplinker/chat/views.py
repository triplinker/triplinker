import json
from itertools import chain
from operator import attrgetter
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import Message
from accounts.models.TLAccount_frequest import TLAccount


def messages_page(request, user_id):

    message_to_user = get_object_or_404(TLAccount, id=user_id)

    context = {
        'message_to_user': message_to_user,
    }
    return render(request, 'chat/messages_page.html', context)

@csrf_exempt
def send_message(request, user_id):
    from_user = TLAccount.objects.get(id=request.user.id)
    to_user = TLAccount.objects.get(id=user_id)

    message = request.POST.get("message_body", "")
    new_message = Message.objects.create(
        from_user=from_user,
        to_user=to_user,
        message = message 
    )
    json = {'author': str(new_message.from_user), 
            'message_id': str(new_message.id)}
    return JsonResponse(json, safe=False)


@csrf_exempt
def get_all_messages(request, user_id):
    from_user = get_object_or_404(TLAccount, id=request.user.id)
    to_user = get_object_or_404(TLAccount, id=user_id)

    msg = Message.objects.filter(from_user=from_user).filter(to_user=to_user)
    msg2 = Message.objects.filter(from_user=to_user).filter(to_user=from_user)

    raw_all_messages = msg | msg2  # Merge Querysets
    ordered_messages = raw_all_messages.order_by('timestamp')
     
    context = {}
    for message in ordered_messages:
        context[message.id] = [message.from_user.email, message.message]

    return JsonResponse(context, safe=False)
