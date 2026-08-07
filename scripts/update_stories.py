import json
import re
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

URL = "https://academicallamerica.com/archives.aspx"
LIMIT = 10
DATE_PATTERN = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")


class ArchivesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.rows = []
        self.current_row = []
        self.current_text = []
        self.current_href = ""
        self.current_link_text = []
        self.table_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "table":
            self.table_depth += 1
            self.in_table = True
            return

        if not self.in_table:
            return

        if tag == "tr":
            self.in_row = True
            self.current_row = []

        elif self.in_row and tag in ("td", "th"):
            self.in_cell = True
            self.current_text = []
            self.current_href = ""
            self.current_link_text = []

        elif self.in_cell and tag == "a":
            attributes = dict(attrs)
            self.current_href = attributes.get("href", "")
            self.current_link_text = []

    def handle_data(self, data):
        if not self.in_cell:
            return

        self.current_text.append(data)

        if self.current_href:
            self.current_link_text.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in ("td", "th") and self.in_cell:
            cell_text = " ".join("".join(self.current_text).split())
            link_text = " ".join("".join(self.current_link_text).split())

            self.current_row.append({
                "text": cell_text,
                "href": self.current_href,
                "link_text": link_text
            })

            self.in_cell = False

        elif tag == "tr" and self.in_row:
            if self.current_row:
                self.rows.append(self.current_row)

            self.in_row = False
            self.current_row = []

        elif tag == "table":
            self.table_depth -= 1

            if self.table_depth == 0:
                self.in_table = False


def main():
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 (CSC Academic All-America Widget)"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = ArchivesParser()
    parser.feed(html)

    stories = []

    for row in parser.rows:
        if not row:
            continue

        # The first column is the posted date.
        date = row[0]["text"].strip()

        if not DATE_PATTERN.match(date):
            continue

        # Find the headline link in the row.
        headline_cell = None

        for cell in row:
            if cell["href"] and cell["link_text"]:
                headline_cell = cell
                break

        if headline_cell is None:
            continue

        title = headline_cell["link_text"].strip()
        link = urljoin(URL, headline_cell["href"])

        if not title or not link:
            continue

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
        json.dump(
            stories,
            file,
            indent=2,
            ensure_ascii=False
        )
        file.write("\n")

    print(f"Updated {len(stories)} stories.")


if __name__ == "__main__":
    main()
