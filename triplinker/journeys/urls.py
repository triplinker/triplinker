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
    path('separate-journeys/<int:journey_id>/remove/<int:user_id>',
         views.remove_from_journey, name='remove'),
    path('<int:user_id>/', views.user_journey_list,
         name='journey-list'),
    path('new-journey/', views.add_new_journey, name="new-journey"),
    path('edit-journey/<int:journey_id>/', views.edit_journey,
         name="edit-journey"),
    path('edit-activity/<int:activity_id>/', views.edit_activity,
         name="edit-activity"),

    # The sorting of journeys
    path('sort-by-date/<int:user_id>', views.sort_journeys_by_date,
         name="sort-journeys-by-date"),
    path('sort-by-rating/<int:user_id>', views.sort_journeys_by_rating_of_place,
         name="sort-journeys-by-rating-of-place"),
    path('journey-form-api/', views.journey_form_api,
         name="journey-form-api"),
    path('activity-form-api/', views.activity_form_api,
         name="activity-form-api"),
]
