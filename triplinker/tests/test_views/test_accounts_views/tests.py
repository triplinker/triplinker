import pytest

from django.urls import reverse

from tests.helpers.create_user import new_user


@pytest.mark.django_db
def test_signup_view(client):
    url = reverse('accounts:signup')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_signin_view(client):
    url = reverse('accounts:login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view(client):
    response = new_user()['client']
    url = reverse('accounts:profile')
    response = response.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_profile_edit_view(client):
#     response = new_user()['client']
#     url = reverse('accounts:profile_edit')
#     response = response.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_feed_view(client):
#     response = new_user()['client']
#     url = reverse('accounts:feed')
#     response = response.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_feed_view(client):
#     response = new_user()['client']
#     url = reverse('accounts:all_users_list')
#     response = response.get(url)
#     assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client):
    response  = new_user()['client']
    url = reverse('accounts:logout')
    response = response.get(url)
    assert response.status_code == 200
