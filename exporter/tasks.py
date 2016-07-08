from celery import Celery
import config as config


def make_celery(app):
    """
    Simple helper function to tie together the Flask and Celery parts of the exporter

    Args:
        app (Flask.App): The Flask application object

    Returns:
        Celery: The celery application
    """
    celery = Celery(app.import_name, backend=config.CELERY_RESULT_BACKEND, broker=config.CELERY_BROKER_URL)
    celery.conf.update(CELERY_ACCEPT_CONTENT=['json'], CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json')

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


