from django.urls import path

from .views import all_views as views


app_name = 'accounts'

urlpatterns = [
    # Home page.
    path('feed/', views.show_feed, name="feed"),

    # All users list.
    path('users/', views.all_users_list, name='all_users_list'),

    # SetAvatar.
    path('set-avatar/', views.set_avatar_view, name='set-avatar'),

    # User's photo gallery.
    path('users/<int:user_id>/photo-gallery/', views.photos_of_user,
         name='user-photo-gallery'),

    # A particular profile of user.
    path('users/<int:user_id>/', views.detail_profile,
         name="detail_profile"),

    # Friends system.
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

    # Followers and following.
    path('users/<int:user_id>/follow/', views.follow_user, name="follow"),
    path('users/<int:user_id>/unfollow/', views.unfollow_user, name="unfollow"),

    path('users/<int:user_id>/followers/', views.followers_list,
         name="followers-list"),
    path('users/<int:user_id>/following/', views.following_list,
         name="following-list"),

    # Profile, reg, auth.
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/', views.ActivateView.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(),
         name='profile_edit')
]
