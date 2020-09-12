import pytest
from django.urls import reverse
from accounts.models.TLAccount_frequest import TLAccount
from django.test.client import Client


def new_user():
    TLAccount.objects.create_user(first_name='John', second_name='Li', 
                                  email='john@test.com', sex='M', 
                                  date_of_birth='2000-10-12', country='BY',
                                  password='secret')

    TLAccount.objects.create_user(first_name='Nick', 
    	                                         second_name='Tibo', 
                                  email='nick@test.com', sex='M', 
                                  date_of_birth='2000-10-12', country='BY',
                                  password='secret')


    another_user = TLAccount.objects.get(email='nick@test.com')
    client = Client()
    response = client.post('/login/', {'username':'john@test.com', 
                                       'password':'secret'})

    return {'client':client, 'another_user': another_user}

@pytest.mark.django_db
def test_signup_view(client):
    url = reverse('accounts:signup')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_signin_view(client):
    url = reverse('accounts:login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view(client):
    response = new_user()['client']
    url = reverse('accounts:profile')
    response = response.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_edit_view(client):
    response = new_user()['client']
    url = reverse('accounts:profile_edit')
    response = response.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_feed_view(client):
    response = new_user()['client']
    url = reverse('accounts:feed')
    response = response.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_feed_view(client):
    response = new_user()['client']
    url = reverse('accounts:feed')
    response = response.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_feed_view(client):
    response = new_user()['client']
    url = reverse('accounts:all_users_list')
    response = response.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client):
    response = new_user()['client']
    url = reverse('accounts:logout')
    response = response.get(url)
    assert response.status_code == 200



# @pytest.mark.django_db
# def test_detail_profile_view(client):
#     response = new_user()['client']
#     another_user = response['another_user']
#     user_id = another_user.id
#     print(user_id)
#     url = reverse('accounts:detail_profile', kwargs={'user_id':0})
#     response = response.get(url)
#     assert response.status_code == 200








