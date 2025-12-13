from celery import Celery
import os
import requests
import asyncio
from playwright.async_api import async_playwright
from django.conf import settings

async def handle_response(response):
    url = response.url
    if "ajax.json" in url:
        try:
            r = requests.get(url)
        except Exception as e:
            print("Error fetching URL:", e)


async def combined_crawl():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # wrap async handler for Playwright events
        page.on("response", lambda resp: asyncio.create_task(handle_response(resp)))

        await page.goto(settings.COMBINED_CRAWL_URL)

        # async wait just like your time.sleep(2)
        await asyncio.sleep(2)

        await browser.close()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app = Celery(
    'scrape_tgju_table',
    broker=F'amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//',
    backend='rpc://'
)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(40.0, scrape_tgju_table.s(), name='scrape_tgju_table')

@app.task
def scrape_tgju_table():
    asyncio.run(combined_crawl())



