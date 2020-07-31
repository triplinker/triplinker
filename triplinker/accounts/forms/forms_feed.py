from django import forms
from django.forms import ModelForm

from accounts.models.feed import Post
    

class AddPostForm(forms.ModelForm):
    content = forms.CharField(widget= forms.Textarea
                           (attrs={'class':'form-control',
                                    'id':'message',
                                    'rows': "3",
                                    'placeholder': 'What are you thinking?'}))
    class Meta:
        model = Post
        fields = ['content', 'author']