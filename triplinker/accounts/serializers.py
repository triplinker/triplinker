from .models.TLAccount_frequest import TLAccount
from rest_framework import serializers


class TLAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLAccount
        exclude = ['password', 'vkontakte', 'twitter', 'facebook', 'friends',
                   'followers', 'people_which_follow', 'can_get_message_from',
                   'strangers', 'date_joined', 'is_admin', 'is_active',
                   'is_staff']
