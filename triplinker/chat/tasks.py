# Another project modules.
from celery.decorators import task
from .celery_views import (get_associated_messages_celery,
                           get_associated_messages_group_chat_celery)


@task(name='get_associated_messages_task')
def get_associated_messages_task(from_user, to_user):
    return get_associated_messages_celery(from_user, to_user)


@task(name='get_associated_messages_group_chat_task')
def get_associated_messages_group_chat_task(chat_name_slug):
    return get_associated_messages_group_chat_celery(chat_name_slug)
