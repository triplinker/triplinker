from django import forms

from .models import Place, Photo, Feedback


class AddPlaceForm(forms.ModelForm):
    name_of_place = forms.CharField(widget=forms.TextInput(attrs={
                                     'class': 'form-control', }))

    place_description = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control',
                                     'rows': '5'}))

    class Meta:
        model = Place
        fields = ['name_of_place', 'type_of_place', 'place_description',
                  'place_pic', 'place_description', 'location']


class AddPhotoToPlaceGalleryForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['place', 'place_pic', 'author']


class AddFeedbackForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control rounded-0',
                                     'id': 'exampleFormControlTextarea2',
                                     'rows': "3",
                                     'placeholder': 'Comment'}))

    CHOICES = [
        ("no", "Without any assessment"),
        ("1", "★"),
        ("2", "★★"),
        ("3", "★★★"),
        ("4", "★★★★"),
        ("5", "★★★★★"),
    ]
    rating = forms.ChoiceField(widget=forms.Select(attrs={
                               'class': 'browser-default custom-select mb-4',
                               }), choices=CHOICES, initial='no')

    class Meta:
        model = Feedback
        fields = ['place', 'rating', 'comment', 'author']
