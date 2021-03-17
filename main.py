#!/usr/bin/env python3

# Link checker - Jaivin Wylde - 12/03/21
import proxyscrape
import asyncio
import pyppeteer


async def main():
    # Get link
    link = input("Link: ")
    print("\nLoading...")

    # Get proxy
    print("\nGetting proxy")
    collector = proxyscrape.create_collector("main", "https")
    proxy = collector.get_proxy(
        {"code": "us", "type": "https", "anonymous": True})
    print(f"Using {proxy.host} from {proxy.country}")

    # Initialize pyppeteer
    print("\nLaunching browser")
    browser = await pyppeteer.launch(
        ignoreHTTPSErrors=True,
        args=[f"--proxy-server={proxy.host}:{proxy.port}"])

    page = await browser.newPage()
    await page.setUserAgent("gaming browser")
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })

    # Get root
    root = link.split(".")
    root[-1] = root[-1].split("/")[0]
    root_url = ".".join(root)

    print("\nRequesting root")
    await page.goto(root_url, waitUntil="networkidle2", timeout=0)
    print(f"Root is {page.url}")
    await page.screenshot(path="root.png")
    print("Screenshot: root.png")

    # Get link
    print("\nRequesting link")
    await page.goto(link, waitUntil="networkidle2", timeout=0)

    if page.url != link:
        print(f"\nRedirects to {page.url}")
        await page.screenshot(path="redirect.png")
        print("Screenshot: redirect.png")

    await browser.close()

    print("\nDone")

asyncio.get_event_loop().run_until_complete(main())
