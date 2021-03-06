# Python modules.
import datetime

# Another project modules.
from crispy_forms import helper
from crispy_forms.layout import Submit

# Django modules.
from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       AuthenticationForm)
from django.urls import reverse
from django.contrib.auth.models import User

# !Triplinker modules:

# Current app module.
from accounts.models.TLAccount_frequest import (TLAccount, AvatarTLAccount,
                                                UserPhotoGallery)


class CreateUser(UserCreationForm):
    """Form for creating user account in the system."""
    class Meta:
        model = TLAccount

        fields = ['first_name', 'second_name', 'email', 'sex', 'date_of_birth',
                  'country', 'place_of_work', 'short_description', 'hobbies',
                  'vkontakte', 'twitter', 'facebook',
                  ]

        help_texts = {
            "first_name": "Enter your real First name",
            "second_name": "Enter your real Second name",
            "email": "Enter your email",
            "sex": "Select your sex",
            "date_of_birth": "Enter your date of birth",
            "country": "Select your country from the list",
            "place_of_work": "Let us know about your current place of work",
            "short_description": "Write some words about yourself",
            "hobbies": "Tell us about your hobbies and interests!",
            "vkontakte": "Here you can place a link to your Vkontakte profile",
            "twitter": "Do you have a Twitter account? That's a good " +
                       "opportunity to insert a link to your profile here :)",

            "facebook": "Share your Facebook profile with us!",
        }

    def clean(self, *args, **kwargs):
        """Compare first_name and second_name fields in form, checks that their
        value is not the same."""
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        second_name = cleaned_data.get('second_name')

        if first_name == second_name:
            raise forms.ValidationError("First name and Second name must be " +
                                        "different!")
        return cleaned_data

    def clean_first_name(self, *args, **kwargs):
        """Checks that first_name field doesn't contain digits and field's
        length is not over 15 characters."""
        first_name = self.cleaned_data.get('first_name')

        for i in first_name:
            if i.isdigit():
                raise forms.ValidationError("The First name cannot contain" +
                                            "numbers")

        if len(first_name) <= 15:
            return first_name
        else:
            raise forms.ValidationError("This is not a valid First Name!")

    def clean_second_name(self, *args, **kwargs):
        """Checks that second_name field doesn't contain digits and field's
        length is not over 15 characters."""
        second_name = self.cleaned_data.get('second_name')

        for i in second_name:
            if i.isdigit():
                raise forms.ValidationError("The Second name cannot contain" +
                                            "numbers")

        if len(second_name) <= 15:
            return second_name
        else:
            raise forms.ValidationError("This is not a valid Second Name!")


class SignUpForm(UserCreationForm):
    """Only email and password are needed."""
    class Meta:
        model = TLAccount
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        self.helper = helper.FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('accounts:signup')

        self.helper.help_text_inline = False
        self.helper.html5_required = True
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-md-12 control-label'
        self.helper.field_class = 'col-md-12'

        self.helper.add_input(
            Submit('send_button', u'Signup', css_class='col-md-12'))

        super(SignUpForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(SignUpForm, self).save(*args, **kwargs)
        return self


class AccountActivationForm(UserChangeForm):
    """The form to fill out some additional information about the current user.
    """
    class Meta:
        model = TLAccount
        fields = (
            'email',
            'first_name',
            'second_name',
            'sex',
            'date_of_birth',
            'country',
            'qualities',
            'can_get_message_from',
            'place_of_work',
            'hobbies',
            'motto',
            'short_description',
            'vkontakte',
            'twitter',
            'facebook',
        )

    this_year = datetime.datetime.today().year
    years_range = range(this_year - 1, this_year - 100, -1)
    email = forms.EmailField(widget=forms.HiddenInput)
    date_of_birth = forms.DateField(
            initial=None,
            widget=forms.SelectDateWidget(
                years=years_range,
                attrs={'required': True}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'required': True}))
    second_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': True}))

    def save(self, *args, **kwargs):
        super(AccountActivationForm, self).save(*args, **kwargs)
        return self


class LoginForm(AuthenticationForm):
    """Email and passwrod are needed."""
    class Meta:
        model = User
        fields = ('email', 'password',)

    def __init__(self, *args, **kwargs):

        self.helper = helper.FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('accounts:login')

        self.helper.help_text_inline = False
        self.helper.html5_required = True
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-md-12 control-label'
        self.helper.field_class = 'col-md-12'

        self.helper.add_input(
            Submit('send_button', u'Login', css_class='col-md-12'))

        super(LoginForm, self).__init__(*args, **kwargs)


class ProfileEditForm(UserChangeForm):
    """The possibility of editing information that was wrote down when the user
    was going through the process of registration."""
    class Meta:
        model = TLAccount
        exclude = ('password', 'last_login', 'groups', 'user_permissions',
                   'friends', 'followers', 'strangers', 'people_which_follow',
                   'date_joined', 'is_superuser', 'is_active', 'is_admin',
                   'is_staff',)

    def __init__(self, *args, **kwargs):

        self.helper = helper.FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('accounts:profile_edit')

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-5'

        self.helper.add_input(Submit('send_button', u'Save'))

        super(ProfileEditForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(ProfileEditForm, self).save(*args, **kwargs)
        return self


class SetAvatarForm(forms.ModelForm):
    """Gives the possibility to set an avatar for user."""
    class Meta:
        model = AvatarTLAccount
        exclude = ['timestamp', ]


class AddPhotoToUserGalleryForm(forms.ModelForm):
    """The possibility of adding new photo to the gallery of the current user.
    """
    class Meta:
        model = UserPhotoGallery
        fields = ['photo', 'author']
