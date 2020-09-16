from django.urls import reverse
from django.test import TestCase, Client

from accounts.models.TLAccount_frequest import TLAccount
from .models import Post, Comment


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

        self.user_1.friends.add(self.user_2)
        self.user_2.friends.add(self.user_1)

        # Creating post.
        self.post = Post.objects.create()
        self.kwargs_post = {'post_id': self.post.id}

        # Creating comment.
        self.comment = Comment.objects.create(user=self.user_1, 
                                              post=self.post)
        self.kwargs_comment = {'comment_id': self.comment.id}

    def test_like_post_api_view(self):
        url = reverse('feed:likes-api-post', kwargs=self.kwargs_post)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_like_comment_api_view(self):
        url = reverse('feed:likes-api-comment', kwargs=self.kwargs_comment)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)
