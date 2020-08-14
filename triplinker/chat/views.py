from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Message
from accounts.models.TLAccount_frequest import TLAccount


def messages_page(request):

    try:
        friends_of_user = request.user.friends.all()

    except AttributeError:
        friends_of_user = 0

    context = {
        'friends_of_user': friends_of_user,
    }
    return render(request, 'chat/messages_page.html', context)


def send_message(request, user_id, message):
    from_user = TLAccount.objects.get(id=request.user.id)
    to_user = TLAccount.objects.get(id=user_id)
    Message.objects.create(
        from_user=request_from_user,
        to_user=request_to_user,
        message = message 
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_message(request, message_id):
    message_to_remove = Message.objects.filter(id=message_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
