# Python modules.
import os
import json
import base64
import random
from datetime import datetime

# Django Modules.
from django.core.files.images import ImageFile
from django.shortcuts import render
from django.http import (HttpResponseRedirect, JsonResponse,
                         HttpResponseBadRequest)
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.template.defaultfilters import slugify

# !Triplinker modules:

# Another app module.
from accounts.models.TLAccount_frequest import TLAccount

# Current app modules.
from chat.tasks import get_associated_messages_group_chat_task
from chat.models import (GroupChat, GroupChatMainPhoto, GroupChatMessage,
                         GroupChatMessagePhoto)
from chat.forms import (SendMessageForm, ChatWithMainPhotoForm,
                        CreateGroupChatForm, InviteFriendToChatForm)


def create_group_chat(request):
    """Displays the form to create group chat, creates group chat."""
    template = 'chat/create_group_chat.html'
    usr = TLAccount.objects.get(id=request.user.id)
    context = {'form': CreateGroupChatForm(usr),
               'form_photo': GroupChatMainPhoto()}
    if request.method == 'POST':
        get_file = request.FILES.get('chat_image', None)

        form = CreateGroupChatForm(usr, request.POST, request.FILES)
        if form.is_valid():
            final_form = form.save(commit=False)
            final_form.creator = usr

            cht_name = form.cleaned_data.get('chat_name')

            slug_of_chat = final_form.slug = slugify(cht_name)
            final_form.save()

            all_particapants = form.cleaned_data.get('participants')
            for participant in all_particapants:
                if participant == usr:
                    continue
                else:
                    particapant = TLAccount.objects.get(id=int(participant))  # noqa:F841, E501
                    final_form.participants.add(participant)

            final_form.participants.add(usr)
            final_form.save()

            if get_file:
                group_chat = GroupChat.objects.get(slug=slug_of_chat)
                form_photo = ChatWithMainPhotoForm(request.POST, request.FILES)
                if form_photo.is_valid():
                    one_more_final_form = form_photo.save(commit=False)
                    one_more_final_form.group_chat = group_chat
                    one_more_final_form.save()
                else:
                    context['form'] = form
                    context['form_photo'] = form_photo
                    return render(request, template, context)
        else:
            context['form'] = form
            return render(request, template, context)

        return HttpResponseRedirect(reverse('chat:group-chats'))
    else:
        return render(request, template, context)


def list_of_group_chats(request):
    """Displays the list of groupchats where the current user is participating.
    """
    usr = TLAccount.objects.get(id=request.user.id)
    order_v = '-timestamp'
    chts = GroupChat.objects.filter(participants=request.user).order_by(order_v)
    chat_and_last_message = {}

    P = '-timestamp'
    for c in chts:
        lstM = GroupChatMessage.objects.filter(group_chat=c).order_by(P).first()

        chat_photo = None
        try:
            chat_photo = c.get_main_photo_of_chat.all().first()
        except Exception:
            pass

        chat_and_last_message[c] = [lstM, chat_photo]

    context = {
        'group_chats': chat_and_last_message,
        'form': SendMessageForm(usr=usr)  # For little button with envelope
    }
    return render(request, 'chat/list_of_group_chats.html', context)


def particular_group_chat(request, chat_name_slug):
    """Shows the page with messages of a chat participants."""
    group_chat = GroupChat.objects.get(slug=chat_name_slug)
    context = {'group_chat': group_chat}
    return render(request, 'chat/particular_group_chat.html', context)


@csrf_exempt
def send_message_in_group_chat(request, chat_name_slug):
    """Iserts message into db(ONLY FOR GROUPCHATS)"""
    current_user = TLAccount.objects.get(id=request.user.id)
    message = request.POST.get("message_body", "")

    group_chat = GroupChat.objects.get(slug=chat_name_slug)

    data = {
        'group_chat': group_chat,
        'msg_from_user': current_user,
        'message': message
    }
    new_message = GroupChatMessage.objects.create(**data)

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

        new_msge_with_pic = GroupChatMessagePhoto.objects.create(
                                                        message=new_message,
                                                        name_of_file=poFileStr)
        new_msge_with_pic.image = ImageFile(open(new_path, "rb"))
        new_msge_with_pic.save()
        get_msg_with_photo = GroupChatMessagePhoto.objects.get(
                                                         name_of_file=poFileStr)

    json = {'author': str(new_message.msg_from_user),
            'message_id': str(new_message.id)}
    try:
        image_url = get_msg_with_photo.image.url
        index = image_url.rfind('/media')
        imgs_url_for_fronted = image_url[index:]
        json['image_url'] = imgs_url_for_fronted
    except AttributeError:
        pass

    return JsonResponse(json, safe=False)


def get_all_messages_for_group_chat(request, chat_name_slug):
    """Celery used view. Returns json for a groupchat, which has following data:
       context[message.id] = [message.msg_from_user.email, message.message,
                               image_or_none, avtr]
       context is dict-like object.
    """
    m = get_associated_messages_group_chat_task.delay(chat_name_slug)
    parsed_json = json.loads(m.get())
    return JsonResponse(parsed_json, safe=False)


# GroupChat extra features
def view_participants(request, chat_name_slug):
    """Displaying participants of a chat."""
    usr = TLAccount.objects.get(id=request.user.id)
    chat = GroupChat.objects.get(slug=chat_name_slug)
    chat_particapants = chat.participants.all()

    context = {
        'chat': chat,
        'particapants': chat_particapants,
        'form': InviteFriendToChatForm(usr, chat_name_slug)
    }

    if request.method == 'POST':
        form = InviteFriendToChatForm(usr, chat_name_slug, request.POST)

        if form.is_valid():
            pass
        else:
            context['form'] = form
            return render(request, 'chat/participants_list.html', context)
    # If HTTP method is GET
    else:
        return render(request, 'chat/participants_list.html', context)


def delete_user_from_chat(request, chat_name_slug, user_id):
    """Deletes user from chat. Avaiable only for the creator of a chat."""
    current_usr = request.user
    chat = GroupChat.objects.get(slug=chat_name_slug)
    user_to_remove = TLAccount.objects.get(id=user_id)
    chat.participants.remove(user_to_remove)

    partipnts = chat.participants.all()
    last_usr_in_partipnts = partipnts[0]
    if len(partipnts) == 1 and last_usr_in_partipnts.email == current_usr.email:
        chat.delete()
        return HttpResponseRedirect(reverse('chat:group-chats'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def invite_to_chat(request, chat_name_slug):
    """Adds users to a chat. Avaiable for all participants of a chat."""
    chat = GroupChat.objects.get(slug=chat_name_slug)

    chat_particapants = chat.participants.all()
    form = InviteFriendToChatForm(request.user, chat_name_slug, request.POST)

    if form.is_valid():
        all_particapants = form.cleaned_data.get('participants')
        for participant in all_particapants:
            particapant = TLAccount.objects.get(id=int(participant))  # noqa: F841, E501

            if participant not in chat_particapants:
                chat.participants.add(participant)

            else:
                HttpResponseBadRequest()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return HttpResponseBadRequest()


def leave_chat(request, chat_name_slug):
    """Deletes the current user from chat. If there is only one user in the
    participants list of a chat, then the chat will be deleted from DB. If
    creator leaves the chat then new creator will be choisen randomly."""

    # The user who is leaving chat.
    usr = TLAccount.objects.get(id=request.user.id)
    chat = GroupChat.objects.get(slug=chat_name_slug)
    chat.participants.remove(usr)

    # New creator.
    amount_of_particapants = len(chat.participants.all())

    if amount_of_particapants == 0:
        chat.delete()
    else:
        if usr.email == chat.creator.email:
            new_amount_ptnts = amount_of_particapants - 1
            choice_random_participant = random.randint(0, new_amount_ptnts)
            new_creator = chat.participants.all()[choice_random_participant]
            chat.creator = new_creator
            chat.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
