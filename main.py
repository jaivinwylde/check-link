#!/usr/bin/env python3

# Link checker - Jaivin Wylde - 12/03/21
import sys
import proxyscrape
import asyncio
import pyppeteer


class LinkChecker:
    def __init__(self):
        self.collector = proxyscrape.create_collector("main", "https")
        self.proxy_tries = 3
        self.timeout = 8

    def __await__(self):
        """Define async code that gets run when the class is initialized
        (awaited). We need to do it in this __await__ method because we can't
        await anything in __init__.
        """
        async def init():
            print("\nLaunching browser")
            await self.launch_browser()

            return self

        return init().__await__()

    def get_proxy(self):
        """Get a new anonymous HTTPS proxy from our proxy collector
        (proxyscrape).
        """
        self.proxy = self.collector.get_proxy({
            "type": "https",
            "anonymous": True
        })

        print(f"Using {self.proxy.host} from {self.proxy.country}")

    async def launch_browser(self):
        """Get a new proxy and launch a pyppeteer browser that uses that new
        proxy, then take control of the current page and give it our desired
        settings.
        """
        # Get new proxy
        self.get_proxy()

        # Launch browser with proxy
        self.browser = await pyppeteer.launch(
            ignoreHTTPSErrors=True,
            args=[f"--proxy-server={self.proxy.host}:{self.proxy.port}"])

        # Setup current page
        self.page = await self.browser.pages()
        self.page = self.page[0]
        await self.page.setUserAgent("gaming browser")
        await self.page.setViewport({
            "width": 1920,
            "height": 1080
        })

    async def get(self, url):
        """A wrapper around pyppeteer's goto url method. To finish a request,
        it has to wait until there's been no more than 2 network connections
        for at least 500 milliseconds (this means the site will be 99% loaded,
        but it won't stall on a small thing that's taking forever), or until a
        timeout exception has been raised. If the request fails, it will try
        again, and it will keep trying until it has tried more times than it's
        allowed to with the same proxy. If it reaches that limit, it will
        blacklist the current proxy, get a new one, relaunch the browser, and
        start making more requests. It will continue doing this until a
        successful request has been returned.
        """
        tries = 0

        while True:
            try:
                # Make request
                response = await asyncio.wait_for(
                    self.page.goto(url, waitUntil="networkidle2"),
                    self.timeout)

                return response

            except Exception:
                tries += 1

                if tries > self.proxy_tries:
                    print("Request failed, trying again with a new proxy")

                    # Blacklist current proxy
                    self.collector.blacklist_proxy(self.proxy)

                    # Relaunch browser with new proxy
                    await self.browser.close()
                    await self.launch_browser()

                    tries = 0

                else:
                    print("Request failed, trying again")


async def main():
    # Get link
    link = input("Link: ")

    if link.endswith("/"):
        link = link[:-1]

    print("\nLoading...")

    checker = await LinkChecker()

    # Find root
    root = link.split(".")
    root[-1] = root[-1].split("/")[0]
    root_url = ".".join(root)

    # Get root
    print("\nRequesting root")
    await checker.get(root_url)
    print(f"Root is {checker.page.url}")

    await checker.page.screenshot(path="root.png")
    print("Screenshot: root.png")

    # Get link

    # Check if the link is more than its root
    if len(link.split("/")) > 3:
        print("\nRequesting link")
        await checker.get(link)

        if checker.page.url != link:
            print(f"Redirects to {checker.page.url}")

        else:
            print("Does not redirect")

        await checker.page.screenshot(path="link.png")
        print("Screenshot: link.png")

    await checker.browser.close()

    print("\nDone")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        sys.exit()
