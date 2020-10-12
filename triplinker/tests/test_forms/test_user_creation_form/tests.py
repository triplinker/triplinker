# Another app modules.
import pytest

# !Triplinker modules:
from accounts.forms.forms import CreateUser


@pytest.fixture
def form():
    form = CreateUser()
    return form


# Testing labels 
def test_reg_form_first_name_field_label(form):
    assert (form.fields['first_name'].label == 'First name' or
        form.fields['first_name'].label == None)


def test_reg_form_second_name_field_label(form):
    assert (form.fields['second_name'].label == 'Second name' or
        form.fields['second_name'].label == None)



def test_reg_form_email_field_label(form):
    assert (form.fields['email'].label == 'E-mail' or
    	form.fields['email'].label == None)


def test_reg_form_sex_field_label(form):
    assert (form.fields['sex'].label == 'Sex' or
    	form.fields['sex'].label == None)


def test_reg_form_date_of_birth_field_label(form):
    assert (form.fields['date_of_birth'].label == 'Date of birth' or
		form.fields['date_of_birth'].label == None)


def test_reg_form_country_field_label(form):
    assert (form.fields['country'].label == 'Country' or
        form.fields['country'].label == None)


def test_reg_form_place_of_work_field_label(form):
    assert (form.fields['place_of_work'].label == 'Place of work' or
        form.fields['place_of_work'].label == None)


def test_reg_form_short_description_field_label(form):
    assert (form.fields['short_description'].label =='Short description' or
        form.fields['short_description'].label == None)


def test_reg_form_hobbies_field_label(form):
    assert (form.fields['hobbies'].label == 'Hobbies' or
        form.fields['hobbies'].label == None)


def test_reg_form_vkontakte_field_label(form):
    assert (form.fields['vkontakte'].label == 'VKontakte' or
        form.fields['vkontakte'].label == None)


def test_reg_form_twitter_field_label(form):
    assert (form.fields['twitter'].label == 'Twitter' or
        form.fields['twitter'].label == None)


def test_reg_form_facebook_field_label(form):
    assert (form.fields['facebook'].label == 'Facebook' or
        form.fields['facebook'].label == None)

# Testing help texts
def test_reg_form_first_name_field_help_text(form):
	assert form.fields['first_name'].help_text == 'Enter your real First name'


def test_reg_form_second_name_field_help_text(form):
	assert form.fields['second_name'].help_text == 'Enter your real Second name'


def test_reg_form_email_field_help_text(form):
	assert form.fields['email'].help_text == 'Enter your email'


def test_reg_form_date_of_birth_field_help_text(form):
	assert form.fields['date_of_birth'].help_text == 'Enter your date of birth'


def test_reg_form_country_field_help_text(form):
	assert (form.fields['country'].help_text == 'Select your country from ' + 
		'the list')


def test_reg_form_place_of_work_field_help_text(form):
	assert (form.fields['place_of_work'].help_text == 'Let us know about ' +
		'your current place of work')


def test_reg_form_short_description_field_help_text(form):
	assert (form.fields['short_description'].help_text == 'Write some words ' +
		'about yourself')


def test_reg_form_hobbies_field_help_text(form):
	assert (form.fields['hobbies'].help_text == 'Tell us about your hobbies ' +
		'and interests!')


def test_reg_form_vkontakte_field_help_text(form):
	assert (form.fields['vkontakte'].help_text == 'Here you can place a link ' + 
		'to your Vkontakte profile')


def test_reg_form_twitter_field_help_text(form):
	assert (form.fields['twitter'].help_text == "Do you have a Twitter " + 
		"account? That's a good opportunity to insert a link to your profile " +
		"here :)")


def test_reg_form_facebook_field_help_text(form):
	assert (form.fields['facebook'].help_text == 'Share your Facebook ' +
		'profile with us!')


# Testing form's clean and clean_<fieldname> methods
def test_clean_first_name_equals_second_name():
	data = {
		'first_name':'Adam',
		'second_name':'Adam',
		'email':'adam@example',
		'sex':'M',
		'date_of_birth':'1992-01-16',
		'country':'BY',
		'password1':'topSecret123',
		'password2':'topSecret123',
	}

	form = CreateUser(data)
	assert form.is_valid() == False 


def test_clean_first_name_method():
	data_1 = {
		'first_name':'Adam123',
		'second_name':'Robinson',
		'email':'adam@example',
		'sex':'M',
		'date_of_birth':'1992-01-16',
		'country':'BY',
		'password1':'topSecret123',
		'password2':'topSecret123',
	}

	form = CreateUser(data_1)
	assert form.is_valid() == False

	data_2 = {
		'first_name':'Adam' * 4,
		'second_name':'Robinson',
		'email':'adam@example',
		'sex':'M',
		'date_of_birth':'1992-01-16',
		'country':'BY',
		'password1':'topSecret123',
		'password2':'topSecret123',
	}

	form = CreateUser(data_2)
	assert form.is_valid() == False


def test_clean_second_name_method():
	data_1 = {
		'first_name':'Adam',
		'second_name':'Robinson123',
		'email':'adam@example',
		'sex':'M',
		'date_of_birth':'1992-01-16',
		'country':'BY',
		'password1':'topSecret123',
		'password2':'topSecret123',
	}

	form = CreateUser(data_1)
	assert form.is_valid() == False

	data_2 = {
		'first_name':'Adam',
		'second_name':'Robinson' * 2,
		'email':'adam@example',
		'sex':'M',
		'date_of_birth':'1992-01-16',
		'country':'BY',
		'password1':'topSecret123',
		'password2':'topSecret123',
	}

	form = CreateUser(data_2)
	assert form.is_valid() == False
