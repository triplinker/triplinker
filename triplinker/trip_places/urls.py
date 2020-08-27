from django.urls import path

from . import views


app_name = 'trip_places'

urlpatterns = [
    path('', views.all_places, name='all-places'),
    path('add-place/', views.add_place, name='add-place'),
    path('<int:place_id>', views.place_page, name='place-page'),
    path('favourite/<int:place_id>/', views.favourite_api,
         name="favourite"),
]
