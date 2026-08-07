import json
import urllib.parse
import urllib.request

BASE_URL = "https://academicallamerica.com/services/archives.ashx/stories"

LIMIT = 10

params = {
    "index": 1,
    "page_size": 30,
    "sport": "",
    "season": "",
    "school": "",
    "search": ""
}

url = BASE_URL + "?" + urllib.parse.urlencode(params)

request = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://academicallamerica.com/archives.aspx"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    raw = response.read().decode("utf-8", errors="replace")

data = json.loads(raw)

# The service may return:
# 1. a normal list of story dictionaries
# 2. a list containing JSON strings
# 3. an object containing the list
if isinstance(data, dict):
    for key in ("data", "stories", "items", "results"):
        if key in data:
            data = data[key]
            break

# If individual entries are JSON strings, decode them.
if isinstance(data, list):
    decoded = []

    for item in data:
        if isinstance(item, str):
            try:
                item = json.loads(item)
            except json.JSONDecodeError:
                continue

        if isinstance(item, dict):
            decoded.append(item)

    data = decoded

if not isinstance(data, list):
    raise RuntimeError(
        "Academic All-America returned an unexpected response."
    )

stories = []

for item in data:
    title = str(item.get("story_headline", "")).strip()
    date = str(item.get("story_postdate", "")).strip()
    path = str(item.get("story_path", "")).strip()

    if not title or not path:
        continue

    if path.startswith("http"):
        link = path
    else:
        link = urllib.parse.urljoin(
            "https://academicallamerica.com/",
            path
        )

    stories.append({
        "title": title,
        "date": date,
        "link": link
    })

    if len(stories) >= LIMIT:
        break

if len(stories) < LIMIT:
    raise RuntimeError(
        f"Found only {len(stories)} usable stories. Expected at least {LIMIT}."
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
