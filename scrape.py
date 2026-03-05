import json
import httpx
from lxml import html
from datetime import datetime

url = "https://www.imdb.com/chart/top/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

response = httpx.get(url, headers=headers)

print("Status code:", response.status_code)

if response.status_code != 200:
    print("Failed to fetch page")
    exit()

tree = html.fromstring(response.text)

movies = []

items = tree.cssselect(".ipc-metadata-list-summary-item")

for item in items[:10]:  # limit for testing
    title = item.cssselect(".ipc-title__text")[0].text_content()
    rating = item.cssselect(".ipc-rating-star")[0].text_content()

    movies.append({
        "title": title,
        "rating": rating
    })

filename = f"imdb_{datetime.now().strftime('%Y-%m-%d')}.json"

with open(filename, "w") as f:
    json.dump(movies, f, indent=2)

print("Saved:", filename)
