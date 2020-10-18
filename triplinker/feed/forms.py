# Django modules.
from django import forms

# !Triplinker modules:

# Current app modules.
from .models import Post, Comment


class AddPostToProfileForm(forms.ModelForm):
    """The form that will be displayed in own profile of current user."""
    content = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control',
                                     'id': 'message',
                                     'rows': "3",
                                     'placeholder': 'What are you thinking?'}))

    class Meta:
        model = Post
        fields = ['content', 'author']


class AddPostToPlacePageForm(forms.ModelForm):
    """The form that will be displayed in own profile of current user."""
    placeholder = 'Write some news which are connected with this place!'
    content = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control',
                                     'id': 'message',
                                     'rows': "3",
                                     'placeholder': placeholder}))

    class Meta:
        model = Post
        fields = ['content', 'author', 'place', 'is_place']


class AddCommentForm(forms.ModelForm):
    """The form that will be displayed in comment section below every post on
    the site."""
    body = forms.CharField(widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'id': 'message',
                                  'rows': "3"}))

    class Meta:
        model = Comment
        fields = ['body', 'user', 'post']
