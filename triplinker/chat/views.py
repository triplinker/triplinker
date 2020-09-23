import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.template.defaultfilters import slugify

from accounts.models.TLAccount_frequest import TLAccount
from chat.tasks import (get_associated_messages_task,
                        get_associated_messages_group_chat_task)

from .models import Message, GroupChat, GroupChatMessage
from .helpers.get_last_messages_with_friends import get_last_mssges_from_dialogs
from .forms import SendMessageForm, CreateGroupChatForm


def messages_page(request):
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

    # group_chat = GroupChat.objects.filter(participants=usr)
    # dict_ = {'user': usr}  #!
    context = {
        'ordered_messages': msg,
        'form': SendMessageForm(usr=usr)
    }
    return render(request, 'chat/messages_page.html', context)


def messages_dialog_page(request, user_id):
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
def send_message(request, user_id, dict_for_messages={}):
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
    json = {'author': str(new_message.from_user),
            'message_id': str(new_message.id)}
    return JsonResponse(json, safe=False)


def send_message_from_dialogs_page(request):
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
    messages = get_associated_messages_task.delay(request.user.id, user_id)
    parsed_json = json.loads(messages.get())
    return JsonResponse(parsed_json, safe=False)


# Group Chats
def create_group_chat(request):
    template = 'chat/create_group_chat.html'
    usr = TLAccount.objects.get(id=request.user.id)
    context = {'form': CreateGroupChatForm()}
    if request.method == 'POST':
        form = CreateGroupChatForm(request.POST)
        if form.is_valid():
            final_form = form.save(commit=False)
            final_form.creator = usr
            cht_name = form.cleaned_data.get('chat_name')
            final_form.slug = slugify(cht_name)
            final_form.save()
            final_form.participants.add(usr)
            final_form.save()

        else:
            context['form'] = form
            return render(request, template, context)

        return HttpResponseRedirect(reverse('chat:messages-page'))
    else:
        return render(request, template, context)


def list_of_group_chats(request):
    order_v = '-timestamp'
    chts = GroupChat.objects.filter(participants=request.user).order_by(order_v)

    context = {
        'group_chats': chts
    }
    return render(request, 'chat/list_of_group_chats.html', context)


def particular_group_chat(request, chat_name_slug):
    group_chat = GroupChat.objects.get(slug=chat_name_slug)
    context = {'group_chat': group_chat}
    return render(request, 'chat/particular_group_chat.html', context)


@csrf_exempt
def send_message_in_group_chat(request, chat_name_slug):
    current_user = TLAccount.objects.get(id=request.user.id)
    message = request.POST.get("message_body", "")
    group_chat = GroupChat.objects.get(slug=chat_name_slug)

    # participants = group_chat.participants.all()

    data = {
        'group_chat': group_chat,
        'msg_from_user': current_user,
        'message': message
    }
    new_message = GroupChatMessage.objects.create(**data)
    json = {'author': str(new_message.msg_from_user),
            'message_id': str(new_message.id)}
    return JsonResponse(json, safe=False)


def get_all_messages_for_group_chat(request, chat_name_slug):
    # Messages
    m = get_associated_messages_group_chat_task.delay(chat_name_slug)
    parsed_json = json.loads(m.get())
    return JsonResponse(parsed_json, safe=False)
