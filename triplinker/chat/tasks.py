from celery.decorators import task
from .celery_views import get_associated_messages_celery


@task(name='get_associated_messages_task')
def get_associated_messages_task(from_user, to_user):
    return get_associated_messages_celery(from_user, to_user)
