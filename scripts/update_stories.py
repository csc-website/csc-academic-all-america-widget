import urllib.request

URL = (
    "https://academicallamerica.com/services/archives.ashx/stories"
    "?index=1&page_size=30"
)

request = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://academicallamerica.com/archives.aspx"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    raw = response.read().decode("utf-8", errors="replace")

print("HTTP STATUS:")
print(response.status)
print()

print("RESPONSE:")
print(raw[:10000])
