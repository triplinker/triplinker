from django.urls import path

from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.messages_page, name='messages-page'),
    path('<int:user_id>/', views.messages_dialog_page,
         name='messages-dialog'),
    path('send-message-api/<int:user_id>/', views.send_message,
         name='send-message'),
    path('get-all-messages-api/<int:user_id>/',
         views.get_all_messages, name='get-all-messages'),
]
