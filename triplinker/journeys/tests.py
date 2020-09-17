from django.urls import reverse
from django.test import TestCase, Client

from accounts.models.TLAccount_frequest import TLAccount
from .models import Journey, Participant


# class TestTLAccountViews(TestCase):

#     def setUp(self):
#         self.user_1 = TLAccount.objects.create_user(first_name='John', 
#                                   second_name='Li', 
#                                   email='john@test.com', sex='M', 
#                                   date_of_birth='2000-10-12', country='BY',
#                                   password='secret')
#         self.client_user_1 = Client()
#         self.client_user_1.login(username='john@test.com', password='secret')

#         self.user_2 = TLAccount.objects.create_user(first_name='Nick', 
#                                   second_name='Moo', 
#                                   email='nick@test.com', sex='M', 
#                                   date_of_birth='2000-10-12', country='BY',
#                                   password='secret')
#         self.client_user_2 = Client()
#         self.client_user_2.login(username='nick@test.com', password='secret')

#         self.user_1_acc = TLAccount.objects.get(first_name='John')
#         self.user_2_acc = TLAccount.objects.get(first_name='Nick')

#         self.kwargs_user_2 = {'user_id': self.user_2_acc.id}

#         self.user_1.friends.add(self.user_2)
#         self.user_2.friends.add(self.user_1)

#         # Creating Journey & participant
#         self.journey = Journey.objects.create(journey_from='START', 
#                                               who_added_the_journey=self.user_1)
#         self.new_journey = Journey.objects.get(journey_from='START')
#         self.participant = Participant(journey=self.new_journey, 
#                                        participant=self.user_1)
                                              
#         self.journey_kwargs = {'journey_id': self.journey.id}

#     def test_journey_page_view(self):
#         url = reverse('journeys:journey-page', kwargs=self.journey_kwargs)
#         response = self.client_user_1.get(url)
#         self.assertEquals(response.status_code, 200)

#     def test_user_journey_list_view(self):
#         url = reverse('journeys:journey-list', kwargs=self.kwargs_user_2)
#         response = self.client_user_1.get(url)
#         self.assertEquals(response.status_code, 200)

#     def test_sort_journeys_by_date_view(self):
#         url = reverse('journeys:sort-journeys-by-date', 
#                       kwargs=self.kwargs_user_2)
#         response = self.client_user_1.get(url)
#         self.assertEquals(response.status_code, 200)

#     def test_sort_journeys_by_rating_of_place_view(self):
#         url = reverse('journeys:sort-journeys-by-rating-of-place', 
#                       kwargs=self.kwargs_user_2)
#         response = self.client_user_1.get(url)
#         self.assertEquals(response.status_code, 200)
