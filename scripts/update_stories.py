import json
import urllib.parse
import urllib.request

SERVICE_URL = "https://academicallamerica.com/services/archives.ashx/stories"
LIMIT = 10

params = {
    "index": 1,
    "page_size": 30,
    "sport": 0,
    "season": 0,
    "school": 0,
    "search": ""
}

url = SERVICE_URL + "?" + urllib.parse.urlencode(params)

request = urllib.request.Request(
    url,
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

print("RESPONSE:")
print(raw[:10000])
