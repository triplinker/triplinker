# Django modules.
from django import forms

# !Triplinker modules:

# Current app modules.
from .models import Journey, Activity


class AddJourneyForm(forms.ModelForm):
    journey_from = forms.CharField(widget=forms.TextInput(attrs={
                                     'class': 'form-control', }))
    date_of_start = forms.DateField(widget=forms.DateInput(attrs={
                                     'class': 'form-control',
                                     'type': 'date'}))
    journey_to = forms.CharField(widget=forms.TextInput(attrs={
                                     'class': 'form-control'}))

    date_of_end = forms.DateField(widget=forms.DateInput(attrs={
                                     'class': 'form-control',
                                     'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control',
                                     'rows': '5'}))

    class Meta:
        model = Journey
        fields = ['journey_from', 'place_from', 'date_of_start', 'journey_to',
                  'place_to', 'date_of_end', 'description', 'visibility']


class AddActivityForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
                                     'class': 'form-control',
                                     'rows': '5'}))

    date_of_start = forms.DateField(widget=forms.DateInput(attrs={
                                    'class': 'form-control',
                                    'type': 'date'}))

    date_of_end = forms.DateField(widget=forms.DateInput(attrs={
                                    'class': 'form-control',
                                    'type': 'date'}))

    class Meta:
        model = Activity
        fields = ['description', 'place', 'date_of_start',
                  'date_of_end']
