from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import TLAccount


class CreateUser(UserCreationForm):

	class Meta:
		model = TLAccount

		fields = ['first_name', 'second_name', 'email', 'sex', 'date_of_birth',
			'country', 'place_of_work', 'short_description', 'hobbies',
			'vkontakte', 'twitter', 'facebook',
		]

		help_texts = {
			"first_name": "Enter your real First name",
			"second_name":"Enter your real Second name",
			"email":"Enter your email",
			"sex":"Select your sex",
			"date_of_birth":"Enter your date of birth",
			"country":"Select your country from the list",
			"place_of_work":"Let us know about your current place of work",
			"short_description":"Write some words about yourself",
			"hobbies":"Tell us about your hobbies and interests!",
			"vkontakte":"Here you can place a link to your Vkontakte profile",
			"twitter":"Do you have a Twitter account? That's a good " +
				"opportunity to insert a link to your profile here :)",

			"facebook":"Share your Facebook profile with us!",
        }

	def clean(self, *args, **kwargs):
		cleaned_data = super().clean()
		first_name = cleaned_data.get('first_name')
		second_name = cleaned_data.get('second_name')

		if first_name == second_name:
	 		raise forms.ValidationError("First name and Second name must be " +
	 			"different!")
		return cleaned_data

	def clean_first_name(self, *args, **kwargs):
		first_name = self.cleaned_data.get('first_name')

		for i in first_name:
			if i.isdigit():
				raise forms.ValidationError("The First name cannot contain" + "numbers")

		if len(first_name) <= 15:
			return first_name
		else:
			raise forms.ValidationError("This is not a valid First Name!")

	def clean_second_name(self, *args, **kwargs):
		second_name = self.cleaned_data.get('second_name')

		for i in second_name:
			if i.isdigit():
				raise forms.ValidationError("The Second name cannot contain" +
					"numbers")

		if len(second_name) <= 15:
			return second_name
		else:
			raise forms.ValidationError("This is not a valid Second Name!")


class UserCreationForm(UserCreationForm):

	class Meta:
		model = TLAccount
		fields = ('email',)


class UserChangeForm(UserChangeForm, UserCreationForm):
	pass
