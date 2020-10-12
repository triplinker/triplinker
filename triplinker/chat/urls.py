# Django modules.
from django.urls import path

# !Triplinker modules:

# Current app modules.
from .views import all_views as views


app_name = 'chat'

urlpatterns = [
    path('', views.messages_page, name='messages-page'),
    path('<int:user_id>/', views.messages_dialog_page,
         name='messages-dialog'),
    path('send-message-api/<int:user_id>/', views.send_message,
         name='send-message'),
    path('send-message-from-dialogs-page/',
         views.send_message_from_dialogs_page,
         name='send-message-from-dialogs-page'),
    path('get-all-messages-api/<int:user_id>/',
         views.get_all_messages, name='get-all-messages'),

    # GroupChat possibility.
    path('create-group-chat', views.create_group_chat,
         name='create-group-chat'),
    path('group-chats/', views.list_of_group_chats, name='group-chats'),
    path('<slug:chat_name_slug>/', views.particular_group_chat,
         name='particular-group-chat'),
    path('<slug:chat_name_slug>/send-message-group-chat-api/',
         views.send_message_in_group_chat, name='send-message-group-chat'),
    path('<slug:chat_name_slug>/get-all-messages-api/',
         views.get_all_messages_for_group_chat,
         name='get-all-messages-group-chat'),

    # GroupChat extra features.
    path('<slug:chat_name_slug>/participants/', views.view_participants,
         name='participants'),
    path('invite-person/<slug:chat_name_slug>/',
         views.invite_to_chat, name='invite-to-chat'),
    path('delete-from-chat/<slug:chat_name_slug>/<int:user_id>/',
         views.delete_user_from_chat, name='delete-from-chat'),
    path('leave-chat/<slug:chat_name_slug>/', views.leave_chat,
         name='leave-chat'),
]
