import json
import httpx
import time
from datetime import datetime, UTC
from lxml import html

url = "https://www.imdb.com/chart/top/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

response = None

# retry logic
for attempt in range(5):
    try:
        print(f"Attempt {attempt+1}...")
        response = httpx.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            break
    except httpx.ReadTimeout:
        print("Timeout... retrying")
        time.sleep(5)

if response is None:
    raise Exception("Failed to fetch IMDb page")

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
