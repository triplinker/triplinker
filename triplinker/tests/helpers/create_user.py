from accounts.models.TLAccount_frequest import TLAccount
from django.test.client import Client


def new_user():
    TLAccount.objects.create_user(first_name='John', second_name='Li', 
                                  email='john@test.com', sex='M', 
                                  date_of_birth='2000-10-12', country='BY',
                                  password='secret')

    TLAccount.objects.create(first_name='Nick', second_name='Yohanson',
                             email='nick@test.com', sex='M', 
                             date_of_birth='2000-10-12', country='BY',
                             password='secret')

    current_user = TLAccount.objects.get(email='john@test.com')
    another_user = TLAccount.objects.get(email='nick@test.com')
    client = Client()
    response = client.post('/login/', {'username':'john@test.com', 
                                       'password':'secret'})

    return {'client':client, 'current_user': current_user, 
            'another_user': another_user}
