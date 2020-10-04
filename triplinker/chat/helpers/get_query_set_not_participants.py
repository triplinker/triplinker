from accounts.models.TLAccount_frequest import TLAccount

from chat.models import GroupChat


def get_friends_not_participants(usr, chat_name_slug):
    usr = TLAccount.objects.get(id=usr.id)
    friends_of_user = usr.friends.all()
    chat = GroupChat.objects.get(slug=chat_name_slug)
    partispnts = chat.participants.all()

    original_set_object_friends = set()
    original_set_object_partispnts = set()

    for f in friends_of_user:
        original_set_object_friends.add(f)

    for p in partispnts:
        original_set_object_partispnts.add(p)

    difference = original_set_object_friends - original_set_object_partispnts
    return difference
