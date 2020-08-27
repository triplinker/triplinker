from django import forms

from .models import Place


class AddPlaceForm(forms.ModelForm):
    name_of_place = forms.CharField(widget=forms.TextInput(attrs={
                                     'class': 'form-control', }))

    place_description = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control',
                                     'rows': '5'}))

    class Meta:
        model = Place
        fields = ['name_of_place', 'type_of_place', 'place_description',
                  'place_pic', 'place_description', 'location', 'rating']
