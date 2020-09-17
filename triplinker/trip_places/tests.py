from django.urls import reverse
from django.test import TestCase, Client

from accounts.models.TLAccount_frequest import TLAccount
from .models import Place


class TestTripPlacesViews(TestCase):

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

        Place.objects.create(name_of_place='TEST', 
                             type_of_place='TownCity',
                             place_description='TEST description',
                             location='US',
                             who_added_place_on_site=self.user_1)
        self.place_1 = Place.objects.get(name_of_place='TEST')
        self.place_kwargs = {'place_id': self.place_1.id}


    def test_favourite_places_view(self):
        url = reverse('trip_places:favourite-places', kwargs=self.kwargs_user_1)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_place_page_view(self):
        url = reverse('trip_places:place-page', kwargs=self.place_kwargs)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_photos_of_place_view(self):
        url = reverse('trip_places:photos-of-place', kwargs=self.place_kwargs)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_comments_rating_page_view(self):
        url = reverse('trip_places:rating-comments', kwargs=self.place_kwargs)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_edit_place_inf_view(self):
        url = reverse('trip_places:edit-place', kwargs=self.place_kwargs)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)

    def test_favourite_api_view(self):
        url = reverse('trip_places:favourite', kwargs=self.place_kwargs)
        response = self.client_user_1.get(url)
        self.assertEquals(response.status_code, 200)
