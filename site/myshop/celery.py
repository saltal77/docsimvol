# coding: utf-8
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")
app = Celery('myshop', backend='amqp', broker='amqp://guest@localhost//', include=['myshop.tasks'])