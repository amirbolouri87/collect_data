# import os
# import asyncio
#
# from celery import Celery
# from django.conf import settings
# from .tasks import *
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
# app = Celery(
#     'config',
#     broker=f'amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//',
#     backend='rpc://'
# )
# app.autodiscover_tasks()
#
# app.conf.update(
#     task_serializer='json',
#     result_serializer='json',
#     accept_content=['json'],
#     # worker_prefetch_multiplier=4,
#     timezone='Asia/Tehran',
#     enable_utc=True,
# )
#
#
#
# @app.task
# def scrape_tgju_table():
#     asyncio.run(combined_crawl())
#
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test_print('hello') every 10 seconds
#     # sender.add_periodic_task(10.0, test_print.s('hello'), name='add every 10')
#     sender.add_periodic_task(60.0, scrape_tgju_table.s(), name='scrape_tgju_table_60s')
import os
import asyncio
from celery import Celery
from django.conf import settings
from .crawl import combined_crawl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery(
    'config',
    broker=f'amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//',
    backend='rpc://'
)
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Tehran',
    enable_utc=True,
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task
def scrape_tgju_table():
    asyncio.run(combined_crawl())
