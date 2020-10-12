from django.urls import path

from . import views


app_name = 'feed'

urlpatterns = [
    # Like/Unlike system.
    path('likes-api-post/<int:post_id>/', views.like_post_api,
         name="likes-api-post"),
    path('likes-api-comment/<int:comment_id>/', views.like_comment_api,
         name="likes-api-comment"),

    # Notifications
    path('notifications/', views.notifications_list,
         name="notifications"),
]
