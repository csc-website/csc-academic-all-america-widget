import json
import urllib.request

SERVICE_URL = "https://academicallamerica.com/services/archives.ashx/stories"
LIMIT = 10

request = urllib.request.Request(
    SERVICE_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.loads(response.read().decode("utf-8"))

stories = []

for item in data:
    title = item.get("story_headline", "").strip()
    date = item.get("story_postdate", "").strip()
    path = item.get("story_path", "").strip()

    if not title or not path:
        continue

    if path.startswith("http"):
        link = path
    else:
        link = "https://academicallamerica.com" + path

    stories.append({
        "title": title,
        "date": date,
        "link": link
    })

    if len(stories) >= LIMIT:
        break

if len(stories) < LIMIT:
    raise RuntimeError(
        f"Found only {len(stories)} stories. Expected at least {LIMIT}."
    )

with open("stories.json", "w", encoding="utf-8") as file:
    json.dump(stories, file, indent=2, ensure_ascii=False)
    file.write("\n")

print(f"Updated {len(stories)} stories.")
