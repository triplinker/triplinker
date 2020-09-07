from django.urls import path

from . import views


app_name = 'journeys'

urlpatterns = [
    path('separate-journeys/<int:journey_id>/', views.journey_page,
         name='journey-page'),
    path('separate-journeys/<int:journey_id>/join', views.join_journey,
         name='join'),
    path('separate-journeys/<int:journey_id>/leave', views.leave_journey,
         name='leave'),
    path('<int:user_id>/', views.user_journey_list,
         name='journey-list'),
    path('new-journey/', views.add_new_journey, name="new-journey"),

    # The sorting of journeys
    path('sort-by-date/<int:user_id>', views.sort_journeys_by_date,
         name="sort-journeys-by-date"),
    path('sort-by-rating/<int:user_id>', views.sort_journeys_by_rating_of_place,
         name="sort-journeys-by-rating-of-place"),
]
