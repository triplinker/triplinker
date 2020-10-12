# Django modules.
from django.urls import reverse
from django.test import TestCase, Client

# !Triplinker modules:

# Another app modules.
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

    def test_detail_profile_view(self):
        url = reverse('accounts:detail_profile', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_all_incoming_frequests_view(self):
        url = reverse('accounts:incoming-frequests', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_friends_list_view(self):
        url = reverse('accounts:friends-list', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_friends_list_view(self):
        url = reverse('accounts:friends-list', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_delete_user_from_friends_view(self):
        url = reverse('accounts:delete-friend', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 302)

    def test_send_request_view(self):
        url = reverse('accounts:send-frequest', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 302)

    def test_accept_friend_request_view(self):
        url = reverse('accounts:accept-frequest', kwargs=self.kwargs_user_1)
        response = self.client_user_2.get(url)
        self.assertEquals(response.status_code, 302)

    def test_cancel_friend_request_view(self):
        url = reverse('accounts:cancel-frequest', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 302)

    def test_delete_friend_request_view(self):
        url = reverse('accounts:delete-frequest', kwargs=self.kwargs_user_1)
        response = self.client_user_2.get(url)
        self.assertEquals(response.status_code, 302)

    def test_follow_user_view(self):
        url = reverse('accounts:follow', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 302)

    def test_unfollow_user_view(self):
        url = reverse('accounts:unfollow', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 302)

    def test_followers_list_view(self):
        url = reverse('accounts:followers-list', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_following_list_view(self):
        url = reverse('accounts:following-list', kwargs=self.kwargs_user_2)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)
