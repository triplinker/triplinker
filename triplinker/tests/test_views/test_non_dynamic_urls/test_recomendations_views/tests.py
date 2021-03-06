# Another app modules.
import pytest

# Django modules.
from django.urls import reverse

# !Triplinker modules:
from tests.helpers.create_user import new_user


@pytest.mark.django_db
def test_recommendations_view(client):
    response = new_user()['client']
    url = reverse('recommendations:all-recommendations')
    response = response.get(url)
    assert response.status_code == 200
