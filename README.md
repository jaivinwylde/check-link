# Check link
Investigates a link and takes screenshots of everything it finds. Good for
safely checking shady links.

---

## What it finds

### The root of the site
![root example](images/root_example.png)

It will follow where the root of the site takes it. It ended up here in this
example, and this is the screenshot it took:
![root destination](images/root_destination.png)

### The redirect
It will follow where the main link takes it. It ended up here in this example,
and this is the screenshot it took:
![redirect destination](images/redirect_destination.png)

---

## Peace of mind
All requests are run through an anonymous proxy so your IP address is safe.

```python
# Get proxy
collector = proxyscrape.create_collector("main", "https")
proxy = collector.get_proxy(
    {"code": ["us", "ca"], "type": "https", "anonymous": True})

# Initialize pyppeteer
browser = await pyppeteer.launch(
    ignoreHTTPSErrors=True,
    args=[f"--proxy-server={proxy.host}:{proxy.port}"])
```

This is all an attacker would see:
![ip grab example](images/ip_grab_example.png)
