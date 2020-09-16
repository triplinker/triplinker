from django.urls import reverse
from django.test import TestCase, Client

from accounts.models.TLAccount_frequest import TLAccount


class TestTLAccountViews(TestCase):

    def setUp(self):
        self.user_1 = TLAccount.objects.create_user(first_name='John', 
                                  second_name='Li', 
                                  email='john@test.com', sex='M', 
                                  date_of_birth='2000-10-12', country='BY',
                                  password='secret')
        self.client_user_1 = Client()
        self.client_user_1.login(username='john@test.com', password='secret')

        self.user_2 = TLAccount.objects.create_user(first_name='Nick', 
                                  second_name='Moo', 
                                  email='nick@test.com', sex='M', 
                                  date_of_birth='2000-10-12', country='BY',
                                  password='secret')
        self.client_user_2 = Client()
        self.client_user_2.login(username='nick@test.com', password='secret')

        self.user_1_acc = TLAccount.objects.get(first_name='John')
        self.user_2_acc = TLAccount.objects.get(first_name='Nick')

        self.kwargs_user_1 = {'user_id': self.user_1_acc.id}
        self.kwargs_user_2 = {'user_id': self.user_2_acc.id}

        self.user_1.friends.add(self.user_2)
        self.user_2.friends.add(self.user_1)

    def test_messages_dialog_page_view(self):
        url = reverse('chat:messages-dialog', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_send_message_view(self):
        url = reverse('chat:send-message', kwargs=self.kwargs_user_2)
        data = {
            'message_body': 'test'
        }
        response = self.client_user_1.post(url, data)
        self.assertEquals(response.status_code, 200)

    def test_get_all_messages_view(self):
        url = reverse('chat:get-all-messages', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

