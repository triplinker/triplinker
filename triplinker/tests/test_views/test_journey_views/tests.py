import pytest

from django.urls import reverse

from tests.helpers.create_user import new_user


@pytest.mark.django_db
def test_add_new_journey_view(client):
    response = new_user()['client']
    url = reverse('journeys:new-journey')
    response = response.get(url)
    assert response.status_code == 200










