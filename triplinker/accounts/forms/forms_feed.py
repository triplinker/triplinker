from django import forms

from accounts.models.feed import Post, Comment


class AddPostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control',
                                     'id': 'message',
                                     'rows': "3",
                                     'placeholder': 'What are you thinking?'}))

    class Meta:
        model = Post
        fields = ['content', 'author']


class AddCommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'id': 'message',
                                  'rows': "3"}))

    class Meta:
        model = Comment
        fields = ['body', 'user', 'post']
