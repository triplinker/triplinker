import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chat.tasks import get_associated_messages_task


from .models import Message
from accounts.models.TLAccount_frequest import TLAccount


def messages_page(request):
    usr = get_object_or_404(TLAccount, id=request.user.id)
    the_friends_of_user = usr.friends.all()

    last_messages = []
    for frnd in the_friends_of_user:
        message_with_frnd = Message.objects.filter(from_user=usr, to_user=frnd)
        last_msg = message_with_frnd.order_by('-timestamp').first()
        last_messages.append(last_msg)

    last_messages = filter(None, last_messages)

    try:
        msg = sorted(last_messages, key=lambda msg: msg.timestamp, reverse=True)
    # If user doesn't have friends and list 'last_messages' is empty
    except AttributeError:
        msg = None

    context = {
        'ordered_messages': msg,
        'time': str(int(datetime.datetime.now().timestamp()))
    }
    return render(request, 'chat/messages_page.html', context)


def messages_dialog_page(request, user_id):
    current_user = get_object_or_404(TLAccount, id=request.user.id)
    message_to_user = get_object_or_404(TLAccount, id=user_id)

    if (current_user not in message_to_user.friends.all() or
            message_to_user not in current_user.friends.all()):
        context = {'user_that_is_not_friend': message_to_user}
        return render(request, 'chat/message_error.html', context)

    context = {
        'message_to_user': message_to_user,
    }
    return render(request, 'chat/messages_dialog.html', context)


@csrf_exempt
def send_message(request, user_id):
    from_user = TLAccount.objects.get(id=request.user.id)
    to_user = TLAccount.objects.get(id=user_id)

    message = request.POST.get("message_body", "")
    new_message = Message.objects.create(
        from_user=from_user,
        to_user=to_user,
        message=message
    )
    json = {'author': str(new_message.from_user),
            'message_id': str(new_message.id)}
    return JsonResponse(json, safe=False)


def get_all_messages(request, user_id):
    messages = get_associated_messages_task.delay(request.user.id, user_id)
    parsed_json = json.loads(messages.get())
    return JsonResponse(parsed_json, safe=False)
