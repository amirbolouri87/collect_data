import requests
import asyncio
from playwright.async_api import async_playwright
from django.conf import settings
from elasticsearch import Elasticsearch


async def insert_data(data):
    es = Elasticsearch(
        hosts=[f"http://192.168.88.229:9200"],
        basic_auth=(
            "elastic",
            "Pass123"
        ),
        verify_certs=False,
        headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"}
    )

    # doc = json.loads(data)
    await asyncio.to_thread(
        es.index,
        index="text_data",
        document={"content": data}
    )
    print('inserted . ')


async def handle_response(response):
    url = response.url
    if "ajax.json" in url:
        try:
            r = requests.get(url)
            print(r.text[: 30])
            await insert_data(r.text)

        except Exception as e:
            print("Error fetching URL:", e)


async def combined_crawl():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--single-process",
                "--no-zygote",
            ]
        )
        page = await browser.new_page()

        # wrap async handler for Playwright events
        page.on("response", lambda resp: asyncio.create_task(handle_response(resp)))

        await page.goto(settings.COMBINED_CRAWL_URL)
        await asyncio.sleep(4)
        await browser.close()



