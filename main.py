#!/usr/bin/env python3

# link checker - jaivin wylde - 12/03/21
import time

from selenium import webdriver

print("READY\n")
link = input("link (ctrl+shift+v to paste): ")

print("\nloading...")

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

# get root
root = link.split(".")
root[1] = root[1].split("/")[0]
root = ".".join(root)

driver.get(root)
time.sleep(1)

print(f"\nroot is {driver.current_url}")
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

driver.quit()
print("\ndone")

print("click on 'code' tab to see screenshots")
