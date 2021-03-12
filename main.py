#!/usr/bin/env python3

# link checker - jaivin wylde - 12/03/21
import time

from selenium import webdriver

# link = input("link: ")
link = "https://discordgift.site/ALlJL9NjcwQdXJ9n"

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)

print("\nloading...")

# get root
root = "/".join(link.split("/")[:-1])
driver.get(root)
time.sleep(1)

print(f"\ngoes to {driver.current_url}")
time.sleep(2)
screenshot = driver.save_screenshot("root.png")
print("screenshot: root.png")

# get link
driver.get(link)
time.sleep(1)

# check redirect
if driver.current_url != link:
    print(f"\nredirects to {driver.current_url}")
    time.sleep(2)
    screenshot = driver.save_screenshot("redirect.png")
    print("screenshot: redirect.png")

print("\ndone")
driver.quit()
