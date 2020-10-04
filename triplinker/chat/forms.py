from django import forms

from accounts.models.TLAccount_frequest import TLAccount

from .models import Message, GroupChat, GroupChatMainPhoto
from .helpers.get_query_set_not_participants import get_friends_not_participants


class SendMessageForm(forms.ModelForm):

    def __init__(self, usr={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = TLAccount.objects.get(id=usr.id)
        self.queryset = self.user.friends.all()
        self.fields['to_user'].queryset = self.queryset

    message = forms.CharField(widget=forms.Textarea(attrs={
                                         'class': 'form-control',
                                         'rows': '5'}))

    to_user = forms.ModelChoiceField(queryset=TLAccount.objects.all())

    class Meta:
        model = Message
        fields = ['to_user', 'message']


class CreateGroupChatForm(forms.ModelForm):

    def __init__(self, usr={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = TLAccount.objects.get(id=usr.id)
        self.friends = self.user.friends.all()
        self.tuples = [(i.id, i.email) for i in self.friends]
        self.fields['participants'].choices = self.tuples

    chat_name = forms.CharField(widget=forms.TextInput(attrs={
                                     'class': 'form-control', }))

    OPTIONS = (('n', 'none'))
    widget = forms.CheckboxSelectMultiple
    participants = forms.MultipleChoiceField(widget=widget, choices=OPTIONS)

    def clean_chat_name(self):
        current_chat_name = self.cleaned_data['chat_name']

        chat_names = []
        chats = GroupChat.objects.all()
        for c in chats:
            chat_name = c.get_name()
            chat_names.append(chat_name)

        if current_chat_name in chat_names:
            msg = 'Chat with name %s is alredy exists' % current_chat_name
            raise forms.ValidationError(msg)
        return current_chat_name

    class Meta:
        model = GroupChat
        exclude = ['timestamp', ]


class ChatWithMainPhotoForm(forms.ModelForm):

    class Meta:
        model = GroupChatMainPhoto
        exclude = ['timestamp', ]


class InviteFriendToChatForm(forms.Form):

    def __init__(self, usr, chat_slug_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = TLAccount.objects.get(id=usr.id)
        self.query = get_friends_not_participants(usr, chat_slug_name)
        self.tuples = [(i.id, i.email) for i in self.query]
        self.fields['participants'].choices = self.tuples

    OPTIONS = (('n', 'none'))
    widget = forms.CheckboxSelectMultiple
    participants = forms.MultipleChoiceField(widget=widget, choices=OPTIONS)


# class PinImageToMessageForm(forms.ModelForm):
#     class Meta:
#         model = MessagePhoto
#         fields = '__all__'
