import urllib.parse
import urllib.request

SERVICE_URL = "https://academicallamerica.com/services/archives.ashx/stories"

params = {
    "index": 1,
    "page_size": 30,
    "sport": "",
    "season": "",
    "school": "",
    "search": ""
}

url = SERVICE_URL + "?" + urllib.parse.urlencode(params)

print("REQUEST URL:")
print(url)
print()

request = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Referer": "https://academicallamerica.com/archives.aspx"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    raw = response.read().decode("utf-8", errors="replace")

    print("HTTP STATUS:")
    print(response.status)
    print()

    print("CONTENT TYPE:")
    print(response.headers.get("Content-Type"))
    print()

    print("RESPONSE LENGTH:")
    print(len(raw))
    print()

    print("FIRST 5000 CHARACTERS OF RESPONSE:")
    print(raw[:5000])

print()
print("DIAGNOSTIC COMPLETE")
