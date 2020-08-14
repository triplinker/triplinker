from django.urls import path

from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.messages_page, name='messages-page'),

]
