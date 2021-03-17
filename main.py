#!/usr/bin/env python3

# Link checker - Jaivin Wylde - 12/03/21
import asyncio

from pyppeteer import launch


async def main():
    # Get link
    link = input("link (ctrl+shift+v to paste): ")

    browser = await launch()

    page = await browser.newPage()
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })

    # Get root
    root = link.split(".")
    root[-1] = root[-1].split("/")[0]
    root_url = ".".join(root)

    await page.goto(root_url, waitUntil="networkidle0")
    print(f"\nroot is {page.url}")
    await page.screenshot(path="root.png")
    print("screenshot: root.png")

    # Get link
    await page.goto(link, waitUntil="networkidle0")

    if page.url != link:
        print(f"\nredirects to {page.url}")
        await page.screenshot(path="redirect.png")
        print("screenshot: redirect.png")

    await browser.close()

    print("\ndone")

    print("click on the 'code' tab to see screenshots")

asyncio.get_event_loop().run_until_complete(main())
