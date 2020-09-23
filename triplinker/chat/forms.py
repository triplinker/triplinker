from django import forms

from accounts.models.TLAccount_frequest import TLAccount

from .models import Message, GroupChat


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

    chat_name = forms.CharField(widget=forms.TextInput(attrs={
                                     'class': 'form-control', }))

    class Meta:
        model = GroupChat
        exclude = ['timestamp', ]
