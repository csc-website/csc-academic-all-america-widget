import json
import urllib.parse
import urllib.request

SERVICE_URL = "https://academicallamerica.com/services/archives.ashx/stories"
LIMIT = 10

params = {
    "index": 1,
    "page_size": 30,
    "sport": "",
    "season": "",
    "school": "",
    "search": ""
}

url = SERVICE_URL + "?" + urllib.parse.urlencode(params)

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


def find_stories(value):
    """
    Search the returned JSON recursively for dictionaries
    containing the Academic All-America story fields.
    """

    found = []

    if isinstance(value, dict):

        # This is a story record.
        if (
            "story_headline" in value
            and "story_path" in value
        ):
            found.append(value)
            return found

        # Otherwise search all values.
        for child in value.values():
            found.extend(find_stories(child))

    elif isinstance(value, list):

        for child in value:
            found.extend(find_stories(child))

    elif isinstance(value, str):

        # Sometimes a service returns JSON encoded as a string.
        try:
            decoded = json.loads(value)
            found.extend(find_stories(decoded))
        except (json.JSONDecodeError, TypeError):
            pass

    return found


records = find_stories(data)

stories = []
seen_links = set()

for item in records:

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

    if link in seen_links:
        continue

    seen_links.add(link)

    stories.append({
        "title": title,
        "date": date,
        "link": link
    })

    if len(stories) >= LIMIT:
        break


if len(stories) < LIMIT:
    raise RuntimeError(
        f"Found only {len(stories)} usable stories. "
        f"Expected at least {LIMIT}."
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

for story in stories:
    print(f"{story['date']} - {story['title']}")
