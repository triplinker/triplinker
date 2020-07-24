from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('users/', views.AllUsersList.as_view(), name='all_users_list'),
    path('users/<int:user_id>/', views.detail_profile, name = "detail_profile"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/>', views.ProfileView.as_view(), name='profile'),
]
