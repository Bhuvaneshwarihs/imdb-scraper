import json
import httpx
from datetime import datetime, UTC
from lxml import html
import time

url = "https://www.imdb.com/chart/top/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for attempt in range(3):  # retry 3 times
    try:
        response = httpx.get(url, headers=headers, timeout=30)
        break
    except httpx.ReadTimeout:
        print("Timeout... retrying")
        time.sleep(5)

tree = html.fromstring(response.text)

movies = []

for item in tree.cssselect(".ipc-metadata-list-summary-item"):
    title = item.cssselect(".ipc-title__text")[0].text_content()
    rating = item.cssselect(".ipc-rating-star")[0].text_content()

    movies.append({
        "title": title,
        "rating": rating
    })

now = datetime.now(UTC)

filename = f"imdb_{now.strftime('%Y-%m-%d')}.json"

with open(filename, "w") as f:
    json.dump(movies, f, indent=2)

print("Saved:", filename)
