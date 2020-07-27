from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.AllUsersList.as_view(), name='all_users_list'),
    path('users/<int:user_id>/', views.detail_profile,
         name="detail_profile"),

    path('users/<int:user_id>/incoming-friend-requests/',
         views.all_incoming_friquests_list, name="incoming-frequests"),
    path('users/<int:user_id>/outgoing-friend-riquests/',
         views.all_outgoing_friquests_list, name="outgoing-frequests"),
    path('users/<int:user_id>/friend-list/', views.friends_list,
         name="friends-list"),
    path('users/<int:user_id>/delete-friend/', views.delete_user_from_friends,
         name="delete-friend"),

    path('users/<int:user_id>/send-request/', views.send_request,
         name="send-frequest"),
    path('users/<int:user_id>/accept-request/', views.accept_friend_request,
         name="accept-frequest"),
    path('users/<int:user_id>/cancel-request/', views.cancel_friend_request,
         name="cancel-frequest"),
    path('users/<int:user_id>/delete-request/', views.delete_friend_request,
         name="delete-frequest"),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]
