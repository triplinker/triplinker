# Django modules.
from django.urls import path

# !Triplinker modules:

# Current app modules.
from . import views


app_name = 'trip_places'

urlpatterns = [
    path('', views.all_places, name='all-places'),
    path('favourite-list/<int:user_id>/', views.favourite_places,
         name='favourite-places'),
    path('add-place/', views.add_place, name='add-place'),
    path('<int:place_id>', views.place_page, name='place-page'),
    path('<int:place_id>/photos', views.photos_of_place,
         name='photos-of-place'),
    path('<int:place_id>/feedback', views.comments_rating_page,
         name='rating-comments'),
    path('<int:place_id>/edit', views.edit_place_inf,
         name='edit-place'),
    path('favourite/<int:place_id>/', views.favourite_api,
         name="favourite"),
]
