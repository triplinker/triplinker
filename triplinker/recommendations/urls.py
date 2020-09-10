from django.urls import path

from . import views


app_name = 'recommendations'

urlpatterns = [
    path('', views.similar_jouneys, name='similar-journeys')
]
