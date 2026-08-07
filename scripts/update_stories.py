```python
import json
import urllib.parse
import urllib.request
from datetime import datetime

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
    data = json.loads(response.read().decode("utf-8"))

if data.get("error"):
    raise RuntimeError(
        "Academic All-America returned an error: "
        + str(data["error"])
    )

records = data.get("data")

if not isinstance(records, list):
    raise RuntimeError(
        "Academic All-America did not return a story list."
    )

stories = []

for item in records[:LIMIT]:
    title = str(item.get("story_headline", "")).strip()
    raw_date = str(item.get("story_postdate", "")).strip()
    path = str(item.get("story_path", "")).strip()

    if not title or not path:
        continue

    # Format date as "August 7, 2026"
    try:
        date = datetime.strptime(
            raw_date,
            "%m/%d/%Y"
        ).strftime("%B %-d, %Y")
    except ValueError:
        date = raw_date

    link = urllib.parse.urljoin(
        "https://academicallamerica.com/",
        path
    )

    stories.append({
        "title": title,
        "date": date,
        "link": link
    })

if len(stories) != LIMIT:
    raise RuntimeError(
        f"Expected {LIMIT} stories but found {len(stories)}."
    )

with open("stories.json", "w", encoding="utf-8") as file:
    json.dump(
        stories,
        file,
        indent=2,
        ensure_ascii=False
    )
    file.write("\n")

print(f"Updated {len(stories)} stories.")
```
