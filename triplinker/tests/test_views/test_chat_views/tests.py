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
def test_messages_page_view(client):
    response = new_user()['client']
    url = reverse('chat:messages-page')
    response = response.get(url)
    assert response.status_code == 200










