from django.urls import path

from . import views


app_name = 'recommendations'

urlpatterns = [
    path('', views.all_recommendations, name='all-recommendations'),
    path('journeys-only/', views.jouneys_only, name='journeys-only'),
    path('places-only', views.places_only, name='places-only'),
]
