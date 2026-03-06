import requests
import json
from datetime import datetime
from lxml import html

url = "https://www.imdb.com/chart/top/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers, timeout=60)

tree = html.fromstring(response.content)

movies = []

for item in tree.cssselect(".ipc-metadata-list-summary-item"):
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
