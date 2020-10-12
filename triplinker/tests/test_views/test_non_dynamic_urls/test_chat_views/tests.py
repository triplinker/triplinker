# Another app modules.
import pytest

# Django app modules.
from django.urls import reverse

# !Triplinker modules:
from tests.helpers.create_user import new_user


@pytest.mark.django_db
def test_messages_page_view(client):
    response = new_user()['client']
    url = reverse('chat:messages-page')
    response = response.get(url)
    assert response.status_code == 200
