# Another app modules.
import pytest

# Django modules.
from django.urls import reverse

# !Triplinker modules:
from tests.helpers.create_user import new_user


@pytest.mark.django_db
def test_all_places_view(client):
    response = new_user()['client']
    url = reverse('trip_places:all-places')
    response = response.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_new_place_view(client):
    response = new_user()['client']
    url = reverse('trip_places:add-place')
    response = response.get(url)
    assert response.status_code == 200
