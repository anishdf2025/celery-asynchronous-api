from __future__ import absolute_import, unicode_literals
from celery import Celery
from app.core.config import settings

# Create the Celery app
celery_app = Celery(
    "app",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.math_tasks"]
)

# Optional configurations
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    enable_utc=True,
    task_track_started=True,
    result_expires=60 * 60 * 24,  # Results expire after 1 day
)

# If this file is run directly, this will allow you to call tasks locally
if __name__ == "__main__":
    celery_app.start()
