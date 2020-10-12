# Python modules.
import os
import json
import base64
from datetime import datetime

# Django Modules.
from django.core.files.images import ImageFile
from django.shortcuts import render, get_object_or_404
from django.http import (HttpResponseNotFound, HttpResponseRedirect,
                         JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# !Triplinker modules:

# Another app module.
from accounts.models.TLAccount_frequest import TLAccount

# Current app modules.
from chat.tasks import get_associated_messages_task
from chat.models import Message, DialogPhoto
from chat.helpers.mssges_with_friends import get_last_mssges_from_dialogs
from chat.forms import SendMessageForm


def messages_page(request):
    """Page with user's messages (only dialogs)."""
    usr = get_object_or_404(TLAccount, id=request.user.id)
    last_messages = get_last_mssges_from_dialogs(usr)

    try:
        msg = sorted(last_messages, key=lambda msg: msg.timestamp, reverse=True)
        for message in msg:
            if message.from_user.email == usr.email:
                message.users_who_read_message.add(usr)

    # If user doesn't have friends and list 'last_messages' is empty
    except AttributeError:
        msg = None

    context = {
        'ordered_messages': msg,
        'form': SendMessageForm(usr=usr)
    }
    return render(request, 'chat/messages_page.html', context)


def messages_dialog_page(request, user_id):
    """The page with the dialog window."""
    current_user = get_object_or_404(TLAccount, id=request.user.id)
    message_to_user = get_object_or_404(TLAccount, id=user_id)

    if current_user.id == message_to_user.id:
        return HttpResponseNotFound()

    elif message_to_user.can_get_message_from == 'All':
        context = {
            'message_to_user': message_to_user,
        }
        return render(request, 'chat/messages_dialog.html', context)

    elif message_to_user.can_get_message_from == 'Friends':
        if (current_user not in message_to_user.friends.all() and
           message_to_user not in current_user.friends.all() and
           current_user not in message_to_user.strangers.all() and
           message_to_user not in current_user.strangers.all()):

            context = {
                'user_that_is_not_friend': message_to_user
            }
            return render(request, 'chat/message_error.html', context)

        elif (current_user not in message_to_user.friends.all() and
              message_to_user not in current_user.friends.all() and
              current_user in message_to_user.strangers.all() and
              message_to_user in current_user.strangers.all()):

            context = {
                'message_to_user': message_to_user,
            }
            return render(request, 'chat/messages_dialog.html', context)

        context = {
            'message_to_user': message_to_user,
        }
        return render(request, 'chat/messages_dialog.html', context)

    else:
        return HttpResponseNotFound()


@csrf_exempt
def send_message(request, user_id: int, dict_for_messages={}):
    """Iserts messages into DB."""
    from_user = TLAccount.objects.get(id=request.user.id)
    to_user = TLAccount.objects.get(id=user_id)
    is_dialog_page = dict_for_messages.get('is_dialog_page', None)

    if not is_dialog_page:
        message = request.POST.get("message_body", "")
    else:
        message = dict_for_messages['message']

    new_message = None
    if from_user in to_user.friends.all():
        new_message = Message.objects.create(
            from_user=from_user,
            to_user=to_user,
            message=message
        )
    elif (from_user not in to_user.friends.all() and
          to_user not in from_user.friends.all()):

        from_user.strangers.add(to_user)
        to_user.strangers.add(from_user)
        new_message = Message.objects.create(
            from_user=from_user,
            to_user=to_user,
            message=message
        )

    new_message.users_who_read_message.add(request.user)

    get_msg_with_photo = None
    imgs_url_for_fronted = None
    image_base64 = request.POST.get("image_or_nothing", "").partition(",")[2]
    if image_base64:
        decoding = base64.b64decode(image_base64)
        current_date = str(datetime.now())
        poFileStr = str(request.user) + current_date + '.jpg'

        cur_path = os.path.dirname(__file__)

        additional_dirs = 'public/media/'

    # .../triplinker/triplinker/public/media/chat/pictures_of_messages/image.jpg
    # ... - means system dirctories which are not connected with the project
    # Need to change cur_path.rstrip('chat') if the name of application will be
    # changed!
        new_path = cur_path.rstrip('chat') + additional_dirs + poFileStr
        new_path = ''.join(new_path)

        with open(new_path, 'wb') as f:
            f.write(decoding)

        new_msge_with_pic = DialogPhoto.objects.create(message=new_message,
                                                       name_of_file=poFileStr)
        new_msge_with_pic.image = ImageFile(open(new_path, "rb"))
        new_msge_with_pic.save()
        get_msg_with_photo = DialogPhoto.objects.get(name_of_file=poFileStr)

    json = {'author': str(new_message.from_user),
            'message_id': str(new_message.id)}

    try:
        image_url = get_msg_with_photo.image.url
        index = image_url.rfind('/media')
        imgs_url_for_fronted = image_url[index:]
        json['image_url'] = imgs_url_for_fronted
    except AttributeError:
        pass

    return JsonResponse(json, safe=False)


def send_message_from_dialogs_page(request):
    """The possibility of sending messages without rederecting to the dialog
    page with user."""
    usr = get_object_or_404(TLAccount, id=request.user.id)
    msg_to_another_user_form = SendMessageForm(usr, request.POST)
    if msg_to_another_user_form.is_valid():
        to_user = msg_to_another_user_form.cleaned_data.get('to_user')
        msg = msg_to_another_user_form.cleaned_data.get('message')
        another_user = TLAccount.objects.get(email=to_user)
        another_user_id = another_user.id
        dict_for_messages = {'message': msg, 'is_dialog_page': True}
        send_message(request, another_user.id, dict_for_messages)
        return HttpResponseRedirect(reverse('chat:messages-dialog',
                                    kwargs={'user_id': another_user_id}))


def get_all_messages(request, user_id):
    """Celery used view. Used in dialogs.Returns json response for FrontEnd
    with json ,which has following format:
    context[message.id] = [message.from_user.email, message.message,
                               image_or_none]
    * context is dict-like object.
    """
    messages = get_associated_messages_task.delay(request.user.id, user_id)
    parsed_json = json.loads(messages.get())
    return JsonResponse(parsed_json, safe=False)
