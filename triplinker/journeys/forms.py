from django import forms
from .models import Journey


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
        fields = ['journey_from', 'date_of_start', 'journey_to', 'date_of_end',
                  'participants', 'place', 'description']
