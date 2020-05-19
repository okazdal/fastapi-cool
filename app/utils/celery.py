from __future__ import absolute_import
from celery import Celery

from ..middleware import celery

celery_app = Celery("worker")

celery_app.config_from_object(celery)