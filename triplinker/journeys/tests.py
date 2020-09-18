from django.urls import reverse
from django.test import TestCase, Client

from accounts.models.TLAccount_frequest import TLAccount
from trip_places.models import Place

from .models import Journey, Participant


class TestJourneysViews(TestCase):

    def setUp(self):
        self.user_1 = TLAccount.objects.create_user(first_name='John', 
                                   second_name='Li', 
                                   email='john@test.com', sex='M', 
                                   date_of_birth='2000-10-12', country='BY',
                                   password='secret')
        self.client_user_1 = Client()
        self.client_user_1.login(username='john@test.com', password='secret')

        self.user_1_acc = TLAccount.objects.get(first_name='John')

        self.kwargs_user_1 = {'user_id': self.user_1_acc.id}

        # Creating Journey
        self.place = Place.objects.create()
        Participant.objects.create(participant=self.user_1)

        self.particapant = Participant.objects.get(participant=self.user_1)
        self.journey = Journey.objects.create(place_from=self.place, 
                                              place_to=self.place,
                                              who_added_the_journey=self.user_1)
        self.particapant.journey = self.journey
        self.particapant.save()
        
        self.new_journey = Journey.objects.get(place_from=self.place)
                                              
        self.journey_kwargs = {'journey_id': self.journey.id}


    def test_journey_page_view(self):
        url = reverse('journeys:journey-page', kwargs=self.journey_kwargs)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_user_journey_list_view(self):
        url = reverse('journeys:journey-list', kwargs=self.kwargs_user_1)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_sort_journeys_by_date_view(self):
        url = reverse('journeys:sort-journeys-by-date', 
                      kwargs=self.kwargs_user_1)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_sort_journeys_by_rating_of_place_view(self):
        url = reverse('journeys:sort-journeys-by-rating-of-place', 
                      kwargs=self.kwargs_user_1)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)
